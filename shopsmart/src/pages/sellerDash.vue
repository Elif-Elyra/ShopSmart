<template>
  <div class="min-h-screen bg-gray-100 p-6">
    <div class="max-w-6xl mx-auto space-y-6">
      <DashboardHeader @add="openAdd" />

      <!-- Loading -->
      <div v-if="loading" class="flex justify-center items-center py-20">
        <span
          class="animate-spin h-10 w-10 border-[6px] border-[#967255] border-t-transparent rounded-full"
        ></span>
      </div>

      <!-- Error -->
      <div v-if="error" class="bg-red-100 text-red-600 px-4 py-3 rounded-lg">
        {{ error }}
      </div>

      <!-- Products -->
      <ProductGrid
        v-if="!loading && Array.isArray(products) && products.length"
        :products="products"
        @edit="editHandler"
        @delete="handleDelete"
      />

      <!-- Empty -->
      <EmptyState v-if="!loading && !products.length" />
    </div>

    <!-- Modal -->
    <ProductModal
      :show="showModal"
      :form="form"
      :editing="editing"
      :categories="categories"
      @update-field="updateField"
      @save="saveProduct"
      @update:show="showModal = $event"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

import DashboardHeader from "../components/dashboard/DashboardHeader.vue";
import ProductGrid from "../components/dashboard/ProductGrid.vue";
import ProductModal from "../components/dashboard/SellerProductModel.vue";
import EmptyState from "../components/dashboard/EmptyState.vue";

import {
  getCategories,
  getSellerProducts,
  createProduct,
  updateProduct,
  deleteProduct,
} from "../services/product";

// STATE
const products = ref([]);
const categories = ref([]);

const loading = ref(false);
const saving = ref(false);

const error = ref("");

const showModal = ref(false);
const editing = ref(false);

// FORM
const getEmptyForm = () => ({
  id: null,
  title: "",
  slug: "",
  sku: "",
  category: "",
  price: 0,
  stock: 0,
  description: "",
  thumbnail: null,
  images: [],
});
const updateField = ({ key, value }) => {
  form.value[key] = value;
};
const form = ref(getEmptyForm());

// FETCH
const fetchDashboardData = async () => {
  try {
    loading.value = true;
    error.value = "";

    const [productsData, categoriesData] = await Promise.all([
      getSellerProducts(),
      getCategories(),
    ]);

    products.value = productsData;                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
    console.log(productsData)
    categories.value = categoriesData;
  } catch (err) {
    error.value = err.detail || "Failed to load dashboard.";
  } finally {
    loading.value = false;
  }
};

// MODAL
const openAdd = () => {
  editing.value = false;
  form.value = getEmptyForm();
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

const editHandler = (product) => {
  editing.value = true;

  form.value = {
    id: product.id,
    title: product.title,
    slug: product.slug,
    sku: product.sku,
    category: product.category,
    price: product.price,
    stock: product.stock,
    description: product.description,
    thumbnail: null,
    images: [],
  };

  showModal.value = true;
};

// FILES
const handleThumbnail = (file) => {
  form.value.thumbnail = file;
};

const handleImages = (files) => {
  form.value.images = files;
};

// FORM DATA
const buildFormData = () => {
  const data = new FormData();

  data.append("title", form.value.title);
  data.append("slug", form.value.slug);
  data.append("sku", form.value.sku);
  data.append("category", form.value.category);
  data.append("price", form.value.price);
  data.append("stock", form.value.stock);
  data.append("description", form.value.description);

  if (form.value.thumbnail) {
    data.append("thumbnail", form.value.thumbnail);
  }

  const images = Array.from(form.value.images || []);

  for (const file of images) {
    data.append("images", file);
  }

  return data;
};

// SAVE
const saveProduct = async () => {
  try {
    saving.value = true;

    const data = buildFormData();

    if (editing.value) {
      await updateProduct(form.value.slug, data);
      console.log("slug", form.value.slug);
    } else {
      await createProduct(data);
    }

    await fetchDashboardData();

    closeModal();
  } catch (err) {
    error.value = err.detail || "Failed to save product.";
  } finally {
    saving.value = false;
  }
};

// DELETE
const handleDelete = async (slug) => {
  console.log("DELETE slug:", slug);
  const confirmed = confirm("Delete this product?");
  if (!confirmed) return;
  try {
    await deleteProduct(slug);
    products.value = products.value.filter((p) => p.slug !== slug);
  } catch (err) {
    error.value = err.detail || "Failed to delete product.";
  }
};

onMounted(fetchDashboardData);
</script>
