# IHM Gurukul: Project Overview

**Title**: IHM Gurukul - Chef Community Learning & Hiring Platform

**Vision**:
> “A place for chefs to **learn**, **affiliate**, **get certified**, **get hired** or **hire others**. A **community for chefs, by the chefs**.”

---

## 🧩 **Core Modules & Features**

### 1. 🧠 Learning & Upskilling (Coursera-like)

> For chefs to take or offer courses and learn new skills.

**Features:**

* Free & Paid **Courses**, **eBooks**, **Webinars**, **Trainings**
* Certification upon completion
* Search and filter content by category (e.g. bakery, continental, vegan, etc.)
* Track user progress
* Allow course creators to upload content
* Integrated video platform (YouTube/Vimeo embed or native)
* Downloadable resources

**Focus:**

* Quality UX for course consumption
* Payment gateway for paid content
* Access control (paid vs free content)

---

### 2. 🧾 Resume Builder & Job Posting (LinkedIn-like for Chefs)

> Let chefs create profiles and employers post jobs.

**Features:**

* Create chef profile (photo, skills, experience, certifications, specialties)
* Resume builder (ATS-friendly exportable PDF)
* Job board: post & apply for jobs
* Search chefs based on skill/location
* Filters for part-time/full-time/internship
* Chat with candidates/employers

**Focus:**

* Seamless resume generation
* Modern job board UX
* Search/filter system

---

### 3. 👨‍👩‍👧‍👦 Affiliate & Certification Program

> Build community and offer recognition.

**Features:**

* 1-on-1 sessions / mentorship
* Community forums or groups (like Facebook groups)
* Affiliate programs for referrals
* Consultancy for restaurant opening
* Certification tracks with digital credentials (badges)

**Focus:**

* Gamified certifications
* Role-based access for mentors/consultants
* Forum integration

---

### 4. 🛒 E-commerce / Purchase System

> Allow users to purchase courses, books, memberships.

**Features:**

* Course & eBook sales
* Webinar tickets
* Membership plans (monthly/yearly)
* Wallet or credits system
* Invoice generation

**Focus:**

* Secure payments (Razorpay/Stripe)
* Easy purchase tracking per user
* Dashboard for orders/downloads

---

### 5. 🧑‍💼 Admin & CRM (Back Office)

> For team to manage content, users, and operations.

**Features:**

* Admin dashboard
* User management (ban/edit roles)
* Course/webinar/content management
* Job post approvals
* Reports & analytics (sales, user growth)

**Focus:**

* Role-based access (admin/instructor/employer/user)
* Intuitive UI to manage platform

---

### 6. 🤖 Smart Assistant (Optional, Phase 2)

> Provide support and guidance using automation.

**Features:**

* Basic chatbot for FAQ
* Guided resume builder with AI inputs
* Course recommendations

**Focus:**

* Low-code chatbot integration (Tidio, Crisp, or custom)
* Add intelligent suggestions later with GPT or fine-tuned models

---

## 🎯 Feature Priority (MVP to Full Launch)

| Priority          | Features                                                          |
| ----------------- | ----------------------------------------------------------------- |
| **High**          | User login & profile, Course selling, Resume builder, Job board   |
| **Medium**        | Certification system, Admin CRM, Membership plans                 |
| **Low (Phase 2)** | Chatbot, Community forum, AI resume assistant, Affiliate tracking |

---

## 🏗️ Tech / Plugin Stack Recommendation (WordPress-based)

To align with your current platform:

* **Learning (LMS)**: LearnDash or Tutor LMS
* **Job Portal**: WP Job Manager + Resume Builder plugin
* **Courses & eBook Store**: WooCommerce
* **Community & Membership**: BuddyBoss or Ultimate Member + Paid Memberships Pro
* **Chatbot**: Tidio or Landbot
* **Admin Panel**: Custom WP admin pages or CRM plugin
* **Certifications**: AutomatorWP + LearnDash Certificates

---

## 📌 Action Items for Restructuring

1. **Audit current site** — structure, content, users
2. **Set plugin base** — select LMS, job portal, membership
3. **Design user flows** — chef, recruiter, admin
4. **Migrate content** — courses, users, products
5. **Build MVP features** — learning, hiring, profiles
6. **Iterate and test** — feedback from real chefs
7. **Launch and scale** — add chatbots, AI resume, affiliate systems

---

## 🔚 Final Note

Think of this platform as a mix of:

* **LinkedIn** → for chef resumes & job connections
* **Coursera/Coding Ninja** → for chef training & upskilling
* **Udemy** → for selling chef content
* **Slack/FB Groups** → for community building


`slide deck format for client presentation`

Great call, Adarsh. Migrating away from WordPress to a **modular, scalable stack** will give you performance, flexibility, and maintainability — without forcing you to build every little thing from scratch.

---
<br/>

# ✅ **Revamped Project: Tech Stack Overview**

### 🌐 Frontend (Modern, Fast, Component-Driven)

* **Framework**: `Next.js` (App Router + Server Actions or traditional API routes)
* **Styling/UI**: Tailwind CSS + shadcn/ui
* **State Management**: Zustand (lightweight) or TanStack Query (for data fetching)
* **Forms**: React Hook Form + Zod (for validation)
* **Animation**: Framer Motion (optional for polish)

---

### 🔐 Authentication

* **Clerk** → Full-featured auth with:

  * OAuth
  * Email/Password
  * User profile management
  * Role-based access control

---

### 🧠 Backend Options

#### Option 1: **Supabase (Best for Speed, MVP, and Feature-Rich DB)**

* **Database**: PostgreSQL (via Supabase)
* **Auth**: Disabled, since Clerk is used
* **Storage**: Supabase Storage (for images, PDFs, resumes, eBooks)
* **Realtime**: Built-in (for chat/notifications)
* **Edge Functions** (for custom logic)
* **Row-Level Security (RLS)**

#### Option 2: **Node.js + Express (for full custom control)**

* **Database**: MongoDB or PostgreSQL
* **File Storage**: Cloudinary or AWS S3
* **Hosting**: Railway / Render / Fly.io / Vercel + DB

---

### 🛠️ Admin Dashboard

* **Open-source CRM options**:

  * [React Admin](https://marmelab.com/react-admin/)
  * \[Nhost Console]\(if using Nhost alternative to Supabase)
  * Or build your own using shadcn/ui + Clerk roles

---

## 🧩 Feature Modules with 3rd-Party / Open Source Tools

| Feature                       | Solution / Tool                                      | Notes                                                 |
| ----------------------------- | ---------------------------------------------------- | ----------------------------------------------------- |
| **User Auth & Profile**       | Clerk                                                | Fully integrated UI for profile, sessions, MFA, etc.  |
| **Course Platform (LMS)**     | [Graphy](https://in.graphy.com/) SDK or Custom Build | Or build: video player + progress tracker + chapters  |
| **Video Streaming / Hosting** | Mux / Vimeo / YouTube                                | Mux = best for professional video + progress tracking |
| **Payments**                  | Stripe / Razorpay                                    | Course purchase, eBooks, webinars, membership         |
| **Resume Builder (PDF)**      | react-pdf / puppeteer / html2pdf.js                  | Generate downloadable resume from user profile        |
| **Job Portal (Post & Apply)** | Custom DB Schema + TanStack Query                    | Use RLS if using Supabase                             |
| **Chat System (Basic)**       | Socket.io (Node) / Supabase Realtime                 | Internal chat for job discussions                     |
| **Forum / Community**         | Discourse Embed / Circle.so / Custom                 | Optional, can use existing community tools            |
| **Newsletter / Email**        | Resend / Mailchimp                                   | Email marketing, webinar notifications                |
| **Certification Engine**      | react-pdf + auto cert gen (PDF)                      | Auto-generate certificate after course completion     |
| **Admin Dashboard**           | React Admin / custom CMS with Clerk roles            | Manage users, courses, jobs, content                  |

---

## 🧠 Planning Notes (MVP First)

* ✅ Start with **course selling + job portal + resume builder**
* Then add:

  * Webinars
  * Certifications
  * Memberships
* Community/Chat/Forum can come in Phase 2

---

## 📦 All-in-One Toolkit (Bonus)

| Feature                | Tool                                                |
| ---------------------- | --------------------------------------------------- |
| Email Templates        | React Email + Resend                                |
| File Uploads           | UploadThing / Supabase Storage                      |
| Analytics              | Vercel Analytics / PostHog                          |
| CMS (for blogs/events) | Notion as CMS / Sanity / Contentlayer               |
| Error Monitoring       | Sentry                                              |
| Deployment             | Vercel (frontend), Supabase (backend), Clerk (auth) |

---