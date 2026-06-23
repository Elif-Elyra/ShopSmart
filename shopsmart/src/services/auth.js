import api from "./api";

// ----------------------------
// REGISTER (OTP sent backend se)
// ----------------------------
export const register = async (data) => {
  const res = await api.post("auth/register/", data);
  return res.data;
};

// ----------------------------
// LOGIN
// ----------------------------
export const login = async (data) => {
  const res = await api.post("auth/login/", data);
  return res.data;
};

// ----------------------------
// LOGOUT
// ----------------------------
export const logoutApi = async (refresh) => {
  const res = await api.post("auth/logout/", {
    refresh,
  });
  return res.data;
};

// ----------------------------
// PROFILE (ME)
// ----------------------------
export const me = async () => {
  const res = await api.get("me/");
  return res.data;
};

// ----------------------------
// VERIFY OTP (UPDATED - OLD VERIFY EMAIL REMOVED)
// ----------------------------
export const verifyOtp = async (email, otp) => {
  const res = await api.post("auth/verify-otp/", {
    email,
    otp,
  });
  return res.data;
};

// ----------------------------
// RESEND OTP
// ----------------------------
export const resendOtp = async (email) => {
  const res = await api.post("auth/resend-otp/", {
    email,
  });
  return res.data;
};

// ----------------------------
// RESET PASSWORD (FORGOT PASSWORD FLOW)
// ----------------------------
export const resetPassword = async (data) => {
  const res = await api.post("auth/reset-password/", data);
  return res.data;
};

// ----------------------------
// Become Seller
// ----------------------------


export const becomeSeller = async () => {
  const res = await api.post(
    "me/become-seller/"
  );

  return res.data;
};