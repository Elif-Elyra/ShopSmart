<template>
  <div
    class="min-h-screen bg-[#f8f5f2]"
    style="font-family: &quot;Inter&quot;, system-ui, sans-serif"
  >
    <!-- Loading -->
    <div
      v-if="!product && !errorMessage"
      class="h-screen flex flex-col items-center justify-center gap-4"
    >
      <div
        class="w-10 h-10 rounded-full border-4 border-[#e0d8d0] border-t-[#a5856f] animate-spin"
      ></div>
      <p class="text-[#a0907e] text-sm">Loading product…</p>
    </div>

    <!-- Error banner -->
    <div v-if="errorMessage" class="max-w-7xl mx-auto pt-6 px-6">
      <div
        class="flex items-center gap-3 bg-red-50 border border-red-200 text-red-700 px-5 py-4 rounded-2xl text-sm"
      >
        <svg
          class="w-4 h-4 shrink-0"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          viewBox="0 0 24 24"
        >
          <circle cx="12" cy="12" r="10" />
          <line x1="12" y1="8" x2="12" y2="12" />
          <line x1="12" y1="16" x2="12.01" y2="16" />
        </svg>
        {{ errorMessage }}
      </div>
    </div>

    <div
      v-if="product"
      class="max-w-7xl mx-auto px-5 md:px-8 lg:px-12 py-8 md:py-12"
    >
      <!-- Breadcrumb -->
      <nav class="flex items-center gap-2 text-xs text-[#b0a090] mb-10">
        <RouterLink to="/" class="hover:text-[#8c6b55] transition"
          >Home</RouterLink
        >
        <svg
          class="w-3 h-3"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          viewBox="0 0 24 24"
        >
          <path d="M9 18l6-6-6-6" />
        </svg>
        <span class="hover:text-[#8c6b55] cursor-pointer transition">{{
          product.category_name
        }}</span>
        <svg
          class="w-3 h-3"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          viewBox="0 0 24 24"
        >
          <path d="M9 18l6-6-6-6" />
        </svg>
        <span class="text-[#4a3728] font-medium truncate max-w-[200px]">{{
          product.title
        }}</span>
      </nav>

      <!-- ══════════════ MAIN GRID ══════════════ -->
      <div class="grid lg:grid-cols-2 gap-10 xl:gap-16">
        <!-- ── LEFT: Images ── -->
        <div class="space-y-4">
          <!-- Main image -->
          <div
            class="bg-white rounded-3xl border border-[#ede8e3] overflow-hidden shadow-sm"
          >
            <img
              :src="selectedImage"
              :alt="product.title"
              class="w-full h-[340px] md:h-[520px] object-contain p-6 transition-all duration-300"
            />
          </div>

          <!-- Thumbnails -->
          <div v-if="allImages.length > 1" class="grid grid-cols-4 gap-3">
            <button
              v-for="img in allImages"
              :key="img.id"
              @click="selectedImage = img.image"
              :class="[
                'bg-white rounded-2xl border overflow-hidden h-[80px] md:h-[100px] transition-all duration-200',
                selectedImage === img.image
                  ? 'border-[#a5856f] ring-2 ring-[#a5856f]/30 shadow-sm'
                  : 'border-[#ede8e3] hover:border-[#c4a882]',
              ]"
            >
              <img
                :src="img.image"
                class="w-full h-full object-contain p-1.5"
              />
            </button>
          </div>
        </div>

        <!-- ── RIGHT: Details ── -->
        <div class="space-y-5">
          <!-- Badges -->
          <div class="flex items-center gap-2 flex-wrap">
            <span
              class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-green-50 text-green-700 border border-green-100 capitalize"
            >
              <span class="w-1.5 h-1.5 rounded-full bg-green-500"></span>
              {{ product.condition }}
            </span>
            <span
              :class="[
                'inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold border',
                product.stock > 0
                  ? 'bg-blue-50 text-blue-700 border-blue-100'
                  : 'bg-red-50 text-red-700 border-red-100',
              ]"
            >
              <span
                :class="[
                  'w-1.5 h-1.5 rounded-full',
                  product.stock > 0 ? 'bg-blue-500' : 'bg-red-500',
                ]"
              ></span>
              {{
                product.stock > 0 ? `${product.stock} in stock` : "Out of stock"
              }}
            </span>
          </div>

          <!-- Title -->
          <h1
            class="text-3xl md:text-4xl font-bold text-[#2d1f14] leading-tight tracking-tight"
          >
            {{ product.title }}
          </h1>

          <!-- Rating row -->
          <div class="flex items-center gap-4 flex-wrap">
            <div class="flex items-center gap-2">
              <div class="flex">
                <span
                  v-for="i in 5"
                  :key="i"
                  :class="
                    i <= Math.round(product.average_rating || 0)
                      ? 'text-[#c9a574]'
                      : 'text-[#e0d8d0]'
                  "
                  class="text-[18px] leading-none"
                  >★</span
                >
              </div>
              <span class="font-bold text-[#2d1f14]">{{
                product.average_rating || 0
              }}</span>
              <span class="text-sm text-[#a0907e]"
                >({{ product.review_count || 0 }} reviews)</span
              >
            </div>
            <button
              @click="reviewModal = true"
              class="text-sm text-[#8c6b55] font-medium hover:text-[#6b4f38] transition underline underline-offset-2 decoration-[#c4a882]"
            >
              Write a review
            </button>
          </div>

          <!-- Price -->
          <div class="flex items-baseline gap-3">
            <span class="text-4xl font-bold text-[#8c6b55]"
              >${{ product.price }}</span
            >
            <span class="text-sm text-[#a0907e]">USD</span>
          </div>

          <!-- Seller -->
          <div class="flex items-center gap-2">
            <span class="text-sm text-[#a0907e]">Sold by</span>
            <RouterLink
              to="/seller/dashboard"
              class="inline-flex items-center gap-1.5 text-sm font-semibold text-[#2d1f14] hover:text-[#8c6b55] transition"
            >
              {{ product.seller_name }}
              <svg
                class="w-3.5 h-3.5 text-[#8d6040]"
                fill="none"
                stroke="currentColor"
                stroke-width="2.5"
                viewBox="0 0 24 24"
              >
                <path d="M9 18l6-6-6-6" />
              </svg>
            </RouterLink>
          </div>

          <!-- Meta strip -->
          <div class="flex gap-6 py-4 border-y border-[#ede8e3]">
            <div>
              <p
                class="text-xs text-[#a0907e] uppercase tracking-wider font-medium"
              >
                SKU
              </p>
              <p class="text-sm font-semibold text-[#2d1f14] mt-1">
                {{ product.sku }}
              </p>
            </div>
            <div class="w-px bg-[#ede8e3]"></div>
            <div>
              <p
                class="text-xs text-[#a0907e] uppercase tracking-wider font-medium"
              >
                Category
              </p>
              <p class="text-sm font-semibold text-[#2d1f14] mt-1">
                {{ product.category_name }}
              </p>
            </div>
          </div>

          <!-- Quantity -->
          <div class="space-y-2">
            <label class="text-sm font-medium text-[#4a3728]">Quantity</label>
            <div class="flex items-center gap-3">
              <button
                @click="qty = Math.max(1, qty - 1)"
                class="w-10 h-10 rounded-xl bg-white border border-[#ede8e3] text-[#4a3728] font-bold hover:border-[#a5856f] hover:text-[#a5856f] transition flex items-center justify-center"
              >
                −
              </button>
              <input
                type="number"
                min="1"
                :max="product.stock"
                v-model="qty"
                class="w-16 text-center py-2.5 bg-white rounded-xl border border-[#ede8e3] text-[#2d1f14] font-semibold text-sm focus:outline-none focus:border-[#a5856f] focus:ring-2 focus:ring-[#a5856f]/15 transition"
              />
              <button
                @click="qty = Math.min(product.stock, qty + 1)"
                class="w-10 h-10 rounded-xl bg-white border border-[#ede8e3] text-[#4a3728] font-bold hover:border-[#a5856f] hover:text-[#a5856f] transition flex items-center justify-center"
              >
                +
              </button>
              <span class="text-xs text-[#a0907e]"
                >{{ product.stock }} available</span
              >
            </div>
          </div>

          <!-- CTAs -->
          <div class="space-y-3 pt-1">
            <button
              @click="CartHandler"
              :disabled="product.stock < 1"
              class="w-full flex items-center justify-center gap-2.5 bg-white border-2 border-[#a5856f] text-[#a5856f] px-8 py-3.5 rounded-2xl font-semibold hover:bg-[#a5856f] hover:text-white transition-all duration-200 disabled:opacity-40 disabled:cursor-not-allowed"
            >
              <svg
                class="w-4.5 h-4.5"
                style="width: 18px; height: 18px"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                viewBox="0 0 24 24"
              >
                <path
                  d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"
                />
              </svg>
              Add to Cart
            </button>
            <button
              @click="BuyNowHandler"
              :disabled="product.stock < 1"
              class="w-full flex items-center justify-center gap-2.5 bg-gradient-to-br from-[#a5856f] to-[#7c5a3e] text-white px-8 py-3.5 rounded-2xl font-semibold hover:brightness-110 transition-all duration-200 shadow-md shadow-[#a5856f]/25 disabled:opacity-40 disabled:cursor-not-allowed"
            >
              <svg
                class="w-4.5 h-4.5"
                style="width: 18px; height: 18px"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                viewBox="0 0 24 24"
              >
                <path d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              Buy it Now
            </button>
          </div>

          <!-- Description -->
          <div class="pt-2">
            <p class="text-[#6a5748] leading-relaxed text-sm">
              {{ product.description }}
            </p>
          </div>
        </div>
      </div>

      <!-- ══════════════ REVIEWS ══════════════ -->
      <section class="mt-20 md:mt-28">
        <!-- Section header -->
        <div class="flex items-end justify-between mb-10">
          <div>
            <p
              class="text-xs text-[#a0907e] uppercase tracking-widest font-semibold mb-2"
            >
              What customers say
            </p>
            <h2 class="text-3xl font-bold text-[#2d1f14]">Customer Reviews</h2>
          </div>

          <!-- Aggregate score -->
          <div
            v-if="reviews.length"
            class="hidden md:flex flex-col items-end gap-1"
          >
            <div class="flex items-baseline gap-2">
              <span class="text-5xl font-bold text-[#8c6b55]">{{
                product.average_rating || 0
              }}</span>
              <span class="text-[#a0907e] text-lg font-medium">/5</span>
            </div>
            <div class="flex gap-0.5">
              <span
                v-for="i in 5"
                :key="i"
                :class="
                  i <= Math.round(product.average_rating || 0)
                    ? 'text-[#c9a574]'
                    : 'text-[#e0d8d0]'
                "
                class="text-xl"
                >★</span
              >
            </div>
            <p class="text-xs text-[#a0907e]">
              {{ product.review_count || 0 }} reviews
            </p>
          </div>
        </div>

        <!-- Review grid using ReviewCard component -->
        <div
          v-if="reviews.length"
          class="grid sm:grid-cols-2 lg:grid-cols-3 gap-5"
        >
          <ReviewCard v-for="r in reviews" :key="r.id" :review="r" />
        </div>

        <!-- Empty state -->
        <div
          v-else
          class="flex flex-col items-center justify-center py-16 gap-4 bg-white rounded-3xl border border-[#ede8e3]"
        >
          <div
            class="w-14 h-14 rounded-2xl bg-[#f4ede6] flex items-center justify-center"
          >
            <svg
              class="w-7 h-7 text-[#c9a882]"
              fill="none"
              stroke="currentColor"
              stroke-width="1.5"
              viewBox="0 0 24 24"
            >
              <path
                d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
              />
            </svg>
          </div>
          <div class="text-center">
            <p class="font-semibold text-[#4a3728]">No reviews yet</p>
            <p class="text-sm text-[#a0907e] mt-1">
              Be the first to share your experience
            </p>
          </div>
          <button
            @click="reviewModal = true"
            class="mt-1 px-6 py-2.5 rounded-xl bg-[#a5856f] text-white text-sm font-semibold hover:brightness-110 transition"
          >
            Write the first review
          </button>
        </div>
      </section>
    </div>

    <!-- ══════════════ REVIEW MODAL ══════════════ -->
    <Modal v-model="reviewModal" title="Write a Review">
      <template #default>
        <div class="space-y-5">
          <!-- Star picker -->
          <div>
            <label class="block text-sm font-medium mb-3 text-[#4a3728]"
              >Your Rating</label
            >
            <div class="flex gap-2">
              <button
                v-for="i in 5"
                :key="i"
                @click="reviewForm.rating = i"
                :class="[
                  'text-3xl transition-transform hover:scale-110',
                  i <= reviewForm.rating ? 'text-[#c9a574]' : 'text-[#e0d8d0]',
                ]"
              >
                ★
              </button>
              <span class="ml-2 text-sm text-[#a0907e] self-center"
                >{{ reviewForm.rating }} / 5</span
              >
            </div>
          </div>

          <!-- Comment -->
          <div>
            <label class="block text-sm font-medium mb-2 text-[#4a3728]"
              >Your Review</label
            >
            <textarea
              v-model="reviewForm.comment"
              rows="5"
              maxlength="500"
              placeholder="What did you think of this product? Be specific — your review helps other shoppers."
              class="w-full border border-[#e0d8d0] bg-[#faf7f4] rounded-2xl px-4 py-3 text-sm text-[#2d1f14] placeholder-[#c4b5a5] resize-none focus:outline-none focus:border-[#a5856f] focus:ring-2 focus:ring-[#a5856f]/15 transition"
            ></textarea>
            <div class="flex justify-between items-center mt-2">
              <span class="text-xs text-[#c4b5a5]"
                >Be honest and constructive</span
              >
              <span
                :class="[
                  'text-xs font-medium',
                  reviewForm.comment.length > 450
                    ? 'text-amber-600'
                    : 'text-[#a0907e]',
                ]"
                >{{ reviewForm.comment.length }}/500</span
              >
            </div>
          </div>
        </div>
      </template>

      <template #footer>
        <div class="flex justify-end gap-3">
          <button
            @click="reviewModal = false"
            class="px-5 py-2.5 rounded-xl border border-[#e0d8d0] text-[#4a3728] text-sm font-medium hover:bg-[#f4f0ec] transition"
          >
            Cancel
          </button>
          <button
            @click="submitReview"
            :disabled="reviewLoading || !reviewForm.comment.trim()"
            class="px-6 py-2.5 rounded-xl bg-gradient-to-br from-[#a5856f] to-[#7c5a3e] text-white text-sm font-semibold hover:brightness-110 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          >
            <span
              v-if="reviewLoading"
              class="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin"
            ></span>
            {{ reviewLoading ? "Submitting…" : "Submit Review" }}
          </button>
        </div>
      </template>
    </Modal>
  </div>
</template>

<script setup>
import { ref, watch, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import Modal from "../components/ui/ReuseModel.vue";
import ReviewCard from "../components/productPages/ReviewCard.vue";
import {
  getProduct,
  addCartItem,
  getCart,
  createReview,
  getProductReviews,
} from "../services/product";

// ProductDetail.vue — script setup mein add karo
import { useCartStore } from "../store/cartStore";
const cartStore = useCartStore();

const router = useRouter();
const route = useRoute();
const product = ref(null);
const selectedImage = ref(null);
const qty = ref(1);
const errorMessage = ref("");

const reviews = ref([]);
const reviewModal = ref(false);
const reviewForm = ref({ rating: 5, comment: "" });
const reviewLoading = ref(false);

watch(
  () => route.params.slug,
  async (slug) => {
    try {
      const res = await getProduct(slug);
      product.value = res;
      selectedImage.value = res.thumbnail;
      reviews.value = res.reviews || [];
    } catch (err) {
      errorMessage.value = err.detail || "Failed to load product";
    }
  },
  { immediate: true },
);

const allImages = computed(() => {
  if (!product.value) return [];
  const images = [];
  if (product.value.thumbnail)
    images.push({ id: "thumb", image: product.value.thumbnail });
  if (product.value.images?.length) images.push(...product.value.images);
  return images;
});


// ✅ CartHandler
const CartHandler = async () => {
  try {
    errorMessage.value = "";
    if (qty.value < 1) return (errorMessage.value = "Invalid quantity");
    if (qty.value > product.value.stock) return (errorMessage.value = "Not enough stock");

    await cartStore.addItem(product.value.id, qty.value); // ✅ Store se
  } catch (err) {
    errorMessage.value = err.detail || "Failed to add to cart";
  }
};

// ✅ BuyNowHandler
const BuyNowHandler = async () => {
  try {
    errorMessage.value = "";
    if (qty.value < 1) return (errorMessage.value = "Invalid quantity");
    if (qty.value > product.value.stock) return (errorMessage.value = "Not enough stock");

    await cartStore.addItem(product.value.id, qty.value); // ✅ Store se
    router.push("/checkout");
  } catch (err) {
    errorMessage.value = err.detail || "Failed to proceed to checkout";
  }
};

const submitReview = async () => {
  try {
    reviewLoading.value = true;
    const payload = {
      product: product.value.id,
      rating: reviewForm.value.rating,
      comment: reviewForm.value.comment,
    };
    const res = await createReview(payload);
    reviews.value.unshift(res);
    reviewModal.value = false;
    reviewForm.value = { rating: 5, comment: "" };
  } catch (err) {
    errorMessage.value = err.detail || "Failed to submit review";
  } finally {
    reviewLoading.value = false;
  }
};
</script>
