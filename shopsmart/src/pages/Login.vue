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
        <p class="text-white/70 text-xs mt-1">Your smart shopping companion</p>
      </div>

      <!-- Body -->
      <div class="px-8 py-7">
        <div v-if="errorMessage" class="flex items-center gap-2 bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg px-4 py-3 mb-5">
          <span>⚠</span> {{ errorMessage }}
        </div>

        <form @submit.prevent="handleLogin" class="space-y-4">
          <div>
            <label class="block text-xs font-medium text-gray-500 mb-1.5">Email or Username</label>
            <div class="relative">
              <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
              </span>
              <input v-model="identifier" type="text" required
                class="w-full pl-9 pr-4 py-2.5 border border-gray-200 rounded-lg bg-gray-50 text-sm focus:outline-none focus:border-[#8d6040] focus:ring-2 focus:ring-[#8d6040]/10"
                placeholder="example@email.com" />
            </div>
          </div>

          <div>
            <div class="flex justify-between items-center mb-1.5">
              <label class="text-xs font-medium text-gray-500">Password</label>
              <router-link to="/forgot-password" class="text-xs text-[#8d6040] hover:underline">Forgot password?</router-link>
            </div>
            <div class="relative">
              <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0110 0v4"/></svg>
              </span>
              <input v-model="password" type="password" required
                class="w-full pl-9 pr-4 py-2.5 border border-gray-200 rounded-lg bg-gray-50 text-sm focus:outline-none focus:border-[#8d6040] focus:ring-2 focus:ring-[#8d6040]/10"
                placeholder="Enter password" />
            </div>
          </div>

          <button type="submit" :disabled="loading"
            class="w-full bg-[#7c5a3e] hover:bg-[#5c3d2e] text-white py-2.5 rounded-lg text-sm font-medium flex items-center justify-center gap-2 mt-2 transition-colors">
            <span v-if="!loading">Login</span>
            <span v-else class="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
          </button>
        </form>

        <div class="border-t border-gray-100 mt-6 pt-5">
          <p class="text-xs text-center text-gray-400">
            Don't have an account?
            <router-link to="/register" class="text-[#8d6040] hover:underline font-medium">Register</router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../store/authStore";

const auth = useAuthStore();
const router = useRouter();

const identifier = ref("");
const password = ref("");
const loading = ref(false);
const errorMessage = ref("");

const handleLogin = async () => {
  loading.value = true;
  errorMessage.value = "";

  try {
    await auth.loginUser({
      identifier: identifier.value.trim(),
      password: password.value,
    });

    router.push("/");
  } catch (err) {
     const message =
      err?.response?.data?.error ||
      err?.response?.data?.message ||
      err?.response?.data?.detail ||
      "Login failed";

    errorMessage.value = message;
  } finally {
    loading.value = false;
  }
};
</script>
