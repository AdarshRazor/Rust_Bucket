Here are the documents you requested.

### **Project Requirements Document (PRD_File)**

---

**1. Introduction**

This document outlines the requirements for a "Full-Stack E-Commerce Application." The project's primary goal is to demonstrate proficiency in full-stack development by building a functional, secure, and performant mini e-commerce platform. The application will feature a Node.js (Express) back end with an MVC architecture and a Next.js front end, integrating both SQL and MongoDB databases to handle different aspects of the e-commerce flow.

**2. Project Goal**

To build a proof-of-concept e-commerce website that allows users to register, browse products, manage a shopping cart, place orders, and view key sales reports. The project emphasizes clean code, a well-organized MVC structure, efficient database usage, and modern front-end practices like Server-Side Rendering (SSR).

**3. Core Features & Functional Requirements**

**3.1. User Account Management**
*   **User Registration:** New users must be able to create an account. Passwords must be securely hashed before being stored in the database.
*   **User Login:** Registered users must be able to log in to access their accounts and protected features. The system will use JWT or sessions for authentication.
*   **Order History:** Logged-in users can view a list of their past orders.

**3.2. Product Catalog**
*   **Product Listing:** All available products shall be displayed on a single page. This page will use Server-Side Rendering (SSR) for SEO and performance benefits.
*   **Product Detail Page:** Users can click on a product to view its dedicated details page using dynamic routing.
*   **Search & Filtering:** The product list can be searched by name or category using a MongoDB aggregation or text/regex query.
*   **Pagination:** If the number of products is large, the product listing page will implement pagination to ensure efficient data loading.

**3.3. Shopping Cart & Checkout**
*   **Add to Cart:** Logged-in users can add products to their personal shopping cart.
*   **Cart Management:** Users can view the items in their cart and potentially remove them.
*   **Checkout Process:** Users can proceed to a checkout page to place an order. Upon successful checkout, an order record is created in the SQL database, linking the user to the purchased products.
*   **Cart Clearing:** The shopping cart is automatically cleared after a successful checkout.

**3.4. Reporting**
*   **Data Aggregation:** The application will feature advanced queries to generate insightful reports.
    *   **SQL Report:** Generate a report for daily revenue over the last 7 days or list the top spending users.
    *   **MongoDB Report:** Generate a report summarizing product sales by category.
*   **Reports Page:** A dedicated "Reports" page on the front end will fetch and display this data from a secure `/reports` API endpoint.

**4. Technical & Non-Functional Requirements**

*   **Back End:**
    *   **Framework:** Node.js with Express.
    *   **Architecture:** Must follow the Model-View-Controller (MVC) pattern.
    *   **Database (SQL):** PostgreSQL or MySQL for `users`, `orders`, and `order_items` tables.
    *   **Database (MongoDB):** For the `products` collection and optionally for `carts` or `categories`.
*   **Front End:**
    *   **Framework:** Next.js.
    *   **Language:** TypeScript (using `.tsx` files).
    *   **Rendering:** Server-Side Rendering (SSR) is required for the main product listing page.
*   **Security:**
    *   Passwords must be hashed using a strong algorithm (e.g., bcrypt).
    *   API routes that modify data (cart, orders) must be protected and require user authentication.
    *   User inputs must be validated to prevent SQL injection and other vulnerabilities.
*   **Performance:**
    *   Use indexes on frequently queried fields in MongoDB to ensure query efficiency.
    *   Implement pagination for product lists to manage data load.
    *   Avoid N+1 query problems in SQL.

**5. Testing & Deployment**

*   **Testing:** The project must include at least one unit or integration test for a critical feature, such as the checkout process or user authentication.
*   **Deployment:** The application must be deployed to a public hosting service (e.g., Vercel, Netlify, Heroku) with the GitHub repository linked for continuous deployment.
*   **Documentation:** A `README.md` file must be provided with clear instructions for installation, database setup, and running the application.

---

### **Project TODO List**

### **Phase 1: Project Setup & Backend Foundation**
This initial phase focuses on setting up the development environment, version control, and the foundational structure for the back-end application.

| Task ID | Task Description | Status | Priority | Dependency |
| :--- | :--- | :--- | :--- | :--- |
| 1.1 | Initialize public GitHub repository: `FullStackExam<yourname><date>` | Not Started | High | - |
| 1.2 | Set up Node.js + Express project with TypeScript support | Not Started | High | 1.1 |
| 1.3 | Create MVC folder structure (`/controllers`, `/models`, `/routes`) | Not Started | High | 1.2 |
| 1.4 | Set up PostgreSQL/MySQL database and get connection credentials | Not Started | High | - |
| 1.5 | Set up MongoDB database and get connection credentials | Not Started | High | - |
| 1.6 | Implement database connection logic for both SQL and MongoDB | Not Started | High | 1.4, 1.5 |
| 1.7 | Set up environment variables (`.env`) for secrets and configuration | Not Started | High | 1.6 |

---

### **Phase 2: Backend - Models & Authentication**
This phase involves defining the data structures and implementing the core user authentication system.

| Task ID | Task Description | Status | Priority | Dependency |
| :--- | :--- | :--- | :--- | :--- |
| 2.1 | Define and create SQL schema: `users`, `orders`, `order_items` | Not Started | High | 1.4 |
| 2.2 | Create SQL models: `User.js`, `Order.js`, `OrderItem.js` | Not Started | High | 2.1 |
| 2.3 | Create MongoDB model: `Product.js` | Not Started | High | 1.5 |
| 2.4 | Implement user registration logic with bcrypt password hashing | Not Started | High | 2.2 |
| 2.5 | Implement user login logic and JWT/session generation | Not Started | High | 2.4 |
| 2.6 | Create `AuthController.ts` and `authRoutes.ts` | Not Started | High | 2.5 |
| 2.7 | Create authentication middleware to protect routes | Not Started | High | 2.5 |

---

### **Phase 3: Backend - Feature Implementation**
In this phase, all core e-commerce API endpoints for products, cart, orders, and reports will be built.

| Task ID | Task Description | Status | Priority | Dependency |
| :--- | :--- | :--- | :--- | :--- |
| 3.1 | Create `ProductController.ts` for product CRUD operations | Not Started | High | 2.3 |
| 3.2 | Implement search/filter logic in `ProductController` (MongoDB aggregation) | Not Started | Medium | 3.1 |
| 3.3 | Implement pagination for product listing endpoint | Not Started | Medium | 3.1 |
| 3.4 | Create `productRoutes.ts` and wire to controller | Not Started | High | 3.1 |
| 3.5 | Create `CartController.ts` for adding/removing items | Not Started | High | 2.7, 3.1 |
| 3.6 | Create `cartRoutes.ts` and protect with auth middleware | Not Started | High | 3.5 |
| 3.7 | Create `OrderController.ts` for checkout and order history | Not Started | High | 2.2, 3.5 |
| 3.8 | Implement checkout logic (create order in SQL, clear cart) | Not Started | High | 3.7 |
| 3.9 | Create `orderRoutes.ts` and protect with auth middleware | Not Started | High | 3.8 |
| 3.10 | Implement advanced SQL query for report (e.g., daily revenue) | Not Started | Medium | 2.2 |
| 3.11 | Implement MongoDB aggregation for report (e.g., sales by category) | Not Started | Medium | 2.3 |
| 3.12 | Create `ReportController.ts` and `reportRoutes.ts` | Not Started | Medium | 3.10, 3.11|

---

### **Phase 4: Frontend - Setup & Core Pages**
This phase covers the setup of the Next.js front end and the creation of the primary, non-interactive pages.

| Task ID | Task Description | Status | Priority | Dependency |
| :--- | :--- | :--- | :--- | :--- |
| 4.1 | Initialize Next.js project with TypeScript | Not Started | High | - |
| 4.2 | Set up basic UI components (Navbar, Footer, ProductCard) | Not Started | High | 4.1 |
| 4.3 | Create Product Listing Page (`/pages/index.tsx`) | Not Started | High | 4.2 |
| 4.4 | Implement SSR (`getServerSideProps`) to fetch products | Not Started | High | 3.4, 4.3 |
| 4.5 | Create dynamic Product Detail Page (`/pages/products/[id].tsx`) | Not Started | High | 4.2 |
| 4.6 | Fetch single product data for the detail page | Not Started | High | 3.4, 4.5 |

---

### **Phase 5: Frontend - Feature Integration**
Here, the front end is connected to the back-end APIs to create a fully interactive user experience.

| Task ID | Task Description | Status | Priority | Dependency |
| :--- | :--- | :--- | :--- | :--- |
| 5.1 | Create pages and forms for User Registration and Login | Not Started | High | 2.6 |
| 5.2 | Implement state management for authentication (e.g., Context API) | Not Started | High | 5.1 |
| 5.3 | Connect "Add to Cart" button to the cart API endpoint | Not Started | High | 3.6, 4.6 |
| 5.4 | Create Cart Page to display items and total | Not Started | High | 5.3 |
| 5.5 | Implement Checkout Flow, calling the order creation endpoint | Not Started | High | 3.9, 5.4 |
| 5.6 | Create Order History page to display user's past orders | Not Started | Medium | 3.9 |
| 5.7 | Create Reports page to fetch and display data from reports API | Not Started | Medium | 3.12 |

---

### **Phase 6: Testing & Documentation**
This crucial phase ensures the application is reliable and easy to understand for other developers.

| Task ID | Task Description | Status | Priority | Dependency |
| :--- | :--- | :--- | :--- | :--- |
| 6.1 | Write one integration test for the checkout process | Not Started | High | 5.5 |
| 6.2 | Perform manual end-to-end testing of all features | Not Started | High | 5.7 |
| 6.3 | Write `README.md` with all required instructions | Not Started | High | 6.2 |

---

### **Phase 7: Deployment**
The final phase involves making the application publicly accessible and ensuring it runs correctly in a production environment.

| Task ID | Task Description | Status | Priority | Dependency |
| :--- | :--- | :--- | :--- | :--- |
| 7.1 | Deploy Node.js back end (e.g., Heroku, AWS) | Not Started | High | 6.3 |
| 7.2 | Deploy Next.js front end (e.g., Vercel, Netlify) | Not Started | High | 6.3 |
| 7.3 | Configure production environment variables | Not Started | High | 7.1, 7.2 |
| 7.4 | Link GitHub repo for continuous deployment | Not Started | High | 7.1, 7.2 |
| 7.5 | Test the final deployed application | Not Started | High | 7.3 |