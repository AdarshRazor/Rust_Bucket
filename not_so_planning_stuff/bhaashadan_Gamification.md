# **Bhashadaan Gamification Engine**

**Version:** 1.1
**Date:** October 28, 2025
**Author:** AdarshRazor

## **The Problem**

The current badge-only reward system on Bhashadaan suffers from low user motivation. As identified, the core issues are:
*   A lack of immediate gratification and feedback.
*   An absence of social and competitive elements.
*   Predictable and intangible rewards with no external value.
*   A core "validation" task that lacks a clear "win" state, failing to trigger a dopamine response.

## **Core Features & Requirements**

**1. Feature: Points & Scoring System ("Bhasha Points")**
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

**2. Feature: Real-time Feedback & Daily Streaks**
*   **Description:** To make the experience feel alive and responsive, we need to provide immediate visual feedback and reward consistent behavior.
*   **User Stories:**
    *   As a user, after I complete a task, I want to see a small animation showing the points I earned (e.g., "+10").
    *   As a user, if I contribute for several days in a row, I want to be recognized and rewarded for my commitment.
*   **Requirements:**
    *   Frontend to display a non-intrusive points animation on action completion.
    *   Backend logic to track a user's daily contribution streak.
    *   Offer bonus multipliers for maintaining a streak (e.g., Day 3 = 1.2x points, Day 7 = 2x points).
    *   A daily cron job to reset streaks for users who have not contributed in the last 24 hours.

**3. Feature: Leaderboards & Social Ranking**
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

**4. Feature: Levels & Progress Visualization**
*   **Description:** Badges are slow; levels are continuous. A leveling system gives a constant sense of forward momentum.
*   **User Stories:**
    *   As a user, I want to see a progress bar that fills up as I earn points, showing me how close I am to the next level.
    *   As a user, when I reach a new level, I want to receive a clear notification and perhaps a small reward.
*   **Requirements:**
    *   Define an exponential point system for levels (e.g., Level 2 at 500 BP, Level 3 at 1500 BP, etc.).
    *   Assign creative, language-themed titles to levels (e.g., Level 1: "Shishya", Level 5: "Lipik", Level 10: "Pandit").
    *   A progress bar/XP bar must be visible on the user's main profile/dashboard.

**5. Feature: Virtual Currency & Store ("Dhwani Coins")**
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

## **Success Metrics**
*   **Engagement:** Increase in Daily Active Users (DAU) and Monthly Active Users (MAU).
*   **Contribution:** 25% increase in the number of submissions/validations per user session.
*   **Retention:** Increase in Day 7 and Day 30 user retention rates.

***

## **Project TODO & Implementation Plan**

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
