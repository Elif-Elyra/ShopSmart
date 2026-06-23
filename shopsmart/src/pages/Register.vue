<template>
  <div class="min-h-screen flex items-center justify-center px-4 bg-[#f5f0eb]">
    <div class="w-full max-w-md bg-white shadow-xl rounded-2xl overflow-hidden">

      <!-- Header -->
      <div class="bg-gradient-to-br from-[#5c3d2e] via-[#8d6040] to-[#b8916a] px-8 py-8 text-center">
        <div class="w-14 h-14 rounded-full bg-white/15 border-2 border-white/40 flex items-center justify-center mx-auto mb-3">
          <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/>
            <line x1="3" y1="6" x2="21" y2="6" stroke-linecap="round"/>
            <path stroke-linecap="round" stroke-linejoin="round" d="M16 10a4 4 0 01-8 0"/>
          </svg>
        </div>
        <h1 class="text-xl font-medium text-white tracking-wide">ShopSmart</h1>
        <p class="text-white/70 text-xs mt-1">
          {{ step === 'register' ? 'Create your account' : 'Verify your email' }}
        </p>
      </div>

      <!-- Body -->
      <div class="px-8 py-7">

        <!-- Error Message -->
        <div
          v-if="errors.general"
          class="flex items-center gap-2 bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg px-4 py-3 mb-5"
        >
          <span>⚠</span> {{ errors.general }}
        </div>

        <!-- ================= REGISTER FORM ================= -->
        <form v-if="step === 'register'" @submit.prevent="handleRegister" class="space-y-4">

          <!-- Fullname -->
          <div>
            <label class="block text-xs font-medium text-gray-500 mb-1.5">Full Name</label>
            <div class="relative">
              <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/>
                  <circle cx="12" cy="7" r="4"/>
                </svg>
              </span>
              <input
                v-model="fullname"
                type="text"
                required
                placeholder="Muhammad Ali"
                class="w-full pl-9 pr-4 py-2.5 border border-gray-200 rounded-lg bg-gray-50 text-sm focus:outline-none focus:border-[#8d6040] focus:ring-2 focus:ring-[#8d6040]/10"
              />
            </div>
          </div>

          <!-- Username -->
          <div>
            <label class="block text-xs font-medium text-gray-500 mb-1.5">Username</label>
            <div class="relative">
              <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/>
                  <circle cx="12" cy="7" r="4"/>
                  <path d="M16 3.13a4 4 0 010 7.75"/>
                </svg>
              </span>
              <input
                v-model="username"
                type="text"
                required
                placeholder="muhammadali"
                class="w-full pl-9 pr-4 py-2.5 border border-gray-200 rounded-lg bg-gray-50 text-sm focus:outline-none focus:border-[#8d6040] focus:ring-2 focus:ring-[#8d6040]/10"
              />
            </div>
          </div>

          <!-- Email -->
          <div>
            <label class="block text-xs font-medium text-gray-500 mb-1.5">Email</label>
            <div class="relative">
              <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                  <polyline points="22,6 12,13 2,6"/>
                </svg>
              </span>
              <input
                v-model="email"
                type="email"
                required
                placeholder="example@email.com"
                class="w-full pl-9 pr-4 py-2.5 border border-gray-200 rounded-lg bg-gray-50 text-sm focus:outline-none focus:border-[#8d6040] focus:ring-2 focus:ring-[#8d6040]/10"
              />
            </div>
          </div>

          <!-- Password -->
          <div>
            <label class="block text-xs font-medium text-gray-500 mb-1.5">Password</label>
            <div class="relative">
              <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <rect x="3" y="11" width="18" height="11" rx="2"/>
                  <path d="M7 11V7a5 5 0 0110 0v4"/>
                </svg>
              </span>
              <input
                v-model="password"
                type="password"
                required
                placeholder="Create a password"
                class="w-full pl-9 pr-4 py-2.5 border border-gray-200 rounded-lg bg-gray-50 text-sm focus:outline-none focus:border-[#8d6040] focus:ring-2 focus:ring-[#8d6040]/10"
              />
            </div>
          </div>

          <!-- Confirm Password -->
          <div>
            <label class="block text-xs font-medium text-gray-500 mb-1.5">Confirm Password</label>
            <div class="relative">
              <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <rect x="3" y="11" width="18" height="11" rx="2"/>
                  <path d="M7 11V7a5 5 0 0110 0v4"/>
                  <path d="M9 16l2 2 4-4" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </span>
              <input
                v-model="confirmPassword"
                type="password"
                required
                placeholder="Repeat your password"
                class="w-full pl-9 pr-4 py-2.5 border border-gray-200 rounded-lg bg-gray-50 text-sm focus:outline-none focus:border-[#8d6040] focus:ring-2 focus:ring-[#8d6040]/10"
              />
            </div>
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full bg-[#7c5a3e] hover:bg-[#5c3d2e] text-white py-2.5 rounded-lg text-sm font-medium flex items-center justify-center gap-2 mt-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="!loading">Create Account</span>
            <span v-else class="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
          </button>
        </form>

        <!-- ================= OTP FORM ================= -->
        <form v-else @submit.prevent="handleVerifyOtp" class="space-y-4">

          <!-- Info Banner -->
          <div class="flex items-start gap-2 bg-green-50 border border-green-200 text-green-700 text-sm rounded-lg px-4 py-3">
            <svg class="w-4 h-4 mt-0.5 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
              <polyline points="22,6 12,13 2,6"/>
            </svg>
            <span>OTP sent to <strong>{{ email }}</strong></span>
          </div>

          <!-- OTP Input -->
          <div>
            <label class="block text-xs font-medium text-gray-500 mb-1.5">Enter OTP</label>
            <div class="relative">
              <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                </svg>
              </span>
              <input
                v-model="otp"
                type="text"
                required
                placeholder="6-digit code"
                maxlength="6"
                class="w-full pl-9 pr-4 py-2.5 border border-gray-200 rounded-lg bg-gray-50 text-sm focus:outline-none focus:border-[#8d6040] focus:ring-2 focus:ring-[#8d6040]/10 tracking-widest text-center font-mono"
              />
            </div>
          </div>

          <button
            type="submit"
            class="w-full bg-[#7c5a3e] hover:bg-[#5c3d2e] text-white py-2.5 rounded-lg text-sm font-medium flex items-center justify-center gap-2 mt-2 transition-colors"
          >
            Verify OTP
          </button>

          <button
            type="button"
            @click="handleResendOtp"
            class="w-full text-sm text-[#8d6040] hover:underline py-1"
          >
            Didn't receive it? Resend OTP
          </button>
        </form>

        <!-- Footer -->
        <div class="border-t border-gray-100 mt-6 pt-5">
          <p class="text-xs text-center text-gray-400">
            Already have an account?
            <router-link to="/login" class="text-[#8d6040] hover:underline font-medium">Login</router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { register, verifyOtp, resendOtp } from "../services/auth";
import { useRouter } from "vue-router";

const router = useRouter();

const step = ref("register");

const fullname = ref("");
const username = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const otp = ref("");

const errors = ref({});
const loading = ref(false);

async function handleRegister() {
  errors.value = {};

  if (password.value !== confirmPassword.value) {
    errors.value.general = err.detail || "Passwords do not match";
    return;
  }

  loading.value = true;

  try {
    await register({
      fullname: fullname.value,
      username: username.value,
      email: email.value,
      password: password.value,
    });

    step.value = "otp";
  } catch (err) {
    errors.value.general =
      err.detail || "Registration failed. Please try again.";
  } finally {
    loading.value = false;
  }
}

async function handleVerifyOtp() {
  errors.value = {};
  try {
    await verifyOtp(email.value, otp.value);
    router.push("/login");
  } catch (err) {
    errors.value.general = err.detail || "Invalid or expired OTP. Please try again.";
  }
}

async function handleResendOtp() {
  errors.value = {};
  try {
    await resendOtp(email.value);
  } catch (err) {
    errors.value.general = err.detail || "Failed to resend OTP. Please try again.";
  }
}
</script>
