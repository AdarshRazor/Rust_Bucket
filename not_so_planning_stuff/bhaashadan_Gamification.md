Of course. It's great that you're looking to infuse gamification into the Bhashadaan platform. Your analysis of the current system's shortcomings is spot-on and aligns perfectly with the core principles of what makes games engaging. You've already done the hard part: diagnosing the problem.

Let's structure a plan to build these addictive gaming concepts into your platform. I'll act as your project management partner here, providing the necessary documentation and a clear, phased implementation plan. Based on your backend stack, these features are highly achievable.

First, here is the Project Requirements Document (PRD) that outlines the vision and core features for this initiative.

***

### **PRD_File: Bhashadaan Gamification Engine**

**Version:** 1.0
**Date:** October 29, 2025
**Author:** Project Manager

#### **1. Vision & Mission**

*   **Vision:** To transform the Bhashadaan contribution experience from a civic duty into a compelling and rewarding game, creating a vibrant community of "Language Warriors" dedicated to enriching India's digital linguistic landscape.
*   **Mission:** We will implement a multi-layered gamification engine to provide immediate feedback, foster healthy competition, and create a tangible sense of progress. This will significantly boost user engagement, data contribution rates, and long-term user retention.

#### **2. The Problem**

The current badge-only reward system on Bhashadaan suffers from low user motivation. As identified, the core issues are:
*   A lack of immediate gratification and feedback.
*   An absence of social and competitive elements.
*   Predictable and intangible rewards with no external value.
*   A core "validation" task that lacks a clear "win" state, failing to trigger a dopamine response.

This project will directly address these shortcomings by introducing a holistic, game-like ecosystem.

#### **3. Core Features & Requirements**

**3.1. Feature: Points & Scoring System ("Bhasha Points")**
*   **Description:** This is the foundational element. Users earn "Bhasha Points" (BP) for every positive action they take on the platform. This system provides immediate, quantifiable feedback on a user's contribution.
*   **User Stories:**
    *   As a user, when I submit a new sentence, I want to earn points instantly.
    *   As a user, when I validate a sentence, I want to receive points.
    *   As a user, if my validation matches the community consensus, I want to receive bonus points to feel that I was "correct."
*   **Requirements:**
    *   Award points for:
        *   New Text Submission (~10 BP)
        *   Text Validation (~5 BP)
        *   "Correct" Validation Bonus (+5 BP) - *A validation is deemed "correct" if it matches the majority vote after N number of validations.*
    *   The user's total BP score should be prominently displayed on their dashboard.

**3.2. Feature: Real-time Feedback & Daily Streaks**
*   **Description:** To make the experience feel alive and responsive, we need to provide immediate visual feedback and reward consistent behavior.
*   **User Stories:**
    *   As a user, after I complete a task, I want to see a small animation showing the points I earned (e.g., "+10").
    *   As a user, if I contribute for several days in a row, I want to be recognized and rewarded for my commitment.
*   **Requirements:**
    *   Frontend to display a non-intrusive points animation on action completion.
    *   Backend logic to track a user's daily contribution streak.
    *   Offer bonus multipliers for maintaining a streak (e.g., Day 3 = 1.2x points, Day 7 = 2x points).
    *   A daily cron job to reset streaks for users who have not contributed in the last 24 hours.

**3.3. Feature: Leaderboards & Social Ranking**
*   **Description:** This directly addresses the need for social competition. Leaderboards give context to a user's score and create a powerful motivational driver.
*   **User Stories:**
    *   As a user, I want to see how my total score ranks against other contributors.
    *   As a user, I want to compete with others on a weekly basis to see who can contribute the most.
*   **Requirements:**
    *   Implement three leaderboard types:
        1.  **Weekly:** Resets every Monday. Rewards the top performers of the week.
        2.  **Monthly:** Resets on the 1st of each month.
        3.  **All-Time:** A permanent hall of fame.
    *   The UI should show the Top 10 users and the current user's position, even if they are not in the top 10 (e.g., "You are #2,451").

**3.4. Feature: Levels & Progress Visualization**
*   **Description:** Badges are slow; levels are continuous. A leveling system gives a constant sense of forward momentum.
*   **User Stories:**
    *   As a user, I want to see a progress bar that fills up as I earn points, showing me how close I am to the next level.
    *   As a user, when I reach a new level, I want to receive a clear notification and perhaps a small reward.
*   **Requirements:**
    *   Define an exponential point system for levels (e.g., Level 2 at 500 BP, Level 3 at 1500 BP, etc.).
    *   Assign creative, language-themed titles to levels (e.g., Level 1: "Shishya", Level 5: "Lipik", Level 10: "Pandit").
    *   A progress bar/XP bar must be visible on the user's main profile/dashboard.

**3.5. Feature: Virtual Currency & Store ("Dhwani Coins")**
*   **Description:** This feature introduces variable rewards and gives tangible value to effort. Users earn "Dhwani Coins" (DC) for specific achievements, which can be spent on cosmetic items.
*   **User Stories:**
    *   As a user, when I level up or complete a 7-day streak, I want to earn a special currency.
    *   As a user, I want to spend my currency to customize my profile with a unique avatar frame or banner.
*   **Requirements:**
    *   Award Dhwani Coins for:
        *   Leveling up.
        *   Hitting streak milestones (7 days, 30 days).
        *   Finishing in the Top 3 of a weekly leaderboard.
    *   Create a simple virtual store where users can purchase non-functional, cosmetic items (e.g., profile themes, unique badge designs). This makes the rewards socially visible.

#### **4. Success Metrics**
*   **Engagement:** Increase in Daily Active Users (DAU) and Monthly Active Users (MAU).
*   **Contribution:** 25% increase in the number of submissions/validations per user session.
*   **Retention:** Increase in Day 7 and Day 30 user retention rates.

***

### **Project TODO & Implementation Plan**

Here’s a breakdown of the project into phases and actionable tasks. We’ll start with the foundational elements and build from there.

| Task No. | Task Name | Phase | Status | Priority | Dependencies |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **Database Schema Design** for new tables (user_stats, user_streaks, virtual_currency) | 0: Foundation | Not Started | **High** | - |
| 2 | Create DB migration scripts for the new tables | 0: Foundation | Not Started | **High** | 1 |
| 3 | **Implement Points Logic:** Modify contribution/validation endpoints to award Bhasha Points (BP) | 1: Core Loop | Not Started | **High** | 2 |
| 4 | Create user_stats API endpoint (`GET /api/user/stats`) to fetch points, level, and progress | 1: Core Loop | Not Started | **High** | 3 |
| 5 | **Frontend: User Dashboard UI:** Display user's level, BP, and a progress bar to the next level | 1: Core Loop | Not Started | **High** | 4 |
| 6 | **Frontend: Real-time Feedback:** Create a simple "+10 BP" animation on task completion | 1: Core Loop | Not Started | Medium | 5 |
| 7 | Implement Daily Streak logic and a `node-cron` job to manage resets | 1: Core Loop | Not Started | Medium | 3 |
| 8 | **Backend: Leaderboard Logic:** Use Redis Sorted Sets to store weekly, monthly, and all-time scores | 2: Social | Not Started | **High** | 3 |
| 9 | Create Leaderboard API endpoint (`GET /api/leaderboard?type=weekly`) | 2: Social | Not Started | **High** | 8 |
| 10 | **Frontend: Leaderboard Page:** Design and build the UI to display rankings | 2: Social | Not Started | **High** | 9 |
| 11 | Update User Profile pages to be public-facing to enhance social proof (show level, badges, etc.) | 2: Social | Not Started | Low | 5 |
| 12 | **Implement "Correct" Validation Bonus:** Use Bull/Redis queue to process validations asynchronously | 3: Adv. Features | Not Started | Medium | 3 |
| 13 | **Backend: Virtual Currency Logic:** Implement logic for earning and spending Dhwani Coins (DC) | 3: Adv. Features | Not Started | Medium | 1 |
| 14 | Create Virtual Store API endpoints (`GET /api/store/items`, `POST /api/store/buy`) | 3: Adv. Features | Not Started | Low | 13 |
| 15 | **Frontend: Virtual Store UI:** Design a simple interface for browsing and purchasing cosmetic items | 3: Adv. Features | Not Started | Low | 14 |
| 16 | Setup monitoring dashboards (e.g., Grafana) to track success metrics (DAU, contributions, etc.) | 4: Deploy | Not Started | Medium | 5, 10 |
| 17 | Final QA & A/B testing of different point values | 4: Deploy | Not Started | **High** | 1-15 |
| 18 | Production Deployment | 4: Deploy | Not Started | **High** | 17 |

### **How to Approach This Like a Project Manager**

Alright, that's the "what" and the "how." Now, let's talk strategy.

1.  **Iterate, Don't Boil the Ocean:** Don't try to build all of this at once. The beauty of this plan is that it's phased. Launch **Phase 1** as a "beta." The core loop of earning points, getting immediate feedback, and leveling up is a massive improvement on its own. It will give you an instant engagement lift.
2.  **Use Your Stack Wisely:** Your `Node.js` stack is perfect for this.
    *   Use `pg-promise` for storing permanent user stats that need to be accurate (total points, level, currency).
    *   Lean heavily on **`redis`** for anything real-time and ephemeral. Leaderboards are a textbook use case for Redis Sorted Sets—they are incredibly fast and efficient. User session streaks are also a great fit here.
    *   Use **`bull`** for the "Correct Validation Bonus" (Task 12). This task can be computationally heavy. Don't make the user wait. When a user validates, fire off a background job. That job can check if a consensus has been reached and award the bonus points later. The user will get a notification, which is a great re-engagement hook.
3.  **Balance the Economy:** The points and levels need to feel right. The first few levels should be quick to get the user hooked. Later levels should require more effort to create a sense of achievement. Before launching, model it out in a spreadsheet. How many contributions does it take to get to Level 2? Level 5? Level 10? You want the journey to be challenging but not impossible.
4.  **Celebrate the "Win":** The "Level Up" moment is critical. Don't just tick a number from 4 to 5. Make it an event. A full-screen overlay, a congratulatory message, a share button ("I just became a Bhasha Pandit on Bhashadaan!"), and the awarding of some Dhwani Coins. This is the dopamine hit you're looking for.

This is a very exciting and high-impact project. By methodically implementing these features, you can fundamentally change the user experience on Bhashadaan for the better. Let's get started.
