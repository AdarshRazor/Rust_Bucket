/**
 * Recommendation List Component for Agent Mira Frontend
 * Displays the list of property recommendations
 * Location: client/src/components/recommendations/RecommendationList.tsx
 */

"use client";

import { Recommendation } from "@/lib/types";
import { RecommendationCard } from "./RecommendationCard";

interface RecommendationListProps {
  recommendations: Recommendation[];
  onNewSearch?: () => void;
}

export function RecommendationList({ recommendations, onNewSearch }: RecommendationListProps) {
  if (recommendations.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">No recommendations available</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">
            Your Top {recommendations.length} Recommendations
          </h3>
          <p className="text-sm text-gray-600">
            Ranked by compatibility with your preferences
          </p>
        </div>
        {onNewSearch && (
          <button
            onClick={onNewSearch}
            className="text-sm text-indigo-600 hover:text-indigo-800 font-medium"
          >
            New Search
          </button>
        )}
      </div>

      {/* Recommendations */}
      <div className="space-y-4">
        {recommendations.map((recommendation, index) => (
          <RecommendationCard
            key={recommendation.property.id}
            recommendation={recommendation}
            rank={index + 1}
            onViewDetails={(property) => {
              // TODO: Implement property details modal/page
              console.log('View details for property:', property.id);
            }}
            onAddToFavorites={(property) => {
              // TODO: Implement favorites functionality
              console.log('Add to favorites:', property.id);
            }}
          />
        ))}
      </div>

      {/* Summary */}
      <div className="bg-gray-50 rounded-lg p-4 mt-6">
        <h4 className="text-sm font-medium text-gray-900 mb-2">Search Summary</h4>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div>
            <span className="text-gray-600">Properties Found:</span>
            <span className="ml-1 font-medium">{recommendations.length}</span>
          </div>
          <div>
            <span className="text-gray-600">Avg. Score:</span>
            <span className="ml-1 font-medium">
              {(recommendations.reduce((sum, rec) => sum + rec.total_score, 0) / recommendations.length).toFixed(1)}%
            </span>
          </div>
          <div>
            <span className="text-gray-600">Price Range:</span>
            <span className="ml-1 font-medium">
              ${Math.min(...recommendations.map(r => r.property.price)).toLocaleString()} - 
              ${Math.max(...recommendations.map(r => r.property.price)).toLocaleString()}
            </span>
          </div>
          <div>
            <span className="text-gray-600">Locations:</span>
            <span className="ml-1 font-medium">
              {new Set(recommendations.map(r => r.property.location)).size}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
