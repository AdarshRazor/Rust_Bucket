import Navbar from '../../components/Navbar';
import Footer from '../../components/Footer';
import ProductCard from '../../components/ProductCard';

interface Product {
  id: string;
  name: string;
  price: number;
  imageUrl: string;
}

async function fetchProducts() {
  const res = await fetch('http://localhost:3001/api/products'); // Adjust port if needed
  if (!res.ok) throw new Error('Failed to fetch products');
  const data = await res.json();
  return data.products as Product[];
}

export default async function ProductsPage() {
  const products = await fetchProducts();
  return (
    <div>
      <Navbar />
      <main className="max-w-5xl mx-auto py-8 px-4 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8">
        {products.map((product) => (
          <ProductCard key={product.id} {...product} />
        ))}
      </main>
      <Footer />
    </div>
  );
}
