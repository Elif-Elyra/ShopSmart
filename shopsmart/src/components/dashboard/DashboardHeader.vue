<template>
  <div class="flex justify-between items-center">
    <h1 class="text-2xl font-bold text-gray-800">Seller Dashboard</h1>

    <button
      @click="$emit('add')"
      class="px-4 py-2 bg-[#b08b6d] text-white rounded-lg hover:bg-[#967255]"
    >
      Add Product
    </button>
  </div>
</template>
