import React from 'react';
import Navbar from '../../../components/Navbar';
import Footer from '../../../components/Footer';
import { useRouter } from 'next/router';

interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  imageUrl: string;
  category: string;
  stock: number;
}

export default function ProductDetailPage() {
  const router = useRouter();
  const { id } = router.query;
  const [product, setProduct] = React.useState<Product | null>(null);
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    if (id) {
      fetch(`http://localhost:3001/api/products/${id}`)
        .then((res) => res.json())
        .then((data) => {
          setProduct(data);
          setLoading(false);
        });
    }
  }, [id]);

  if (loading) return <div>Loading...</div>;
  if (!product) return <div>Product not found.</div>;

  return (
    <div>
      <Navbar />
      <main className="max-w-2xl mx-auto py-8 px-4">
        <img src={product.imageUrl} alt={product.name} className="w-full h-64 object-cover rounded mb-4" />
        <h1 className="text-2xl font-bold mb-2">{product.name}</h1>
        <p className="text-lg mb-2">${product.price.toFixed(2)}</p>
        <p className="mb-2">Category: {product.category}</p>
        <p className="mb-2">Stock: {product.stock}</p>
        <p className="mb-4">{product.description}</p>
        <button className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Add to Cart</button>
      </main>
      <Footer />
    </div>
  );
}
