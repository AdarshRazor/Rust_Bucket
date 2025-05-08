import { NextResponse } from 'next/server';
import { Client } from '@notionhq/client';

const notion = new Client({ auth: process.env.NEXT_PUBLIC_NOTION_API });

export async function GET() {
  try {
    const databaseId = '1ed444a8256d8090a385e21cee71ede5';
    const response = await notion.databases.query({
      database_id: databaseId,
    });
    
    return NextResponse.json(response.results);
  } catch (error) {
    console.error('Error fetching data from Notion:', error);
    return NextResponse.json({ error: 'Failed to fetch data' }, { status: 500 });
  }
} 