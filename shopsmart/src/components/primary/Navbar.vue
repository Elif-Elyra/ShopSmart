<template>
  <nav
    class="sticky top-0 z-50 h-16 bg-[#faf8f5]/95 backdrop-blur-md border-b border-[#e8e0d8]"
    role="navigation"
    aria-label="Main navigation"
  >
    <div class="max-w-7xl mx-auto h-full px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-full gap-6">
        <!-- LOGO -->
        <router-link
          to="/"
          class="flex items-center gap-2 shrink-0"
          aria-label="ShopSmart Home"
        >
          <div
            class="w-7 h-7 rounded-lg bg-gradient-to-br from-[#7c5a3e] to-[#b8916a] flex items-center justify-center shadow-sm"
          >
            <svg
              class="w-4 h-4 text-white"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"
              />
              <line x1="3" y1="6" x2="21" y2="6" stroke-linecap="round" />
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M16 10a4 4 0 01-8 0"
              />
            </svg>
          </div>
          <span class="text-[15px] font-semibold tracking-tight text-[#2d2016]">
            Shop<span class="text-[#8d6040]">Smart</span>
          </span>
        </router-link>

        <!-- DESKTOP NAV -->
        <ul class="hidden lg:flex items-center gap-1 flex-1">
          <li>
            <router-link to="/" class="nav-link" aria-current-value="page"
              >Home</router-link
            >
          </li>

          <li v-if="auth.user?.is_seller">
            <router-link to="/seller/dashboard" class="nav-link"
              >My Products</router-link
            >
          </li>
        </ul>

        <!-- RIGHT SIDE ACTIONS -->
        <div class="hidden lg:flex items-center gap-2">
          <!-- CART -->
          <router-link
            to="/cart"
            class="relative flex items-center gap-1.5 px-3 py-2 rounded-lg text-[13px] font-medium text-[#4a3728] hover:bg-[#f0ebe4] transition-colors duration-200"
            aria-label="Cart"
          >
            <svg
              class="w-4 h-4"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              viewBox="0 0 24 24"
            >
              <path d="M6 2 3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z" />
              <line x1="3" y1="6" x2="21" y2="6" />
              <path d="M16 10a4 4 0 01-8 0" />
            </svg>
            Cart
            <span
              v-if="cartCount > 0"
              class="absolute -top-0.5 -right-0.5 bg-[#8d6040] text-white text-[9px] font-bold min-w-[16px] h-4 px-1 flex items-center justify-center rounded-full"
              :aria-label="`${cartCount} items in cart`"
            >
              {{ cartCount }}
            </span>
          </router-link>

          <!-- GUEST LINKS -->
          <template v-if="!isAuthenticated">
            <router-link
              to="/login"
              class="px-4 py-2 rounded-lg text-[13px] font-medium text-[#4a3728] hover:bg-[#f0ebe4] transition-colors duration-200"
            >
              Login
            </router-link>
            <router-link
              to="/register"
              class="px-4 py-2 rounded-lg bg-gradient-to-br from-[#7c5a3e] to-[#a5724f] text-white text-[13px] font-medium hover:brightness-110 transition-all duration-200 shadow-sm"
            >
              Register
            </router-link>
          </template>

          <!-- USER DROPDOWN -->
          <div v-else class="relative group">
            <button
              class="flex items-center gap-2 pl-3 pr-2.5 py-2 rounded-lg text-[13px] font-medium text-[#4a3728] hover:bg-[#f0ebe4] transition-colors duration-200"
              aria-haspopup="true"
            >
              <!-- Avatar circle -->
              <span
                class="w-6 h-6 rounded-full bg-gradient-to-br from-[#7c5a3e] to-[#b8916a] flex items-center justify-center text-white text-[10px] font-bold shrink-0"
              >
                {{ auth.user?.fullname?.[0]?.toUpperCase() || "A" }}
              </span>
              <span>Account</span>
              <svg
                class="w-3.5 h-3.5 text-[#8d8078] transition-transform duration-200 group-hover:rotate-180"
                fill="none"
                stroke="currentColor"
                stroke-width="2.5"
                viewBox="0 0 24 24"
              >
                <path d="M6 9l6 6 6-6" />
              </svg>
            </button>

            <!-- Dropdown -->
            <div
              class="absolute top-full right-0 mt-2 w-44 invisible opacity-0 translate-y-1 group-hover:visible group-hover:opacity-100 group-hover:translate-y-0 transition-all duration-200 rounded-xl bg-white border border-[#ede8e2] shadow-lg shadow-black/8 overflow-hidden"
            >
              <div class="px-4 py-3 border-b border-[#f0ebe4]">
                <p
                  class="text-[11px] text-[#a0907e] font-medium uppercase tracking-wider"
                >
                  Signed in as
                </p>
                <p
                  class="text-[13px] text-[#2d2016] font-medium truncate mt-0.5"
                >
                  {{ auth.user?.fullname || "User" }}
                </p>
              </div>
              <router-link
                to="/profile"
                class="flex items-center gap-2.5 px-4 py-2.5 text-[13px] text-[#4a3728] hover:bg-[#f7f4f0] transition-colors"
              >
                <svg
                  class="w-3.5 h-3.5 text-[#8d6040]"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  viewBox="0 0 24 24"
                >
                  <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2" />
                  <circle cx="12" cy="7" r="4" />
                </svg>
                Profile
              </router-link>
              <button
                @click="logout"
                class="w-full flex items-center gap-2.5 px-4 py-2.5 text-[13px] text-red-600 hover:bg-red-50 transition-colors"
              >
                <svg
                  class="w-3.5 h-3.5"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4M16 17l5-5-5-5M21 12H9"
                  />
                </svg>
                Logout
              </button>
            </div>
          </div>
        </div>

        <!-- MOBILE: Cart + Hamburger -->
        <div class="flex lg:hidden items-center gap-2">
          <router-link
            to="/cart"
            class="relative w-9 h-9 rounded-lg flex items-center justify-center text-[#4a3728] hover:bg-[#f0ebe4] transition-colors"
            aria-label="Cart"
          >
            <svg
              class="w-5 h-5"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              viewBox="0 0 24 24"
            >
              <path d="M6 2 3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z" />
              <line x1="3" y1="6" x2="21" y2="6" />
              <path d="M16 10a4 4 0 01-8 0" />
            </svg>
            <span
              v-if="cartCount > 0"
              class="absolute -top-0.5 -right-0.5 bg-[#8d6040] text-white text-[9px] font-bold min-w-[15px] h-[15px] px-0.5 flex items-center justify-center rounded-full"
            >
              {{ cartCount }}
            </span>
          </router-link>

          <button
            class="w-9 h-9 rounded-lg flex items-center justify-center text-[#4a3728] hover:bg-[#f0ebe4] transition-colors"
            @click="toggleMenu"
            :aria-expanded="isOpen"
            aria-label="Toggle menu"
          >
            <svg
              v-if="!isOpen"
              class="w-5 h-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 6h16M4 12h16M4 18h16"
              />
            </svg>
            <svg
              v-else
              class="w-5 h-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- MOBILE MENU -->

    <transition
      enter-active-class="transition-all duration-250 ease-out"
      enter-from-class="opacity-0 -translate-y-2"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition-all duration-200 ease-in"
      leave-from-class="opacity-100 translate-y-0"
      leave-to-class="opacity-0 -translate-y-2"
    >
      <div
        v-if="isOpen"
        class="lg:hidden absolute top-full left-0 w-full bg-[#faf8f5]/98 backdrop-blur-md shadow-xl border-t border-[#e8e0d8]"
      >
        <!-- User info strip (authenticated) -->
        <div
          v-if="isAuthenticated"
          class="flex items-center gap-3 px-4 py-3 bg-[#f5f0ea] border-b border-[#e8e0d8]"
        >
          <span
            class="w-8 h-8 rounded-full bg-gradient-to-br from-[#7c5a3e] to-[#b8916a] flex items-center justify-center text-white text-xs font-bold shrink-0"
          >
            {{ auth.user?.fullname?.[0]?.toUpperCase() || "A" }}
          </span>
          <div>
            <p class="text-[13px] font-medium text-[#2d2016]">
              {{ auth.user?.fullname || "User" }}
            </p>
            <p class="text-[11px] text-[#a0907e]">
              {{ auth.user?.email || "" }}
            </p>
          </div>
        </div>

        <ul class="py-2 bg-[#efece8]">
          <li>
            <router-link to="/" @click="closeMenu" class="mobile-link">
              <svg
                class="w-4 h-4"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                viewBox="0 0 24 24"
              >
                <path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
                <polyline points="9 22 9 12 15 12 15 22" />
              </svg>
              Home
            </router-link>
          </li>

          <li v-if="auth.user?.is_seller">
            <router-link
              to="/seller/dashboard"
              @click="closeMenu"
              class="mobile-link"
            >
              <svg
                class="w-4 h-4"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                viewBox="0 0 24 24"
              >
                <rect x="2" y="3" width="20" height="14" rx="2" />
                <path d="M8 21h8M12 17v4" />
              </svg>
              My Products
            </router-link>
          </li>

          <template v-if="!isAuthenticated">
            <li class="px-3 pt-2 pb-1">
              <div class="border-t border-[#e8e0d8]"></div>
            </li>
            <li>
              <router-link to="/login" @click="closeMenu" class="mobile-link">
                <svg
                  class="w-4 h-4"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M15 3h4a2 2 0 012 2v14a2 2 0 01-2 2h-4M10 17l5-5-5-5M15 12H3"
                  />
                </svg>
                Login
              </router-link>
            </li>
            <li class="px-4 py-2">
              <router-link
                to="/register"
                @click="closeMenu"
                class="flex items-center justify-center gap-2 w-full py-2.5 rounded-lg bg-gradient-to-br from-[#7c5a3e] to-[#a5724f] text-white text-[13px] font-medium shadow-sm"
              >
                Create Account
              </router-link>
            </li>
          </template>

          <template v-else>
            <li class="px-3 pt-2 pb-1">
              <div class="border-t border-[#e8e0d8]"></div>
            </li>
            <li>
              <router-link to="/profile" @click="closeMenu" class="mobile-link">
                <svg
                  class="w-4 h-4"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  viewBox="0 0 24 24"
                >
                  <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2" />
                  <circle cx="12" cy="7" r="4" />
                </svg>
                Profile
              </router-link>
            </li>
            <li>
              <button
                @click="logout"
                class="mobile-link w-full text-left text-red-600 hover:bg-red-50 hover:text-red-700"
              >
                <svg
                  class="w-4 h-4"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4M16 17l5-5-5-5M21 12H9"
                  />
                </svg>
                Logout
              </button>
            </li>
          </template>
        </ul>
      </div>
    </transition>
  </nav>
</template>

<script setup>
import { ref, computed } from "vue";
import { useCartStore } from "../../store/cartStore";
import { useAuthStore } from "../../store/authStore";
import { storeToRefs } from "pinia";
import { onMounted } from "vue";

const cart = useCartStore();
const { cartCount } = storeToRefs(cart);

const auth = useAuthStore();

const isOpen = ref(false);

const isAuthenticated = computed(() => auth.isAuthenticated);

const toggleMenu = () => (isOpen.value = !isOpen.value);
const closeMenu = () => (isOpen.value = false);

const logout = async () => {
  closeMenu();
  await auth.logout();
  cart.clearCart();
};

onMounted(() => {
  cart.fetchCart();
});
</script>

<style scoped>
.nav-link {
  @apply relative px-3 py-2 rounded-lg text-[13px] font-medium text-[#4a3728]
         hover:bg-[#f0ebe4] hover:text-[#5c3d2e] transition-colors duration-200;
}

/* Active route highlight */
.router-link-active.nav-link {
  @apply text-[#7c5a3e] bg-[#f0ebe4];
}

.mobile-link {
  @apply flex items-center gap-3 px-4 py-3 text-[13px] font-medium text-[#4a3728]
         hover:bg-[#f5f0ea] hover:text-[#5c3d2e] transition-colors duration-200 cursor-pointer;
}

.router-link-active.mobile-link {
  @apply text-[#7c5a3e] bg-[#f5f0ea];
}
</style>
