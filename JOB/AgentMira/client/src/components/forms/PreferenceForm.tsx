/**
 * Preference Form Component for Agent Mira Frontend
 * Handles user preference input with validation
 * Location: client/src/components/forms/PreferenceForm.tsx
 */

"use client";

import { useState } from "react";
import { UserPreferences, FormErrors } from "@/lib/types";
import { formatCurrency } from "@/lib/utils";

interface PreferenceFormProps {
  onSubmit: (preferences: UserPreferences) => void;
  loading?: boolean;
  initialValues?: Partial<UserPreferences>;
}

const AMENITY_OPTIONS = [
  "Gym",
  "Swimming Pool",
  "Parking",
  "Security",
  "Balcony",
  "Private Garden",
  "Smart Home",
  "Garage",
  "Rooftop Terrace",
  "Private Elevator",
  "24/7 Concierge",
  "Fitness Center",
  "BBQ Area",
  "Community Pool",
  "Pet Friendly",
  "Home Office",
  "Solar Panels",
  "Two-Car Garage",
  "Minimalist Design",
  "Smart Appliances",
  "Energy Efficient",
  "Beach Access",
  "Park View",
  "Private Dock",
  "Boat Parking",
  "Backyard",
  "Laundry",
  "Smart Security"
];

export function PreferenceForm({ onSubmit, loading = false, initialValues }: PreferenceFormProps) {
  // Form state
  const [formData, setFormData] = useState<Partial<UserPreferences>>({
    budget: 500000,
    min_bedrooms: 2,
    max_commute_time: 30,
    min_school_rating: 7.0,
    preferred_amenities: [],
    ...initialValues,
  });

  const [errors, setErrors] = useState<FormErrors>({});
  const [touched, setTouched] = useState<Record<string, boolean>>({});

  // Handle input changes
  const handleInputChange = (field: keyof UserPreferences, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: undefined }));
    }
  };

  // Handle amenity selection
  const handleAmenityToggle = (amenity: string) => {
    const currentAmenities = formData.preferred_amenities || [];
    const newAmenities = currentAmenities.includes(amenity)
      ? currentAmenities.filter(a => a !== amenity)
      : [...currentAmenities, amenity];
    
    handleInputChange('preferred_amenities', newAmenities);
  };

  // Validate form
  const validateForm = (): boolean => {
    const newErrors: FormErrors = {};

    // Required fields
    if (!formData.budget || formData.budget <= 0) {
      newErrors.budget = "Budget is required and must be greater than 0";
    }

    if (!formData.min_bedrooms || formData.min_bedrooms < 1) {
      newErrors.min_bedrooms = "Minimum bedrooms must be at least 1";
    }

    if (formData.max_commute_time !== undefined && formData.max_commute_time < 0) {
      newErrors.max_commute_time = "Commute time cannot be negative";
    }

    if (formData.min_school_rating !== undefined && (formData.min_school_rating < 0 || formData.min_school_rating > 10)) {
      newErrors.min_school_rating = "School rating must be between 0 and 10";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Handle form submission
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (validateForm()) {
      onSubmit(formData as UserPreferences);
    }
  };

  // Handle field blur for validation
  const handleBlur = (field: keyof UserPreferences) => {
    setTouched(prev => ({ ...prev, [field]: true }));
    validateForm();
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Budget Input */}
      <div>
        <label htmlFor="budget" className="block text-sm font-medium text-gray-700 mb-2">
          Budget *
        </label>
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <span className="text-gray-500 sm:text-sm">$</span>
          </div>
          <input
            type="number"
            id="budget"
            value={formData.budget || ''}
            onChange={(e) => handleInputChange('budget', parseInt(e.target.value) || 0)}
            onBlur={() => handleBlur('budget')}
            className={`block w-full pl-7 pr-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm ${
              errors.budget ? 'border-red-300' : 'border-gray-300'
            }`}
            placeholder="500000"
            min="0"
            step="1000"
          />
        </div>
        {errors.budget && (
          <p className="mt-1 text-sm text-red-600">{errors.budget}</p>
        )}
        <p className="mt-1 text-sm text-gray-500">
          {formData.budget ? formatCurrency(formData.budget) : 'Enter your maximum budget'}
        </p>
      </div>

      {/* Location Input */}
      <div>
        <label htmlFor="location" className="block text-sm font-medium text-gray-700 mb-2">
          Preferred Location
        </label>
        <input
          type="text"
          id="location"
          value={formData.location || ''}
          onChange={(e) => handleInputChange('location', e.target.value)}
          onBlur={() => handleBlur('location')}
          className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          placeholder="e.g., New York, NY"
        />
        <p className="mt-1 text-sm text-gray-500">
          City, state, or specific area you're interested in
        </p>
      </div>

      {/* Bedrooms and Commute Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Minimum Bedrooms */}
        <div>
          <label htmlFor="min_bedrooms" className="block text-sm font-medium text-gray-700 mb-2">
            Minimum Bedrooms *
          </label>
          <select
            id="min_bedrooms"
            value={formData.min_bedrooms || 1}
            onChange={(e) => handleInputChange('min_bedrooms', parseInt(e.target.value))}
            onBlur={() => handleBlur('min_bedrooms')}
            className={`block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm ${
              errors.min_bedrooms ? 'border-red-300' : 'border-gray-300'
            }`}
          >
            {[1, 2, 3, 4, 5, 6].map(num => (
              <option key={num} value={num}>
                {num} {num === 1 ? 'bedroom' : 'bedrooms'}
              </option>
            ))}
          </select>
          {errors.min_bedrooms && (
            <p className="mt-1 text-sm text-red-600">{errors.min_bedrooms}</p>
          )}
        </div>

        {/* Max Commute Time */}
        <div>
          <label htmlFor="max_commute_time" className="block text-sm font-medium text-gray-700 mb-2">
            Max Commute Time (minutes)
          </label>
          <select
            id="max_commute_time"
            value={formData.max_commute_time || ''}
            onChange={(e) => handleInputChange('max_commute_time', parseInt(e.target.value) || undefined)}
            onBlur={() => handleBlur('max_commute_time')}
            className={`block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm ${
              errors.max_commute_time ? 'border-red-300' : 'border-gray-300'
            }`}
          >
            <option value="">No preference</option>
            <option value="15">15 minutes</option>
            <option value="30">30 minutes</option>
            <option value="45">45 minutes</option>
            <option value="60">60 minutes</option>
            <option value="90">90+ minutes</option>
          </select>
          {errors.max_commute_time && (
            <p className="mt-1 text-sm text-red-600">{errors.max_commute_time}</p>
          )}
        </div>
      </div>

      {/* School Rating */}
      <div>
        <label htmlFor="min_school_rating" className="block text-sm font-medium text-gray-700 mb-2">
          Minimum School Rating (0-10)
        </label>
        <div className="flex items-center space-x-4">
          <input
            type="range"
            id="min_school_rating"
            min="0"
            max="10"
            step="0.1"
            value={formData.min_school_rating || 0}
            onChange={(e) => handleInputChange('min_school_rating', parseFloat(e.target.value))}
            onBlur={() => handleBlur('min_school_rating')}
            className="flex-1 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
          />
          <span className="text-sm font-medium text-gray-700 min-w-[3rem]">
            {formData.min_school_rating?.toFixed(1) || '0.0'}
          </span>
        </div>
        {errors.min_school_rating && (
          <p className="mt-1 text-sm text-red-600">{errors.min_school_rating}</p>
        )}
        <p className="mt-1 text-sm text-gray-500">
          Minimum school district rating you're comfortable with
        </p>
      </div>

      {/* Preferred Amenities */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Preferred Amenities
        </label>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-2 max-h-48 overflow-y-auto border border-gray-300 rounded-md p-3">
          {AMENITY_OPTIONS.map(amenity => (
            <label key={amenity} className="flex items-center space-x-2 cursor-pointer">
              <input
                type="checkbox"
                checked={formData.preferred_amenities?.includes(amenity) || false}
                onChange={() => handleAmenityToggle(amenity)}
                className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
              />
              <span className="text-sm text-gray-700">{amenity}</span>
            </label>
          ))}
        </div>
        <p className="mt-1 text-sm text-gray-500">
          Select amenities that are important to you
        </p>
      </div>

      {/* Submit Button */}
      <div className="pt-4">
        <button
          type="submit"
          disabled={loading}
          className="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? (
            <div className="flex items-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Finding Recommendations...
            </div>
          ) : (
            'Get My Recommendations'
          )}
        </button>
      </div>
    </form>
  );
}
