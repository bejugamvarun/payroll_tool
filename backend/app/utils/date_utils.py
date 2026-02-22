from datetime import date, timedelta
from typing import List
import calendar


def get_month_dates(year: int, month: int) -> List[date]:
    """
    Get all dates in a given month.

    Args:
        year: Year (e.g., 2024)
        month: Month (1-12)

    Returns:
        List of date objects for all days in the month
    """
    num_days = calendar.monthrange(year, month)[1]
    return [date(year, month, day) for day in range(1, num_days + 1)]


def get_working_days(
    year: int,
    month: int,
    holidays: List[date],
    weekend_days: List[int] = [5, 6]
) -> int:
    """
    Calculate the total number of working days in a month.

    Args:
        year: Year (e.g., 2024)
        month: Month (1-12)
        holidays: List of holiday dates
        weekend_days: List of weekday indices (0=Monday, 6=Sunday)

    Returns:
        Total working days in the month
    """
    all_dates = get_month_dates(year, month)
    holiday_set = set(holidays)

    working_days = 0
    for d in all_dates:
        # Skip if it's a weekend
        if d.weekday() in weekend_days:
            continue
        # Skip if it's a holiday
        if d in holiday_set:
            continue
        working_days += 1

    return working_days
