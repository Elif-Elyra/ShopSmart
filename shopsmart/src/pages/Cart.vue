<template>
  <div class="min-h-screen bg-[#f5f0eb] py-10 px-4">
    <div class="max-w-6xl mx-auto">

      <!-- Page Header -->
      <div class="mb-8">
        <h2 class="text-2xl font-bold text-[#2d2016] tracking-tight">Your Cart</h2>
        <p class="text-sm text-[#a0907e] mt-1">
          {{ cart.length }} {{ cart.length === 1 ? 'item' : 'items' }} in your cart
        </p>
      </div>

      <!-- Empty State -->
      <div
        v-if="cart.length === 0"
        class="bg-white rounded-2xl shadow-sm border border-[#ede8e2] py-20 flex flex-col items-center justify-center text-center"
      >
        <div class="w-16 h-16 rounded-2xl bg-[#f5f0ea] flex items-center justify-center mb-4">
          <svg class="w-8 h-8 text-[#b8916a]" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/>
            <line x1="3" y1="6" x2="21" y2="6"/>
            <path stroke-linecap="round" stroke-linejoin="round" d="M16 10a4 4 0 01-8 0"/>
          </svg>
        </div>
        <h3 class="text-[#2d2016] font-semibold text-lg mb-1">Your cart is empty</h3>
        <p class="text-sm text-[#a0907e] mb-6">Add some items to get started</p>
        <router-link
          to="/"
          class="px-6 py-2.5 rounded-xl bg-gradient-to-br from-[#7c5a3e] to-[#a5724f] text-white text-sm font-medium hover:brightness-110 transition-all shadow-sm"
        >
          Browse Products
        </router-link>
      </div>

      <!-- Main Grid -->
      <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-6">

        <!-- Cart Items -->
        <div class="lg:col-span-2 space-y-3">
          <div
            v-for="item in cart"
            :key="item.id"
            class="bg-white rounded-2xl border border-[#ede8e2] shadow-sm hover:shadow-md transition-shadow duration-200 p-4 flex items-center gap-4"
          >
            <!-- Image -->
            <div class="w-24 h-24 shrink-0 rounded-xl bg-[#f5f0ea] overflow-hidden border border-[#ede8e2]">
              <img
                :src="item.product_image"
                :alt="item.product_title"
                class="w-full h-full object-contain p-2"
              />
            </div>

            <!-- Info -->
            <div class="flex-1 min-w-0">
              <h3 class="font-semibold text-[#2d2016] text-sm leading-snug truncate">
                {{ item.product_title }}
              </h3>
              <p class="text-xs text-[#a0907e] mt-0.5">${{ item.product_price }} each</p>

              <!-- Quantity Controls -->
              <div class="flex items-center gap-1 mt-3">
                <button
                  @click="decrease(item)"
                  :disabled="item.quantity <= 1"
                  class="w-7 h-7 rounded-lg bg-[#f5f0ea] hover:bg-[#ede8e2] disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center text-[#4a3728] font-bold text-sm transition-colors"
                >−</button>
                <span class="w-8 text-center text-sm font-semibold text-[#2d2016]">{{ item.quantity }}</span>
                <button
                  @click="increase(item)"
                  class="w-7 h-7 rounded-lg bg-[#f5f0ea] hover:bg-[#ede8e2] flex items-center justify-center text-[#4a3728] font-bold text-sm transition-colors"
                >+</button>
              </div>
            </div>

            <!-- Price + Remove -->
            <div class="text-right shrink-0 flex flex-col items-end gap-3">
              <p class="font-bold text-[#2d2016] text-base">
                ${{ (item.product_price * item.quantity).toFixed(2) }}
              </p>
              <button
                @click="remove(item.id)"
                class="flex items-center gap-1 text-xs text-[#a0907e] hover:text-red-500 transition-colors"
              >
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 01-2 2H8a2 2 0 01-2-2L5 6"/><path d="M10 11v6M14 11v6"/><path d="M9 6V4a1 1 0 011-1h4a1 1 0 011 1v2"/>
                </svg>
                Remove
              </button>
            </div>
          </div>
        </div>

        <!-- Order Summary -->
        <div class="lg:col-span-1">
          <div class="bg-white rounded-2xl border border-[#ede8e2] shadow-sm p-6 sticky top-20">

            <h3 class="text-base font-bold text-[#2d2016] mb-5">Order Summary</h3>

            <div class="space-y-3 text-sm">
              <div class="flex justify-between text-[#6b5a4e]">
                <span>Subtotal ({{ cart.length }} items)</span>
                <span class="font-medium text-[#2d2016]">${{ subtotal.toFixed(2) }}</span>
              </div>
              <div class="flex justify-between text-[#6b5a4e]">
                <span>Shipping</span>
                <span class="font-medium text-[#2d2016]">
                  {{ subtotal >= 100 ? 'Free' : '$5.00' }}
                </span>
              </div>
              <div v-if="subtotal < 100" class="flex items-center gap-1.5 bg-[#f5f0ea] rounded-lg px-3 py-2 text-xs text-[#8d6040]">
                <svg class="w-3.5 h-3.5 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/>
                </svg>
                Add ${{ (100 - subtotal).toFixed(2) }} more for free shipping
              </div>
              <div class="border-t border-[#ede8e2] pt-3 flex justify-between font-bold text-[#2d2016]">
                <span>Total</span>
                <span class="text-lg">${{ total.toFixed(2) }}</span>
              </div>
            </div>

            <button
              @click="checkoutlink()"
              class="w-full mt-6 py-3 rounded-xl bg-gradient-to-br from-[#7c5a3e] to-[#a5724f] text-white text-sm font-semibold flex items-center justify-center gap-2 hover:brightness-110 transition-all duration-200 shadow-sm"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
              </svg>
              Proceed to Checkout
            </button>

            <router-link
              to="/"
              class="block text-center text-xs text-[#a0907e] hover:text-[#7c5a3e] mt-4 transition-colors"
            >
              ← Continue Shopping
            </router-link>
          </div>
        </div>
      </div>

      <!-- Trust Badges -->
      <div class="mt-8 bg-white rounded-2xl border border-[#ede8e2] shadow-sm p-6 grid grid-cols-2 md:grid-cols-4 gap-6">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 rounded-xl bg-[#f5f0ea] flex items-center justify-center shrink-0">
            <svg class="w-5 h-5 text-[#8d6040]" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
              <rect x="1" y="3" width="15" height="13" rx="1"/><path d="M16 8h4l3 5v3h-7V8z"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/>
            </svg>
          </div>
          <div>
            <h4 class="font-semibold text-[#2d2016] text-xs">Free Shipping</h4>
            <p class="text-[11px] text-[#a0907e] mt-0.5">On orders over $100</p>
          </div>
        </div>

        <div class="flex items-center gap-3">
          <div class="w-9 h-9 rounded-xl bg-[#f5f0ea] flex items-center justify-center shrink-0">
            <svg class="w-5 h-5 text-[#8d6040]" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
              <path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 9.81a19.79 19.79 0 01-3.07-8.63A2 2 0 012 .94h3a2 2 0 012 1.72 12.84 12.84 0 00.7 2.81 2 2 0 01-.45 2.11L6.09 8.79a16 16 0 006.12 6.12l1.21-1.21a2 2 0 012.11-.45 12.84 12.84 0 002.81.7A2 2 0 0122 16.92z"/>
            </svg>
          </div>
          <div>
            <h4 class="font-semibold text-[#2d2016] text-xs">24/7 Support</h4>
            <p class="text-[11px] text-[#a0907e] mt-0.5">Always here to help</p>
          </div>
        </div>

        <div class="flex items-center gap-3">
          <div class="w-9 h-9 rounded-xl bg-[#f5f0ea] flex items-center justify-center shrink-0">
            <svg class="w-5 h-5 text-[#8d6040]" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
              <rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0110 0v4"/>
            </svg>
          </div>
          <div>
            <h4 class="font-semibold text-[#2d2016] text-xs">Secure Payment</h4>
            <p class="text-[11px] text-[#a0907e] mt-0.5">100% safe & encrypted</p>
          </div>
        </div>

        <div class="flex items-center gap-3">
          <div class="w-9 h-9 rounded-xl bg-[#f5f0ea] flex items-center justify-center shrink-0">
            <svg class="w-5 h-5 text-[#8d6040]" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
              <polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/>
              <path d="M3.51 9a9 9 0 0114.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0020.49 15"/>
            </svg>
          </div>
          <div>
            <h4 class="font-semibold text-[#2d2016] text-xs">Easy Returns</h4>
            <p class="text-[11px] text-[#a0907e] mt-0.5">30-day return policy</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// ✅ Fix — poora script setup replace karo
import { computed, onMounted } from "vue";
import { useCartStore } from "../store/cartStore";
import { updateCartItem } from "../services/product";
import { useRouter } from "vue-router";
import { storeToRefs } from "pinia";

const router = useRouter();
const cartStore = useCartStore();
const { items: cart } = storeToRefs(cartStore); // ✅ store ka reactive data

const checkoutlink = () => router.push("/checkout");

onMounted(() => {
  cartStore.fetchCart(); // ✅ store se fetch
});

async function increase(item) {
  const newQty = item.quantity + 1;
  try {
    await updateCartItem(item.id, { quantity: newQty });
    item.quantity = newQty; // storeToRefs se direct mutate ho sakta hai
  } catch (error) {
    console.error("Failed to increase quantity");
  }
}

async function decrease(item) {
  if (item.quantity <= 1) return;
  const newQty = item.quantity - 1;
  try {
    await updateCartItem(item.id, { quantity: newQty });
    item.quantity = newQty;
  } catch (error) {
    console.error("Failed to decrease quantity");
  }
}

async function remove(id) {
  await cartStore.removeItem(id); // ✅ store ka action — badge bhi update hoga
}

const subtotal = computed(() =>
  cart.value.reduce((sum, i) => sum + i.product_price * i.quantity, 0)
);

const total = computed(() =>
  subtotal.value >= 100 ? subtotal.value : subtotal.value + 5
);
</script>