import React from 'react';
import { Card, CardContent } from './ui/card';

interface PropertyCardProps {
  title: string;
  price: string;
  location: string;
  imageUrl?: string;
}

export const PropertyCard: React.FC<PropertyCardProps> = ({ title, price, location, imageUrl }) => {
  return (
    <Card className="mb-4">
      <CardContent className="p-4">
        {imageUrl && (
          <img src={imageUrl} alt={title} className="w-full h-48 object-cover rounded-md mb-2" />
        )}
        <h3 className="text-lg font-semibold mb-1">{title}</h3>
        <div className="text-blue-600 font-bold mb-1">{price}</div>
        <div className="text-gray-500 text-sm">{location}</div>
      </CardContent>
    </Card>
  );
}; 