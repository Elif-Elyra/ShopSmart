<template>
  <div class="min-h-screen bg-[#f5f0eb] py-10">
    <div class="max-w-7xl mx-auto px-4 sm:px-6">
      <!-- ===== HEADER ===== -->
      <div
        class="mb-8 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4"
      >
        <div>
          <h1
            class="text-3xl md:text-4xl font-extrabold text-[#2d2016] tracking-tight"
          >
            All Products
          </h1>
          <p class="text-sm text-[#a0907e] mt-1">
            {{ products.length }} products found
          </p>
        </div>

        <!-- DESKTOP SEARCH -->
        <div
          class="hidden md:flex items-center overflow-hidden border border-[#c9b08d] rounded-xl bg-white h-[46px] w-[320px] shadow-sm"
        >
          <input
            v-model="search"
            type="text"
            placeholder="Search products..."
            class="flex-1 px-4 outline-none text-sm bg-transparent text-[#2d2016] placeholder-[#c4b5a8]"
          />
          <button
            class="w-12 h-full bg-[#7c5a3e] hover:bg-[#5c3d2e] flex items-center justify-center transition-colors"
          >
            <svg
              class="w-4 h-4 text-white"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2.5"
                d="M21 21l-4.35-4.35m1.85-5.15a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
          </button>
        </div>

        <!-- MOBILE SEARCH -->
        <div class="flex md:hidden items-center gap-2">
          <div
            v-if="isSearchOpen"
            class="flex items-center overflow-hidden border border-[#c9b08d] rounded-xl bg-white h-[42px] flex-1 shadow-sm"
          >
            <input
              v-model="search"
              type="text"
              placeholder="Search..."
              class="flex-1 px-4 outline-none text-sm bg-transparent text-[#2d2016]"
            />
            <button
              @click="isSearchOpen = false"
              class="w-11 h-full bg-[#7c5a3e] flex items-center justify-center"
            >
              <svg
                class="w-4 h-4 text-white"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2.5"
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>
          <button
            v-else
            @click="isSearchOpen = true"
            class="w-11 h-11 rounded-xl bg-[#7c5a3e] flex items-center justify-center shadow-sm"
          >
            <svg
              class="w-4 h-4 text-white"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2.5"
                d="M21 21l-4.35-4.35m1.85-5.15a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
          </button>
        </div>
      </div>

      <!-- ===== FILTER BAR ===== -->
      <div class="flex flex-wrap items-center gap-3 mb-8">
        <!-- Category -->
        <div class="relative">
          <select
            v-model="selectedCategory"
            class="appearance-none h-10 pl-4 pr-9 bg-white border border-[#ede8e2] rounded-xl text-sm text-[#4a3728] font-medium focus:outline-none focus:border-[#8d6040] focus:ring-2 focus:ring-[#8d6040]/10 shadow-sm cursor-pointer"
          >
            <option value="">All Categories</option>
            <option
              v-for="category in categories"
              :key="category.id"
              :value="category.id"
            >
              {{ category.name }}
            </option>
          </select>
          <svg
            class="absolute right-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-[#a0907e] pointer-events-none"
            fill="none"
            stroke="currentColor"
            stroke-width="2.5"
            viewBox="0 0 24 24"
          >
            <path d="M6 9l6 6 6-6" />
          </svg>
        </div>

        <!-- Sort -->
        <div class="relative">
          <select
            v-model="sortBy"
            class="appearance-none h-10 pl-4 pr-9 bg-white border border-[#ede8e2] rounded-xl text-sm text-[#4a3728] font-medium focus:outline-none focus:border-[#8d6040] focus:ring-2 focus:ring-[#8d6040]/10 shadow-sm cursor-pointer"
          >
            <option value="default">Sort: Default</option>
            <option value="low">Price: Low to High</option>
            <option value="high">Price: High to Low</option>
          </select>
          <svg
            class="absolute right-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-[#a0907e] pointer-events-none"
            fill="none"
            stroke="currentColor"
            stroke-width="2.5"
            viewBox="0 0 24 24"
          >
            <path d="M6 9l6 6 6-6" />
          </svg>
        </div>

        <!-- Active filter chip -->
        <div
          v-if="selectedCategory"
          class="flex items-center gap-1.5 bg-[#7c5a3e] text-white text-xs font-semibold px-3 py-1.5 rounded-full"
        >
          <span>{{
            categories.find((c) => c.id == selectedCategory)?.name
          }}</span>
          <button
            @click="selectedCategory = ''"
            class="hover:text-white/70 transition-colors"
          >
            <svg
              class="w-3 h-3"
              fill="none"
              stroke="currentColor"
              stroke-width="3"
              viewBox="0 0 24 24"
            >
              <path d="M18 6L6 18M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      <!-- ===== LOADING ===== -->
      <div v-if="loading" class="grid grid-cols-2 xl:grid-cols-4 gap-5">
        <div
          v-for="n in 8"
          :key="n"
          class="bg-white rounded-2xl overflow-hidden border border-[#ede8e2] animate-pulse"
        >
          <div class="h-56 bg-[#f0ebe4]"></div>
          <div class="p-4 space-y-3">
            <div class="h-3 bg-[#f0ebe4] rounded-full w-1/3"></div>
            <div class="h-4 bg-[#f0ebe4] rounded-full w-3/4"></div>
            <div class="h-3 bg-[#f0ebe4] rounded-full w-1/4"></div>
            <div class="h-9 bg-[#f0ebe4] rounded-xl mt-2"></div>
          </div>
        </div>
      </div>

      <!-- ===== EMPTY STATE ===== -->
      <div
        v-else-if="products.length === 0"
        class="flex flex-col items-center justify-center py-28 text-center"
      >
        <div
          class="w-16 h-16 rounded-2xl bg-white border border-[#ede8e2] flex items-center justify-center mb-4 shadow-sm"
        >
          <svg
            class="w-8 h-8 text-[#c4b5a8]"
            fill="none"
            stroke="currentColor"
            stroke-width="1.5"
            viewBox="0 0 24 24"
          >
            <circle cx="11" cy="11" r="8" />
            <path d="M21 21l-4.35-4.35" />
          </svg>
        </div>
        <h3 class="text-[#2d2016] font-semibold text-lg">No products found</h3>
        <p class="text-sm text-[#a0907e] mt-1 mb-5">
          Try adjusting your search or filters
        </p>
        <button
          @click="
            selectedCategory = '';
            search = '';
          "
          class="px-5 py-2.5 rounded-xl bg-[#7c5a3e] text-white text-sm font-medium hover:bg-[#5c3d2e] transition-colors"
        >
          Clear Filters
        </button>
      </div>

      <!-- ===== PRODUCT GRID ===== -->
      <div v-else class="grid grid-cols-2 xl:grid-cols-4 gap-4 md:gap-5">
        <div
          v-for="p in products"
          :key="p.id"
          class="group bg-white rounded-2xl overflow-hidden border border-[#ede8e2] shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300 cursor-pointer"
          @click="goToProduct(p.slug)"
        >
          <!-- IMAGE -->
          <div class="relative h-48 md:h-64 bg-[#f5f0ea] overflow-hidden">
            <img
              :src="p.thumbnail"
              :alt="p.title"
              class="w-full h-full object-cover group-hover:scale-105 transition duration-500"
            />

            <!-- Gradient overlay on hover -->
            <div
              class="absolute inset-0 bg-gradient-to-t from-black/30 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"
            ></div>

            <!-- View details pill -->
            <div
              class="absolute bottom-3 left-1/2 -translate-x-1/2 opacity-0 group-hover:opacity-100 translate-y-2 group-hover:translate-y-0 transition-all duration-300"
            >
              <span
                class="bg-white text-[#7c5a3e] text-[11px] font-bold px-4 py-1.5 rounded-full shadow-lg whitespace-nowrap"
              >
                View Details →
              </span>
            </div>

            <!-- Wishlist btn -->
            <button
              @click.stop
              class="absolute top-3 right-3 w-8 h-8 rounded-full bg-white/90 border border-[#ede8e2] flex items-center justify-center shadow-sm hover:bg-white hover:scale-110 transition-all"
            >
              <svg
                class="w-4 h-4 text-[#8d6040]"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M4.318 6.318a4.5 4.5 0 016.364 0L12 7.636l1.318-1.318a4.5 4.5 0 116.364 6.364L12 20.364 4.318 12.682a4.5 4.5 0 010-6.364z"
                />
              </svg>
            </button>
          </div>

          <!-- CONTENT -->
          <div class="p-4 space-y-2">
            <!-- Category badge -->
            <span
              class="inline-block text-[10px] uppercase tracking-widest font-semibold text-[#a0907e] bg-[#f5f0ea] px-2 py-0.5 rounded-md"
            >
              {{ p.category_name }}
            </span>

            <!-- Title -->
            <h2
              class="text-sm font-semibold text-[#2d2016] line-clamp-2 leading-snug group-hover:text-[#7c5a3e] transition-colors"
            >
              {{ p.title }}
            </h2>

            <!-- Price row -->
            <div class="flex items-center justify-between pt-1">
              <p class="text-lg font-extrabold text-[#7c5a3e]">
                ${{ p.price }}
              </p>
              <span class="text-amber-400 text-xs">★★★★★</span>
            </div>

            <!-- Button -->
            <button
              @click.stop="goToProduct(p.slug)"
              class="w-full h-10 mt-1 rounded-xl bg-gradient-to-br from-[#7c5a3e] to-[#a5724f] text-white text-xs font-semibold hover:brightness-110 transition-all shadow-sm"
            >
              View Details
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import {
  getProducts,
  getCategories,
  getCategoryProducts,
} from "../services/product";

const router = useRouter();
const route = useRoute();

const products = ref([]);
const categories = ref([]);
const search = ref("");
const sortBy = ref("default");
const selectedCategory = ref(route.query.category || "");
const loading = ref(false);
const isSearchOpen = ref(false);

const goToProduct = (slug) => {
  router.push(`/products/${slug}`);
};

const buildParams = () => {
  const params = {};
  if (search.value?.trim()) params.search = search.value.trim();
  if (sortBy.value === "low") params.ordering = "price";
  if (sortBy.value === "high") params.ordering = "-price";
  return params;
};

const loadProducts = async () => {
  loading.value = true;
  try {
    const categoryId = Number(selectedCategory.value);
    const params = buildParams();
    if (!isNaN(categoryId) && categoryId > 0) {
      products.value = await getCategoryProducts(categoryId, params);
    } else {
      const res = await getProducts(params);
      products.value = res.results || res;
    }
  } catch (err) {
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const loadCategories = async () => {
  try {
    const res = await getCategories();
    categories.value = res.filter((c) => c.parent === null);
  } catch (err) {
    console.error(err);
  }
};

watch([search, selectedCategory, sortBy], async () => {
  await loadProducts();
  router.replace({
    query: {
      category: selectedCategory.value
        ? Number(selectedCategory.value)
        : undefined,
    },
  });
});

watch(
  () => route.query.category,
  (newCategory) => {
    selectedCategory.value =
      newCategory && !isNaN(Number(newCategory)) ? Number(newCategory) : "";
  },
);

onMounted(async () => {
  await Promise.all([loadCategories(), loadProducts()]);
});
</script>
