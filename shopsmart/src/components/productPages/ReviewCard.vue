<template>
  <div
    class="group relative overflow-hidden rounded-2xl bg-white border border-[#ede8e3] p-6 shadow-sm hover:shadow-[0_8px_32px_rgba(139,107,85,0.12)] transition-all duration-400 hover:-translate-y-1"
  >
    <!-- Top: rating + date -->
    <div class="flex items-center justify-between mb-4">
      <!-- Star rating pills -->
      <div class="flex items-center gap-0.5">
        <span
          v-for="i in 5"
          :key="i"
          :class="i <= review.rating ? 'text-[#c9a574]' : 'text-[#e0d8d0]'"
          class="text-[17px] leading-none"
        >★</span>
      </div>
      <span class="text-xs text-[#b0a090]">
        {{ new Date(review.created_at).toLocaleDateString("en-US", { day: "numeric", month: "short", year: "numeric" }) }}
      </span>
    </div>

    <!-- Comment -->
    <p class="text-[#4a3728] text-sm leading-relaxed mb-5 line-clamp-4">
      {{ review.comment }}
    </p>

    <!-- Divider -->
    <div class="h-px bg-[#f0ebe4] mb-5"></div>

    <!-- Reviewer -->
    <div class="flex items-center gap-3">
      <div
        class="w-10 h-10 rounded-xl bg-gradient-to-br from-[#c9a882] to-[#8d6040] flex items-center justify-center text-white font-bold text-sm shrink-0"
      >
        {{ (review.user_name || "?").charAt(0).toUpperCase() }}
      </div>
      <div>
        <p class="text-sm font-semibold text-[#2d1f14]">{{ review.user_name }}</p>
        <div class="flex items-center gap-1.5 mt-0.5">
          <svg class="w-3 h-3 text-[#8d6040]" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
          </svg>
          <span class="text-[11px] text-[#8d6040] font-medium">Verified Purchase</span>
        </div>
      </div>
      <!-- numeric score badge -->
      <div class="ml-auto text-right">
        <span class="text-lg font-bold text-[#8d6040]">{{ review.rating }}</span>
        <span class="text-xs text-[#b0a090]">/5</span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  review: Object,
});
</script>