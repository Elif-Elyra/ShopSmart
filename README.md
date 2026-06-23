# ShopSmart

A full-stack e-commerce marketplace where users can buy and sell products, manage orders, and process payments — built with Django REST Framework on the backend and Vue 3 on the frontend.

---

## Tech Stack

**Backend**
- Python 3.14 / Django 6
- Django REST Framework + SimpleJWT (auth)
- django-filter (filtering, search, ordering)
- Stripe (payments)
- SendGrid (transactional email / OTP)
- SQLite (development database)

**Frontend**
- Vue 3 + Vue Router + Pinia
- Vite (bundler)
- Bootstrap 5 + Tailwind CSS
- Axios

---

## Project Structure

```
ShopSmart/
├── core/               # Django project config (settings, URLs, middleware)
├── apps/
│   ├── account/        # Users, auth, wallet, addresses, withdrawals
│   ├── catalog/        # Products, categories, cart
│   └── orders/         # Orders, checkout, reviews, notifications
├── shopsmart/          # Vue 3 frontend (src + built dist/)
├── mediafiles/         # Uploaded product images
├── manage.py
└── pyproject.toml
```

---

## Getting Started

### Prerequisites

- Python 3.14+
- Node.js 18+
- pip / poetry

### Backend Setup

```bash
# Clone the repo and enter the project directory
cd ShopSmart

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
# or, if using poetry:
poetry install

# Create a .env file (see Environment Variables below)
cp .env.example .env

# Apply migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Run the dev server
python manage.py runserver
```

### Frontend Setup

```bash
cd shopsmart

npm install
npm run dev        # development with HMR
npm run build      # production build → dist/
```

The Django backend serves the built frontend at `/` (everything that isn't under `/api/`).

---

## Environment Variables

Create a `.env` file in the project root:

```env
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
BASE_URL=http://127.0.0.1:8000
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173

SENDGRID_API_KEY=your-sendgrid-key
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

STRIPE_SECRET_KEY=your-stripe-secret-key
```

---

## API Overview

All API routes are prefixed with `/api/`.

### Auth (`/api/auth/`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `auth/register/` | Register a new user |
| POST | `auth/login/` | Log in (returns JWT tokens) |
| POST | `auth/logout/` | Blacklist refresh token |
| POST | `auth/token/refresh/` | Refresh access token |
| POST | `auth/verify-otp/` | Verify OTP code sent via email |
| POST | `auth/resend-otp/` | Resend OTP |
| POST | `auth/reset-password/` | Reset password via OTP |

### User & Wallet

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/PATCH | `me/` | View or update profile |
| POST | `me/become-seller/` | Upgrade account to seller |
| GET | `wallet/` | View wallet balance |
| GET | `wallet/transactions/` | List wallet transactions |
| CRUD | `addresses/` | Manage delivery addresses |
| CRUD | `bank-accounts/` | Manage bank accounts |
| CRUD | `withdrawals/` | Request / manage withdrawals |

### Catalog

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `categories/` | List all categories |
| GET | `categories/<id>/products/` | Products in a category |
| POST | `analytics/category-click/` | Log a category click |
| GET/POST | `products/` | Browse all active products |
| GET | `products/<id>/` | Product detail |
| CRUD | `seller/products/` | Seller's own product management |
| GET | `cart/` | View cart |
| CRUD | `cart/items/` | Add / update / remove cart items |

### Orders

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `checkout/` | Create an order from cart (Stripe payment) |
| GET | `orders/` | Buyer's order list |
| GET | `orders/<id>/` | Order detail |
| POST | `orders/<id>/cancel/` | Cancel an order |
| GET | `seller/orders/` | Seller's incoming orders |
| POST | `seller/orders/<id>/ship/` | Mark order as shipped |
| POST | `seller/orders/<id>/deliver/` | Confirm delivery |
| CRUD | `reviews/` | Product reviews |
| GET | `notifications/` | User notifications |

---

## Authentication

The API uses JWT Bearer tokens. Include the access token in the `Authorization` header:

```
Authorization: Bearer <access_token>
```

Access tokens expire after **2 hours**; refresh tokens last **30 days**.

---

## Running Tests

```bash
python manage.py test apps.account apps.catalog apps.orders
```

---

## Admin

The Django admin panel is available at `/admin/`. Log in with the superuser credentials created during setup.
