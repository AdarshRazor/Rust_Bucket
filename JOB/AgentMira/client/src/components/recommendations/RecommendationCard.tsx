/**
 * Recommendation Card Component for Agent Mira Frontend
 * Displays individual property recommendation with scoring details
 * Location: client/src/components/recommendations/RecommendationCard.tsx
 */

"use client";

import { RecommendationCardProps } from "@/lib/types";
import { formatCurrency, formatNumber, getScoreColor, getScoreLabel } from "@/lib/utils";
import { ScoreBreakdown } from "./ScoreBreakdown";

export function RecommendationCard({ 
  recommendation, 
  rank, 
  onViewDetails, 
  onAddToFavorites 
}: RecommendationCardProps) {
  const { property, total_score, component_scores, reasoning } = recommendation;
  const scoreColor = getScoreColor(total_score);
  const scoreLabel = getScoreLabel(total_score);

  return (
    <div className="bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200">
      {/* Header with Rank and Score */}
      <div className="flex items-start justify-between p-6 pb-4">
        <div className="flex items-center space-x-4">
          {/* Rank Badge */}
          <div className="flex-shrink-0">
            <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
              rank === 1 ? 'bg-yellow-100 text-yellow-800' :
              rank === 2 ? 'bg-gray-100 text-gray-800' :
              rank === 3 ? 'bg-orange-100 text-orange-800' :
              'bg-blue-100 text-blue-800'
            }`}>
              {rank}
            </div>
          </div>

          {/* Property Title and Location */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-1">
              {property.title}
            </h3>
            <p className="text-sm text-gray-600 flex items-center">
              <svg className="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              {property.location}
            </p>
          </div>
        </div>

        {/* Score Display */}
        <div className="text-right">
          <div className={`text-2xl font-bold ${scoreColor}`}>
            {total_score.toFixed(1)}%
          </div>
          <div className="text-sm text-gray-600">{scoreLabel}</div>
        </div>
      </div>

      {/* Property Image */}
      {property.image_urls && property.image_urls.length > 0 && (
        <div className="px-6 pb-4">
          <div className="relative h-48 w-full rounded-lg overflow-hidden">
            <img
              src={property.image_urls[0]}
              alt={property.title}
              className="w-full h-full object-cover"
              onError={(e) => {
                // Fallback to placeholder if image fails to load
                e.currentTarget.src = `https://via.placeholder.com/400x300?text=${encodeURIComponent(property.title)}`;
              }}
            />
            <div className="absolute top-2 right-2">
              <button
                onClick={() => onAddToFavorites?.(property)}
                className="bg-white bg-opacity-90 hover:bg-opacity-100 rounded-full p-2 shadow-sm transition-all duration-200"
                title="Add to favorites"
              >
                <svg className="w-5 h-5 text-gray-600 hover:text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Property Details */}
      <div className="px-6 pb-4">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div>
            <span className="text-gray-600">Price:</span>
            <div className="font-semibold text-lg text-gray-900">
              {formatCurrency(property.price)}
            </div>
          </div>
          <div>
            <span className="text-gray-600">Bedrooms:</span>
            <div className="font-medium text-gray-900">
              {property.bedrooms} {property.bedrooms === 1 ? 'bedroom' : 'bedrooms'}
            </div>
          </div>
          <div>
            <span className="text-gray-600">Bathrooms:</span>
            <div className="font-medium text-gray-900">
              {property.bathrooms} {property.bathrooms === 1 ? 'bathroom' : 'bathrooms'}
            </div>
          </div>
          <div>
            <span className="text-gray-600">Size:</span>
            <div className="font-medium text-gray-900">
              {formatNumber(property.size_sqft)} sq ft
            </div>
          </div>
        </div>

        {/* Additional Details */}
        <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
          {property.year_built && (
            <div>
              <span className="text-gray-600">Year Built:</span>
              <span className="ml-1 font-medium text-gray-900">{property.year_built}</span>
            </div>
          )}
          {property.school_rating && (
            <div>
              <span className="text-gray-600">School Rating:</span>
              <span className="ml-1 font-medium text-gray-900">{property.school_rating}/10</span>
            </div>
          )}
          {property.commute_time && (
            <div>
              <span className="text-gray-600">Commute:</span>
              <span className="ml-1 font-medium text-gray-900">{property.commute_time} min</span>
            </div>
          )}
        </div>

        {/* Amenities */}
        {property.amenities && property.amenities.length > 0 && (
          <div className="mt-4">
            <span className="text-gray-600 text-sm">Amenities:</span>
            <div className="flex flex-wrap gap-1 mt-1">
              {property.amenities.slice(0, 6).map((amenity, index) => (
                <span
                  key={index}
                  className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800"
                >
                  {amenity}
                </span>
              ))}
              {property.amenities.length > 6 && (
                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-600">
                  +{property.amenities.length - 6} more
                </span>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Score Breakdown */}
      <div className="px-6 pb-4">
        <ScoreBreakdown scores={component_scores} />
      </div>

      {/* Reasoning */}
      <div className="px-6 pb-4">
        <h4 className="text-sm font-medium text-gray-900 mb-2">Why This Property?</h4>
        <p className="text-sm text-gray-700 bg-gray-50 rounded-lg p-3">
          {reasoning}
        </p>
      </div>

      {/* Actions */}
      <div className="px-6 py-4 bg-gray-50 rounded-b-lg flex justify-between items-center">
        <button
          onClick={() => onViewDetails?.(property)}
          className="text-indigo-600 hover:text-indigo-800 text-sm font-medium flex items-center"
        >
          <svg className="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
          </svg>
          View Details
        </button>
        
        <div className="flex items-center space-x-2">
          <button
            onClick={() => onAddToFavorites?.(property)}
            className="text-gray-600 hover:text-red-500 text-sm font-medium flex items-center"
          >
            <svg className="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
            Save
          </button>
          <button className="text-gray-600 hover:text-gray-800 text-sm font-medium flex items-center">
            <svg className="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z" />
            </svg>
            Share
          </button>
        </div>
      </div>
    </div>
  );
}
