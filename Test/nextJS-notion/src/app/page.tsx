'use client'
import { useEffect, useState } from 'react';
import { fetchNotionData } from '@/lib/notionIntegration';
import BlogPostCard from '@/components/BlogPostCard';

export default function Home() {
  const [posts, setPosts] = useState<any[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      const data = await fetchNotionData();
      setPosts(data);
    };
    fetchData();
    console.log("Completed !! Check Description for Github Link");
  }, []);

  return (
    <div className="flex flex-col items-center min-h-screen p-8 gap-8 bg-gray-50">
      <h1 className="text-3xl font-bold mb-8">Blog Posts</h1>
      {posts.length === 0 ? (
        <p>Loading...</p>
      ) : (
        posts
          .filter((post) => post.properties.Status.select?.name === 'Published')
          .map((post) => <BlogPostCard key={post.id} post={post} />)
      )}
    </div>
  );
}
