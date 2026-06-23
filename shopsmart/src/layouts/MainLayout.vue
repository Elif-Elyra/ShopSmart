<template>
  <div class="min-h-screen flex flex-col bg-gray-100">
    <!-- Header -->
    <Navbar v-if="!$route.meta.hideLayout" />

    <!-- Page content -->
    <main class="flex-1">
      <div class="max-w-7xl mx-auto">
        <slot />
      </div>
    </main>

    <!-- Footer -->
    <Footer v-if="!$route.meta.hideLayout" />
  </div>
</template>

<script setup>
import Navbar from "../components/primary/Navbar.vue";
import Footer from "../components/primary/Footer.vue";
</script>
