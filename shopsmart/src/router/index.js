import { createRouter, createWebHistory } from "vue-router";
import Home from "../pages/Home.vue";
import Login from "../pages/Login.vue";
import Register from "../pages/Register.vue";
import Profile from "../pages/Profile.vue";
import Cart from "../pages/Cart.vue";
import ProductDetail from "../pages/ProductDetail.vue";
import Product from "../pages/AllProducts.vue";
import Dash from "../pages/sellerDash.vue";
import ForgotPassword from "../components/loginpages/ForgotPassword.vue";
import ResetPassword from "../components/loginpages/ResetPassword.vue";
import { useAuthStore } from "../store/authStore";
import Checkout from "../pages/Checkout.vue";
import AdminPanel from "../pages/AdminPanel.vue";

const routes = [
  { path: "/", name: "home", component: Home },

  {
    path: "/register",
    name: "register",
    component: Register,
    meta: { guestOnly: true },
  },

  {
    path: "/login",
    name: "login",
    component: Login,
    meta: { guestOnly: true },
  },

  {
    path: "/profile",
    name: "profile",
    component: Profile,
    meta: { requiresAuth: true },
  },

  { path: "/cart", name: "cart", component: Cart },

  { path: "/products/:slug", name: "product-detail", component: ProductDetail },

  { path: "/products", name: "products", component: Product },

  {
    path: "/seller/dashboard",
    name: "dashboard",
    component: Dash,
    meta: { requiresAuth: true, sellerOnly: true },
  },
  {
    path: "/forgot-password",
    name: "forgot-password",
    component: ForgotPassword
  },
  {
  path: "/reset-password",
  name: "reset-password",
  component: ResetPassword,
},
{
  path: "/admin-panel",
  name: "admin-panel",
  component: AdminPanel
},
{
  path: "/checkout",
  name: "checkout",
  component: Checkout
}
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to, from, next) => {
  const auth = useAuthStore();

  if (auth.access && !auth.user) {
    await auth.fetchUser();
  }

  if (to.meta.requiresAuth && !auth.access) {
    return next("/login");
  }

  if (to.meta.guestOnly && auth.access) {
    return next("/");
  }

  if (to.meta.sellerOnly && !auth.user?.is_seller) {
    return next("/");
  }

  next();
});
export default router;
