<template>
  <Teleport to="body">
    <Transition
      enter-active-class="transition-all duration-250 ease-out"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition-all duration-200 ease-in"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="show"
        class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm"
        @click.self="$emit('update:show', false)"
      >
        <Transition
          enter-active-class="transition-all duration-250 ease-out"
          enter-from-class="opacity-0 scale-95 translate-y-2"
          enter-to-class="opacity-100 scale-100 translate-y-0"
          leave-active-class="transition-all duration-200 ease-in"
          leave-from-class="opacity-100 scale-100 translate-y-0"
          leave-to-class="opacity-0 scale-95 translate-y-2"
        >
          <div v-if="show" class="w-full max-w-lg bg-white rounded-2xl shadow-2xl overflow-hidden">

            <!-- Modal Header -->
            <div class="bg-gradient-to-br from-[#5c3d2e] via-[#8d6040] to-[#b8916a] px-6 py-5 flex items-center justify-between">
              <div>
                <h2 class="text-base font-semibold text-white tracking-wide">
                  {{ editing ? 'Update Product' : 'Add New Product' }}
                </h2>
                <p class="text-white/60 text-xs mt-0.5">
                  {{ editing ? 'Edit product details below' : 'Fill in the details for your new product' }}
                </p>
              </div>
              <button
                @click="$emit('update:show', false)"
                class="w-8 h-8 rounded-full bg-white/15 hover:bg-white/25 flex items-center justify-center text-white transition-colors"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                  <path d="M18 6L6 18M6 6l12 12"/>
                </svg>
              </button>
            </div>

            <!-- Form Body -->
            <div class="px-6 py-5 overflow-y-auto space-y-4 max-h-[60vh]">

              <!-- Title -->
              <div class="space-y-1.5">
                <label class="block text-xs font-semibold text-[#4a3728]">Title</label>
                <input
                  :value="form.title"
                  @input="updateField('title', $event.target.value)"
                  placeholder="Product name"
                  class="input-field"
                />
              </div>

              <!-- Slug + SKU -->
              <div class="grid grid-cols-2 gap-3">
                <div class="space-y-1.5">
                  <label class="block text-xs font-semibold text-[#4a3728]">Slug</label>
                  <input
                    :value="form.slug"
                    @input="updateField('slug', $event.target.value)"
                    placeholder="product-slug"
                    class="input-field"
                  />
                </div>
                <div class="space-y-1.5">
                  <label class="block text-xs font-semibold text-[#4a3728]">SKU</label>
                  <input
                    :value="form.sku"
                    @input="updateField('sku', $event.target.value)"
                    placeholder="SKU-001"
                    class="input-field"
                  />
                </div>
              </div>

              <!-- Category -->
              <div class="space-y-1.5">
                <label class="block text-xs font-semibold text-[#4a3728]">Category</label>
                <select
                  :value="form.category"
                  @change="updateField('category', $event.target.value)"
                  class="input-field"
                >
                  <option disabled value="">Select a category</option>
                  <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
                </select>
              </div>

              <!-- Price + Stock -->
              <div class="grid grid-cols-2 gap-3">
                <div class="space-y-1.5">
                  <label class="block text-xs font-semibold text-[#4a3728]">Price ($)</label>
                  <input
                    type="number"
                    :value="form.price"
                    @input="updateField('price', Number($event.target.value))"
                    placeholder="0.00"
                    class="input-field"
                  />
                </div>
                <div class="space-y-1.5">
                  <label class="block text-xs font-semibold text-[#4a3728]">Stock</label>
                  <input
                    type="number"
                    :value="form.stock"
                    @input="updateField('stock', Number($event.target.value))"
                    placeholder="0"
                    class="input-field"
                  />
                </div>
              </div>

              <!-- Description -->
              <div class="space-y-1.5">
                <label class="block text-xs font-semibold text-[#4a3728]">Description</label>
                <textarea
                  :value="form.description"
                  @input="updateField('description', $event.target.value)"
                  placeholder="Write a short description..."
                  rows="3"
                  class="input-field resize-none"
                ></textarea>
              </div>

              <!-- File Uploads -->
              <div class="grid grid-cols-2 gap-3">
                <div class="space-y-1.5">
                  <label class="block text-xs font-semibold text-[#4a3728]">Thumbnail</label>
                  <label class="file-upload-btn">
                    <svg class="w-4 h-4 text-[#8d6040]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                      <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M17 8l-5-5-5 5M12 3v12"/>
                    </svg>
                    <span class="text-xs text-[#6b5a4e]">
                      {{ thumbnailName || 'Choose file' }}
                    </span>
                    <input type="file" class="hidden" @change="handleThumbnail" accept="image/*" />
                  </label>
                </div>
                <div class="space-y-1.5">
                  <label class="block text-xs font-semibold text-[#4a3728]">Extra Images</label>
                  <label class="file-upload-btn">
                    <svg class="w-4 h-4 text-[#8d6040]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                      <rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/>
                      <polyline points="21 15 16 10 5 21"/>
                    </svg>
                    <span class="text-xs text-[#6b5a4e]">
                      {{ imagesName || 'Choose files' }}
                    </span>
                    <input type="file" multiple class="hidden" @change="handleImages" accept="image/*" />
                  </label>
                </div>
              </div>

            </div>

            <!-- Footer Actions -->
            <div class="px-6 py-4 border-t border-[#ede8e2] bg-[#faf8f5] flex justify-end gap-2">
              <button
                @click="$emit('update:show', false)"
                class="px-5 py-2.5 rounded-xl border border-[#ede8e2] bg-white hover:bg-[#f5f0ea] text-[#4a3728] text-sm font-medium transition-colors"
              >
                Cancel
              </button>
              <button
                @click="$emit('save')"
                class="px-6 py-2.5 rounded-xl bg-gradient-to-br from-[#7c5a3e] to-[#a5724f] text-white text-sm font-semibold hover:brightness-110 transition-all shadow-sm flex items-center gap-2"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                  <polyline points="20 6 9 17 4 12"/>
                </svg>
                {{ editing ? 'Update Product' : 'Add Product' }}
              </button>
            </div>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, watch } from "vue";

const props = defineProps({
  show: Boolean,
  form: Object,
  editing: Boolean,
  categories: Array,
});

const emit = defineEmits(["update:show", "update-field", "save"]);

const thumbnailName = ref("");
const imagesName = ref("");

const updateField = (key, value) => {
  emit("update-field", { key, value });
};

const handleThumbnail = (e) => {
  const file = e.target.files[0];
  if (file) {
    thumbnailName.value = file.name;
    updateField("thumbnail", file);
  }
};

const handleImages = (e) => {
  const files = Array.from(e.target.files);
  if (files.length) {
    imagesName.value = `${files.length} file${files.length > 1 ? "s" : ""} selected`;
    updateField("images", files);
  }
};

// Reset file names when modal closes
watch(() => props.show, (val) => {
  if (!val) {
    thumbnailName.value = "";
    imagesName.value = "";
  }
});
</script>

<style scoped>
.input-field {
  @apply w-full px-3 py-2.5 text-sm bg-[#f5f0ea] border border-[#ede8e2] rounded-xl
         text-[#2d2016] placeholder-[#c4b5a8]
         focus:outline-none focus:border-[#8d6040] focus:ring-2 focus:ring-[#8d6040]/10 transition-all;
}

.file-upload-btn {
  @apply flex items-center gap-2 w-full px-3 py-2.5 bg-[#f5f0ea] border border-dashed border-[#c4b5a8]
         hover:border-[#8d6040] hover:bg-[#ede8e2] rounded-xl cursor-pointer transition-all duration-200;
}
</style>
