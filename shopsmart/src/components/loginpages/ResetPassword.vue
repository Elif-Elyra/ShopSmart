<template>
  <div class="min-h-screen flex items-center justify-center px-4 bg-[#f5f0eb]">
    <div class="w-full max-w-md bg-white shadow-xl rounded-2xl overflow-hidden">

      <div class="bg-gradient-to-br from-[#5c3d2e] via-[#8d6040] to-[#b8916a] px-8 py-8 text-center">
        <div class="w-14 h-14 rounded-full bg-white/15 border-2 border-white/40 flex items-center justify-center mx-auto mb-3">
          <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
            <path d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
          </svg>
        </div>
        <h1 class="text-xl font-medium text-white">Reset Password</h1>
        <p class="text-white/70 text-xs mt-1">Enter the code sent to your email</p>
      </div>

      <div class="px-8 py-7">
        <div v-if="email" class="flex items-center gap-2 bg-green-50 border border-green-200 text-green-700 text-xs rounded-lg px-3 py-2.5 mb-5">
          <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
          Code sent to <strong>{{ email }}</strong>
        </div>

        <div v-if="errorMessage" class="flex items-center gap-2 bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg px-4 py-3 mb-4">
          <span>⚠</span> {{ errorMessage }}
        </div>
        <div v-if="successMessage" class="flex items-center gap-2 bg-green-50 border border-green-200 text-green-700 text-sm rounded-lg px-4 py-3 mb-4">
          <span>✓</span> {{ successMessage }}
        </div>

        <form @submit.prevent="resetPasswordHandler" class="space-y-4">
          <!-- OTP boxes -->
          <div>
            <label class="block text-xs font-medium text-gray-500 mb-2">Enter OTP</label>
            <div class="flex gap-2 justify-between">
              <input v-for="(_, i) in otpDigits" :key="i" :ref="el => otpRefs[i] = el"
                v-model="otpDigits[i]" maxlength="1" type="text" inputmode="numeric"
                @input="onOtpInput(i)" @keydown="onOtpKey($event, i)"
                class="w-11 h-11 text-center text-lg font-semibold border border-gray-200 rounded-lg bg-gray-50 focus:outline-none focus:border-[#8d6040] focus:ring-2 focus:ring-[#8d6040]/10" />
            </div>
          </div>

          <div>
            <label class="block text-xs font-medium text-gray-500 mb-1.5">New Password</label>
            <div class="relative">
              <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0110 0v4"/></svg>
              </span>
              <input v-model="newPassword" type="password" required
                class="w-full pl-9 pr-4 py-2.5 border border-gray-200 rounded-lg bg-gray-50 text-sm focus:outline-none focus:border-[#8d6040] focus:ring-2 focus:ring-[#8d6040]/10"
                placeholder="Min. 8 characters" />
            </div>
          </div>

          <!-- Timer -->
          <div class="flex items-center justify-center">
            <span :class="['flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs border', isExpired ? 'bg-red-50 border-red-200 text-red-600' : 'bg-gray-50 border-gray-200 text-gray-500']">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
              <span v-if="!isExpired">{{ Math.floor(timeLeft/60) }}:{{ String(timeLeft%60).padStart(2,'0') }}</span>
              <span v-else>OTP expired</span>
            </span>
          </div>

          <button type="submit" :disabled="loading || isExpired"
            class="w-full bg-[#7c5a3e] hover:bg-[#5c3d2e] disabled:opacity-50 text-white py-2.5 rounded-lg text-sm font-medium flex items-center justify-center gap-2 transition-colors">
            <span v-if="!loading">Reset Password</span>
            <span v-else class="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
          </button>

          <button v-if="isExpired" type="button" @click="resend"
            class="w-full text-sm text-[#8d6040] hover:underline py-1">
            Resend OTP
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import { resetPassword, resendOtp } from "../../services/auth";
import { useRouter, useRoute } from "vue-router";

const router = useRouter();
const route = useRoute();
const email = computed(() => route.query.email || "");
if (!route.query.email) router.push("/forgot-password");

// OTP boxes (6 digits)
const otpDigits = ref(["","","","","",""]);
const otpRefs = ref([]);
const otp = computed(() => otpDigits.value.join(""));

const onOtpInput = (i) => {
  if (otpDigits.value[i] && i < 5) otpRefs.value[i+1]?.focus();
};
const onOtpKey = (e, i) => {
  if (e.key === "Backspace" && !otpDigits.value[i] && i > 0) otpRefs.value[i-1]?.focus();
};

const newPassword = ref("");
const loading = ref(false);
const errorMessage = ref("");
const successMessage = ref("");
const timeLeft = ref(120);
const isExpired = ref(false);
let timer = null;

const startTimer = () => {
  clearInterval(timer);
  timeLeft.value = 120;
  isExpired.value = false;
  timer = setInterval(() => {
    if (timeLeft.value > 0) { timeLeft.value--; }
    else { clearInterval(timer); isExpired.value = true; }
  }, 1000);
};

onMounted(() => startTimer());
onUnmounted(() => clearInterval(timer));

const resetPasswordHandler = async () => {
  loading.value = true;
  errorMessage.value = "";
  successMessage.value = "";
  try {
    await resetPassword({ email: email.value, otp: otp.value, new_password: newPassword.value });
    successMessage.value = "Password reset successful";
    setTimeout(() => router.push("/login"), 1200);
  } catch (err) {
    errorMessage.value = err?.response?.data?.error || "Reset failed";
  } finally {
    loading.value = false;
  }
};

const resend = async () => {
  try {
    await resendOtp(email.value);
    startTimer();
  } catch {
    errorMessage.value = "Failed to resend OTP";
  }
};
</script>