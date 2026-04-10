import axios, { AxiosInstance, AxiosRequestConfig, AxiosError, InternalAxiosRequestConfig, AxiosResponse } from 'axios';

// Относительный URL - запросы идут через nginx proxy на /api/v1
const API_BASE = '/api/v1';

const api: AxiosInstance = axios.create({
  baseURL: API_BASE,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: false,
});

// Add token to requests
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error: AxiosError) => {
    console.error('API Error:', error.response?.data || error.message);

    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('refreshToken');
      window.location.reload();
    }
    return Promise.reject(error);
  }
);

// Auth API
export const register = (userData: { email: string; password: string; full_name: string; phone?: string }) =>
  api.post('/auth/register', userData);

export const login = (credentials: { email: string; password: string }) =>
  api.post('/auth/login', credentials);

export const refreshToken = (refreshToken: string) =>
  api.post('/auth/refresh', { refresh_token: refreshToken });

export const logout = (refreshToken: string) =>
  api.post('/auth/logout', { refresh_token: refreshToken });

export const getCurrentUser = () => api.get('/users/me');

// Books API
export const getBooks = (params?: {
  page?: number;
  page_size?: number;
  search?: string;
  genre?: string;
  book_status?: string;
  year?: number;
  owner_id?: number;
  order_by?: string;
}) => api.get('/books', { params });

export const createBook = (bookData: { title: string; author: string; genre: string; year: number; description?: string }) =>
  api.post('/books', bookData);

export const updateBook = (id: number, bookData: Partial<{ title: string; author: string; genre: string; year: number; status: string }>) =>
  api.put(`/books/${id}`, bookData);

export const deleteBook = (id: number) => api.delete(`/books/${id}`);

export const getMyBooks = (page?: number, page_size?: number) =>
  api.get('/books/my/list', { params: { page, page_size } });

export const getAvailableBooks = (page?: number, page_size?: number) =>
  api.get('/books/available/list', { params: { page, page_size } });

export const getTopRatedBooks = (limit?: number) =>
  api.get('/books/top/rated', { params: { limit } });

// Reservations API
export const getReservations = (page?: number, page_size?: number) =>
  api.get('/reservations', { params: { page, page_size } });

export const createReservation = (reservationData: { book_id: number; exchange_point_id: number }) =>
  api.post('/reservations', reservationData);

export const cancelReservation = (id: number) =>
  api.post(`/reservations/${id}/cancel`);

export const confirmPickup = (id: number) =>
  api.post(`/reservations/${id}/pickup`);

export const confirmReturn = (id: number) =>
  api.post(`/reservations/${id}/return`);

export const updateReservationStatus = (id: number, status: string) =>
  api.put(`/reservations/${id}/status`, null, { params: { status } });

export const getActiveReservations = () => api.get('/reservations/active/list');

// Exchange Points API
export const getExchangePoints = () => api.get('/exchange-points');

// Statistics API
export const getStatistics = () => api.get('/statistics');

export const getDetailedStatistics = () => api.get('/statistics/detailed');

// Reviews API
export const getBookReviews = (bookId: number) => api.get(`/reviews/book/${bookId}`);

export const createReview = (reviewData: { book_id: number; rating: number; comment?: string }) =>
  api.post('/reviews', reviewData);

export const deleteReview = (reviewId: number) => api.delete(`/reviews/${reviewId}`);

// Files API
export const uploadFile = (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post('/files/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

export const deleteFile = (id: number) => api.delete(`/files/${id}`);

export const downloadFile = (id: number) => api.get(`/files/download/${id}`);

export default api;
