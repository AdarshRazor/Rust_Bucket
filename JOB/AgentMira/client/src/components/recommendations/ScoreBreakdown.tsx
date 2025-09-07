/**
 * Score Breakdown Component for Agent Mira Frontend
 * Displays detailed scoring breakdown for recommendations
 * Location: client/src/components/recommendations/ScoreBreakdown.tsx
 */

"use client";

import { ComponentScores } from "@/lib/types";
import { getScoreColor } from "@/lib/utils";

interface ScoreBreakdownProps {
  scores: ComponentScores;
}

const SCORE_CATEGORIES = [
  {
    key: 'price_match' as keyof ComponentScores,
    label: 'Price Match',
    weight: 30,
    description: 'How well the price fits your budget',
    icon: '💰'
  },
  {
    key: 'bedroom' as keyof ComponentScores,
    label: 'Bedrooms',
    weight: 20,
    description: 'Meets your bedroom requirements',
    icon: '🛏️'
  },
  {
    key: 'school_rating' as keyof ComponentScores,
    label: 'School District',
    weight: 15,
    description: 'Quality of local schools',
    icon: '🎓'
  },
  {
    key: 'commute' as keyof ComponentScores,
    label: 'Commute',
    weight: 15,
    description: 'Convenience to city center',
    icon: '🚗'
  },
  {
    key: 'property_age' as keyof ComponentScores,
    label: 'Property Age',
    weight: 10,
    description: 'Modern vs established construction',
    icon: '🏗️'
  },
  {
    key: 'amenities' as keyof ComponentScores,
    label: 'Amenities',
    weight: 10,
    description: 'Matches your preferred features',
    icon: '⭐'
  }
];

export function ScoreBreakdown({ scores }: ScoreBreakdownProps) {
  return (
    <div>
      <h4 className="text-sm font-medium text-gray-900 mb-3">Score Breakdown</h4>
      <div className="space-y-3">
        {SCORE_CATEGORIES.map((category) => {
          const score = scores[category.key];
          const scoreColor = getScoreColor(score);
          const weightColor = score >= 80 ? 'text-green-600' : score >= 60 ? 'text-yellow-600' : 'text-red-600';
          
          return (
            <div key={category.key} className="flex items-center justify-between">
              <div className="flex items-center space-x-3 flex-1">
                <span className="text-lg">{category.icon}</span>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-gray-700">
                      {category.label}
                    </span>
                    <div className="flex items-center space-x-2">
                      <span className={`text-sm font-semibold ${scoreColor}`}>
                        {score.toFixed(1)}%
                      </span>
                      <span className="text-xs text-gray-500">
                        ({category.weight}%)
                      </span>
                    </div>
                  </div>
                  
                  {/* Progress Bar */}
                  <div className="mt-1">
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full transition-all duration-300 ${
                          score >= 80 ? 'bg-green-500' :
                          score >= 60 ? 'bg-yellow-500' :
                          'bg-red-500'
                        }`}
                        style={{ width: `${Math.min(score, 100)}%` }}
                      />
                    </div>
                  </div>
                  
                  <p className="text-xs text-gray-500 mt-1">
                    {category.description}
                  </p>
                </div>
              </div>
            </div>
          );
        })}
      </div>
      
      {/* Legend */}
      <div className="mt-4 pt-3 border-t border-gray-200">
        <div className="flex items-center justify-between text-xs text-gray-500">
          <span>Score Legend:</span>
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-1">
              <div className="w-3 h-3 bg-green-500 rounded-full"></div>
              <span>80-100%</span>
            </div>
            <div className="flex items-center space-x-1">
              <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
              <span>60-79%</span>
            </div>
            <div className="flex items-center space-x-1">
              <div className="w-3 h-3 bg-red-500 rounded-full"></div>
              <span>0-59%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
