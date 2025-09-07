/**
 * TypeScript type definitions for Agent Mira Frontend
 * Centralized type definitions for better type safety
 * Location: client/src/lib/types.ts
 */

// User preference types
export interface UserPreferences {
  session_id: string;
  budget: number;
  location?: string;
  min_bedrooms?: number;
  max_commute_time?: number;
  min_school_rating?: number;
  preferred_amenities?: string[];
}

// Property types
export interface Property {
  id: number;
  title: string;
  price: number;
  location: string;
  bedrooms: number;
  bathrooms: number;
  size_sqft: number;
  year_built?: number;
  amenities: string[];
  image_urls: string[];
  school_rating?: number;
  commute_time?: number;
  created_at?: string;
  updated_at?: string;
}

// Recommendation scoring types
export interface ComponentScores {
  price_match: number;
  bedroom: number;
  school_rating: number;
  commute: number;
  property_age: number;
  amenities: number;
}

export interface Recommendation {
  property: Property;
  total_score: number;
  component_scores: ComponentScores;
  reasoning: string;
}

// API response types
export interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
}

// Form validation types
export interface FormErrors {
  [key: string]: string | undefined;
}

// UI state types
export interface LoadingState {
  isLoading: boolean;
  message?: string;
}

export interface ErrorState {
  hasError: boolean;
  message?: string;
  details?: string;
}

// Component prop types
export interface PropertyCardProps {
  property: Property;
  showActions?: boolean;
  onViewDetails?: (property: Property) => void;
  onAddToFavorites?: (property: Property) => void;
}

export interface RecommendationCardProps {
  recommendation: Recommendation;
  rank: number;
  onViewDetails?: (property: Property) => void;
  onAddToFavorites?: (property: Property) => void;
}

export interface PreferenceFormProps {
  onSubmit: (preferences: UserPreferences) => void;
  loading?: boolean;
  initialValues?: Partial<UserPreferences>;
}

// Filter types
export interface PropertyFilters {
  location?: string;
  min_bedrooms?: number;
  max_price?: number;
  min_school_rating?: number;
  max_commute_time?: number;
  amenities?: string[];
}

// Search and pagination types
export interface SearchParams {
  query?: string;
  filters?: PropertyFilters;
  page?: number;
  limit?: number;
  sort_by?: 'price' | 'score' | 'bedrooms' | 'size';
  sort_order?: 'asc' | 'desc';
}

// Analytics and tracking types
export interface UserInteraction {
  type: 'view' | 'click' | 'search' | 'recommendation_view';
  property_id?: number;
  recommendation_id?: number;
  timestamp: number;
  session_id: string;
}

// Theme and styling types
export type Theme = 'light' | 'dark' | 'system';

export interface ThemeConfig {
  theme: Theme;
  primaryColor: string;
  secondaryColor: string;
}

// Notification types
export interface Notification {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  title: string;
  message: string;
  duration?: number;
  action?: {
    label: string;
    onClick: () => void;
  };
}

// Modal and dialog types
export interface ModalState {
  isOpen: boolean;
  type?: 'property_details' | 'preferences' | 'filters' | 'comparison';
  data?: any;
}

// Local storage types
export interface StoredData {
  preferences?: UserPreferences;
  favorites?: number[];
  recent_searches?: string[];
  theme?: Theme;
}

// Error boundary types
export interface ErrorBoundaryState {
  hasError: boolean;
  error?: Error;
  errorInfo?: any;
}

// Loading skeleton types
export interface SkeletonProps {
  width?: string | number;
  height?: string | number;
  className?: string;
  variant?: 'text' | 'rectangular' | 'circular';
}

// Chart and visualization types (for future analytics)
export interface ScoreBreakdown {
  category: string;
  score: number;
  weight: number;
  color: string;
}

export interface RecommendationAnalytics {
  total_recommendations: number;
  average_score: number;
  score_distribution: ScoreBreakdown[];
  top_amenities: { amenity: string; count: number }[];
  location_distribution: { location: string; count: number }[];
}
