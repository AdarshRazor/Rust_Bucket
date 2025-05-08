export interface NotionDatabase {
  Title: string;
  HeaderImage: string;
  Content: string;
  Tags: string[];
  Date: string; // ISO 8601 format
  Status: string;
}