/**
 * API Integration Layer for Agent Mira Frontend
 * Handles all communication with the backend API
 * Location: client/src/lib/api.ts
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Types for API requests and responses
export interface UserPreferences {
  session_id: string;
  budget: number;
  location?: string;
  min_bedrooms?: number;
  max_commute_time?: number;
  min_school_rating?: number;
  preferred_amenities?: string[];
}

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

export interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
}

// API Client Class
class ApiClient {
  private baseURL: string;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    try {
      const url = `${this.baseURL}${endpoint}`;
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        return {
          error: errorData.detail || `HTTP ${response.status}: ${response.statusText}`,
        };
      }

      const data = await response.json();
      return { data };
    } catch (error) {
      return {
        error: error instanceof Error ? error.message : 'Network error occurred',
      };
    }
  }

  // Health check
  async healthCheck(): Promise<ApiResponse<{ status: string; service: string; ml_service: boolean }>> {
    return this.request('/health');
  }

  // Submit user preferences
  async submitPreferences(preferences: UserPreferences): Promise<ApiResponse<{ message: string; preference_id: number; session_id: string }>> {
    return this.request('/api/preferences', {
      method: 'POST',
      body: JSON.stringify(preferences),
    });
  }

  // Get property recommendations
  async getRecommendations(sessionId: string, topN: number = 3): Promise<ApiResponse<Recommendation[]>> {
    return this.request(`/api/recommendations?session_id=${sessionId}&top_n=${topN}`);
  }

  // Get all properties with optional filtering
  async getProperties(filters?: {
    skip?: number;
    limit?: number;
    location?: string;
    min_bedrooms?: number;
    max_price?: number;
  }): Promise<ApiResponse<Property[]>> {
    const params = new URLSearchParams();
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined) {
          params.append(key, value.toString());
        }
      });
    }
    
    const queryString = params.toString();
    const endpoint = queryString ? `/api/properties?${queryString}` : '/api/properties';
    return this.request(endpoint);
  }

  // Get specific property details
  async getProperty(propertyId: number): Promise<ApiResponse<Property>> {
    return this.request(`/api/properties/${propertyId}`);
  }

  // Predict property price using ML model
  async predictPrice(features: {
    bedrooms: number;
    bathrooms: number;
    size_sqft: number;
    year_built?: number;
    location: string;
    amenities: string[];
  }): Promise<ApiResponse<{ predicted_price: number; features: any }>> {
    return this.request('/api/ml/predict-price', {
      method: 'POST',
      body: JSON.stringify(features),
    });
  }

  // Get ML model information
  async getModelInfo(): Promise<ApiResponse<{ status: string; model_type?: string; features?: string[] }>> {
    return this.request('/api/ml/model-info');
  }
}

// Export singleton instance
export const apiClient = new ApiClient();

// Utility functions for common operations
export const generateSessionId = (): string => {
  return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
};

export const formatCurrency = (amount: number): string => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
};

export const formatNumber = (num: number): string => {
  return new Intl.NumberFormat('en-US').format(num);
};
