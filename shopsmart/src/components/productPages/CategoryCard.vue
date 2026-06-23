<template>
  <div
    @click="handleCategoryClick"
    class="group relative overflow-hidden rounded-[28px] bg-white border border-gray-100 p-7 shadow-sm hover:shadow-2xl transition-all duration-500 hover:-translate-y-2 cursor-pointer"
  >
    <!-- background glow -->
    <div
      class="absolute top-[-50px] right-[-50px] w-[140px] h-[140px] rounded-full bg-[#b08b6d]/10 blur-3xl opacity-0 group-hover:opacity-100 transition duration-500"
    ></div>

    <!-- icon -->
    <div
      class="relative z-10 w-16 h-16 rounded-2xl bg-[#b08b6d]/10 flex items-center justify-center mb-6 group-hover:bg-[#b08b6d] transition duration-300"
    >
      <component
        :is="getCategoryIcon(name)"
        class="w-8 h-8 text-[#b08b6d] group-hover:text-white transition duration-300"
      />
    </div>

    <!-- content -->
    <div class="relative z-10">
      <h3
        class="font-bold text-xl text-gray-900 group-hover:text-[#b08b6d] transition"
      >
        {{ name }}
      </h3>

      <p class="text-sm text-gray-500 mt-2 leading-6">
        Explore premium {{ name.toLowerCase() }} collections
      </p>
    </div>

    <div
      class="relative z-10 mt-6 flex items-center text-[#b08b6d] font-semibold"
    >
      Explore Now
    </div>
  </div>
</template>

<script setup>
import api from "../../services/api";
import {
  Headphones,
  Shirt,
  Footprints,
  Watch,
  Sofa,
  Dumbbell,
  Sparkles,
  BookOpen,
  ShoppingBag,
} from "lucide-vue-next";

const emit = defineEmits(["select"]);

const props = defineProps({
  id: Number,
  name: String,
});

const icons = {
  electronics: Headphones,
  fashion: Shirt,
  shoes: Footprints,
  watches: Watch,
  furniture: Sofa,
  sports: Dumbbell,
  beauty: Sparkles,
  books: BookOpen,
};

const getCategoryIcon = (name) => {
  return icons[name?.toLowerCase()] || ShoppingBag;
};

const handleCategoryClick = async () => {
  try {
    await api.post("/analytics/category-click/", {
      category_id: props.id,
    });
  } catch (err) {
    console.error("Analytics failed", err);
  }

  emit("select");
};
</script>