<template>
  <div
    class="group bg-white rounded-2xl overflow-hidden border border-[#ede8e2] shadow-sm hover:shadow-lg transition-all duration-300"
  >
    <!-- Image Area -->
    <div class="relative overflow-hidden bg-[#f5f0ea] h-48">
      <img
        v-if="product.images?.length"
        :src="getImageUrl(product.images[0].image)"
        :alt="product.title"
        class="w-full h-full object-contain p-3 group-hover:scale-105 transition duration-500"
      />
      <div
        v-else
        class="w-full h-full flex flex-col items-center justify-center gap-2 text-[#c4b5a8]"
      >
        <svg
          class="w-10 h-10"
          fill="none"
          stroke="currentColor"
          stroke-width="1.2"
          viewBox="0 0 24 24"
        >
          <rect x="3" y="3" width="18" height="18" rx="2" />
          <circle cx="8.5" cy="8.5" r="1.5" />
          <polyline points="21 15 16 10 5 21" />
        </svg>
        <span class="text-xs font-medium">No Image</span>
      </div>

      <!-- Condition Badge -->
      <div
        class="absolute top-2.5 left-2.5 bg-white/90 backdrop-blur px-2.5 py-1 rounded-full text-[10px] font-semibold text-[#4a3728] shadow-sm border border-[#ede8e2]"
      >
        {{ product.condition }}
      </div>

      <!-- Stock Badge -->
      <div class="absolute top-2.5 right-2.5">
        <span
          v-if="product.stock > 0"
          class="bg-emerald-50 text-emerald-700 border border-emerald-200 text-[10px] px-2.5 py-1 rounded-full font-semibold"
        >
          In Stock
        </span>
        <span
          v-else
          class="bg-red-50 text-red-600 border border-red-200 text-[10px] px-2.5 py-1 rounded-full font-semibold"
        >
          Out of Stock
        </span>
      </div>
    </div>

    <!-- Content -->
    <div class="p-4 space-y-3">
      <!-- Category -->
      <span
        class="inline-block text-[10px] uppercase tracking-widest font-semibold text-[#a0907e] bg-[#f5f0ea] px-2 py-0.5 rounded-md"
      >
        {{ product.category_name }}
      </span>

      <!-- Title -->
      <h3
        class="text-sm font-semibold text-[#2d2016] line-clamp-2 leading-snug"
      >
        {{ product.title }}
      </h3>

      <!-- Price row -->
      <div class="flex items-end justify-between">
        <p class="text-xl font-bold text-[#7c5a3e]">${{ product.price }}</p>
        <div class="text-right">
          <p class="text-[10px] text-[#a0907e]">
            SKU:
            <span class="font-medium text-[#6b5a4e]">{{ product.sku }}</span>
          </p>
          <p class="text-[10px] text-[#a0907e]">
            Stock:
            <span
              class="font-semibold"
              :class="product.stock > 0 ? 'text-emerald-600' : 'text-red-500'"
              >{{ product.stock }}</span
            >
          </p>
        </div>
      </div>

      <!-- Actions -->
      <div class="flex gap-2 pt-1">
        <button
          @click="$emit('edit')"
          class="flex-1 py-2 rounded-xl border border-[#ede8e2] bg-[#f5f0ea] hover:bg-[#ede8e2] text-[#4a3728] text-xs font-semibold flex items-center justify-center gap-1.5 transition-colors"
        >
          <svg
            class="w-3.5 h-3.5"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            viewBox="0 0 24 24"
          >
            <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7" />
            <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z" />
          </svg>
          Edit
        </button>
        <button
          @click="$emit('delete')"
          class="flex-1 py-2 rounded-xl bg-red-50 hover:bg-red-100 text-red-600 border border-red-200 text-xs font-semibold flex items-center justify-center gap-1.5 transition-colors"
        >
          <svg
            class="w-3.5 h-3.5"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            viewBox="0 0 24 24"
          >
            <polyline points="3 6 5 6 21 6" />
            <path d="M19 6l-1 14a2 2 0 01-2 2H8a2 2 0 01-2-2L5 6" />
            <path d="M10 11v6M14 11v6" />
            <path d="M9 6V4a1 1 0 011-1h4a1 1 0 011 1v2" />
          </svg>
          Delete
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
const getImageUrl = (path) => {
  if (!path || typeof path !== "string") {
    return "";
  }

  const BASE_URL = import.meta.env.VITE_API_BASE_URL;
  return path.startsWith("http") ? path : `${BASE_URL}${path}`;

  // return path.startsWith("http") ? path : `http://127.0.0.1:8000${path}`;

  // const imageUrl = path.startsWith("http")
  //   ? path
  //   : `${BASE_URL.replace(/\/api\/?$/, "")}${path}`;
};

defineProps({
  product: Object,
});
</script>
