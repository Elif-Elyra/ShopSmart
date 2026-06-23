<template>
  <footer class="bg-[#f2f0ea] border-t border-black/7">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-10 pb-0">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 lg:gap-12 pb-8">

        <!-- Brand -->
        <div>
          <div class="flex items-center gap-2.5 mb-3">
            <div class="w-9 h-9 rounded-[10px] bg-[#b08b6d] flex items-center justify-center">
              <svg class="w-[18px] h-[18px] text-white" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/>
                <line x1="3" y1="6" x2="21" y2="6" stroke-linecap="round"/>
                <path stroke-linecap="round" stroke-linejoin="round" d="M16 10a4 4 0 01-8 0"/>
              </svg>
            </div>
            <span class="text-[18px] font-bold tracking-tight">
              <span class="text-[#2d2d2d]">Shop</span><span class="text-[#a5856f]">Smart</span>
            </span>
          </div>
          <p class="text-sm text-gray-400 leading-relaxed mb-4">
            Smart shopping platform for modern users.
          </p>
          <div class="flex gap-2">
            <a class="footer-social" aria-label="Instagram" href="#">
              <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 24 24"><rect x="2" y="2" width="20" height="20" rx="5" ry="5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M16 11.37A4 4 0 1112.63 8 4 4 0 0116 11.37z" fill="none" stroke="currentColor" stroke-width="2"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5" stroke="currentColor" stroke-width="2"/></svg>
            </a>
            <a class="footer-social" aria-label="Twitter" href="#">
              <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 24 24"><path d="M23 3a10.9 10.9 0 01-3.14 1.53 4.48 4.48 0 00-7.86 3v1A10.66 10.66 0 013 4s-4 9 5 13a11.64 11.64 0 01-7 2c9 5 20 0 20-11.5a4.5 4.5 0 00-.08-.83A7.72 7.72 0 0023 3z" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </a>
            <a class="footer-social" aria-label="Facebook" href="#">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M18 2h-3a5 5 0 00-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 011-1h3z"/></svg>
            </a>
          </div>
        </div>

        <!-- Quick Links -->
        <div>
          <h3 class="footer-col-title">Quick Links</h3>
          <ul class="space-y-1">
            <li><router-link to="/" class="footer-link">Home</router-link></li>
            <li><router-link to="/dash" class="footer-link">Products</router-link></li>
            <li><router-link to="/cart" class="footer-link">Cart</router-link></li>
          </ul>
        </div>

        <!-- Account -->
        <div>
          <h3 class="footer-col-title">Account</h3>
          <ul class="space-y-1">
            <li><router-link to="/login" class="footer-link">Login</router-link></li>
            <li><router-link to="/register" class="footer-link">Register</router-link></li>
            <li><router-link to="/profile" class="footer-link">Profile</router-link></li>
            <li><router-link to="/forgot-password" class="footer-link">Reset Password</router-link></li>
          </ul>
        </div>
      </div>
    </div>

    <div class="border-t border-black/7">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex flex-col sm:flex-row items-center justify-between gap-2">
        <p class="text-xs text-gray-400">© 2026 ShopSmart. All rights reserved.</p>
        <p class="text-xs text-gray-300 flex items-center gap-1.5">
          <svg class="w-3.5 h-3.5 text-[#c28f63]" fill="currentColor" viewBox="0 0 20 20"><path d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z"/></svg>
          Made for smart shoppers
        </p>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer-col-title {
  @apply text-[11px] font-bold text-gray-400 uppercase tracking-widest mb-3;
}
.footer-link {
  @apply flex items-center text-sm text-gray-500 hover:text-[#a5856f] transition duration-200 py-1;
}
.footer-social {
  @apply w-8 h-8 rounded-full bg-[#e8e4de] flex items-center justify-center text-gray-500
         hover:bg-[#b08b6d] hover:text-white transition duration-200 cursor-pointer;
}
</style>
