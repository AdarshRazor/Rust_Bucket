export default function Footer() {
  return (
    <footer className="w-full py-4 px-8 bg-gray-100 dark:bg-gray-900 text-center text-sm mt-8">
      <div>&copy; {new Date().getFullYear()} E-Commerce. All rights reserved.</div>
      <div className="mt-2">
        <a href="/about" className="mx-2 hover:underline">About</a>
        <a href="/contact" className="mx-2 hover:underline">Contact</a>
      </div>
    </footer>
  );
}
