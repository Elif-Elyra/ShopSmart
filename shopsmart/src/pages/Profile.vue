<template>
  <div class="min-h-screen bg-[#f5f0eb] py-10 px-4">
    <div class="max-w-6xl mx-auto space-y-6">

      <!-- Page Loading -->
      <div v-if="pageLoading" class="flex justify-center items-center py-32">
        <span class="animate-spin h-8 w-8 border-[3px] border-[#8d6040] border-t-transparent rounded-full"></span>
      </div>

      <template v-else>

        <!-- ===== PROFILE HEADER ===== -->
        <div class="rounded-2xl overflow-hidden shadow-md border border-[#c9a882]/30">
          <!-- Gradient Banner — full info inside -->
          <div class="bg-gradient-to-br from-[#3d2712] via-[#7c5a3e] to-[#c4956a] px-8 py-8 relative">

            <!-- Subtle pattern overlay -->
            <div class="absolute inset-0 opacity-10"
              style="background-image: radial-gradient(circle at 20% 50%, #fff 1px, transparent 1px), radial-gradient(circle at 80% 20%, #fff 1px, transparent 1px); background-size: 40px 40px;">
            </div>

            <div class="relative flex flex-col md:flex-row md:items-center md:justify-between gap-6">

              <!-- Left: Avatar + Info -->
              <div class="flex items-center gap-5">
                <!-- Avatar -->
                <div class="w-20 h-20 md:w-24 md:h-24 rounded-2xl bg-white/15 border-2 border-white/30 text-white flex items-center justify-center text-3xl font-bold shadow-xl backdrop-blur-sm shrink-0">
                  {{ initials }}
                </div>

                <!-- Info -->
                <div>
                  <div class="flex items-center gap-2.5 flex-wrap">
                    <h1 class="text-2xl md:text-3xl font-bold text-white tracking-tight">{{ auth.user?.fullname }}</h1>
                    <span
                      v-if="auth.user?.is_seller"
                      class="px-3 py-1 rounded-full bg-white/20 border border-white/30 text-white text-xs font-semibold backdrop-blur-sm"
                    >
                      ✦ Seller
                    </span>
                  </div>
                  <p class="text-white/70 text-sm mt-1">{{ auth.user?.email }}</p>
                  <p class="text-white/45 text-xs mt-1">Member since {{ formattedDate }}</p>

                  <!-- Quick stats pills (lg only) -->
                  <div v-if="auth.user?.is_seller" class="hidden md:flex items-center gap-3 mt-3">
                    <span class="text-xs bg-white/10 border border-white/20 text-white/80 px-3 py-1 rounded-full">
                      {{ stats.products }} Products
                    </span>
                    <span class="text-xs bg-white/10 border border-white/20 text-white/80 px-3 py-1 rounded-full">
                      {{ stats.orders }} Orders
                    </span>
                    <span class="text-xs bg-emerald-400/20 border border-emerald-300/30 text-emerald-200 px-3 py-1 rounded-full font-semibold">
                      ${{ stats.revenue }} Revenue
                    </span>
                  </div>
                </div>
              </div>

              <!-- Right: Actions -->
              <div class="flex flex-wrap gap-3 md:shrink-0">
                <button
                  v-if="!auth.user?.is_seller"
                  @click="becomeSellerHandler"
                  :disabled="loading"
                  class="h-11 px-6 rounded-xl bg-white text-[#7c5a3e] text-sm font-bold hover:bg-white/90 transition-all shadow-lg disabled:opacity-50 flex items-center gap-2"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                  </svg>
                  <span v-if="!loading">Become a Seller</span>
                  <span v-else class="flex items-center gap-2">
                    <span class="animate-spin h-3.5 w-3.5 border-2 border-[#7c5a3e] border-t-transparent rounded-full"></span>
                    Activating...
                  </span>
                </button>

                <RouterLink
                  v-if="auth.user?.is_seller"
                  to="/admin-panel"
                  class="h-11 px-6 rounded-xl bg-white text-[#7c5a3e] text-sm font-bold hover:bg-white/90 transition-all shadow-lg flex items-center gap-2"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/>
                    <rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>
                  </svg>
                  Seller Dashboard
                </RouterLink>
              </div>
            </div>
          </div>
        </div>

        <!-- ===== SELLER STATS ===== -->
        <div v-if="auth.user?.is_seller" class="grid grid-cols-2 md:grid-cols-4 gap-4">

          <div class="bg-white rounded-2xl border border-[#ede8e2] shadow-sm p-5 flex items-center gap-4">
            <div class="w-10 h-10 rounded-xl bg-[#f5f0ea] flex items-center justify-center shrink-0">
              <svg class="w-5 h-5 text-[#8d6040]" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
                <path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/>
                <path d="M16 10a4 4 0 01-8 0"/>
              </svg>
            </div>
            <div>
              <p class="text-xs text-[#a0907e] font-medium">Products</p>
              <h2 class="text-2xl font-bold text-[#2d2016] mt-0.5">{{ stats.products }}</h2>
            </div>
          </div>

          <div class="bg-white rounded-2xl border border-[#ede8e2] shadow-sm p-5 flex items-center gap-4">
            <div class="w-10 h-10 rounded-xl bg-[#f5f0ea] flex items-center justify-center shrink-0">
              <svg class="w-5 h-5 text-[#8d6040]" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
                <path d="M9 17H5a2 2 0 00-2 2v2h18v-2a2 2 0 00-2-2h-4M12 3v10M9 10l3 3 3-3"/>
              </svg>
            </div>
            <div>
              <p class="text-xs text-[#a0907e] font-medium">Orders</p>
              <h2 class="text-2xl font-bold text-[#2d2016] mt-0.5">{{ stats.orders }}</h2>
            </div>
          </div>

          <div class="bg-white rounded-2xl border border-[#ede8e2] shadow-sm p-5 flex items-center gap-4">
            <div class="w-10 h-10 rounded-xl bg-[#f5f0ea] flex items-center justify-center shrink-0">
              <svg class="w-5 h-5 text-[#8d6040]" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
              </svg>
            </div>
            <div>
              <p class="text-xs text-[#a0907e] font-medium">Reviews</p>
              <h2 class="text-2xl font-bold text-[#2d2016] mt-0.5">{{ stats.reviews }}</h2>
            </div>
          </div>

          <div class="bg-white rounded-2xl border border-[#ede8e2] shadow-sm p-5 flex items-center gap-4">
            <div class="w-10 h-10 rounded-xl bg-emerald-50 flex items-center justify-center shrink-0">
              <svg class="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
                <line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/>
              </svg>
            </div>
            <div>
              <p class="text-xs text-[#a0907e] font-medium">Revenue</p>
              <h2 class="text-2xl font-bold text-emerald-600 mt-0.5">${{ stats.revenue }}</h2>
            </div>
          </div>

        </div>

        <!-- ===== ACCOUNT INFO + ORDERS ===== -->
        <div class="grid lg:grid-cols-3 gap-6">

          <!-- Account Info -->
          <div class="lg:col-span-1 bg-white rounded-2xl border border-[#ede8e2] shadow-sm p-6">
            <h2 class="text-sm font-bold text-[#2d2016] uppercase tracking-wider mb-5">Account Information</h2>

            <div class="space-y-4">
              <div v-for="field in accountFields" :key="field.label" class="flex items-start gap-3">
                <div class="w-8 h-8 rounded-lg bg-[#f5f0ea] flex items-center justify-center shrink-0 mt-0.5">
                  <component :is="'svg'" class="w-4 h-4 text-[#8d6040]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" v-html="field.icon"></component>
                </div>
                <div>
                  <p class="text-[11px] text-[#a0907e] font-medium uppercase tracking-wide">{{ field.label }}</p>
                  <p class="text-sm font-semibold text-[#2d2016] mt-0.5">{{ field.value }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Recent Orders -->
          <div class="lg:col-span-2 bg-white rounded-2xl border border-[#ede8e2] shadow-sm p-6">
            <div class="flex items-center justify-between mb-5">
              <h2 class="text-sm font-bold text-[#2d2016] uppercase tracking-wider">Recent Orders</h2>
              <span class="text-[11px] text-[#a0907e] bg-[#f5f0ea] px-2.5 py-1 rounded-full font-medium">
                {{ orders.length }} orders
              </span>
            </div>

            <!-- Orders List -->
            <div v-if="orders.length" class="space-y-3">
              <div
                v-for="order in orders"
                :key="order.id"
                class="flex items-center justify-between p-4 rounded-xl border border-[#ede8e2] bg-[#faf8f5] hover:bg-[#f5f0ea] transition-colors"
              >
                <div class="flex items-center gap-3">
                  <div class="w-9 h-9 rounded-xl bg-white border border-[#ede8e2] flex items-center justify-center shrink-0">
                    <svg class="w-4 h-4 text-[#8d6040]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                      <path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/>
                    </svg>
                  </div>
                  <div>
                    <p class="text-sm font-semibold text-[#2d2016]">{{ order.product }}</p>
                    <p class="text-[11px] text-[#a0907e] mt-0.5">
                      Buyer: <span class="text-[#6b5a4e]">{{ order.buyer_name }}</span>
                      · Seller: <span class="text-[#6b5a4e]">{{ order.seller_name }}</span>
                    </p>
                  </div>
                </div>

                <div class="text-right shrink-0 ml-4">
                  <p class="text-sm font-bold text-[#7c5a3e]">${{ order.amount }}</p>
                  <span class="inline-block mt-1 text-[10px] px-2 py-0.5 rounded-full font-semibold"
                    :class="order.status === 'paid'
                      ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                      : 'bg-amber-50 text-amber-700 border border-amber-200'"
                  >
                    {{ order.status || 'Paid' }}
                  </span>
                </div>
              </div>
            </div>

            <!-- Empty Orders -->
            <div v-else class="flex flex-col items-center justify-center py-14 text-center">
              <div class="w-12 h-12 rounded-2xl bg-[#f5f0ea] flex items-center justify-center mb-3">
                <svg class="w-6 h-6 text-[#c4b5a8]" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path d="M9 17H5a2 2 0 00-2 2v2h18v-2a2 2 0 00-2-2h-4M12 3v10M9 10l3 3 3-3"/>
                </svg>
              </div>
              <p class="text-sm font-medium text-[#6b5a4e]">No orders yet</p>
              <p class="text-xs text-[#c4b5a8] mt-1">Orders will appear here once placed</p>
            </div>
          </div>

        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useAuthStore } from "../store/authStore";
import {
  getSellerProducts,
  getSellerOrders,
  getProductReviews,
} from "../services/product";

const auth = useAuthStore();
const loading = ref(false);
const pageLoading = ref(false);

const stats = ref({ products: 0, orders: 0, reviews: 0, revenue: 0 });
const orders = ref([]);

// Account fields for clean rendering
const accountFields = computed(() => [
  {
    label: "Full Name",
    value: auth.user?.fullname || "—",
    icon: '<path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/>',
  },
  {
    label: "Email Address",
    value: auth.user?.email || "—",
    icon: '<path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/>',
  },
  {
    label: "Username",
    value: auth.user?.username ? `@${auth.user.username}` : "—",
    icon: '<circle cx="12" cy="12" r="4"/><path d="M16 8v5a3 3 0 006 0v-1a10 10 0 10-3.92 7.94"/>',
  },
  {
    label: "Account Type",
    value: auth.user?.is_seller ? "Seller Account" : "Buyer Account",
    icon: '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
  },
]);

const formattedDate = computed(() => {
  if (!auth.user?.created_at) return "";
  return new Date(auth.user.created_at).toLocaleDateString("en-US", {
    year: "numeric", month: "long", day: "numeric",
  });
});

const initials = computed(() => {
  const name = auth.user?.fullname;
  if (!name) return "?";
  return name.split(" ").map((w) => w[0]).join("").toUpperCase().slice(0, 2);
});

const loadDashboardData = async () => {
  try {
    pageLoading.value = true;
    const [productsData, ordersData] = await Promise.all([
      getSellerProducts(),
      getSellerOrders(),
    ]);

    const products = Array.isArray(productsData) ? productsData : [];
    const sellerOrders = Array.isArray(ordersData) ? ordersData : [];

    stats.value.products = products.length;
    stats.value.orders = sellerOrders.length;
    stats.value.revenue = sellerOrders.reduce(
      (total, order) => total + Number(order.subtotal || 0), 0
    );

    let totalReviews = 0;
    await Promise.all(
      products.map(async (product) => {
        try {
          const reviews = await getProductReviews(product.id);
          if (Array.isArray(reviews)) totalReviews += reviews.length;
          else if (reviews?.results) totalReviews += reviews.results.length;
        } catch {}
      })
    );
    stats.value.reviews = totalReviews;

    orders.value = sellerOrders.slice(0, 5).map((order) => ({
      id: order.id,
      product: `Order #${order.order}`,
      amount: order.subtotal,
      buyer_name: order.buyer_name,
      seller_name: order.seller_name,
      status: order.status,
    }));
  } catch (error) {
    console.error("Dashboard Error:", error);
  } finally {
    pageLoading.value = false;
  }
};

onMounted(async () => {
  try {
    if (!auth.user) await auth.fetchUser();
    if (auth.user?.is_seller) await loadDashboardData();
  } catch (error) {
    console.error(error);
  }
});

const becomeSellerHandler = async () => {
  try {
    loading.value = true;
    await auth.activateSeller();
    await auth.fetchUser();
    if (auth.user?.is_seller) await loadDashboardData();
  } catch (error) {
    console.error(error.response?.data || error);
  } finally {
    loading.value = false;
  }
};
</script>