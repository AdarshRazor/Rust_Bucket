# Creating CMS using Notion and Strapi - USing NextJS 
## Project Overview
I want to create a NextJS app and use Notion as a CMS to manage my content. I just want to display some simple data. Below are the steps i am working on to achieve this.

## Steps

* [done] Create a new NextJS app (obvisously)

* [done] Create a new Notion app (obvisously)

* [done] Create a new Strapi app (obvisously) .. Hope you got that 

* [done] Install the dependencies [code is below]

* [done] Create a new Notion database 🔵
    * Title, Header Image, Content, Tags, Date, Status

* [done] Get the Notion database ID and API key 🔑 **[NEXT_PUBLIC_NOTION_API]**
    - can use `webHook` to pass or fetch the data from `3rd Party`
    
      steps:
      - get api key and database id from notion.
      - connect notion database to integration.

* [done] Implement it in the NextJS app 🔵

* [done] Create a page to display the data 🟠
  - [done] fetch the data from the Notion database 
  - [done] display the data in the page (in a better way)

* [done] Complete 🎉🙌

### Please do not use my API >_<

* [done] Add features to ease my work in streamlabs

> 💡 Use replit or firebase studio to quickly achieve the something result.

## Variables and Usefull stuffs

* **Database ID**: `1ed444a8256d8090a385e21cee71ede5`



## Code Snippets

    ```
    "dependencies": {
      "@notion-render/bookmark-plugin": "^0.0.2",
      "@notion-render/client": "^0.0.2",
      "@notion-render/hljs-plugin": "^0.0.2",
      "@notionhq/client": "^3.0.0",
      "next": "15.3.2",
      "react": "^19.0.0",
      "react-dom": "^19.0.0"
      },
    "devDependencies": {
        "@tailwindcss/postcss": "^4",
        "@types/node": "^20",
        "@types/react": "^19",
        "@types/react-dom": "^19",
        "tailwindcss": "^4",
        "typescript": "^5"
      }
    ```