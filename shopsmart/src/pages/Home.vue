<template>
  <div class="bg-[#f5f0eb]">
  
    
   
    <!-- ===== Hero ===== -->
     <section class="relative bg-[#f5f0eb] overflow-hidden min-h-[90vh] flex items-center">
      <!-- Glow blobs -->
      <div class="absolute top-[-150px] right-[-100px] w-[500px] h-[500px] rounded-full bg-[#c9a882]/25 blur-[120px] pointer-events-none"></div>
      <div class="absolute bottom-[-100px] left-[-80px] w-[350px] h-[350px] rounded-full bg-[#8d6040]/15 blur-[100px] pointer-events-none"></div>
 
      <div class="max-w-7xl mx-auto px-6 py-16 lg:py-0 grid lg:grid-cols-2 gap-12 lg:gap-20 items-center w-full">
 
        <!-- LEFT -->
        <div class="space-y-7">
          <!-- Badge -->
          <span class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-[#7c5a3e]/10 border border-[#7c5a3e]/20 text-[#7c5a3e] text-xs font-semibold tracking-widest uppercase">
            <span class="w-1.5 h-1.5 rounded-full bg-[#7c5a3e] animate-pulse"></span>
            New Collection 2026
          </span>
 
          <!-- Heading -->
          <h1 class="text-5xl md:text-6xl font-extrabold leading-[1.08] tracking-tight text-[#2d2016]">
            Upgrade Your Style
            <span class="block">With
              <span class="relative inline-block text-[#8d6040]">
                Premium
                <svg class="absolute -bottom-1 left-0 w-full" viewBox="0 0 300 10" fill="none">
                  <path d="M2 7 Q150 1 298 7" stroke="#c9a882" stroke-width="3" stroke-linecap="round"/>
                </svg>
              </span>
              Products
            </span>
          </h1>
 
          <p class="text-base text-[#6b5a4e] max-w-lg leading-relaxed">
            Discover trending products with premium quality, fast shipping, and exclusive discounts crafted for modern shoppers.
          </p>
 
          <!-- CTAs -->
          <div class="flex flex-wrap gap-3 pt-1">
            <router-link
              to="/products"
              class="inline-flex items-center gap-2 bg-gradient-to-br from-[#7c5a3e] to-[#a5724f] text-white px-7 py-3.5 rounded-xl font-semibold text-sm hover:brightness-110 transition-all shadow-lg shadow-[#7c5a3e]/30"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                <path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/>
                <path d="M16 10a4 4 0 01-8 0"/>
              </svg>
              Shop Now
            </router-link>
            <router-link
              to="/products"
              class="inline-flex items-center gap-2 border border-[#c9a882] text-[#7c5a3e] px-7 py-3.5 rounded-xl font-semibold text-sm hover:bg-[#f0ebe4] transition-all"
            >
              Explore Deals
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </router-link>
          </div>
 
          <!-- Trust row -->
          <div class="flex items-center gap-4 pt-2">
            <div class="flex -space-x-3">
              <img src="https://randomuser.me/api/portraits/women/44.jpg" class="w-10 h-10 rounded-full border-2 border-white shadow" />
              <img src="https://randomuser.me/api/portraits/men/32.jpg" class="w-10 h-10 rounded-full border-2 border-white shadow" />
              <img src="https://randomuser.me/api/portraits/women/68.jpg" class="w-10 h-10 rounded-full border-2 border-white shadow" />
            </div>
            <div>
              <p class="text-sm font-semibold text-[#2d2016]">Trusted by 20,000+ customers</p>
              <div class="flex items-center gap-1 mt-0.5">
                <span class="text-amber-400 text-xs">★★★★★</span>
                <span class="text-xs text-[#a0907e]">Premium Shopping Experience</span>
              </div>
            </div>
          </div>
        </div>
 
        <!-- RIGHT IMAGE -->
        <div class="relative hidden lg:block">
          <div class="absolute inset-0 rounded-[2.5rem] bg-gradient-to-br from-[#c9a882]/20 to-transparent -m-4 blur-sm"></div>
          <img
            src="https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=1200&q=80"
            class="relative rounded-[2.5rem] shadow-2xl h-[620px] object-cover w-full"
          />
 
          <!-- Floating product card -->
          <div class="absolute top-10 -left-10 bg-white rounded-2xl shadow-xl p-4 border border-[#ede8e2] flex items-center gap-3 max-w-[200px]">
            <img
              src="https://images.unsplash.com/photo-1523275335684-37898b6baf30?q=80&w=200"
              class="w-14 h-14 rounded-xl object-cover shrink-0"
            />
            <div>
              <p class="text-xs font-bold text-[#2d2016]">Premium Watch</p>
              <p class="text-[#8d6040] font-bold text-sm mt-0.5">$159</p>
              <div class="flex gap-0.5 mt-1">
                <span class="text-amber-400 text-[10px]">★★★★★</span>
              </div>
            </div>
          </div>
 
          <!-- Floating stat card -->
          <div class="absolute bottom-10 -right-6 bg-white rounded-2xl shadow-xl p-4 border border-[#ede8e2] text-center min-w-[120px]">
            <p class="text-2xl font-extrabold text-[#7c5a3e]">50K+</p>
            <p class="text-xs text-[#a0907e] mt-0.5">Happy Customers</p>
          </div>
        </div>
      </div>
    </section>
 
    <!-- ===== CATEGORIES ===== -->
    <section class="py-20 bg-white">
      <div class="max-w-7xl mx-auto px-6">
        <div class="text-center max-w-xl mx-auto mb-12">
          <span class="text-xs uppercase tracking-[5px] text-[#8d6040] font-semibold">Browse Categories</span>
          <h2 class="text-3xl md:text-4xl font-bold text-[#2d2016] mt-3">Shop by Category</h2>
          <p class="text-[#a0907e] mt-3 text-sm leading-relaxed">
            Discover curated collections from trusted categories designed for premium shopping.
          </p>
        </div>
 
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
          <CategoryCard
            v-for="c in categories"
            :key="c.id"
            :id="c.id"
            :name="c.name"
            @select="selectCategory(c)"
          />
        </div>
      </div>
    </section>
 
    <!-- ===== FEATURED PRODUCTS ===== -->
    <section class="py-20 bg-[#f5f0eb]">
      <div class="max-w-7xl mx-auto px-6">
 
        <!-- Header -->
        <div class="flex flex-col md:flex-row md:items-end md:justify-between gap-3 mb-10">
          <div>
            <span class="text-xs uppercase tracking-[4px] text-[#8d6040] font-semibold">Premium Collection</span>
            <h2 class="text-3xl md:text-4xl font-bold text-[#2d2016] mt-2 leading-tight">Our Top Picks</h2>
          </div>
          <router-link
            to="/products"
            class="inline-flex items-center gap-2 border border-[#c9a882] text-[#7c5a3e] px-5 py-2.5 rounded-xl text-sm font-semibold hover:bg-[#f0ebe4] transition-all self-start md:self-auto whitespace-nowrap"
          >
            View All Products
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
          </router-link>
        </div>
 
        <!-- Bento Grid -->
        <div class="grid grid-cols-2 lg:grid-cols-3 gap-4 md:gap-5">
 
          <!-- LARGE FEATURED CARD -->
          <router-link
            to="/products"
            class="group col-span-2 lg:col-span-1 lg:row-span-2 relative rounded-2xl overflow-hidden shadow-md hover:shadow-2xl transition-all duration-400 hover:-translate-y-1 min-h-[280px] lg:min-h-[500px]"
          >
            <img :src="products[0]?.image" :alt="products[0]?.name" class="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition duration-600"/>
            <div class="absolute inset-0 bg-gradient-to-t from-[#1a0f07]/90 via-[#1a0f07]/30 to-transparent"></div>
            <div class="absolute inset-x-0 bottom-0 p-6">
              <span class="inline-block text-[10px] uppercase tracking-widest font-semibold text-white/60 bg-white/10 border border-white/15 px-2.5 py-1 rounded-full mb-2">✦ Featured</span>
              <h3 class="text-xl font-bold text-white leading-snug">{{ products[0]?.name }}</h3>
              <div class="flex items-center justify-between mt-3">
                <div>
                  <p class="text-white font-extrabold text-2xl">$199</p>
                  <span class="text-amber-300 text-xs">★★★★★</span>
                </div>
                <span class="bg-white text-[#7c5a3e] text-xs font-bold px-4 py-2 rounded-xl shadow-lg group-hover:bg-[#f0ebe4] transition-colors">Shop Now →</span>
              </div>
            </div>
          </router-link>
 
          <!-- SMALL CARDS -->
          <router-link
            to="/products"
            v-for="item in products.slice(1)"
            :key="item.id"
            class="group relative bg-white rounded-2xl overflow-hidden border border-[#ede8e2] shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300"
          >
            <div class="relative overflow-hidden bg-[#f5f0ea] h-40 md:h-52">
              <img :src="item.image" :alt="item.name" class="w-full h-full object-cover group-hover:scale-105 transition duration-500"/>
              <div class="absolute inset-0 bg-gradient-to-t from-black/30 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              <div class="absolute bottom-3 left-1/2 -translate-x-1/2 opacity-0 group-hover:opacity-100 translate-y-2 group-hover:translate-y-0 transition-all duration-300 whitespace-nowrap">
                <span class="bg-white text-[#7c5a3e] text-[11px] font-bold px-4 py-1.5 rounded-full shadow-lg">View Product →</span>
              </div>
              <button class="absolute top-3 right-3 w-8 h-8 rounded-full bg-white/90 border border-[#ede8e2] flex items-center justify-center shadow-sm hover:scale-110 transition-transform" @click.prevent>
                <svg class="w-4 h-4 text-[#8d6040]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 016.364 0L12 7.636l1.318-1.318a4.5 4.5 0 116.364 6.364L12 20.364 4.318 12.682a4.5 4.5 0 010-6.364z"/>
                </svg>
              </button>
            </div>
            <div class="p-4">
              <span class="text-[10px] uppercase tracking-widest font-semibold text-[#a0907e] bg-[#f5f0ea] px-2 py-0.5 rounded-md">Premium</span>
              <h3 class="text-sm font-semibold text-[#2d2016] group-hover:text-[#7c5a3e] transition mt-1.5 line-clamp-1">{{ item.name }}</h3>
              <div class="flex items-center justify-between mt-2">
                <p class="font-extrabold text-[#7c5a3e]">$199</p>
                <span class="text-amber-400 text-xs">★★★★★</span>
              </div>
            </div>
          </router-link>
 
        </div>
      </div>
    </section>
 
 
    <!-- ===== SALE BANNER ===== -->
    <section class="py-16 bg-white">
      <div class="max-w-7xl mx-auto px-5 lg:px-8">
        <div class="relative overflow-hidden rounded-3xl h-[520px] group shadow-2xl">
          <!-- BG Image -->
          <img
            src="https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=1200&q=80"
            alt="Sale"
            class="absolute inset-0 w-full h-full object-cover scale-100 group-hover:scale-105 transition duration-[4000ms]"
          />
          <!-- Overlay -->
          <div class="absolute inset-0 bg-gradient-to-r from-[#1a0f07]/90 via-[#3d2712]/70 to-transparent"></div>
          <!-- Gold glow -->
          <div class="absolute top-[-80px] right-[-80px] w-[350px] h-[350px] rounded-full bg-[#c9a882]/20 blur-[90px]"></div>
 
          <!-- Content -->
          <div class="relative z-10 flex items-center h-full px-8 md:px-16 lg:px-20 py-16">
            <div class="max-w-xl space-y-6">
              <span class="inline-flex items-center px-4 py-1.5 rounded-full border border-white/20 bg-white/10 backdrop-blur-xl text-[11px] uppercase tracking-[0.25em] text-[#d7c1ab] font-semibold">
                ⚡ Limited Time Offer
              </span>
 
              <h2 class="text-white text-4xl md:text-5xl font-extrabold leading-tight">
                Special Discount
                <span class="block text-[#d7c1ab] mt-1">Up To 50% Off</span>
              </h2>
 
              <p class="text-gray-300 text-sm leading-relaxed max-w-md">
                Discover premium fashion, luxury accessories, and modern collections crafted for your lifestyle.
              </p>
 
              <div class="flex flex-wrap gap-4 pt-2">
                <router-link
                  to="/products"
                  class="inline-flex items-center gap-2 bg-[#c9a882] hover:bg-[#b8916a] text-[#1a0f07] px-7 py-3 rounded-xl font-bold text-sm transition-all shadow-lg"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                    <path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/>
                    <path d="M16 10a4 4 0 01-8 0"/>
                  </svg>
                  Shop The Sale
                </router-link>
                <router-link
                  to="/products"
                  class="inline-flex items-center gap-2 border border-white/25 bg-white/10 backdrop-blur-lg px-7 py-3 text-white rounded-xl font-semibold text-sm hover:bg-white/20 transition"
                >
                  Explore Collection
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                </router-link>
              </div>
 
              <!-- Stats -->
              <div class="flex flex-wrap gap-8 pt-4 border-t border-white/10">
                <div>
                  <h3 class="text-2xl font-bold text-white">50K+</h3>
                  <p class="text-gray-400 text-xs mt-0.5">Happy Customers</p>
                </div>
                <div>
                  <h3 class="text-2xl font-bold text-white">1K+</h3>
                  <p class="text-gray-400 text-xs mt-0.5">Premium Products</p>
                </div>
                <div>
                  <h3 class="text-2xl font-bold text-white">24/7</h3>
                  <p class="text-gray-400 text-xs mt-0.5">Customer Support</p>
                </div>
              </div>
            </div>
          </div>
 
          <!-- Discount card -->
          <div class="hidden lg:flex absolute right-12 top-1/2 -translate-y-1/2 flex-col items-center justify-center rounded-3xl bg-white/10 backdrop-blur-2xl border border-white/15 p-8 shadow-2xl min-w-[160px]">
            <p class="text-6xl font-extrabold text-white leading-none">50%</p>
            <p class="text-[#d7c1ab] font-bold text-sm mt-2 tracking-widest uppercase">Off This Week</p>
            <div class="mt-4 w-full h-px bg-white/20"></div>
            <p class="text-white/60 text-xs mt-3 text-center">Ends soon. Don't miss it.</p>
          </div>
        </div>
      </div>
    </section>
 
    <!-- ===== SELLER CTA ===== -->
    <section v-if="!auth.user?.is_seller" class="py-20 bg-[#f5f0eb]">
      <div class="max-w-5xl mx-auto px-6">
        <div class="relative overflow-hidden rounded-3xl bg-gradient-to-br from-[#3d2712] via-[#7c5a3e] to-[#b8916a] px-8 lg:px-16 py-16 text-center shadow-2xl">
          <!-- Decorative circles -->
          <div class="absolute top-[-60px] left-[-60px] w-[200px] h-[200px] rounded-full border border-white/10"></div>
          <div class="absolute bottom-[-40px] right-[-40px] w-[150px] h-[150px] rounded-full border border-white/10"></div>
          <div class="absolute top-8 right-16 w-3 h-3 rounded-full bg-white/20"></div>
          <div class="absolute bottom-12 left-20 w-2 h-2 rounded-full bg-white/15"></div>
 
          <div class="relative space-y-6">
            <span class="inline-block px-4 py-1.5 rounded-full bg-white/15 border border-white/20 text-white/80 text-xs font-semibold uppercase tracking-widest">
              Marketplace Partner
            </span>
 
            <h2 class="text-3xl md:text-5xl font-extrabold text-white leading-tight">
              Start Selling on
              <span class="text-[#f0d9c0]"> ShopSmart</span>
            </h2>
 
            <p class="text-white/65 text-sm md:text-base max-w-xl mx-auto leading-relaxed">
              Build your brand, reach more customers, and grow your business with a modern commerce experience designed for ambitious sellers.
            </p>
 
            <!-- Feature pills -->
            <div class="flex flex-wrap justify-center gap-3 pt-2">
              <span class="flex items-center gap-1.5 text-xs text-white/75 bg-white/10 border border-white/15 px-4 py-2 rounded-full">
                <svg class="w-3.5 h-3.5 text-[#f0d9c0]" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>
                Zero listing fees
              </span>
              <span class="flex items-center gap-1.5 text-xs text-white/75 bg-white/10 border border-white/15 px-4 py-2 rounded-full">
                <svg class="w-3.5 h-3.5 text-[#f0d9c0]" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>
                Instant dashboard access
              </span>
              <span class="flex items-center gap-1.5 text-xs text-white/75 bg-white/10 border border-white/15 px-4 py-2 rounded-full">
                <svg class="w-3.5 h-3.5 text-[#f0d9c0]" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>
                20,000+ buyers waiting
              </span>
            </div>
 
            <div class="pt-2">
              <router-link
                to="/register"
                class="inline-flex items-center gap-2 bg-white text-[#7c5a3e] px-8 py-3.5 rounded-xl font-bold text-sm hover:bg-[#f0ebe4] transition-all shadow-xl"
              >
                Create Seller Account
                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </section>

   
  </div>
</template>

<script setup>
import CategoryCard from "../components/productPages/CategoryCard.vue";
import ReviewCard from "../components/productPages/ReviewCard.vue";
import { useAuthStore } from "../store/authStore";
import { storeToRefs } from "pinia";
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { getCategories } from "../services/product";

const router = useRouter();
const auth = useAuthStore();
const { user } = storeToRefs(auth);

const categories = ref([]);

const products = [
  {
    id: 1,
    name: "Luxury Chair",
    image: "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85",
  },
  {
    id: 2,
    name: "Premium Sneakers",
    image: "https://images.unsplash.com/photo-1542291026-7eec264c27ff",
  },
  {
    id: 3,
    name: "Luxury Watch",
    image: "https://images.unsplash.com/photo-1523170335258-f5ed11844a49",
  },
  {
    id: 4,
    name: "Modern Fashion",
    image: "https://images.unsplash.com/photo-1496747611176-843222e1e57c",
  },
];

const reviews = [
  { id: 1, user: "Ali", text: "Great quality products." },
  { id: 2, user: "Sara", text: "Fast delivery and trusted sellers." },
  { id: 3, user: "John", text: "Very easy to use marketplace." },
];

const loadCategories = async () => {
  try {
    const res = await getCategories();
    categories.value = res.filter((c) => c.parent === null);
  } catch (err) {
    console.error(err);
  }
};

const selectCategory = (category) => {
  if (!category?.id) return;
  router.push({ path: "/products", query: { category: Number(category.id) } });
};

onMounted(() => {
  loadCategories();
});
</script>
