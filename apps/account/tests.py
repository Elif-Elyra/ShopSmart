from django.test import TestCase

# Create your tests here.
# ============================================================
# test_users.py
# Users app ki saari APIs ka test file.
# Har class ek feature ko test karti hai.
# Run karo: python manage.py test apps.users.tests.test_users
# ============================================================

from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch
from django.utils import timezone
from datetime import timedelta

from apps.account.models import User, OTP, Address, BankAccount, Withdrawal


# ============================================================
# HELPER — test mein baar baar user banana padta hai
# Yahan se banao taake code repeat na ho
# ============================================================

def make_user(email='test@mail.com', password='Test@1234', is_active=True, is_seller=False):
    user = User.objects.create_user(
        email=email,
        password=password,
        username=email.split('@')[0],
        is_active=is_active,
        is_seller=is_seller
    )
    return user


def make_otp(email, code='123456', is_used=False, minutes_ago=0):
    """
    OTP banao — minutes_ago se pehle ki created_at set hoti hai.
    Expired OTP test karne ke liye minutes_ago=20 pass karo.
    """
    otp = OTP.objects.create(email=email, code=code, is_used=is_used)
    if minutes_ago:
        OTP.objects.filter(pk=otp.pk).update(
            created_at=timezone.now() - timedelta(minutes=minutes_ago)
        )
        otp.refresh_from_db()
    return otp


# ============================================================
# REGISTER TESTS
# ============================================================

class RegisterTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = '/api/auth/register/'
        self.valid_data = {
            'email': 'newuser@mail.com',
            'password': 'Test@1234',
            'username': 'newuser',
            'fullname': 'New User'
        }

    # send_otp_email ko mock karo — real email nahi bhejna
    @patch('apps.account.views.send_otp_email')
    def test_valid_registration_returns_201(self, mock_email):
        mock_email.return_value = {'success': True}
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch('apps.account.views.send_otp_email')
    def test_user_is_inactive_after_registration(self, mock_email):
        # Naya user inactive hona chahiye — jab tak OTP verify na ho
        mock_email.return_value = {'success': True}
        self.client.post(self.url, self.valid_data)
        user = User.objects.get(email='newuser@mail.com')
        self.assertFalse(user.is_active)

    @patch('apps.account.views.send_otp_email')
    def test_duplicate_email_returns_400(self, mock_email):
        # Same email se dobara register nahi ho sakta
        mock_email.return_value = {'success': True}
        make_user(email='newuser@mail.com')
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_email_returns_400(self):
        data = {'password': 'Test@1234', 'username': 'abc'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_password_returns_400(self):
        data = {'email': 'x@mail.com', 'username': 'abc'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# ============================================================
# VERIFY OTP TESTS
# ============================================================

class VerifyOTPTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = '/api/auth/verify-otp/'
        self.user = make_user(email='v@mail.com', is_active=False)

    def test_valid_otp_activates_user(self):
        make_otp(email='v@mail.com', code='654321')
        response = self.client.post(self.url, {
            'email': 'v@mail.com',
            'otp': '654321'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.user.is_email_verified)

    def test_wrong_otp_returns_400(self):
        make_otp(email='v@mail.com', code='111111')
        response = self.client.post(self.url, {
            'email': 'v@mail.com',
            'otp': '999999'        # galat code
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_used_otp_returns_400(self):
        # Ek baar use ho chuka OTP dobara kaam nahi karta
        make_otp(email='v@mail.com', code='222222', is_used=True)
        response = self.client.post(self.url, {
            'email': 'v@mail.com',
            'otp': '222222'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_expired_otp_returns_400(self):
        # 20 minute purana OTP expire ho gaya hoga
        make_otp(email='v@mail.com', code='333333', minutes_ago=20)
        response = self.client.post(self.url, {
            'email': 'v@mail.com',
            'otp': '333333'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# ============================================================
# RESEND OTP TESTS
# ============================================================

class ResendOTPTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = '/api/auth/resend-otp/'

    @patch('apps.account.views.send_otp_email')
    def test_resend_creates_new_otp(self, mock_email):
        mock_email.return_value = {'success': True}
        make_user(email='r@mail.com', is_active=False)
        make_otp(email='r@mail.com', code='000000')  # purana OTP

        response = self.client.post(self.url, {'email': 'r@mail.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Purana OTP delete ho gaya, naya ban gaya
        otps = OTP.objects.filter(email='r@mail.com')
        self.assertEqual(otps.count(), 1)
        self.assertNotEqual(otps.first().code, '000000')

    def test_resend_for_nonexistent_user_returns_404(self):
        response = self.client.post(self.url, {'email': 'ghost@mail.com'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# ============================================================
# LOGIN TESTS
# ============================================================

class LoginTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = '/api/auth/login/'
        self.user = make_user(email='login@mail.com', password='Pass@123')

    def test_login_with_email_returns_tokens(self):
        response = self.client.post(self.url, {
            'identifier': 'login@mail.com',
            'password': 'Pass@123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_with_username_works(self):
        # Email ya username dono se login ho sakta hai
        response = self.client.post(self.url, {
            'identifier': 'login',     # username
            'password': 'Pass@123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_wrong_password_returns_401(self):
        response = self.client.post(self.url, {
            'identifier': 'login@mail.com',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_inactive_user_cannot_login(self):
        # Email verify nahi ki — login band hona chahiye
        inactive_user = make_user(email='inactive@mail.com', is_active=False)
        response = self.client.post(self.url, {
            'identifier': 'inactive@mail.com',
            'password': 'Test@1234'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_missing_credentials_returns_400(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nonexistent_user_returns_401(self):
        response = self.client.post(self.url, {
            'identifier': 'nobody@mail.com',
            'password': 'anything'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# ============================================================
# LOGOUT TESTS
# ============================================================

class LogoutTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = '/api/auth/logout/'
        self.user = make_user()

    def _get_tokens(self):
        # Login karke tokens lo
        response = self.client.post('/api/auth/login/', {
            'identifier': 'test@mail.com',
            'password': 'Test@1234'
        })
        return response.data

    def test_logout_with_valid_token_returns_200(self):
        tokens = self._get_tokens()
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {'refresh': tokens['refresh']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_without_refresh_token_returns_400(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthenticated_logout_returns_401(self):
        response = self.client.post(self.url, {'refresh': 'faketoken'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# ============================================================
# PROFILE TESTS
# ============================================================

class ProfileTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = '/api/auth/profile/'
        self.user = make_user()

    def test_authenticated_user_can_view_profile(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_unauthenticated_user_gets_401(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# ============================================================
# BECOME SELLER TESTS
# ============================================================

class BecomeSellerTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = '/api/auth/become-seller/'
        self.user = make_user()

    def test_user_becomes_seller(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_seller)

    def test_already_seller_returns_message(self):
        self.user.is_seller = True
        self.user.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Already', response.data['message'])


# ============================================================
# ADDRESS TESTS
# ============================================================

class AddressTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = '/api/auth/addresses/'
        self.user = make_user()
        self.client.force_authenticate(user=self.user)

    def test_create_address(self):
        response = self.client.post(self.url, {
            'label': 'Home',
            'line': '123 Main St',
            'city': 'Lahore',
            'postal_code': '54000',
            'country': 'Pakistan'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_returns_only_own_addresses(self):
        # Dusre user ka address nahi dikhna chahiye
        other = make_user(email='other@mail.com')
        Address.objects.create(user=other, line='Other St', city='KHI', country='PK')
        Address.objects.create(user=self.user, line='My St', city='LHR', country='PK')

        response = self.client.get(self.url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['city'], 'LHR')

    def test_unauthenticated_returns_401(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# ============================================================
# RESET PASSWORD TESTS
# ============================================================

class ResetPasswordTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = '/api/auth/reset-password/'
        self.user = make_user(email='reset@mail.com')

    def test_valid_otp_resets_password(self):
        make_otp(email='reset@mail.com', code='777777')
        response = self.client.post(self.url, {
            'email': 'reset@mail.com',
            'otp': '777777',
            'new_password': 'NewPass@999'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewPass@999'))

    def test_invalid_otp_returns_400(self):
        make_otp(email='reset@mail.com', code='111111')
        response = self.client.post(self.url, {
            'email': 'reset@mail.com',
            'otp': '000000',          # galat code
            'new_password': 'NewPass@999'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)