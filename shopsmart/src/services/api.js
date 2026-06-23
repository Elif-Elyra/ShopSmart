import axios from "axios";

// Main API instance (with interceptor)
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
});

// Separate instance for refresh (NO interceptors)
const refreshApi = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
});

// Attach access token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

// Response interceptor for auto refresh
api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const originalRequest = error.config;

    if (
      error.response?.status !== 401 ||
      originalRequest._retry
    ) {
      return Promise.reject(error);
    }

    originalRequest._retry = true;

    const refresh = localStorage.getItem("refresh");

    if (!refresh) {
      localStorage.removeItem("access");
      localStorage.removeItem("refresh");
      return Promise.reject(error);
    }

    try {
      const { data } = await refreshApi.post("auth/token/refresh/", {
        refresh,
      });

      localStorage.setItem("access", data.access);

      originalRequest.headers.Authorization = `Bearer ${data.access}`;

      return api(originalRequest);
    } catch (err) {
      localStorage.removeItem("access");
      localStorage.removeItem("refresh");

      return Promise.reject(err);
    }
  }
);

export default api;