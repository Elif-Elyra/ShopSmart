<template>
  <router-link
    :to="`/products/${product.slug}`"
    class="bg-white rounded-xl shadow hover:shadow-xl transition overflow-hidden"
  >
    <div class="h-40 bg-gray-200">
      <img
        :src="product.image"
        :alt="product.name"
        class="w-full h-full object-contain rounded-lg"
      />
    </div>

    <div class="p-4 flex justify-between items-center">
      <p class="font-semibold text-gray-800">
        {{ product.name }}
      </p>

      <p class="text-[#967255] font-bold">${{ product.price }}</p>
    </div>
  </router-link>
</template>

<script setup>
defineProps({
  product: Object,
});

import { useRoute } from "vue-router";
const route = useRoute();
const slug = route.params.slug;
</script>
