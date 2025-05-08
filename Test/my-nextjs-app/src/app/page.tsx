
import { useEffect } from 'react';

export default function Home() {

  useEffect(() => {
    
    const fetchNotionData = async () => {
      try {
        const response = await fetch('/api/notion');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        console.log(data);
      } catch (error) {
        console.error('Error fetching data from Notion:', error);
      }
    };

    fetchNotionData();

  }, [])
  
  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
    Hi there
    </div>
  );
}
