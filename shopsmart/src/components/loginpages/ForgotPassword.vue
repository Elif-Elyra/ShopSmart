<template>
  <div class="min-h-screen flex items-center justify-center px-4 bg-[#f5f0eb]">
    <div class="w-full max-w-md bg-white shadow-xl rounded-2xl overflow-hidden">
      <div
        class="bg-gradient-to-br from-[#5c3d2e] via-[#8d6040] to-[#b8916a] px-8 py-8 text-center"
      >
        <div
          class="w-14 h-14 rounded-full bg-white/15 border-2 border-white/40 flex items-center justify-center mx-auto mb-3"
        >
          <svg
            class="w-7 h-7 text-white"
            fill="none"
            stroke="currentColor"
            stroke-width="1.8"
            viewBox="0 0 24 24"
          >
            <rect x="3" y="11" width="18" height="11" rx="2" />
            <path d="M7 11V7a5 5 0 0110 0v4" />
            <circle cx="12" cy="16" r="1" fill="currentColor" />
          </svg>
        </div>
        <h1 class="text-xl font-medium text-white">Forgot Password?</h1>
        <p class="text-white/70 text-xs mt-1">
          No worries — we'll send you a reset code
        </p>
      </div>

      <div class="px-8 py-7">
        <p class="text-sm text-gray-500 text-center mb-5 leading-relaxed">
          Enter the email address linked to your account and we'll send you a
          one-time code.
        </p>

        <div
          v-if="errorMessage"
          class="flex items-center gap-2 bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg px-4 py-3 mb-4"
        >
          <span>⚠</span> {{ errorMessage }}
        </div>

        <form @submit.prevent="sendOtp" class="space-y-4">
          <div class="relative">
            <span
              class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
            >
              <svg
                class="w-4 h-4"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                viewBox="0 0 24 24"
              >
                <path
                  d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"
                />
                <polyline points="22,6 12,13 2,6" />
              </svg>
            </span>
            <input
              v-model="email"
              type="email"
              required
              class="w-full pl-9 pr-4 py-2.5 border border-gray-200 rounded-lg bg-gray-50 text-sm focus:outline-none focus:border-[#8d6040] focus:ring-2 focus:ring-[#8d6040]/10"
              placeholder="example@email.com"
            />
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full bg-[#7c5a3e] hover:bg-[#5c3d2e] text-white py-2.5 rounded-lg text-sm font-medium flex items-center justify-center gap-2 transition-colors"
          >
            <span v-if="!loading">Send OTP</span>
            <span
              v-else
              class="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"
            ></span>
          </button>
        </form>

        <div class="border-t border-gray-100 mt-6 pt-5">
          <p class="text-xs text-center text-gray-400">
            Remember it?
            <router-link
              to="/login"
              class="text-[#8d6040] hover:underline font-medium"
              >Back to login</router-link
            >
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { resendOtp } from "../../services/auth";
import { useRouter } from "vue-router";

const router = useRouter();

const email = ref("");
const loading = ref(false);
const errorMessage = ref("");

const sendOtp = async () => {
  loading.value = true;
  errorMessage.value = "";

  try {
    await resendOtp(email.value);

    router.push({
      name: "reset-password",
      query: { email: email.value },
    });
  } catch (err) {
    console.log("FULL ERROR:", err);
    console.log("RESPONSE:", err.response);
    console.log("DATA:", err.response?.data);
    console.log("STATUS:", err.response?.status);

    errorMessage.value =
      err?.response?.data?.error || err?.message || "Failed to send OTP";
  } finally {
    loading.value = false;
  }
};
</script>
