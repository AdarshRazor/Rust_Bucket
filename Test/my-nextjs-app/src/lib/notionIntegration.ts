import { Client } from '@notionhq/client';

// Initialize the Notion client
const notion = new Client({ auth: process.env.NEXT_PUBLIC_NOTION_API });

/**
 * Fetch data from the Notion database
 * @returns {Promise<any>} The data from the Notion database
 */
export async function fetchNotionData(): Promise<any> {
  try {
    const databaseId: string = '1ed444a8256d8090a385e21cee71ede5';
    const response = await notion.databases.query({
      database_id: databaseId,
    });
    return response.results;
  } catch (error) {
    console.error('Error fetching data from Notion:', error);
    throw error;
  }
}