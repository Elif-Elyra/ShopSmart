<script setup>
import { ref, computed, onMounted, watch } from "vue";
import {
  getCart,
  getaddresses,
  checkout,
  createAddress,
} from "../services/product";

const loading = ref(false);
const checkoutLoading = ref(false);
const error = ref("");
const success = ref("");
const cart = ref(null);
const addresses = ref([]);
const selectedAddress = ref(null);
const showAddressForm = ref(false);

const addressForm = ref({
  label: "",
  line: "",
  line2: "",
  city: "",
  region: "",
  postal_code: "",
  country: "Pakistan",
  is_default: false,
});

const payment = ref({
  card_number: "",
  holder_name: "",
  expiry_month: "",
  expiry_year: "",
  cvv: "",
});

const citySearch = ref("");
const cities = [
  "Lahore",
  "Faisalabad",
  "Rawalpindi",
  "Multan",
  "Gujranwala",
  "Sialkot",
  "Bahawalpur",
  "Sargodha",
  "Sheikhupura",
  "Rahim Yar Khan",
  "Karachi",
  "Islamabad",
  "Peshawar",
  "Quetta",
];

watch(citySearch, (value) => {
  addressForm.value.city = value;
});

const filteredCities = computed(() => {
  if (!citySearch.value.trim()) return [];
  return cities.filter((c) =>
    c.toLowerCase().includes(citySearch.value.toLowerCase()),
  );
});

const selectCity = (city) => {
  citySearch.value = city;
  addressForm.value.city = city;
};

const cartTotal = computed(() => {
  if (!cart.value?.items?.length) return 0;
  return cart.value.items.reduce(
    (sum, item) => sum + Number(item.product_price) * item.quantity,
    0,
  );
});

const shipping = computed(() => (cartTotal.value >= 100 ? 0 : 5));
const grandTotal = computed(() => cartTotal.value + shipping.value);

const fetchData = async () => {
  loading.value = true;
  error.value = "";
  try {
    const [cartRes, addrRes] = await Promise.all([getCart(), getaddresses()]);
    cart.value = cartRes;
    addresses.value = addrRes || [];
    if (addresses.value.length > 0) {
      const def = addresses.value.find((a) => a.is_default);
      selectedAddress.value = def?.id || addresses.value[0]?.id;
    }
  } catch (err) {
    error.value = err?.response?.data?.detail || "Failed to load data";
  } finally {
    loading.value = false;
  }
};

onMounted(fetchData);

const saveAddress = async () => {
  error.value = "";
  try {
    const res = await createAddress(addressForm.value);
    addresses.value.unshift(res);
    selectedAddress.value = res.id;
    showAddressForm.value = false;
    addressForm.value = {
      label: "",
      line: "",
      line2: "",
      city: "",
      region: "",
      postal_code: "",
      country: "Pakistan",
      is_default: false,
    };
    citySearch.value = "";
    success.value = "Address saved successfully";
  } catch (err) {
    error.value = err?.response?.data?.detail || "Failed to save address";
  }
};

const validatePayment = () => {
  const { card_number, holder_name, expiry_month, expiry_year, cvv } =
    payment.value;
  if (!card_number || !holder_name || !expiry_month || !expiry_year || !cvv) {
    error.value = "Please fill in all payment details";
    return false;
  }
  if (!/^\d{16}$/.test(card_number.replace(/\s/g, ""))) {
    error.value = "Card number must be 16 digits";
    return false;
  }
  if (!/^\d{3,4}$/.test(cvv)) {
    error.value = "Invalid CVV";
    return false;
  }
  const now = new Date();
  if (
    Number(expiry_year) < now.getFullYear() ||
    (Number(expiry_year) === now.getFullYear() &&
      Number(expiry_month) < now.getMonth() + 1)
  ) {
    error.value = "Card has expired";
    return false;
  }
  return true;
};

const placeOrder = async () => {
  if (checkoutLoading.value) return;
  error.value = "";
  success.value = "";
  if (!selectedAddress.value) {
    error.value = "Please select a shipping address";
    return;
  }
  if (!validatePayment()) return;
  checkoutLoading.value = true;
  try {
    const res = await checkout(
      {
        address_id: selectedAddress.value,
        payment: {
          card_number: payment.value.card_number,
          holder_name: payment.value.holder_name,
          expiry_month: Number(payment.value.expiry_month),
          expiry_year: Number(payment.value.expiry_year),
          cvv: payment.value.cvv,
        },
      },
      crypto.randomUUID(),
    );
    success.value = res.message || "Order placed successfully!";
    payment.value = {
      card_number: "",
      holder_name: "",
      expiry_month: "",
      expiry_year: "",
      cvv: "",
    };
    await fetchData();
  } catch (err) {
    error.value =
      err?.response?.data?.detail || "Checkout failed. Please try again.";
  } finally {
    checkoutLoading.value = false;
  }
};
</script>

<template>
  <div class="min-h-screen bg-[#f5f0eb] py-10 px-4">
    <div class="max-w-6xl mx-auto">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-extrabold text-[#2d2016] tracking-tight">
          Checkout
        </h1>
        <p class="text-sm text-[#a0907e] mt-1">
          Review your order and complete your purchase
        </p>
      </div>

      <!-- Loading -->
      <div
        v-if="loading"
        class="bg-white rounded-2xl border border-[#ede8e2] p-16 text-center shadow-sm"
      >
        <span
          class="inline-block animate-spin h-8 w-8 border-[3px] border-[#8d6040] border-t-transparent rounded-full"
        ></span>
        <p class="text-sm text-[#a0907e] mt-4">Loading your checkout...</p>
      </div>

      <!-- Empty Cart -->
      <div
        v-else-if="!cart?.items?.length"
        class="bg-white rounded-2xl border border-[#ede8e2] p-16 text-center shadow-sm"
      >
        <div
          class="w-14 h-14 rounded-2xl bg-[#f5f0ea] flex items-center justify-center mx-auto mb-4"
        >
          <svg
            class="w-7 h-7 text-[#c4b5a8]"
            fill="none"
            stroke="currentColor"
            stroke-width="1.5"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"
            />
            <line x1="3" y1="6" x2="21" y2="6" />
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M16 10a4 4 0 01-8 0"
            />
          </svg>
        </div>
        <h2 class="text-lg font-semibold text-[#2d2016]">Your cart is empty</h2>
        <p class="text-sm text-[#a0907e] mt-1">
          Add products before checking out
        </p>
        <router-link
          to="/products"
          class="inline-flex items-center gap-2 mt-5 px-5 py-2.5 rounded-xl bg-gradient-to-br from-[#7c5a3e] to-[#a5724f] text-white text-sm font-semibold shadow-sm hover:brightness-110 transition-all"
        >
          Browse Products
        </router-link>
      </div>

      <!-- Main Content -->
      <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- LEFT COLUMN -->
        <div class="lg:col-span-2 space-y-5">
          <!-- ===== ORDER ITEMS ===== -->
          <div
            class="bg-white rounded-2xl border border-[#ede8e2] shadow-sm overflow-hidden"
          >
            <div
              class="px-6 py-4 border-b border-[#f0ebe4] flex items-center gap-2"
            >
              <svg
                class="w-4 h-4 text-[#8d6040]"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                viewBox="0 0 24 24"
              >
                <path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z" />
                <line x1="3" y1="6" x2="21" y2="6" />
                <path d="M16 10a4 4 0 01-8 0" />
              </svg>
              <h2
                class="text-sm font-bold text-[#2d2016] uppercase tracking-wider"
              >
                Order Items
              </h2>
              <span
                class="ml-auto text-xs text-[#a0907e] bg-[#f5f0ea] px-2 py-0.5 rounded-full"
                >{{ cart.items.length }} items</span
              >
            </div>

            <div class="divide-y divide-[#f5f0ea]">
              <div
                v-for="item in cart.items"
                :key="item.id"
                class="flex items-center gap-4 px-6 py-4"
              >
                <div
                  class="w-16 h-16 rounded-xl bg-[#f5f0ea] border border-[#ede8e2] overflow-hidden shrink-0"
                >
                  <img
                    :src="item.product_image"
                    :alt="item.product_title"
                    class="w-full h-full object-cover"
                  />
                </div>
                <div class="flex-1 min-w-0">
                  <h3 class="text-sm font-semibold text-[#2d2016] line-clamp-1">
                    {{ item.product_title }}
                  </h3>
                  <p class="text-xs text-[#a0907e] mt-0.5">
                    Qty: {{ item.quantity }} × ${{ item.product_price }}
                  </p>
                </div>
                <p class="text-sm font-bold text-[#7c5a3e] shrink-0">
                  ${{ (Number(item.product_price) * item.quantity).toFixed(2) }}
                </p>
              </div>
            </div>
          </div>

          <!-- ===== SHIPPING ADDRESS ===== -->
          <div
            class="bg-white rounded-2xl border border-[#ede8e2] shadow-sm overflow-hidden"
          >
            <div
              class="px-6 py-4 border-b border-[#f0ebe4] flex items-center justify-between"
            >
              <div class="flex items-center gap-2">
                <svg
                  class="w-4 h-4 text-[#8d6040]"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  viewBox="0 0 24 24"
                >
                  <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z" />
                  <circle cx="12" cy="10" r="3" />
                </svg>
                <h2
                  class="text-sm font-bold text-[#2d2016] uppercase tracking-wider"
                >
                  Shipping Address
                </h2>
              </div>
              <button
                @click="showAddressForm = !showAddressForm"
                class="flex items-center gap-1.5 text-xs font-semibold px-3 py-1.5 rounded-lg border transition-colors"
                :class="
                  showAddressForm
                    ? 'border-red-200 text-red-600 bg-red-50 hover:bg-red-100'
                    : 'border-[#c9a882] text-[#7c5a3e] bg-[#f5f0ea] hover:bg-[#ede8e2]'
                "
              >
                <svg
                  v-if="!showAddressForm"
                  class="w-3 h-3"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2.5"
                  viewBox="0 0 24 24"
                >
                  <path d="M12 5v14M5 12h14" />
                </svg>
                <svg
                  v-else
                  class="w-3 h-3"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2.5"
                  viewBox="0 0 24 24"
                >
                  <path d="M18 6L6 18M6 6l12 12" />
                </svg>
                {{ showAddressForm ? "Cancel" : "Add New" }}
              </button>
            </div>

            <div class="p-6 space-y-4">
              <!-- Saved addresses -->
              <div v-if="addresses.length" class="space-y-2">
                <label
                  v-for="addr in addresses"
                  :key="addr.id"
                  class="flex items-start gap-3 p-4 rounded-xl border cursor-pointer transition-all"
                  :class="
                    selectedAddress === addr.id
                      ? 'border-[#8d6040] bg-[#f5f0ea] ring-1 ring-[#8d6040]/20'
                      : 'border-[#ede8e2] hover:border-[#c9a882] hover:bg-[#faf8f5]'
                  "
                >
                  <input
                    type="radio"
                    :value="addr.id"
                    v-model="selectedAddress"
                    class="mt-0.5 accent-[#7c5a3e]"
                  />
                  <div>
                    <p class="text-sm font-semibold text-[#2d2016]">
                      {{ addr.label }}
                    </p>
                    <p class="text-xs text-[#a0907e] mt-0.5">
                      {{ addr.line }}{{ addr.line2 ? ", " + addr.line2 : "" }},
                      {{ addr.city }}, {{ addr.region }} {{ addr.postal_code }}
                    </p>
                    <span
                      v-if="addr.is_default"
                      class="inline-block mt-1 text-[10px] font-semibold text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded-full"
                      >Default</span
                    >
                  </div>
                </label>
              </div>
              <p
                v-else-if="!showAddressForm"
                class="text-sm text-[#a0907e] text-center py-4"
              >
                No saved addresses. Add one below.
              </p>

              <!-- Add address form -->
              <div
                v-if="showAddressForm"
                class="border-t border-[#f0ebe4] pt-5 space-y-3"
              >
                <p
                  class="text-xs font-bold text-[#2d2016] uppercase tracking-wider"
                >
                  New Address
                </p>

                <input
                  v-model="addressForm.label"
                  placeholder="Label (e.g. Home, Office)"
                  class="checkout-input"
                />
                <input
                  v-model="addressForm.line"
                  placeholder="Street address"
                  class="checkout-input"
                />
                <input
                  v-model="addressForm.line2"
                  placeholder="Apartment, suite, etc. (optional)"
                  class="checkout-input"
                />

                <!-- City search -->
                <div class="relative">
                  <input
                    v-model="citySearch"
                    placeholder="Search city..."
                    class="checkout-input"
                  />
                  <div
                    v-if="filteredCities.length"
                    class="absolute top-full left-0 w-full bg-white border border-[#ede8e2] rounded-xl shadow-lg z-20 mt-1 overflow-hidden"
                  >
                    <div
                      v-for="city in filteredCities"
                      :key="city"
                      @click="selectCity(city)"
                      class="px-4 py-2.5 text-sm text-[#4a3728] hover:bg-[#f5f0ea] cursor-pointer transition-colors"
                    >
                      {{ city }}
                    </div>
                  </div>
                </div>

                <div class="grid grid-cols-2 gap-3">
                  <input
                    v-model="addressForm.region"
                    placeholder="Province"
                    class="checkout-input"
                  />
                  <input
                    v-model="addressForm.postal_code"
                    placeholder="Postal code"
                    class="checkout-input"
                  />
                </div>

                <input v-model="addressForm.country" class="checkout-input" />

                <label
                  class="flex items-center gap-2 text-sm text-[#4a3728] cursor-pointer"
                >
                  <input
                    type="checkbox"
                    v-model="addressForm.is_default"
                    class="w-4 h-4 rounded accent-[#7c5a3e]"
                  />
                  Set as default address
                </label>

                <button
                  @click="saveAddress"
                  class="w-full h-10 rounded-xl bg-gradient-to-br from-[#7c5a3e] to-[#a5724f] text-white text-sm font-semibold hover:brightness-110 transition-all shadow-sm"
                >
                  Save Address
                </button>
              </div>
            </div>
          </div>

          <!-- ===== PAYMENT ===== -->
          <div
            class="bg-white rounded-2xl border border-[#ede8e2] shadow-sm overflow-hidden"
          >
            <div
              class="px-6 py-4 border-b border-[#f0ebe4] flex items-center gap-2"
            >
              <svg
                class="w-4 h-4 text-[#8d6040]"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                viewBox="0 0 24 24"
              >
                <rect x="1" y="4" width="22" height="16" rx="2" />
                <line x1="1" y1="10" x2="23" y2="10" />
              </svg>
              <h2
                class="text-sm font-bold text-[#2d2016] uppercase tracking-wider"
              >
                Payment Details
              </h2>
              <!-- Card logos -->
              <div class="ml-auto flex items-center gap-1.5">
                <span
                  class="text-[10px] font-bold bg-[#1a1f71] text-white px-2 py-0.5 rounded"
                  >VISA</span
                >
                <span
                  class="text-[10px] font-bold bg-[#eb001b] text-white px-2 py-0.5 rounded"
                  >MC</span
                >
              </div>
            </div>

            <div class="p-6 space-y-4">
              <!-- Card number -->
              <div class="space-y-1.5">
                <label class="block text-xs font-semibold text-[#4a3728]"
                  >Card Number</label
                >
                <div class="relative">
                  <svg
                    class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[#a0907e]"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    viewBox="0 0 24 24"
                  >
                    <rect x="1" y="4" width="22" height="16" rx="2" />
                    <line x1="1" y1="10" x2="23" y2="10" />
                  </svg>
                  <input
                    v-model="payment.card_number"
                    placeholder="1234 5678 9012 3456"
                    maxlength="16"
                    class="checkout-input pl-9"
                  />
                </div>
              </div>

              <!-- Holder name -->
              <div class="space-y-1.5">
                <label class="block text-xs font-semibold text-[#4a3728]"
                  >Card Holder Name</label
                >
                <div class="relative">
                  <svg
                    class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[#a0907e]"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    viewBox="0 0 24 24"
                  >
                    <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2" />
                    <circle cx="12" cy="7" r="4" />
                  </svg>
                  <input
                    v-model="payment.holder_name"
                    placeholder="Name on card"
                    class="checkout-input pl-9"
                  />
                </div>
              </div>

              <!-- Expiry + CVV -->
              <div class="grid grid-cols-3 gap-3">
                <div class="space-y-1.5">
                  <label class="block text-xs font-semibold text-[#4a3728]"
                    >Month</label
                  >
                  <input
                    v-model="payment.expiry_month"
                    placeholder="MM"
                    maxlength="2"
                    class="checkout-input text-center"
                  />
                </div>
                <div class="space-y-1.5">
                  <label class="block text-xs font-semibold text-[#4a3728]"
                    >Year</label
                  >
                  <input
                    v-model="payment.expiry_year"
                    placeholder="YYYY"
                    maxlength="4"
                    class="checkout-input text-center"
                  />
                </div>
                <div class="space-y-1.5">
                  <label class="block text-xs font-semibold text-[#4a3728]"
                    >CVV</label
                  >
                  <input
                    v-model="payment.cvv"
                    type="password"
                    placeholder="•••"
                    maxlength="4"
                    class="checkout-input text-center"
                  />
                </div>
              </div>

              <!-- Security note -->
              <div
                class="flex items-center gap-2 bg-emerald-50 border border-emerald-200 rounded-xl px-4 py-2.5"
              >
                <svg
                  class="w-4 h-4 text-emerald-600 shrink-0"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  viewBox="0 0 24 24"
                >
                  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
                </svg>
                <span class="text-xs text-emerald-700 font-medium"
                  >Your payment info is encrypted and secure</span
                >
              </div>
            </div>
          </div>

          <!-- Error / Success -->
          <div
            v-if="error"
            class="flex items-center gap-2 bg-red-50 border border-red-200 text-red-700 text-sm rounded-xl px-4 py-3"
          >
            <svg
              class="w-4 h-4 shrink-0"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              viewBox="0 0 24 24"
            >
              <circle cx="12" cy="12" r="10" />
              <path d="M12 8v4M12 16h.01" />
            </svg>
            {{ error }}
          </div>
          <div
            v-if="success"
            class="flex items-center gap-2 bg-emerald-50 border border-emerald-200 text-emerald-700 text-sm rounded-xl px-4 py-3"
          >
            <svg
              class="w-4 h-4 shrink-0"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              viewBox="0 0 24 24"
            >
              <polyline points="20 6 9 17 4 12" />
            </svg>
            {{ success }}
          </div>
        </div>

        <!-- RIGHT COLUMN — Order Summary -->
        <div class="lg:col-span-1">
          <div
            class="bg-white rounded-2xl border border-[#ede8e2] shadow-sm p-6 sticky top-20"
          >
            <h2
              class="text-sm font-bold text-[#2d2016] uppercase tracking-wider mb-5"
            >
              Order Summary
            </h2>

            <!-- Items breakdown -->
            <div class="space-y-2 text-sm">
              <div
                v-for="item in cart.items"
                :key="item.id"
                class="flex justify-between text-[#6b5a4e]"
              >
                <span class="line-clamp-1 flex-1 pr-2"
                  >{{ item.product_title }} ×{{ item.quantity }}</span
                >
                <span class="shrink-0"
                  >${{
                    (Number(item.product_price) * item.quantity).toFixed(2)
                  }}</span
                >
              </div>
            </div>

            <div
              class="border-t border-[#f0ebe4] mt-4 pt-4 space-y-2.5 text-sm"
            >
              <div class="flex justify-between text-[#6b5a4e]">
                <span>Subtotal</span>
                <span class="font-medium text-[#2d2016]"
                  >${{ cartTotal.toFixed(2) }}</span
                >
              </div>
              <div class="flex justify-between text-[#6b5a4e]">
                <span>Shipping</span>
                <span
                  class="font-medium"
                  :class="
                    shipping === 0 ? 'text-emerald-600' : 'text-[#2d2016]'
                  "
                >
                  {{ shipping === 0 ? "Free" : "$" + shipping.toFixed(2) }}
                </span>
              </div>
              <div
                v-if="shipping > 0"
                class="flex items-center gap-1.5 bg-[#f5f0ea] rounded-lg px-3 py-2 text-xs text-[#8d6040]"
              >
                <svg
                  class="w-3.5 h-3.5 shrink-0"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  viewBox="0 0 24 24"
                >
                  <circle cx="12" cy="12" r="10" />
                  <path d="M12 8v4M12 16h.01" />
                </svg>
                Add ${{ (100 - cartTotal).toFixed(2) }} more for free shipping
              </div>
            </div>

            <div
              class="border-t border-[#f0ebe4] mt-4 pt-4 flex justify-between"
            >
              <span class="font-bold text-[#2d2016]">Total</span>
              <span class="text-xl font-extrabold text-[#7c5a3e]"
                >${{ grandTotal.toFixed(2) }}</span
              >
            </div>

            <button
              @click="placeOrder"
              :disabled="checkoutLoading"
              class="w-full mt-6 py-3.5 rounded-xl bg-gradient-to-br from-[#7c5a3e] to-[#a5724f] text-white text-sm font-bold hover:brightness-110 transition-all shadow-md flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="!checkoutLoading" class="flex items-center gap-2">
                <svg
                  class="w-4 h-4"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2.5"
                  viewBox="0 0 24 24"
                >
                  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
                </svg>
                Complete Purchase
              </span>
              <span v-else class="flex items-center gap-2">
                <span
                  class="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"
                ></span>
                Processing...
              </span>
            </button>

            <p
              class="text-center text-xs text-[#c4b5a8] mt-4 flex items-center justify-center gap-1"
            >
              <svg
                class="w-3.5 h-3.5"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                viewBox="0 0 24 24"
              >
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
              </svg>
              Secure 256-bit SSL encrypted checkout
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.checkout-input {
  @apply w-full px-3 py-2.5 text-sm bg-[#f5f0ea] border border-[#ede8e2] rounded-xl
         text-[#2d2016] placeholder-[#c4b5a8]
         focus:outline-none focus:border-[#8d6040] focus:ring-2 focus:ring-[#8d6040]/10 transition-all;
}
</style>
