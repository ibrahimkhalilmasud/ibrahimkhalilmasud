# 🏨 Hotels Database

> Track every hotel stay. Always aim for best-value 5-star properties.  
> Boss (67) and Wife (58) — request senior/anniversary upgrades where applicable.

---

## Database Fields

| Field | Type | Notes |
|---|---|---|
| Property Name | Text | Full hotel name |
| City | Text | |
| Country | Text | |
| Check-in Date | Date | |
| Check-out Date | Date | |
| Number of Nights | Formula | Auto-calculated |
| Room Type | Text | e.g. Deluxe King, Junior Suite |
| Floor Preference | Text | High floor preferred |
| Booked Rate (per night) | Number | |
| Total Cost | Number | |
| Currency | Select | |
| Cost (MYR equiv.) | Number | |
| Booking Reference | Text | |
| Booking Platform | Select | Direct / Booking.com / Hotels.com / Expedia / Marriott / Hyatt |
| Loyalty Points Earned | Number | |
| Loyalty Program | Select | Marriott Bonvoy / Hyatt World / IHG / Hilton Honors |
| Status | Select | Upcoming / Active / Completed / Cancelled |
| Upgrade Requested | Checkbox | |
| Upgrade Granted | Select | Yes / No / Pending |
| Linked Trip | Relation | → Trips database |
| Cancellation Policy | Text | Free cancellation until *(date)* |
| Notes | Text | Special requests, early check-in, etc. |

---

## 🎯 Hotel Booking Guidelines

1. **Always target 5-star properties** — research best available discount (senior rates, loyalty rates, promo codes)
2. **Request high floor** on every booking
3. **Mention anniversary / special occasion** when applicable for complimentary upgrades
4. **Check loyalty program** before booking — earn points on every stay
5. **Compare**: Direct booking rate vs. OTA (Booking.com / Hotels.com) vs. Loyalty rate
6. **Cancellation policy**: Prefer free cancellation where possible for flexibility

---

## 💡 Upgrade Request Script (Email/Call)

> *"Good day, I am the Personal Assistant of Mr. Ibrahim Khalil Masud, who will be checking in on [DATE]. He is a valued guest and I would kindly like to inquire about the possibility of a room upgrade if available. He prefers a high-floor room. Thank you very much for your assistance."*

---

## 📋 Current Trip Hotels Log

| Property | City | Check-in | Check-out | Status | Ref |
|---|---|---|---|---|---|
| *(add)* | Barcelona | Oct 2025 | TBC | Active | *(add)* |
| *(add)* | London | TBC | TBC | Upcoming | *(add)* |
| *(add)* | Rio de Janeiro | TBC | TBC | Upcoming | *(add)* |
| *(add)* | Bali | TBC | Jan 2026 | Upcoming | *(add)* |

---

*💡 Tip: Always cross-check hotel loyalty points balance after each stay is completed.*
