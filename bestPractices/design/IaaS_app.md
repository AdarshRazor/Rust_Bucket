# IaaS App : Style Design

## 1. The Name of the Style: "The Linear Look" (or Neo-Technical)
This style, popularized by companies like **Linear, Vercel, and Supabase**, is the dominant aesthetic for dev-tools in 2026.
* **Vibe:** Professional, fast, "Pro-sumer," and technical.
* **Key Keywords:** Dark-mode first, high-contrast, border-radius focused, and keyboard-centric.

## 2. Layout: The "Bento Grid" & "DAG"
For an ETL app, you need two distinct layout patterns:
* **The Bento Grid:** For the main dashboard. It uses modular, rectangular blocks of varying sizes (like a Japanese lunchbox) to group stats like "Pipeline Health," "Rows Processed," and "Active Sources."
* **The DAG (Directed Acyclic Graph):** For the ETL builder itself. This is a node-based interface where users drag and drop "Extract" (Source), "Transform" (Logic), and "Load" (Destination) nodes connected by animated paths.
    * *Pro Tip:* Use **React Flow** or **XYFlow** for the implementation—it’s the industry standard for node-based UIs.

## 3. Texture & Finish: "Liquid Glass" (Glassmorphism 2.0)
We’ve moved past flat design. In 2026, we use **Liquid Glass**.
* **Texture:** Frosted, semi-transparent panels with a subtle **0.5px border** (often in a light gray like `#FFFFFF10`).
* **Depth:** Use "Z-axis layering." Modals shouldn't just pop up; they should look like they are hovering over the background with a soft "backdrop blur" (`blur(12px)`).
* **Grain:** A very subtle **film grain noise** on dark backgrounds adds a premium, tactile feel that prevents the UI from looking "sterile."

## 4. Positioning & Navigation
* **The Command Palette ($Cmd+K$):** This is non-negotiable. Modern users don't want to click through 5 menus. They want to hit $Cmd+K$ and type "Deploy Production Pipeline."
* **Left-Hand Sidebar:** Keep it slim. Icons only by default, expanding on hover, using a "collapsed" state to maximize data workspace.
* **Breadcrumbs:** Essential for ETL. Users need to see exactly where they are: `Pipelines > Marketing_Sync > Transformation_Script`.

## 5. Color Palette & Typography
Don't use pure black (`#000`). It looks "cheap" and causes eye strain.
* **Backgrounds:** Deep charcoals (`#0B0C0E` or `#121212`).
* **Accents:** Hyper-saturated neon colors used sparingly for status.
    * **Success:** Electric Emerald (`#00FF85`)
    * **Error:** Radiant Coral (`#FF4D4D`)
    * **Running:** Cyber Blue (`#1E90FF`)
* **Typography:** * **UI:** A clean, geometric sans-serif (e.g., **Geist** or **Inter**).
    * **Data/Code:** A monospace font (e.g., **JetBrains Mono**) for any raw data or logs to give it that "engineered" feel.

## 6. Best Practices for Stich
* **Status Indicators:** Use "Glow Effects." A running pipeline shouldn't just be a blue dot; it should have a subtle pulsing outer glow.
* **Micro-interactions:** When a user hovers over a data node, it should subtly scale up ($1.02\times$). 
* **Log Transparency:** Put the real-time logs in a bottom drawer. Engineers love seeing the "matrix" under the hood.
