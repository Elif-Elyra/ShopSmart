<script setup>
import { ref, onMounted, computed } from "vue";
import {
  getSellerOrders,
  shipOrder,
  deliverOrder,
  getWallet,
  getTransactions,
  getBankAccounts,
  getWithdrawals,
  createWithdrawal,
  getNotifications,
  getaddresses as getAddresses,
  createAddress as apiCreateAddress,
  deleteAddress as removeAddress,
  createBankAccount,

} from "../services/product";
import {me} from "../services/auth"

const sidebarOpen = ref(false);
const activeTab = ref("addresses");

const menu = [
  {
    key: "addresses",
    label: "Addresses",
    icon: `<svg fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>`,
  },
  {
    key: "wallet",
    label: "Wallet",
    icon: `<svg fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"/></svg>`,
  },
  {
    key: "transactions",
    label: "Transactions",
    icon: `<svg fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>`,
  },
  {
    key: "bank",
    label: "Bank Accounts",
    icon: `<svg fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path d="M3 6l9-3 9 3M3 10h18M5 10v8m4-8v8m6-8v8m4-8v8M3 18h18"/></svg>`,
  },
  {
    key: "withdrawals",
    label: "Withdrawals",
    icon: `<svg fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path d="M12 19V5m0 14l-4-4m4 4l4-4"/></svg>`,
  },
  {
    key: "orders",
    label: "Orders",
    icon: `<svg fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path d="M20 7H4a2 2 0 00-2 2v6a2 2 0 002 2h16a2 2 0 002-2V9a2 2 0 00-2-2z"/><path d="M16 21V5a2 2 0 00-2-2h-4a2 2 0 00-2 2v16"/></svg>`,
  },
  {
    key: "notifications",
    label: "Notifications",
    icon: `<svg fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/></svg>`,
  },
  {
    key: "profile",
    label: "My Profile",
    icon: `<svg fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>`,
  },
];

const loading = ref(false);
const error = ref("");

const addresses = ref([]);
const orders = ref([]);
const transactions = ref([]);
const bankAccounts = ref([]);
const withdrawals = ref([]);
const wallet = ref({ balance: 0 });
const notifications = ref([]);

// ── Profile state ──────────────────────────────────────────────
const profile = ref(null);
const profileLoading = ref(false);

const userInitial = computed(() => {
  const name = profile.value?.first_name || profile.value?.username || "";
  return name.charAt(0).toUpperCase() || "?";
});

const userDisplayName = computed(
  () =>
    [profile.value?.first_name, profile.value?.last_name]
      .filter(Boolean)
      .join(" ") ||
    profile.value?.username ||
    "Seller",
);
// ──────────────────────────────────────────────────────────────

const unreadCount = computed(
  () => notifications.value.filter((n) => !n.is_read).length,
);

const withdrawalForm = ref({ amount: 0, bank_account: null });
const addressForm = ref({
  label: "",
  line: "",
  line2: "",
  city: "",
  postal_code: "",
  country: "Pakistan",
});
const bankForm = ref({
  holder_name: "",
  bank_name: "",
  account_number: "",
  routing_code: "",
  is_primary: false,
});

const statusColors = {
  paid: { bg: "bg-blue-50", text: "text-blue-700", dot: "bg-blue-500" },
  shipped: { bg: "bg-amber-50", text: "text-amber-700", dot: "bg-amber-500" },
  delivered: { bg: "bg-green-50", text: "text-green-700", dot: "bg-green-500" },
  pending: { bg: "bg-slate-50", text: "text-slate-600", dot: "bg-slate-400" },
  cancelled: { bg: "bg-red-50", text: "text-red-700", dot: "bg-red-500" },
};
function statusStyle(s) {
  return statusColors[s] || statusColors.pending;
}

async function safeRequest(cb, msg) {
  try {
    loading.value = true;
    error.value = "";
    await cb();
  } catch (err) {
    error.value = err.response?.data?.detail || msg;
  } finally {
    loading.value = false;
  }
}

async function fetchProfile() {
  try {
    profileLoading.value = true;
    profile.value = await me();
  } catch (err) {
    // fail silently — sidebar still works with fallback
    console.error("Failed to load profile:", err);
  } finally {
    profileLoading.value = false;
  }
}

async function fetchAddresses() {
  await safeRequest(async () => {
    addresses.value = await getAddresses();
  }, "Failed to load addresses");
}
async function fetchWallet() {
  await safeRequest(async () => {
    wallet.value = await getWallet();
  }, "Failed to load wallet");
}
async function fetchTransactions() {
  await safeRequest(async () => {
    const d = await getTransactions();
    transactions.value = d.results || d;
  }, "Failed to load transactions");
}
async function fetchBankAccounts() {
  await safeRequest(async () => {
    bankAccounts.value = await getBankAccounts();
  }, "Failed to load bank accounts");
}
async function fetchWithdrawals() {
  await safeRequest(async () => {
    const d = await getWithdrawals();
    withdrawals.value = d.results || d || [];
  }, "Failed to load withdrawals");
}
async function fetchNotifications() {
  await safeRequest(async () => {
    const d = await getNotifications();
    notifications.value = Array.isArray(d?.results) ? d.results : d || [];
  }, "Failed to load notifications");
}
async function fetchOrders() {
  await safeRequest(async () => {
    orders.value = await getSellerOrders();
  }, "Failed to load orders");
}

async function handleCreateAddress() {
  await safeRequest(async () => {
    await apiCreateAddress(addressForm.value);
    addressForm.value = {
      label: "",
      line: "",
      line2: "",
      city: "",
      postal_code: "",
      country: "Pakistan",
    };
    await fetchAddresses();
  }, "Failed to create address");
}
async function deleteAddress(id) {
  await safeRequest(async () => {
    await removeAddress(id);
    await fetchAddresses();
  }, "Failed to delete address");
}
async function handleCreateBankAccount() {
  await safeRequest(async () => {
    await createBankAccount(bankForm.value);
    bankForm.value = {
      holder_name: "",
      bank_name: "",
      account_number: "",
      routing_code: "",
      country: "Pakistan",
      is_primary: false,
    };
    await fetchBankAccounts();
  }, "Failed to save bank account");
}
async function handleCreateWithdrawal() {
  await safeRequest(async () => {
    await createWithdrawal({
      amount: withdrawalForm.value.amount,
      bank_account: withdrawalForm.value.bank_account,
    });
    withdrawalForm.value = { amount: 0, bank_account: null };
    await Promise.all([fetchWithdrawals(), fetchWallet()]);
  }, "Failed to create withdrawal");
}
async function handleShip(id) {
  try {
    const trackingCode = prompt("Enter tracking code");
    if (!trackingCode) return;
    await shipOrder(id, trackingCode);
    await fetchOrders();
  } catch (err) {
    alert(err.response?.data?.detail || "Failed to ship order");
  }
}
async function handleDeliver(id) {
  try {
    await deliverOrder(id);
    await fetchOrders();
  } catch (err) {
    alert(err.response?.data?.detail || "Failed to deliver order");
  }
}

const tabHandlers = {
  addresses: fetchAddresses,
  wallet: fetchWallet,
  transactions: fetchTransactions,
  bank: fetchBankAccounts,
  withdrawals: async () => {
    await fetchBankAccounts();
    await fetchWithdrawals();
  },
  notifications: fetchNotifications,
  orders: fetchOrders,
  profile: fetchProfile,
};

async function changeTab(tab) {
  activeTab.value = tab;
  sidebarOpen.value = false;
  if (tabHandlers[tab]) await tabHandlers[tab]();
}

onMounted(async () => {
  await Promise.all([
    fetchProfile(),
    fetchNotifications(),
    fetchWallet(),
    fetchOrders(),
    fetchTransactions(),
    fetchBankAccounts(),
    fetchWithdrawals(),
  ]);
  await changeTab("addresses");
});

function fmtDate(s) {
  if (!s) return "—";
  return new Date(s).toLocaleDateString("en-US", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}
function fmtTime(s) {
  if (!s) return "";
  return new Date(s).toLocaleTimeString("en-US", {
    hour: "2-digit",
    minute: "2-digit",
  });
}
</script>

<template>
  <div
    class="min-h-screen bg-[#f4f1ee] flex overflow-hidden"
    style="font-family: &quot;Inter&quot;, system-ui, sans-serif"
  >
    <!-- Mobile overlay -->
    <div
      v-if="sidebarOpen"
      @click="sidebarOpen = false"
      class="fixed inset-0 bg-[#2d1f14]/50 backdrop-blur-sm z-30 md:hidden"
    ></div>

    <!-- ═══════════════════════════ SIDEBAR ═══════════════════════════ -->
    <aside
      class="fixed md:relative z-40 w-64 h-screen bg-[#2d1f14] flex flex-col transition-transform duration-300 shadow-2xl"
      :class="
        sidebarOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'
      "
    >
      <!-- Brand -->
      <div
        class="px-6 py-5 border-b border-white/10 flex items-center justify-between shrink-0"
      >
        <div>
          <span class="text-[20px] font-bold tracking-tight leading-none">
            <span class="text-white">Shop</span
            ><span class="text-[#c9a882]">Smart</span>
          </span>
          <p class="text-[11px] text-white/35 mt-1 tracking-wider uppercase">
            Seller Dashboard
          </p>
        </div>
        <button
          class="md:hidden text-white/60 hover:text-white transition"
          @click="sidebarOpen = false"
        >
          <svg
            class="w-5 h-5"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            viewBox="0 0 24 24"
          >
            <path d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Nav -->
      <nav class="flex-1 px-3 py-4 space-y-0.5 overflow-y-auto">
        <p
          class="text-[10px] font-semibold uppercase tracking-[0.15em] text-white/25 px-3 pb-2 pt-1"
        >
          Management
        </p>
        <button
          v-for="item in menu"
          :key="item.key"
          @click="changeTab(item.key)"
          class="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-left transition-all duration-150 group relative"
          :class="
            activeTab === item.key
              ? 'bg-[#c9a882]/15 text-[#c9a882]'
              : 'text-white/50 hover:text-white/80 hover:bg-white/5'
          "
        >
          <!-- Active indicator -->
          <span
            v-if="activeTab === item.key"
            class="absolute left-0 top-1/2 -translate-y-1/2 w-0.5 h-5 bg-[#c9a882] rounded-r"
          ></span>

          <span class="w-4 h-4 shrink-0" v-html="item.icon"></span>
          <span class="text-sm font-medium flex-1">{{ item.label }}</span>
          <span
            v-if="item.key === 'notifications' && unreadCount > 0"
            class="min-w-[18px] h-[18px] px-1.5 rounded-full bg-[#c9a882] text-[#2d1f14] text-[10px] font-bold flex items-center justify-center"
            >{{ unreadCount }}</span
          >
        </button>
      </nav>

      <!-- User card — now powered by me() API -->
      <div class="px-4 py-4 border-t border-white/10 shrink-0">
        <button
          class="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl bg-white/5 hover:bg-white/10 transition text-left"
          @click="changeTab('profile')"
        >
          <!-- Avatar: profile pic or initial -->
          <div class="shrink-0">
            <img
              v-if="profile?.profile_picture"
              :src="profile.profile_picture"
              :alt="userDisplayName"
              class="w-8 h-8 rounded-full object-cover"
            />
            <div
              v-else
              class="w-8 h-8 rounded-full bg-gradient-to-br from-[#c9a882] to-[#8d6040] flex items-center justify-center text-white text-sm font-bold"
            >
              <span
                v-if="profileLoading"
                class="w-3 h-3 border-2 border-white border-t-transparent rounded-full animate-spin"
              ></span>
              <span v-else>{{ userInitial }}</span>
            </div>
          </div>
          <div class="min-w-0">
            <p class="text-sm font-semibold text-white truncate">
              {{ profileLoading ? "Loading…" : userDisplayName }}
            </p>
            <p class="text-[11px] text-white/40 truncate">
              {{ profile?.email || "Seller Account" }}
            </p>
          </div>
          <!-- chevron hint -->
          <svg
            class="w-3.5 h-3.5 text-white/25 shrink-0"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            viewBox="0 0 24 24"
          >
            <path d="M9 18l6-6-6-6" />
          </svg>
        </button>
      </div>
    </aside>

    <!-- ═══════════════════════════ MAIN ═══════════════════════════ -->
    <div class="flex-1 flex flex-col overflow-hidden min-w-0">
      <!-- Header -->
      <header
        class="h-[60px] bg-white/80 backdrop-blur border-b border-[#e8e0d8] flex items-center justify-between px-5 shrink-0"
      >
        <div class="flex items-center gap-4">
          <button
            class="md:hidden text-[#7c5a3e] hover:text-[#2d1f14] transition"
            @click="sidebarOpen = true"
          >
            <svg
              class="w-5 h-5"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              viewBox="0 0 24 24"
            >
              <path d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
          <div>
            <h2 class="text-[15px] font-semibold text-[#2d1f14] capitalize">
              {{ activeTab === "profile" ? "My Profile" : activeTab }}
            </h2>
            <p class="text-[11px] text-[#a0907e] hidden sm:block">
              ShopSmart Seller Panel
            </p>
          </div>
        </div>

        <!-- Header right -->
        <div class="flex items-center gap-3">
          <!-- Wallet quick -->
          <div
            class="hidden md:flex items-center gap-2 px-3 py-1.5 rounded-xl bg-[#f4f1ee] border border-[#e8e0d8]"
          >
            <svg
              class="w-3.5 h-3.5 text-[#8d6040]"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              viewBox="0 0 24 24"
            >
              <path
                d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"
              />
            </svg>
            <span class="text-xs font-semibold text-[#4a3728]"
              >${{ wallet.balance }}</span
            >
          </div>
          <!-- Notification dot -->
          <button
            class="relative p-2 rounded-xl hover:bg-[#f4f1ee] transition"
            @click="changeTab('notifications')"
          >
            <svg
              class="w-4.5 h-4.5 text-[#7c5a3e]"
              style="width: 18px; height: 18px"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              viewBox="0 0 24 24"
            >
              <path
                d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
              />
            </svg>
            <span
              v-if="unreadCount > 0"
              class="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-[#c9a882]"
            ></span>
          </button>
          <!-- Avatar — links to profile tab -->
          <button
            @click="changeTab('profile')"
            class="rounded-full hover:ring-2 hover:ring-[#c9a882]/50 transition"
          >
            <img
              v-if="profile?.profile_picture"
              :src="profile.profile_picture"
              :alt="userDisplayName"
              class="w-8 h-8 rounded-full object-cover"
            />
            <div
              v-else
              class="w-8 h-8 rounded-full bg-gradient-to-br from-[#c9a882] to-[#8d6040] flex items-center justify-center text-white text-xs font-bold"
            >
              {{ userInitial }}
            </div>
          </button>
        </div>
      </header>

      <!-- Content -->
      <main class="flex-1 overflow-y-auto p-5 md:p-6 space-y-5">
        <!-- Global error -->
        <div
          v-if="error"
          class="flex items-center gap-3 px-4 py-3 rounded-xl bg-red-50 border border-red-100 text-red-700 text-sm"
        >
          <svg
            class="w-4 h-4 shrink-0"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            viewBox="0 0 24 24"
          >
            <circle cx="12" cy="12" r="10" />
            <line x1="12" y1="8" x2="12" y2="12" />
            <line x1="12" y1="16" x2="12.01" y2="16" />
          </svg>
          {{ error }}
        </div>

        <!-- ── STATS STRIP ── -->
        <section class="grid grid-cols-2 xl:grid-cols-4 gap-3">
          <div class="bg-white rounded-2xl p-4 border border-[#e8e0d8]">
            <div class="flex items-center justify-between mb-3">
              <p class="text-xs text-[#a0907e] font-medium">Balance</p>
              <div
                class="w-7 h-7 rounded-lg bg-[#8d6040]/10 flex items-center justify-center"
              >
                <svg
                  class="w-3.5 h-3.5 text-[#8d6040]"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"
                  />
                </svg>
              </div>
            </div>
            <p class="text-2xl font-bold text-[#2d1f14]">
              ${{ wallet.balance }}
            </p>
            <p class="text-[11px] text-[#a0907e] mt-1">Available to withdraw</p>
          </div>
          <div class="bg-white rounded-2xl p-4 border border-[#e8e0d8]">
            <div class="flex items-center justify-between mb-3">
              <p class="text-xs text-[#a0907e] font-medium">Orders</p>
              <div
                class="w-7 h-7 rounded-lg bg-amber-50 flex items-center justify-center"
              >
                <svg
                  class="w-3.5 h-3.5 text-amber-600"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M20 7H4a2 2 0 00-2 2v6a2 2 0 002 2h16a2 2 0 002-2V9a2 2 0 00-2-2z"
                  />
                  <path d="M16 21V5a2 2 0 00-2-2h-4a2 2 0 00-2 2v16" />
                </svg>
              </div>
            </div>
            <p class="text-2xl font-bold text-[#2d1f14]">{{ orders.length }}</p>
            <p class="text-[11px] text-[#a0907e] mt-1">Total seller orders</p>
          </div>
          <div class="bg-white rounded-2xl p-4 border border-[#e8e0d8]">
            <div class="flex items-center justify-between mb-3">
              <p class="text-xs text-[#a0907e] font-medium">Transactions</p>
              <div
                class="w-7 h-7 rounded-lg bg-green-50 flex items-center justify-center"
              >
                <svg
                  class="w-3.5 h-3.5 text-green-600"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                  />
                </svg>
              </div>
            </div>
            <p class="text-2xl font-bold text-[#2d1f14]">
              {{ transactions.length }}
            </p>
            <p class="text-[11px] text-[#a0907e] mt-1">Financial records</p>
          </div>
          <div class="bg-white rounded-2xl p-4 border border-[#e8e0d8]">
            <div class="flex items-center justify-between mb-3">
              <p class="text-xs text-[#a0907e] font-medium">Notifications</p>
              <div
                class="w-7 h-7 rounded-lg bg-[#c9a882]/15 flex items-center justify-center"
              >
                <svg
                  class="w-3.5 h-3.5 text-[#8d6040]"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
                  />
                </svg>
              </div>
            </div>
            <p class="text-2xl font-bold text-[#2d1f14]">
              {{ notifications.length }}
            </p>
            <p class="text-[11px] text-[#a0907e] mt-1">
              <span v-if="unreadCount > 0" class="text-[#8d6040] font-semibold"
                >{{ unreadCount }} unread</span
              >
              <span v-else>All caught up</span>
            </p>
          </div>
        </section>

        <!-- ══════════════════ ADDRESSES ══════════════════ -->
        <section v-if="activeTab === 'addresses'" class="space-y-4">
          <!-- Add form card -->
          <div
            class="bg-white rounded-2xl border border-[#e8e0d8] overflow-hidden"
          >
            <div
              class="px-6 py-4 border-b border-[#f0ebe4] flex items-center justify-between"
            >
              <div>
                <h3 class="text-[15px] font-semibold text-[#2d1f14]">
                  Add New Address
                </h3>
                <p class="text-xs text-[#a0907e] mt-0.5">
                  Shipping & billing locations
                </p>
              </div>
              <div
                class="w-8 h-8 rounded-xl bg-[#8d6040]/10 flex items-center justify-center"
              >
                <svg
                  class="w-4 h-4 text-[#8d6040]"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  viewBox="0 0 24 24"
                >
                  <path d="M12 4v16m8-8H4" />
                </svg>
              </div>
            </div>
            <div class="p-6">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div>
                  <label class="field-label">Label</label>
                  <input
                    v-model="addressForm.label"
                    placeholder="Home / Office"
                    class="field-input"
                  />
                </div>
                <div>
                  <label class="field-label">Street Address</label>
                  <input
                    v-model="addressForm.line"
                    placeholder="Street, block, sector…"
                    class="field-input"
                  />
                </div>
                <div>
                  <label class="field-label"
                    >Apartment / Floor
                    <span class="text-[#c4b5a5]">(optional)</span></label
                  >
                  <input
                    v-model="addressForm.line2"
                    placeholder="Flat 3B, Floor 2…"
                    class="field-input"
                  />
                </div>
                <div>
                  <label class="field-label">Postal Code</label>
                  <input
                    v-model="addressForm.postal_code"
                    placeholder="54000"
                    class="field-input"
                  />
                </div>
                <div>
                  <label class="field-label">City</label>
                  <input
                    v-model="addressForm.city"
                    placeholder="Lahore"
                    class="field-input"
                  />
                </div>
                <div>
                  <label class="field-label">Country</label>
                  <input
                    v-model="addressForm.country"
                    placeholder="Pakistan"
                    class="field-input"
                  />
                </div>
              </div>
              <div class="mt-5 flex justify-end">
                <button
                  @click="handleCreateAddress"
                  :disabled="loading"
                  class="btn-primary"
                >
                  <svg
                    v-if="!loading"
                    class="w-3.5 h-3.5"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2.5"
                    viewBox="0 0 24 24"
                  >
                    <path d="M12 4v16m8-8H4" />
                  </svg>
                  <span
                    v-if="loading"
                    class="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin"
                  ></span>
                  Save Address
                </button>
              </div>
            </div>
          </div>

          <!-- Address list -->
          <div
            v-if="addresses.length"
            class="grid grid-cols-1 lg:grid-cols-2 gap-3"
          >
            <div
              v-for="a in addresses"
              :key="a.id"
              class="bg-white rounded-2xl border border-[#e8e0d8] p-5 hover:shadow-md transition group"
            >
              <div class="flex items-start justify-between gap-3">
                <div class="flex items-start gap-3">
                  <div
                    class="w-9 h-9 rounded-xl bg-[#8d6040]/10 flex items-center justify-center shrink-0 mt-0.5"
                  >
                    <svg
                      class="w-4 h-4 text-[#8d6040]"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                      viewBox="0 0 24 24"
                    >
                      <path
                        d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
                      />
                      <path d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                  </div>
                  <div>
                    <h4 class="text-sm font-semibold text-[#2d1f14]">
                      {{ a.label }}
                    </h4>
                    <p class="text-xs text-[#7c6a5e] mt-1 leading-relaxed">
                      {{ a.line }}<span v-if="a.line2">, {{ a.line2 }}</span>
                    </p>
                    <p class="text-xs text-[#a0907e]">
                      {{ a.city
                      }}<span v-if="a.postal_code"> – {{ a.postal_code }}</span
                      >, {{ a.country }}
                    </p>
                  </div>
                </div>
                <button
                  @click="deleteAddress(a.id)"
                  class="opacity-0 group-hover:opacity-100 transition p-1.5 rounded-lg hover:bg-red-50 text-[#c4b5a5] hover:text-red-500"
                >
                  <svg
                    class="w-3.5 h-3.5"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    viewBox="0 0 24 24"
                  >
                    <path
                      d="M3 6h18M19 6l-1 14H6L5 6M10 11v6M14 11v6M9 6V4h6v2"
                    />
                  </svg>
                </button>
              </div>
            </div>
          </div>
          <div v-else class="empty-state">
            <svg
              class="w-8 h-8 text-[#c9a882]"
              fill="none"
              stroke="currentColor"
              stroke-width="1.5"
              viewBox="0 0 24 24"
            >
              <path
                d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
              />
              <path d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            <p class="text-sm font-medium text-[#7c6a5e] mt-2">
              No addresses yet
            </p>
            <p class="text-xs text-[#a0907e]">Add your first address above</p>
          </div>
        </section>

        <!-- ══════════════════ WALLET ══════════════════ -->
        <section v-if="activeTab === 'wallet'" class="space-y-4">
          <div
            class="relative overflow-hidden rounded-2xl bg-gradient-to-br from-[#2d1f14] via-[#7c5a3e] to-[#b8916a] p-8 text-white"
          >
            <div
              class="absolute top-[-60px] right-[-60px] w-[220px] h-[220px] rounded-full border border-white/10"
            ></div>
            <div
              class="absolute bottom-[-40px] left-[-40px] w-[160px] h-[160px] rounded-full border border-white/8"
            ></div>
            <p
              class="text-sm text-white/60 uppercase tracking-widest font-medium"
            >
              Available Balance
            </p>
            <h2 class="text-6xl font-bold mt-3 relative">
              ${{ wallet.balance }}
            </h2>
            <p class="text-white/40 text-xs mt-2">
              ShopSmart Wallet · Seller Account
            </p>
            <div class="flex gap-3 mt-8 relative">
              <button
                class="flex items-center gap-2 bg-white text-[#7c5a3e] px-5 py-2.5 rounded-xl text-sm font-semibold hover:bg-[#f0ebe4] transition shadow"
              >
                <svg
                  class="w-3.5 h-3.5"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2.5"
                  viewBox="0 0 24 24"
                >
                  <path d="M12 19V5m0 14l-4-4m4 4l4-4" />
                </svg>
                Withdraw
              </button>
              <button
                class="flex items-center gap-2 bg-white/15 border border-white/20 text-white px-5 py-2.5 rounded-xl text-sm font-semibold hover:bg-white/20 transition"
              >
                <svg
                  class="w-3.5 h-3.5"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2.5"
                  viewBox="0 0 24 24"
                >
                  <path d="M12 5v14m0-14l4 4m-4-4L8 9" />
                </svg>
                Deposit
              </button>
            </div>
          </div>
        </section>

        <!-- ══════════════════ TRANSACTIONS ══════════════════ -->
        <section v-if="activeTab === 'transactions'">
          <div
            class="bg-white rounded-2xl border border-[#e8e0d8] overflow-hidden"
          >
            <div class="px-6 py-4 border-b border-[#f0ebe4]">
              <h3 class="text-[15px] font-semibold text-[#2d1f14]">
                Transaction History
              </h3>
              <p class="text-xs text-[#a0907e] mt-0.5">
                All financial activity on your account
              </p>
            </div>
            <div v-if="transactions.length" class="divide-y divide-[#f0ebe4]">
              <div
                v-for="t in transactions"
                :key="t.id"
                class="flex items-center justify-between px-6 py-4 hover:bg-[#faf7f4] transition"
              >
                <div class="flex items-center gap-3">
                  <div
                    :class="[
                      'w-9 h-9 rounded-xl flex items-center justify-center shrink-0',
                      t.type === 'credit' ? 'bg-green-50' : 'bg-red-50',
                    ]"
                  >
                    <svg
                      :class="[
                        'w-4 h-4',
                        t.type === 'credit' ? 'text-green-600' : 'text-red-500',
                      ]"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2.5"
                      viewBox="0 0 24 24"
                    >
                      <path
                        v-if="t.type === 'credit'"
                        d="M12 5v14m0-14l4 4m-4-4L8 9"
                      />
                      <path v-else d="M12 19V5m0 14l-4-4m4 4l4-4" />
                    </svg>
                  </div>
                  <div>
                    <p class="text-sm font-semibold text-[#2d1f14] capitalize">
                      {{ t.type }}
                    </p>
                    <p class="text-xs text-[#a0907e]">
                      {{ fmtDate(t.created_at) }} · {{ fmtTime(t.created_at) }}
                    </p>
                  </div>
                </div>
                <p
                  :class="[
                    'text-base font-bold',
                    t.type === 'credit' ? 'text-green-600' : 'text-red-500',
                  ]"
                >
                  {{ t.type === "credit" ? "+" : "-" }}${{ t.amount }}
                </p>
              </div>
            </div>
            <div v-else class="empty-state py-12">
              <svg
                class="w-8 h-8 text-[#c9a882]"
                fill="none"
                stroke="currentColor"
                stroke-width="1.5"
                viewBox="0 0 24 24"
              >
                <path
                  d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                />
              </svg>
              <p class="text-sm font-medium text-[#7c6a5e] mt-2">
                No transactions yet
              </p>
            </div>
          </div>
        </section>

        <!-- ══════════════════ BANK ACCOUNTS ══════════════════ -->
        <section v-if="activeTab === 'bank'" class="space-y-4">
          <div
            class="bg-white rounded-2xl border border-[#e8e0d8] overflow-hidden"
          >
            <div class="px-6 py-4 border-b border-[#f0ebe4]">
              <h3 class="text-[15px] font-semibold text-[#2d1f14]">
                Add Bank Account
              </h3>
              <p class="text-xs text-[#a0907e] mt-0.5">
                Used for withdrawal payouts
              </p>
            </div>
            <div class="p-6">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div>
                  <label class="field-label">Bank Name</label
                  ><input
                    v-model="bankForm.bank_name"
                    placeholder="HBL / UBL / Meezan…"
                    class="field-input"
                  />
                </div>
                <div>
                  <label class="field-label">Account Holder</label
                  ><input
                    v-model="bankForm.holder_name"
                    placeholder="Full name on account"
                    class="field-input"
                  />
                </div>
                <div>
                  <label class="field-label">Account Number</label
                  ><input
                    v-model="bankForm.account_number"
                    placeholder="IBAN or account number"
                    class="field-input"
                  />
                </div>
                <div>
                  <label class="field-label"
                    >Routing Code
                    <span class="text-[#c4b5a5]">(optional)</span></label
                  ><input
                    v-model="bankForm.routing_code"
                    placeholder="SWIFT / IFSC…"
                    class="field-input"
                  />
                </div>
              </div>
              <label class="mt-4 flex items-center gap-3 cursor-pointer group">
                <div class="relative">
                  <input
                    type="checkbox"
                    v-model="bankForm.is_primary"
                    class="sr-only peer"
                  />
                  <div
                    class="w-9 h-5 rounded-full bg-[#e8e0d8] peer-checked:bg-[#8d6040] transition-all"
                  ></div>
                  <div
                    class="absolute top-0.5 left-0.5 w-4 h-4 rounded-full bg-white shadow transition-all peer-checked:translate-x-4"
                  ></div>
                </div>
                <span class="text-sm text-[#4a3728]"
                  >Set as primary account</span
                >
              </label>
              <div class="mt-5 flex justify-end">
                <button
                  @click="handleCreateBankAccount"
                  :disabled="loading"
                  class="btn-primary"
                >
                  <span
                    v-if="loading"
                    class="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin"
                  ></span>
                  Save Account
                </button>
              </div>
            </div>
          </div>

          <div
            v-if="bankAccounts.length"
            class="grid grid-cols-1 md:grid-cols-2 gap-3"
          >
            <div
              v-for="bank in bankAccounts"
              :key="bank.id"
              class="bg-white rounded-2xl border border-[#e8e0d8] p-5 relative"
            >
              <div class="flex items-start gap-3">
                <div
                  class="w-9 h-9 rounded-xl bg-[#8d6040]/10 flex items-center justify-center shrink-0"
                >
                  <svg
                    class="w-4 h-4 text-[#8d6040]"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    viewBox="0 0 24 24"
                  >
                    <path
                      d="M3 6l9-3 9 3M3 10h18M5 10v8m4-8v8m6-8v8m4-8v8M3 18h18"
                    />
                  </svg>
                </div>
                <div class="flex-1 min-w-0">
                  <div class="flex items-center gap-2 flex-wrap">
                    <h4 class="text-sm font-semibold text-[#2d1f14]">
                      {{ bank.bank_name }}
                    </h4>
                    <span
                      v-if="bank.is_primary"
                      class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-green-50 text-green-700 border border-green-100"
                      >Primary</span
                    >
                  </div>
                  <p class="text-xs text-[#7c6a5e] mt-1">
                    {{ bank.holder_name }}
                  </p>
                  <p class="text-xs text-[#a0907e]">
                    ****{{ bank.last4
                    }}<span v-if="bank.routing_code">
                      · {{ bank.routing_code }}</span
                    >
                  </p>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="empty-state">
            <svg
              class="w-8 h-8 text-[#c9a882]"
              fill="none"
              stroke="currentColor"
              stroke-width="1.5"
              viewBox="0 0 24 24"
            >
              <path d="M3 6l9-3 9 3M3 10h18M5 10v8m4-8v8m6-8v8m4-8v8M3 18h18" />
            </svg>
            <p class="text-sm font-medium text-[#7c6a5e] mt-2">
              No bank accounts added
            </p>
            <p class="text-xs text-[#a0907e]">
              Add one above to enable withdrawals
            </p>
          </div>
        </section>

        <!-- ══════════════════ WITHDRAWALS ══════════════════ -->
        <section v-if="activeTab === 'withdrawals'" class="space-y-4">
          <div
            class="bg-white rounded-2xl border border-[#e8e0d8] overflow-hidden"
          >
            <div class="px-6 py-4 border-b border-[#f0ebe4]">
              <h3 class="text-[15px] font-semibold text-[#2d1f14]">
                Request Withdrawal
              </h3>
              <p class="text-xs text-[#a0907e] mt-0.5">
                Transfer wallet balance to your bank · Available:
                <strong class="text-[#8d6040]">${{ wallet.balance }}</strong>
              </p>
            </div>
            <div class="p-6">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div>
                  <label class="field-label">Amount (USD)</label>
                  <div class="relative">
                    <span
                      class="absolute left-4 top-1/2 -translate-y-1/2 text-sm font-semibold text-[#a0907e]"
                      >$</span
                    >
                    <input
                      v-model="withdrawalForm.amount"
                      type="number"
                      placeholder="0.00"
                      class="field-input pl-8"
                    />
                  </div>
                </div>
                <div>
                  <label class="field-label">Bank Account</label>
                  <select
                    v-model="withdrawalForm.bank_account"
                    class="field-input"
                  >
                    <option value="">Select bank account</option>
                    <option v-for="b in bankAccounts" :key="b.id" :value="b.id">
                      {{ b.bank_name }} ····{{ b.last4 }}
                    </option>
                  </select>
                </div>
              </div>
              <div class="mt-5 flex justify-end">
                <button
                  @click="handleCreateWithdrawal"
                  :disabled="loading"
                  class="btn-primary"
                >
                  <span
                    v-if="loading"
                    class="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin"
                  ></span>
                  Request Withdrawal
                </button>
              </div>
            </div>
          </div>

          <div
            v-if="withdrawals.length"
            class="bg-white rounded-2xl border border-[#e8e0d8] overflow-hidden"
          >
            <div class="px-6 py-4 border-b border-[#f0ebe4]">
              <h3 class="text-[15px] font-semibold text-[#2d1f14]">
                Withdrawal History
              </h3>
            </div>
            <div class="divide-y divide-[#f0ebe4]">
              <div
                v-for="w in withdrawals"
                :key="w.id"
                v-if="w"
                class="flex items-center justify-between px-6 py-4 hover:bg-[#faf7f4] transition"
              >
                <div class="flex items-center gap-3">
                  <div
                    class="w-9 h-9 rounded-xl bg-[#8d6040]/10 flex items-center justify-center shrink-0"
                  >
                    <svg
                      class="w-4 h-4 text-[#8d6040]"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                      viewBox="0 0 24 24"
                    >
                      <path d="M12 19V5m0 14l-4-4m4 4l4-4" />
                    </svg>
                  </div>
                  <div>
                    <p class="text-sm font-semibold text-[#2d1f14]">
                      ${{ w.amount }}
                    </p>
                    <p class="text-xs text-[#a0907e]">
                      Bank · {{ w.bank_account }} · {{ fmtDate(w.created_at) }}
                    </p>
                  </div>
                </div>
                <span
                  :class="[
                    'text-xs font-semibold px-2.5 py-1 rounded-full capitalize',
                    statusStyle(w.status).bg,
                    statusStyle(w.status).text,
                  ]"
                  >{{ w.status }}</span
                >
              </div>
            </div>
          </div>
          <div v-else class="empty-state">
            <svg
              class="w-8 h-8 text-[#c9a882]"
              fill="none"
              stroke="currentColor"
              stroke-width="1.5"
              viewBox="0 0 24 24"
            >
              <path d="M12 19V5m0 14l-4-4m4 4l4-4" />
            </svg>
            <p class="text-sm font-medium text-[#7c6a5e] mt-2">
              No withdrawals yet
            </p>
          </div>
        </section>

        <!-- ══════════════════ ORDERS ══════════════════ -->
        <section v-if="activeTab === 'orders'">
          <div
            class="bg-white rounded-2xl border border-[#e8e0d8] overflow-hidden"
          >
            <div
              class="px-6 py-4 border-b border-[#f0ebe4] flex items-center justify-between"
            >
              <div>
                <h3 class="text-[15px] font-semibold text-[#2d1f14]">
                  Seller Orders
                </h3>
                <p class="text-xs text-[#a0907e] mt-0.5">
                  Manage and fulfil customer orders
                </p>
              </div>
              <span
                class="text-xs font-semibold px-2.5 py-1 rounded-full bg-[#f0ebe4] text-[#7c5a3e]"
                >{{ orders.length }} total</span
              >
            </div>

            <div
              v-if="loading"
              class="flex items-center justify-center py-16 gap-2 text-[#a0907e]"
            >
              <span
                class="w-4 h-4 border-2 border-[#c9a882] border-t-transparent rounded-full animate-spin"
              ></span>
              Loading orders…
            </div>

            <div v-else-if="!orders.length" class="empty-state py-16">
              <svg
                class="w-8 h-8 text-[#c9a882]"
                fill="none"
                stroke="currentColor"
                stroke-width="1.5"
                viewBox="0 0 24 24"
              >
                <path
                  d="M20 7H4a2 2 0 00-2 2v6a2 2 0 002 2h16a2 2 0 002-2V9a2 2 0 00-2-2z"
                />
                <path d="M16 21V5a2 2 0 00-2-2h-4a2 2 0 00-2 2v16" />
              </svg>
              <p class="text-sm font-medium text-[#7c6a5e] mt-2">
                No orders yet
              </p>
              <p class="text-xs text-[#a0907e]">
                Orders will appear here once customers purchase your products
              </p>
            </div>

            <div v-else class="divide-y divide-[#f0ebe4]">
              <div
                v-for="order in orders"
                :key="order.id"
                class="p-6 hover:bg-[#faf7f4] transition"
              >
                <div
                  class="flex flex-col md:flex-row md:items-start md:justify-between gap-4"
                >
                  <div class="flex items-start gap-4">
                    <div
                      class="w-10 h-10 rounded-xl bg-[#f0ebe4] flex items-center justify-center shrink-0"
                    >
                      <svg
                        class="w-4.5 h-4.5 text-[#8d6040]"
                        style="width: 18px; height: 18px"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        viewBox="0 0 24 24"
                      >
                        <path
                          d="M20 7H4a2 2 0 00-2 2v6a2 2 0 002 2h16a2 2 0 002-2V9a2 2 0 00-2-2z"
                        />
                        <path d="M16 21V5a2 2 0 00-2-2h-4a2 2 0 00-2 2v16" />
                      </svg>
                    </div>
                    <div>
                      <div class="flex items-center gap-2 flex-wrap">
                        <h4 class="text-sm font-bold text-[#2d1f14]">
                          Order #{{ order.id }}
                        </h4>
                        <span
                          :class="[
                            'text-[10px] font-bold px-2 py-0.5 rounded-full capitalize',
                            statusStyle(order.status).bg,
                            statusStyle(order.status).text,
                          ]"
                        >
                          <span
                            :class="[
                              'inline-block w-1.5 h-1.5 rounded-full mr-1 align-middle',
                              statusStyle(order.status).dot,
                            ]"
                          ></span>
                          {{ order.status }}
                        </span>
                      </div>
                      <div class="mt-2 grid grid-cols-2 gap-x-6 gap-y-1">
                        <p class="text-xs text-[#a0907e]">
                          Subtotal:
                          <span class="font-semibold text-[#4a3728]"
                            >${{ order.subtotal }}</span
                          >
                        </p>
                        <p class="text-xs text-[#a0907e]">
                          Shipping:
                          <span class="font-semibold text-[#4a3728]">{{
                            order.shipping
                          }}</span>
                        </p>
                        <p
                          class="text-xs text-[#a0907e]"
                          v-if="order.tracking_code"
                        >
                          Tracking:
                          <span class="font-semibold text-[#4a3728]">{{
                            order.tracking_code
                          }}</span>
                        </p>
                      </div>
                    </div>
                  </div>
                  <div class="flex gap-2 shrink-0">
                    <button
                      v-if="order.status === 'paid'"
                      @click="handleShip(order.id)"
                      class="btn-primary text-xs py-2 px-4"
                    >
                      <svg
                        class="w-3 h-3"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2.5"
                        viewBox="0 0 24 24"
                      >
                        <path
                          d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4"
                        />
                      </svg>
                      Ship Order
                    </button>
                    <button
                      v-if="order.status === 'shipped'"
                      @click="handleDeliver(order.id)"
                      class="btn-secondary text-xs py-2 px-4"
                    >
                      <svg
                        class="w-3 h-3"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2.5"
                        viewBox="0 0 24 24"
                      >
                        <polyline points="20 6 9 17 4 12" />
                      </svg>
                      Mark Delivered
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- ══════════════════ NOTIFICATIONS ══════════════════ -->
        <section v-if="activeTab === 'notifications'">
          <div
            class="bg-white rounded-2xl border border-[#e8e0d8] overflow-hidden"
          >
            <div
              class="px-6 py-4 border-b border-[#f0ebe4] flex items-center justify-between"
            >
              <div>
                <h3 class="text-[15px] font-semibold text-[#2d1f14]">
                  Notifications
                </h3>
                <p class="text-xs text-[#a0907e] mt-0.5">
                  Activity alerts for your seller account
                </p>
              </div>
              <span
                v-if="unreadCount > 0"
                class="text-xs font-semibold px-2.5 py-1 rounded-full bg-[#c9a882]/15 text-[#7c5a3e]"
                >{{ unreadCount }} unread</span
              >
            </div>

            <div v-if="!notifications.length" class="empty-state py-16">
              <svg
                class="w-8 h-8 text-[#c9a882]"
                fill="none"
                stroke="currentColor"
                stroke-width="1.5"
                viewBox="0 0 24 24"
              >
                <path
                  d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
                />
              </svg>
              <p class="text-sm font-medium text-[#7c6a5e] mt-2">
                You're all caught up
              </p>
              <p class="text-xs text-[#a0907e]">
                No notifications at the moment
              </p>
            </div>

            <div v-else class="divide-y divide-[#f0ebe4]">
              <div
                v-for="n in notifications"
                :key="n.id"
                :class="[
                  'flex items-start gap-4 px-6 py-4 transition hover:bg-[#faf7f4]',
                  !n.is_read ? 'bg-[#fdf9f6]' : '',
                ]"
              >
                <div
                  :class="[
                    'w-9 h-9 rounded-xl flex items-center justify-center shrink-0 mt-0.5',
                    !n.is_read ? 'bg-[#c9a882]/20' : 'bg-[#f0ebe4]',
                  ]"
                >
                  <svg
                    :class="[
                      'w-4 h-4',
                      !n.is_read ? 'text-[#8d6040]' : 'text-[#b8a090]',
                    ]"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    viewBox="0 0 24 24"
                  >
                    <path
                      d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
                    />
                  </svg>
                </div>
                <div class="flex-1 min-w-0">
                  <div class="flex items-center gap-2 flex-wrap">
                    <span
                      class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-[#f0ebe4] text-[#8d6040] uppercase tracking-wide"
                      >{{ n.type_noti }}</span
                    >
                    <span
                      v-if="!n.is_read"
                      class="w-1.5 h-1.5 rounded-full bg-[#c9a882]"
                    ></span>
                  </div>
                  <p class="text-sm text-[#4a3728] mt-1.5 leading-relaxed">
                    {{ n.payload?.message }}
                  </p>
                </div>
                <p
                  class="text-xs text-[#c4b5a5] whitespace-nowrap shrink-0 mt-0.5"
                >
                  {{ fmtDate(n.created_at) }}
                </p>
              </div>
            </div>
          </div>
        </section>

        <!-- ══════════════════ PROFILE ══════════════════ -->
        <section v-if="activeTab === 'profile'" class="space-y-4">
          <!-- Loading skeleton -->
          <div
            v-if="profileLoading"
            class="bg-white rounded-2xl border border-[#e8e0d8] p-8 flex items-center justify-center gap-3 text-[#a0907e]"
          >
            <span
              class="w-5 h-5 border-2 border-[#c9a882] border-t-transparent rounded-full animate-spin"
            ></span>
            Loading profile…
          </div>

          <template v-else-if="profile">
            <!-- Profile hero card -->
            <div
              class="bg-white rounded-2xl border border-[#e8e0d8] overflow-hidden"
            >
              <!-- Cover strip -->
              <div
                class="h-24 bg-gradient-to-r from-[#2d1f14] via-[#7c5a3e] to-[#b8916a]"
              ></div>
              <!-- Avatar + name row -->
              <div class="px-6 pb-6">
                <div class="flex items-end gap-4 -mt-10 mb-4">
                  <div class="shrink-0">
                    <img
                      v-if="profile.profile_picture"
                      :src="profile.profile_picture"
                      :alt="userDisplayName"
                      class="w-20 h-20 rounded-2xl object-cover border-4 border-white shadow-lg"
                    />
                    <div
                      v-else
                      class="w-20 h-20 rounded-2xl bg-gradient-to-br from-[#c9a882] to-[#8d6040] flex items-center justify-center text-white text-3xl font-bold border-4 border-white shadow-lg"
                    >
                      {{ userInitial }}
                    </div>
                  </div>
                  <div class="pb-1">
                    <h3 class="text-xl font-bold text-[#2d1f14]">
                      {{ userDisplayName }}
                    </h3>
                    <p class="text-sm text-[#a0907e]">{{ profile.email }}</p>
                  </div>
                </div>

                <!-- Info grid -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-3 mt-2">
                  <div
                    v-if="profile.username"
                    class="flex items-center gap-3 px-4 py-3 rounded-xl bg-[#faf7f4] border border-[#f0ebe4]"
                  >
                    <div
                      class="w-8 h-8 rounded-lg bg-[#8d6040]/10 flex items-center justify-center shrink-0"
                    >
                      <svg
                        class="w-4 h-4 text-[#8d6040]"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        viewBox="0 0 24 24"
                      >
                        <path
                          d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                        />
                      </svg>
                    </div>
                    <div>
                      <p class="text-[11px] text-[#a0907e] font-medium">
                        Username
                      </p>
                      <p class="text-sm font-semibold text-[#2d1f14]">
                        @{{ profile.username }}
                      </p>
                    </div>
                  </div>

                  <div
                    v-if="profile.email"
                    class="flex items-center gap-3 px-4 py-3 rounded-xl bg-[#faf7f4] border border-[#f0ebe4]"
                  >
                    <div
                      class="w-8 h-8 rounded-lg bg-[#8d6040]/10 flex items-center justify-center shrink-0"
                    >
                      <svg
                        class="w-4 h-4 text-[#8d6040]"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        viewBox="0 0 24 24"
                      >
                        <path
                          d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
                        />
                      </svg>
                    </div>
                    <div>
                      <p class="text-[11px] text-[#a0907e] font-medium">
                        Email
                      </p>
                      <p class="text-sm font-semibold text-[#2d1f14]">
                        {{ profile.email }}
                      </p>
                    </div>
                  </div>

                  <div
                    v-if="profile.phone_number"
                    class="flex items-center gap-3 px-4 py-3 rounded-xl bg-[#faf7f4] border border-[#f0ebe4]"
                  >
                    <div
                      class="w-8 h-8 rounded-lg bg-[#8d6040]/10 flex items-center justify-center shrink-0"
                    >
                      <svg
                        class="w-4 h-4 text-[#8d6040]"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        viewBox="0 0 24 24"
                      >
                        <path
                          d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"
                        />
                      </svg>
                    </div>
                    <div>
                      <p class="text-[11px] text-[#a0907e] font-medium">
                        Phone
                      </p>
                      <p class="text-sm font-semibold text-[#2d1f14]">
                        {{ profile.phone_number }}
                      </p>
                    </div>
                  </div>

                  <div
                    v-if="profile.date_joined"
                    class="flex items-center gap-3 px-4 py-3 rounded-xl bg-[#faf7f4] border border-[#f0ebe4]"
                  >
                    <div
                      class="w-8 h-8 rounded-lg bg-[#8d6040]/10 flex items-center justify-center shrink-0"
                    >
                      <svg
                        class="w-4 h-4 text-[#8d6040]"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        viewBox="0 0 24 24"
                      >
                        <rect
                          x="3"
                          y="4"
                          width="18"
                          height="18"
                          rx="2"
                          ry="2"
                        />
                        <line x1="16" y1="2" x2="16" y2="6" />
                        <line x1="8" y1="2" x2="8" y2="6" />
                        <line x1="3" y1="10" x2="21" y2="10" />
                      </svg>
                    </div>
                    <div>
                      <p class="text-[11px] text-[#a0907e] font-medium">
                        Member Since
                      </p>
                      <p class="text-sm font-semibold text-[#2d1f14]">
                        {{ fmtDate(profile.date_joined) }}
                      </p>
                    </div>
                  </div>

                  <!-- Role / seller badge -->
                  <div
                    v-if="profile.role || profile.is_seller !== undefined"
                    class="flex items-center gap-3 px-4 py-3 rounded-xl bg-[#faf7f4] border border-[#f0ebe4]"
                  >
                    <div
                      class="w-8 h-8 rounded-lg bg-[#8d6040]/10 flex items-center justify-center shrink-0"
                    >
                      <svg
                        class="w-4 h-4 text-[#8d6040]"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        viewBox="0 0 24 24"
                      >
                        <path
                          d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"
                        />
                      </svg>
                    </div>
                    <div>
                      <p class="text-[11px] text-[#a0907e] font-medium">
                        Account Type
                      </p>
                      <p
                        class="text-sm font-semibold text-[#2d1f14] capitalize"
                      >
                        {{
                          profile.role ||
                          (profile.is_seller ? "Seller" : "Buyer")
                        }}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Raw fields fallback: show any extra API fields not explicitly handled -->
            <div
              v-if="
                Object.keys(profile).some(
                  (k) =>
                    ![
                      'username',
                      'email',
                      'first_name',
                      'last_name',
                      'profile_picture',
                      'phone_number',
                      'date_joined',
                      'role',
                      'is_seller',
                      'id',
                    ].includes(k),
                )
              "
              class="bg-white rounded-2xl border border-[#e8e0d8] overflow-hidden"
            >
              <div class="px-6 py-4 border-b border-[#f0ebe4]">
                <h3 class="text-[15px] font-semibold text-[#2d1f14]">
                  Additional Details
                </h3>
              </div>
              <div class="p-6 grid grid-cols-1 md:grid-cols-2 gap-3">
                <template v-for="(val, key) in profile" :key="key">
                  <div
                    v-if="
                      val !== null &&
                      val !== '' &&
                      ![
                        'username',
                        'email',
                        'first_name',
                        'last_name',
                        'profile_picture',
                        'phone_number',
                        'date_joined',
                        'role',
                        'is_seller',
                        'id',
                      ].includes(key)
                    "
                    class="flex items-start gap-3 px-4 py-3 rounded-xl bg-[#faf7f4] border border-[#f0ebe4]"
                  >
                    <div class="min-w-0">
                      <p
                        class="text-[11px] text-[#a0907e] font-medium capitalize"
                      >
                        {{ key.replace(/_/g, " ") }}
                      </p>
                      <p class="text-sm font-semibold text-[#2d1f14] break-all">
                        {{
                          typeof val === "object" ? JSON.stringify(val) : val
                        }}
                      </p>
                    </div>
                  </div>
                </template>
              </div>
            </div>
          </template>

          <!-- Empty / error state -->
          <div v-else class="empty-state py-16">
            <svg
              class="w-8 h-8 text-[#c9a882]"
              fill="none"
              stroke="currentColor"
              stroke-width="1.5"
              viewBox="0 0 24 24"
            >
              <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2" />
              <circle cx="12" cy="7" r="4" />
            </svg>
            <p class="text-sm font-medium text-[#7c6a5e] mt-2">
              Profile unavailable
            </p>
            <p class="text-xs text-[#a0907e]">
              Could not load your account details
            </p>
          </div>
        </section>
      </main>
    </div>
  </div>
</template>

<style scoped>
.field-label {
  @apply block text-xs font-medium text-[#4a3728] mb-1.5;
}
.field-input {
  @apply w-full px-4 py-2.5 rounded-xl bg-[#faf7f4] border border-[#e8e0d8] text-[#2d1f14] text-sm placeholder-[#c4b5a5]
         focus:outline-none focus:border-[#8d6040] focus:ring-2 focus:ring-[#8d6040]/10  transition;
}
.btn-primary {
  @apply inline-flex items-center gap-2 bg-gradient-to-br from-[#7c5a3e] to-[#a5724f] text-white
         px-5 py-2.5 rounded-xl text-sm font-semibold hover:brightness-110 transition-all
         shadow-md shadow-[#7c5a3e]/20 disabled:opacity-60 disabled:cursor-not-allowed;
}
.btn-secondary {
  @apply inline-flex items-center gap-2 bg-[#f0ebe4] text-[#4a3728]
         px-5 py-2.5 rounded-xl text-sm font-semibold hover:bg-[#e8e0d8] transition;
}
.empty-state {
  @apply flex flex-col items-center justify-center py-12 text-center;
}
</style>
