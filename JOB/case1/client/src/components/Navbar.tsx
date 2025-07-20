import Link from 'next/link';

export default function Navbar() {
  return (
    <nav className="w-full flex items-center justify-between py-4 px-8 bg-gray-100 dark:bg-gray-900 shadow">
      <div className="font-bold text-lg">
        <Link href="/">E-Commerce</Link>
      </div>
      <div className="flex gap-6">
        <Link href="/">Home</Link>
        <Link href="/pages/indedx">Products</Link>
        <Link href="/cart">Cart</Link>
        <Link href="/login">Login</Link>
        <Link href="/register">Register</Link>
      </div>
    </nav>
  );
}
