import { defineStore } from "pinia";
import { getCart, addCartItem, deleteCartItem } from "../services/product";

//
// Cart Store - Manages shopping cart state and operations
//
export const useCartStore = defineStore("cart", {
  // state = data
  state: () => ({
    items: [],
    loading: false,
  }),

  // Getters - Data ko Filter/Format Karne Wale

  getters: {
    /** Total items count (for badge) */
    count: (state) => state.items.length,
    /** Check if cart is empty */
    isEmpty: (state) => state.items.length === 0,

    /** Total price calculation */
    totalPrice: (state) => {
      return state.items.reduce((sum, item) => {
        return sum + item.price * item.quantity;
      }, 0);
    },

    /** Alias for badge (optional) */
    cartCount: (state) => state.items.length,
  },

  //  action - Data ko Badalne Wale
  actions: {
    /** Load cart from backend */
    async fetchCart() {
      this.loading = true;

      try {
        const res = await getCart();

        const data = res ?? {};

        this.items = data.items || data.data?.items || [];
      } finally {
        this.loading = false;
      }
    },

    /** Add item to cart */
    // cartStore.js
    async addItem(productId, quantity = 1) {
      try {
        await addCartItem({ product: productId, quantity }); // ✅ API call

        const existing = this.items.find((item) => item.product === productId);
        if (existing) {
          existing.quantity += quantity;
        } else {
          // Optimistic update — sirf count ke liye kafi hai
          this.items.push({ product: productId, quantity });
        }
      } catch (error) {
        console.error("[Cart] addItem error:", error);
        throw error; // ✅ Error aage bhejo taake UI handle kar sake
      }
    },

    // cartStore.js — removeItem
    async removeItem(itemId) {
      try {
        await deleteCartItem(itemId);
        this.items = this.items.filter((item) => item.id !== itemId); // ✅ item.id se match
      } catch (error) {
        console.error("[Cart] removeItem error:", error);
        throw error;
      }
    },

    /** Clear cart */
    clearCart() {
      this.items = [];
    },
  },
});
