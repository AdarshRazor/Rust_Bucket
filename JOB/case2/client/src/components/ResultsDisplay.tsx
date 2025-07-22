import React from 'react';
import RecommendationCard from './RecommendationCard';

type Props = {
  recommendations: Array<{
    property: any;
    predicted_price: number;
    reasoning: string[];
  }>;
};

export default function ResultsDisplay({ recommendations }: Props) {
  if (!recommendations || recommendations.length === 0) {
    return <div className="text-gray-500">No recommendations yet.</div>;
  }
  return (
    <div className="flex flex-wrap gap-6 justify-center">
      {recommendations.map((rec, idx) => (
        <RecommendationCard
          key={rec.property.id || idx}
          property={rec.property}
          predictedPrice={rec.predicted_price}
          reasoning={rec.reasoning}
        />
      ))}
    </div>
  );
} 