import Link from 'next/link';

interface ProductCardProps {
  id: string;
  name: string;
  price: number;
  imageUrl: string;
}

export default function ProductCard({ id, name, price, imageUrl }: ProductCardProps) {
  return (
    <div className="border rounded-lg p-4 flex flex-col items-center shadow hover:shadow-lg transition">
      <img src={imageUrl} alt={name} className="w-32 h-32 object-cover mb-2 rounded" />
      <h3 className="font-semibold text-lg mb-1">{name}</h3>
      <p className="text-primary font-bold mb-2">${price.toFixed(2)}</p>
      <Link href={`/pages/products/${id}`} className="text-blue-600 hover:underline">View Details</Link>
    </div>
  );
}
