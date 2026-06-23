<template>
  <MainLayout>
    <router-view />
  </MainLayout>
</template>

<script setup>
import { onMounted } from "vue";
import MainLayout from "./layouts/MainLayout.vue";
import { useAuthStore } from "./store/authStore";

const auth = useAuthStore();

onMounted(async () => {
  if (auth.access && !auth.user) {
    await auth.fetchUser();
  }
});
</script>