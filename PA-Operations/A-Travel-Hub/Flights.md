# ✈️ Flights Database

> Track every flight booking. Update status after each check-in or change.  
> Dates are in local departure time. All reminders fire in MYT.

---

## Database Fields

| Field | Type | Notes |
|---|---|---|
| Flight No | Text | e.g. QR0521 |
| Route | Text | e.g. KUL → DOH → BCN |
| Departure Date & Time | Date/Time | Local time of departure city |
| Arrival Date & Time | Date/Time | Local time of arrival city |
| Airline | Select | See preferred airlines below |
| Aircraft Type | Text | e.g. A350-900, A380 |
| Loyalty Program Used | Select | Qatar / SQ / EK / MH / Vueling / BA |
| Seat Number | Text | e.g. 12A |
| Class | Select | Economy / Business / First |
| Status | Select | Upcoming / Checked-In / Completed / Cancelled / Changed |
| Booking Reference (PNR) | Text | 6-character code |
| Booking Link | URL | Airline manage-booking URL |
| Cost | Number | In booking currency |
| Currency | Select | MYR / EUR / GBP / BRL / USD |
| Cost (MYR equiv.) | Number | For expense tracking |
| Booked By | Select | Boss / PA |
| Card Used | Text | Last 4 digits |
| Linked Trip | Relation | → Trips database |
| Seat Checklist Done | Checkbox | Seat ✓ Meal ✓ Lounge ✓ |
| Notes | Text | Any special requests or changes |

---

## ✅ Seat Booking Checklist
After logging each flight, complete this checklist:

- [ ] Seat selected (window preferred for long-haul)
- [ ] Meal preference confirmed (healthy/special meal)
- [ ] Lounge access confirmed (Qatar Silver / SQ KrisFlyer / BA Executive Club)
- [ ] Online check-in reminder set (24–48 hrs before departure)
- [ ] Baggage allowance checked
- [ ] Transit visa required? (Check if layover > 4 hrs in a new country)

---

## 🛫 Preferred Airlines & Aircraft

| Airline | Program | Preferred Aircraft |
|---|---|---|
| Qatar Airways | Qatar Privilege Club (Silver) | A350, A380 |
| Singapore Airlines | KrisFlyer | A350, A380 |
| Emirates | Skywards | A380, A350 |
| Malaysia Airlines | Enrich | A330neo, A350 |
| British Airways | Executive Club (Avios) | A320 family, A350 |
| Vueling | Vueling Club | A320 family |

> **Airbus preference:** A318, A319, A320, A321 (narrow-body) and A330neo, A350 (wide-body)

---

## 📋 Current Trip Flights Log

| Flight No | Route | Date (Local) | Airline | Status | PNR |
|---|---|---|---|---|---|
| *(KL → Delhi)* | KUL → DEL | 21 Oct 2025 | TBC | Completed | *(add)* |
| *(Delhi → Spain)* | DEL → BCN | Oct 2025 | TBC | Completed | *(add)* |
| TBC | BCN → BRU | TBC | TBC | Upcoming | *(add)* |
| TBC | BRU → BCN | TBC | TBC | Upcoming | *(add)* |
| TBC | BCN → LHR | TBC | TBC | Upcoming | *(add)* |
| *(Cruise)* | Cruise → Barbados | TBC | Cruise | Upcoming | *(add)* |
| TBC | Barbados → Rio | TBC | TBC | Upcoming | *(add)* |
| TBC | Rio → MAD → BCN | TBC | TBC | Upcoming | *(add)* |
| TBC | BCN → SIN → KUL | TBC | SQ/BA | Upcoming | *(add)* |
| TBC | KUL → Bali (DPS) | TBC | MH/SQ | Upcoming | *(add)* |

---

*⏰ Reminder: Set 48-hour Notion alert + 24-hour WhatsApp update for Boss for every flight.*
