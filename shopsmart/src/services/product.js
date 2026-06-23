// services/sellerProductApi.js

import api from "./api";

const handleError = (error, message) => {
  console.error(message, error);

  const normalized = {
    detail:
      error?.response?.data?.detail ||
      error?.response?.data?.message ||
      message,
  };

  return Promise.reject(normalized);
};

// Get seller products
export const getSellerProducts = async () => {
  try {
    const res = await api.get("seller/products/");
    return res.data;
  } catch (error) {
   return handleError(error, "Unable to fetch seller products.");
  }
};

// =========================
// Create product
// =========================

export const createProduct = async (data) => {
  try {
    const res = await api.post("seller/products/", data);
    return res.data;
  } catch (error) {
    console.log("FULL BACKEND ERROR:", error.response?.data);
    return handleError(error, "Unable to create product.");
  }
};

// =========================
// Update product
// =========================

export const updateProduct = async (slug, data) => {
  try {
    const res = await api.patch(`seller/products/${slug}/`, data);

    return res.data;
  } catch (error) {
   return handleError(error, "Unable to update product.");
  }
};

// =========================
// Delete product
// =========================
export const deleteProduct = async (slug) => {
  try {
    const res = await api.delete(`seller/products/${slug}/`);

    return res.data;
  } catch (error) {
   return handleError(error, "Unable to delete product.");
  }
};

export const getCategories = async () => {
  try {
    const res = await api.get("categories/");
    return res.data;
  } catch (error) {
   return handleError(error, "Unable to fetch categories.");
  }
};

export const getCategoryProducts = async (id, params = {}) => {
  const res = await api.get(`/categories/${id}/products/`, { params });

  return res.data;
};

// =========================
// Get all public products
// =========================
export const getProducts = async (params = {}) => {
  if (!params || typeof params !== "object" || Array.isArray(params)) {
    params = {};
  }

  const res = await api.get("products/", { params });

  return res.data;
};

// =========================
// Get single product
// =========================
export const getProduct = async (slug) => {
  try {
    const res = await api.get(`products/${slug}/`);

    return res.data;
  } catch (error) {
   return handleError(error, "Unable to fetch product.");
  }
};

// =========================
// cart
// =========================

export const getCart = async () => {
  try {
    const res = await api.get("cart/");
    return res.data;
  } catch (error) {
   return handleError(error, "Unable to fetch cart.");
  }
};

export const addCartItem = async (data) => {
  try {
    const res = await api.post("cart/items/", data);
    return res.data;
  } catch (error) {
    return handleError(error, "Unable to add item to cart.");
}
};

export const deleteCartItem = async (id) => {
  try {
    const res = await api.delete(`cart/items/${id}/`);
    return res.data;
  } catch (error) {
   return handleError(error, "Unable to remove cart item.");
  }
};

export const updateCartItem = async (id, data) => {
  try {
    const res = await api.patch(`cart/items/${id}/`, data);
    return res.data;
  } catch (error) {
   return handleError(error, "Unable to update cart item.");
  }
};

// =========================
// checkout
// =========================

export const checkout = async (payloads, idempotencyKey) => {
  const res = await api.post("checkout/", payloads, {
    headers: {
      "Idempotency-Key": idempotencyKey,
    },
  });
  return res.data;
};

export const getaddresses = async () => {
  const res = await api.get("addresses/");
  return res.data;
};

export const createAddress = async (payload) => {
  const res = await api.post("addresses/", payload);
  return res.data;
};

export const getSellerOrders = async () => {
  const res = await api.get("seller/orders/");

  return res.data;
};

export const deleteAddress = async (id) => {
  try {
    const res = await api.delete(`addresses/${id}/`);
    return res.data;
  } catch (error) {
    return handleError(error, "Unable to delete address.");
  }
};

export const shipOrder = async (id, tracking_code) => {
  const res = await api.post(`seller/orders/${id}/ship/`, {
    tracking_code,
  });

  return res.data;
};

export const deliverOrder = async (id) => {
  const res = await api.post(`seller/orders/${id}/deliver/`);

  return res.data;
};

// =========================
// WALLET
// =========================

export const getWallet = async () => {
  try {
    const res = await api.get("wallet/");
    return res.data;
  } catch (error) {
    return handleError(error, "Unable to fetch wallet.");
  }
};

// =========================
// TRANSACTIONS
// =========================

export const getTransactions = async () => {
  try {
    const res = await api.get("wallet/transactions/");
    return res.data;
  } catch (error) {
    return handleError(error, "Unable to fetch transactions.");
  }
};

// =========================
// BANK ACCOUNTS
// =========================

export const getBankAccounts = async () => {
  try {
    const res = await api.get("bank-accounts/");
    return res.data;
  } catch (error) {
    return handleError(error, "Unable to fetch bank accounts.");
  }
};

export const createBankAccount = async (payload) => {
  try {
    const res = await api.post("bank-accounts/", payload);
    return res.data;
  } catch (error) {
    return handleError(error, "Unable to create bank account.");
  }
};

// =========================
// WITHDRAWALS
// =========================

export const getWithdrawals = async () => {
  try {
    const res = await api.get("withdrawals/");
    return res.data;
  } catch (error) {
    return handleError(error, "Unable to fetch withdrawals.");
  }
};

export const createWithdrawal = async (payload) => {
  try {
    const res = await api.post("withdrawals/", payload);
    return res.data;
  } catch (error) {
    return handleError(error, "Unable to create withdrawal.");
  }
};

// =========================
// NOTIFICATIONS
// =========================

export const getNotifications = async () => {
  try {
    const res = await api.get("notifications/");

    return res.data;
  } catch (error) {
    return handleError(error, "Unable to fetch notifications.");
  }
};



// ======================================================
// GET PRODUCT REVIEWS
// ======================================================

export const getProductReviews = async (productId) => {
  try {
    const res = await api.get(`reviews/?product=${productId}`);

    return res.data;
  } catch (error) {
    return handleError(error, "Unable to fetch reviews.");
  }
};

// ======================================================
// CREATE REVIEW
// ======================================================

export const createReview = async (payload) => {
  try {
    const res = await api.post("reviews/", payload);

    return res.data;
  } catch (error) {
   return handleError(error, "Unable to create review.");
  }
};

// ======================================================
// UPDATE REVIEW
// ======================================================

export const updateReview = async (id, payload) => {
  try {
    const res = await api.put(`reviews/${id}/`, payload);

    return res.data;
  } catch (error) {
    return handleError(error, "Unable to update review.");
  }
};

// ======================================================
// DELETE REVIEW
// ======================================================

export const deleteReview = async (id) => {
  try {
    const res = await api.delete(`reviews/${id}/`);

    return res.data;
  } catch (error) {
    return handleError(error, "Unable to delete review.");
  }
};
