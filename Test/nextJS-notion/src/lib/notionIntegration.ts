/**
 * Fetch data from the Notion database through our API route
 * @returns {Promise<any>} The data from the Notion database
 */
export async function fetchNotionData(): Promise<any> {
  try {
    const response = await fetch('/api/notion');
    if (!response.ok) {
      throw new Error('Failed to fetch data');
    }
    return response.json();
  } catch (error) {
    console.error('Error fetching data from Notion:', error);
    throw error;
  }
}