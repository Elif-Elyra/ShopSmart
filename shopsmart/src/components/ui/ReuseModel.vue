<template>
  <Transition name="modal">
    <div
      v-if="modelValue"
      class="fixed inset-0 z-50 flex items-center justify-center px-4"
    >
      <!-- Overlay -->
      <div
        class="absolute inset-0 bg-black/50 backdrop-blur-sm"
        @click="closeModal"
      ></div>

      <!-- Modal -->
      <div
        class="relative w-full max-w-lg bg-white rounded-2xl shadow-2xl overflow-hidden"
        role="dialog"
        aria-modal="true"
        @click.stop
      >
        <!-- Header -->
        <div
          class="flex items-center justify-between px-6 py-4 border-b border-gray-100"
        >
          <h2 class="text-lg font-semibold text-gray-800">
            {{ title }}
          </h2>

          <button
            type="button"
            @click="closeModal"
            class="w-9 h-9 flex items-center justify-center rounded-full hover:bg-gray-100 transition"
          >
            <span class="text-xl text-gray-500">&times;</span>
          </button>
        </div>

        <!-- Body -->
        <div class="p-6 max-h-[70vh] overflow-y-auto">
          <slot />
        </div>

        <!-- Footer -->
        <div
          v-if="$slots.footer"
          class="px-6 py-4 border-t border-gray-100 bg-gray-50"
        >
          <slot name="footer" />
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { watch, onBeforeUnmount } from "vue";

const props = defineProps({
  modelValue: Boolean,
  title: {
    type: String,
    default: "Modal",
  },
});

const emit = defineEmits(["update:modelValue"]);

function closeModal() {
  emit("update:modelValue", false);
}

function handleEscape(event) {
  if (event.key === "Escape") {
    closeModal();
  }
}

watch(
  () => props.modelValue,
  (isOpen) => {
    if (isOpen) {
      window.addEventListener("keydown", handleEscape);
      document.body.style.overflow = "hidden";
    } else {
      window.removeEventListener("keydown", handleEscape);
      document.body.style.overflow = "";
    }
  },
);

onBeforeUnmount(() => {
  window.removeEventListener("keydown", handleEscape);
  document.body.style.overflow = "";
});
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: all 0.25s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
  transform: scale(0.95);
}
</style>
