export interface User {
  id: number;
  email: string;
  full_name: string;
  role_id: number;
  role?: Role;
  is_active: boolean;
  is_verified: boolean;
  avatar_url?: string;
  phone?: string;
}

export interface Role {
  id: number;
  name: string;
  description?: string;
}

export interface Book {
  id: number;
  title: string;
  author: string;
  genre: string;
  year: number;
  description?: string;
  cover_image_url?: string;
  owner_id: number;
  status: BookStatus;
  average_rating: number;
  google_books_id?: string;
  created_at: string;
  updated_at: string;
}

export type BookStatus = 'available' | 'reserved' | 'taken' | 'archived';

export interface Reservation {
  id: number;
  book_id: number;
  book?: Book;
  user_id: number;
  exchange_point_id: number;
  exchange_point?: ExchangePoint;
  reservation_date: string;
  pickup_date: string;
  return_date: string;
  actual_return_date?: string;
  status: ReservationStatus;
  created_at: string;
  updated_at: string;
}

export type ReservationStatus = 'reserved' | 'picked_up' | 'returned' | 'cancelled';

export interface ExchangePoint {
  id: number;
  name: string;
  address: string;
  working_hours: string;
  description?: string;
  contact_person?: string;
  phone?: string;
}

export interface Review {
  id: number;
  book_id: number;
  user_id: number;
  rating: number;
  comment?: string;
  created_at: string;
}

export interface Token {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: User;
}

export interface Statistics {
  platform: {
    total_books: number;
    available_books: number;
    total_reservations: number;
    active_reservations: number;
  };
  user: {
    my_books: number;
    my_reservations: number;
  };
}

export interface BookListResponse {
  items: Book[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}

export interface ReservationListResponse {
  items: Reservation[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}
