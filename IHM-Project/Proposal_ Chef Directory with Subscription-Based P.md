# Proposal: Chef Directory with Subscription-Based Profile Access for IHM Gurukul

## Overview

This document outlines a plan to create a chef directory on the IHM Gurukul website, where users can browse a list of 600 chefs (name and location visible to all registered users), but access full chef profiles only after subscribing—similar to the model used by shaadi.com.

## Objectives

- Display a searchable directory of chefs with basic information (name and location) to all registered users.
- Restrict access to detailed chef profiles (full information, contact details, etc.) to paid subscribers only.
- Implement a smooth registration, payment, and access flow for users.


## Solution Approach

### 1. Directory \& Profile Management

- Use a directory plugin (e.g., Ultimate Member, ProfilePress, Business Directory Plugin) to import and display chef data.
- Configure the directory to show only names and locations publicly.


### 2. Membership \& Payment Integration

- Integrate a membership/paywall plugin (e.g., Paid Memberships Pro, MemberPress, Restrict User Access) to restrict access to detailed profiles.
- Set up subscription plans and payment gateways (PayPal, Stripe, etc.) for seamless transactions.


### 3. User Journey

1. **Registration:** User signs up on the website.
2. **Directory Browsing:** User can browse the list of chefs (name and location visible).
3. **Profile Access:** To view full chef profiles, the user is prompted to subscribe and pay.
4. **Post-Payment:** After successful payment, the user gains access to all detailed chef profiles.

## Recommended Plugin Combinations

| Directory Plugin | Membership/Paywall Plugin | Notes |
| :-- | :-- | :-- |
| Ultimate Member | Paid Memberships Pro | Flexible, widely used, many tutorials available |
| Business Directory | MemberPress | Good for business-style directories |
| Directorist | Built-in Monetization | Directory and paywall in one plugin |

## Implementation Steps

1. **Import Chef Data:** Use the directory plugin’s CSV import feature to upload chef records.
2. **Directory Setup:** Configure the directory to display only names and locations to all users.
3. **Profile Restriction:** Use the membership plugin to restrict detailed profiles to subscribers.
4. **Payment Integration:** Set up payment gateway and subscription plans.
5. **Testing:** Test the registration, browsing, and payment flow to ensure everything works smoothly.

## Additional Notes

- All plugins support customization for registration, login, and payment pages for a seamless user experience.
- The solution is scalable and can be managed without custom coding.


## Summary

By combining a directory plugin with a membership/paywall plugin, we can create a chef directory that displays basic information to all users, but restricts detailed profiles to paid subscribers—offering a professional, scalable, and user-friendly solution for IHM Gurukul.

