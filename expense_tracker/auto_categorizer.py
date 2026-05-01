"""Auto-categorize expenses based on description keywords."""

CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "Food & Dining": [
        "food", "restaurant", "lunch", "dinner", "breakfast", "coffee", "cafe",
        "pizza", "burger", "grocery", "groceries", "meal", "snack", "takeaway",
        "takeout", "eat", "drink", "juice", "tea", "bakery", "sushi", "fast food",
    ],
    "Transport": [
        "uber", "lyft", "taxi", "bus", "train", "metro", "subway", "fuel",
        "petrol", "gas", "parking", "toll", "car", "ride", "transport", "flight",
        "ticket", "fare", "bike", "bicycle",
    ],
    # Entertainment checked before Utilities so "netflix subscription" → Entertainment
    "Entertainment": [
        "movie", "cinema", "netflix", "spotify", "game", "games", "concert",
        "event", "streaming", "music", "show", "theatre", "books",
        "hobby", "sport",
    ],
    "Utilities": [
        "electricity", "water", "internet", "wifi", "phone", "mobile", "bill",
        "utility", "gas bill", "heating", "broadband", "subscription",
    ],
    "Health": [
        "doctor", "hospital", "medicine", "pharmacy", "health", "gym", "fitness",
        "dental", "clinic", "medical", "drug", "vitamin", "therapy", "insurance",
    ],
    "Shopping": [
        "amazon", "shopping", "clothes", "clothing", "shoes", "shirt", "jeans",
        "mall", "store", "purchase", "buy", "online", "delivery", "fashion",
    ],
    "Education": [
        "course", "book", "tuition", "school", "college", "university", "class",
        "study", "training", "workshop", "seminar", "exam", "fee",
    ],
    "Housing": [
        "rent", "mortgage", "repair", "maintenance", "furniture", "home", "house",
        "cleaning", "appliance", "landlord", "lease",
    ],
    "Travel": [
        "hotel", "airbnb", "vacation", "holiday", "travel", "trip", "tour",
        "airport", "luggage", "visa",
    ],
    "Savings & Investment": [
        "investment", "saving", "deposit", "stock", "mutual fund", "crypto",
        "pension", "fund",
    ],
}

DEFAULT_CATEGORY = "Other"


def auto_categorize(description: str) -> str:
    """Return the best-matching category for a given description."""
    lower = description.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in lower:
                return category
    return DEFAULT_CATEGORY


def list_categories() -> list[str]:
    """Return all available categories including the default."""
    return list(CATEGORY_KEYWORDS.keys()) + [DEFAULT_CATEGORY]
