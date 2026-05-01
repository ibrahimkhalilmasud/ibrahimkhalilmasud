# 🔔 Automation & Reminders Setup

> This document defines all automation rules for The Ibrahim Operations Desk.  
> Tools: **Notion** (push alerts) + **Google Calendar** (MYT-based scheduling) + **Zapier/Make** (WhatsApp automation).

---

## ⚙️ Automation Rules

### Rule 1 — Passport Expiry Alert
| Setting | Value |
|---|---|
| **Trigger** | Passport Expiry Date − 6 months |
| **Action** | Send Notion push notification to PA |
| **Message** | "⚠️ ALERT: Boss's passport expires on {DATE}. Renewal action required immediately." |
| **Channel** | Notion push + WhatsApp reminder to self |
| **Repeat** | Every 2 weeks until renewed |
| **Urgency** | 🔴 Critical |

**How to set up in Notion:**
1. Go to Passports-Visas database
2. Click the "Expiry Date" property
3. Add a Reminder: 6 months before date
4. Enable Notion mobile push notifications

---

### Rule 2 — Insurance Renewal Alert
| Setting | Value |
|---|---|
| **Trigger** | Insurance Renewal Date − 60 days |
| **Action** | Notion push + WhatsApp reminder draft |
| **Message** | "⚠️ Insurance renewal due: {POLICY_NAME} with {PROVIDER} on {DATE}. Premium: {AMOUNT}." |
| **Channel** | Notion push + Google Calendar event |
| **Repeat** | Weekly until renewed |
| **Urgency** | 🔴 High |

---

### Rule 3 — Credit Card Payment Reminder
| Setting | Value |
|---|---|
| **Trigger** | Credit Card Due Date − 5 days |
| **Action** | Notion push + draft WhatsApp to Boss |
| **Message** | "💳 Payment reminder: {CARD_NAME} ending {LAST4} due on {DATE}. Amount: ~{AMOUNT}." |
| **Channel** | Notion push |
| **Urgency** | 🟠 High |

---

### Rule 4 — Pre-Flight Checklist (48 hours)
| Setting | Value |
|---|---|
| **Trigger** | Flight Departure Date − 48 hours |
| **Action** | Notion push with seat booking checklist |
| **Message** | "✈️ Flight in 48 hours: {FLIGHT_NO} {ROUTE} on {DATE}. Complete seat booking checklist." |
| **Channel** | Notion push |
| **Urgency** | 🟠 High |

---

### Rule 5 — WhatsApp Update to Boss (24 hours before flight)
| Setting | Value |
|---|---|
| **Trigger** | Flight Departure Date − 24 hours |
| **Action** | Remind PA to send WhatsApp flight update to Boss |
| **Message** | "📱 Send Boss flight update for tomorrow: {FLIGHT_NO} {ROUTE} {TIME_LOCAL}" |
| **Channel** | Notion push to PA |
| **Urgency** | 🔴 High |

**WhatsApp message to send Boss:**
> *"Good morning Sir. Your flight tomorrow: {FLIGHT_NO} departs {ORIGIN} at {TIME_LOCAL} ({DATE}). Please check in online if not done. Seat: {SEAT}. Lounge: {LOUNGE}. Safe travels, Sir."*

---

### Rule 6 — Daily Brief Prompt
| Setting | Value |
|---|---|
| **Trigger** | Every day at 08:00 MYT |
| **Action** | Notify PA to prepare and send Daily Brief |
| **Message** | "🌅 Time to prepare and send today's Daily Brief to Boss." |
| **Channel** | Notion push + Google Calendar recurring event |
| **Urgency** | 🟠 Daily routine |

**Setup:**
1. Create a recurring event in Google Calendar: "Daily Brief" — 08:00 MYT, every day
2. Set notification: 15 minutes before (07:45 MYT)
3. Also set Notion recurring reminder on Daily-Brief page

---

### Rule 7 — Loyalty Points Expiry Alert
| Setting | Value |
|---|---|
| **Trigger** | Loyalty Points Expiry Date − 90 days |
| **Action** | Notion push + review points strategy |
| **Message** | "🏆 ALERT: {PROGRAM} points expiring on {DATE}. Balance: {POINTS}. Action required." |
| **Channel** | Notion push |
| **Repeat** | Monthly until resolved |
| **Urgency** | 🟠 Medium–High |

---

## 🛠️ Tools Setup Guide

### Notion Mobile Push Notifications
1. Install Notion on your phone (iPhone or Android)
2. Go to **Settings & Members → My notifications & settings**
3. Enable: Reminders, Mentions, and Property update alerts
4. Enable date-based reminders on all relevant databases

### Google Calendar Integration (MYT Timezone)
1. Set your Google Calendar default timezone to **Malaysia Time (MYT) — Asia/Kuala_Lumpur**
2. Add calendar events for:
   - All flight dates (with 48-hour and 24-hour alerts)
   - All insurance renewal dates (with 60-day alert)
   - All credit card due dates (with 5-day alert)
   - Daily Brief recurring event (08:00 MYT)
3. Share relevant calendar events with Boss (in his local timezone)

### Google Calendar → Phone Notification
1. In Google Calendar app settings → Notifications
2. Default event notification: 30 minutes before
3. For critical alerts (passport, insurance): add extra 1 day, 1 week notification

### Zapier / Make Automation (Advanced — Future Setup)

**Automation: Insurance Renewal WhatsApp**
- Trigger: Notion database — Insurance Renewal Date is 60 days from today
- Action: Send WhatsApp message (via Twilio or WhatsApp Business API) using Template 4
- Tools: Notion API + Zapier + Twilio WhatsApp

**Automation: Daily Brief Reminder**
- Trigger: Every day at 08:00 MYT
- Action: Send WhatsApp reminder to PA's number: "🌅 Time to send today's Daily Brief"
- Tools: Zapier Schedule + Twilio

**Automation: Flight Tracker**
- Trigger: 24 hours before flight departure (from Notion Flights database)
- Action: Fetch real-time flight status from Flightradar24 API
- Send WhatsApp update to Boss
- Tools: Notion + Zapier + Flightradar24 API + Twilio

> 💡 **Note:** Zapier/Make automations require a paid plan and WhatsApp Business API setup. This is a future enhancement to implement once the manual system is running smoothly.

---

## 📅 Reminder Calendar Setup Checklist

- [ ] Notion mobile app installed with push notifications enabled
- [ ] Google Calendar set to MYT timezone
- [ ] Daily Brief recurring event created (08:00 MYT daily)
- [ ] Insurance renewal dates entered with 60-day alerts
- [ ] Credit card due dates entered with 5-day alerts
- [ ] Passport expiry dates entered with 6-month alerts
- [ ] All flight dates entered with 48-hour and 24-hour alerts
- [ ] Loyalty points expiry dates entered with 90-day alerts

---

*Once all manual reminders are set and the system is running smoothly for 1 month, consider implementing Zapier/Make automations.*
