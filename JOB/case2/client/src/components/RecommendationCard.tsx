import React from 'react';

type Props = {
  property: any;
  predictedPrice: number;
  reasoning: string[];
};

export default function RecommendationCard({ property, predictedPrice, reasoning }: Props) {
  return (
    <div className="border rounded shadow p-4 flex flex-col gap-2 bg-white max-w-sm">
      <img src={property.image_url || '/placeholder.png'} alt={property.title} className="w-full h-40 object-cover rounded" />
      <h2 className="font-bold text-lg">{property.title}</h2>
      <div className="flex gap-2 text-sm">
        <span>Price: <b>${property.price.toLocaleString()}</b></span>
        <span>Predicted: <b>${predictedPrice.toLocaleString()}</b></span>
      </div>
      <div className="text-sm text-gray-600">{property.location}</div>
      <div className="flex gap-2 text-xs">
        <span>{property.bedrooms} bd</span>
        <span>{property.bathrooms} ba</span>
        <span>{property.size_sqft} sqft</span>
      </div>
      <ul className="mt-2 text-xs bg-gray-50 rounded p-2">
        {reasoning.map((line, i) => (
          <li key={i} dangerouslySetInnerHTML={{ __html: line }} />
        ))}
      </ul>
    </div>
  );
} 