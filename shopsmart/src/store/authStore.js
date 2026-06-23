import { defineStore } from "pinia";
import {
  login,
  register,
  me,
  logoutApi,
  resendOtp,
  resetPassword,
  becomeSeller,
  verifyOtp,
} from "../services/auth";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    access: localStorage.getItem("access") || null,
    refresh: localStorage.getItem("refresh") || null,
    loading: false,
    initialized: false,
  }),

  getters: {
    isAuthenticated: (state) => !!localStorage.getItem("access") && !!state.user,
    isSeller: (state) => state.user?.is_seller === true,
  },

  actions: {
    // ----------------------------
    // REGISTER
    // ----------------------------
    async registerUser(payload) {
      this.loading = true;
      try {
        const res = await register(payload);
        return res; // OTP sent
      } finally {
        this.loading = false;
      }
    },

    // ----------------------------
    // VERIFY OTP (NEW FLOW)
    // ----------------------------
    async verifyOtp(payload) {
      this.loading = true;
      try {
        const res = await verifyOtp(payload.email, payload.otp);
        return res;
      } finally {
        this.loading = false;
      }
    },

    // ----------------------------
    // RESEND OTP
    // ----------------------------
    async resendOtp(email) {
      this.loading = true;
      try {
        const res = await resendOtp(email);
        return res;
      } finally {
        this.loading = false;
      }
    },

    // ----------------------------
    // LOGIN
    // ----------------------------
    async loginUser(payload) {
      this.loading = true;
      try {
        const res = await login(payload);

        this.access = res.access;
        this.refresh = res.refresh;

        localStorage.setItem("access", res.access);
        localStorage.setItem("refresh", res.refresh);

        await this.fetchUser();

        return res;
      } finally {
        this.loading = false;
      }
    },

    // ----------------------------
    // FETCH USER
    // ----------------------------
    async fetchUser() {
      try {
        const res = await me();
        this.user = res;
      } catch (err) {
        if (err.response?.status === 401) {
          this.logout();
        }
      } finally {
        this.initialized = true;
      }
    },

   

    // ----------------------------
    // BECOME SELLER
    // ----------------------------
    async activateSeller() {
      this.loading = true;

      try {
        const res = await becomeSeller();

        await this.fetchUser();

        return res;
      } finally {
        this.loading = false;
      }
    },

    // ----------------------------
    // RESET PASSWORD
    // ----------------------------
    async resetPassword(payload) {
      this.loading = true;
      try {
        const res = await resetPassword(payload);
        return res;
      } finally {
        this.loading = false;
      }
    },

    // ----------------------------
    // LOGOUT
    // ----------------------------
    async logout() {
      try {
        if (this.refresh) {
          await logoutApi(this.refresh);
        }
      } catch (error) {
        console.error("Logout error:", error);
      } finally {
        this.user = null;
        this.access = null;
        this.refresh = null;

        localStorage.removeItem("access");
        localStorage.removeItem("refresh");

        window.location.href = "/login";
      }
    },
  },
});
