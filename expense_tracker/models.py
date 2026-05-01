"""Data models for the expense tracker."""
from dataclasses import dataclass, field
from datetime import date
from typing import Optional


@dataclass
class Expense:
    amount: float
    description: str
    category: str
    date: date
    id: Optional[int] = None
    is_recurring: bool = False
    recurrence_interval: Optional[str] = None  # 'daily', 'weekly', 'monthly'


@dataclass
class Budget:
    category: str
    monthly_limit: float
    id: Optional[int] = None
