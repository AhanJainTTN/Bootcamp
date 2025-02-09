"""
Read about itertools.count(start=0, step=1) function which accepts options arguments start and end Based on this, implement a similar `datecount([start, step])` where start is a `datetime.date` object and step can we string values 'alternative', 'daily', 'weekly', 'monthly', 'Quarterly', 'yearly' (ignore case) example execution: >> dc = datecount(step='weekly') >> for i in range(10): print (next(dc)) Output: 2025-01-17 2025-01-24 2025-01-31 2025-02-07 2025-02-14 2025-02-21 2025-02-28 2025-03-07 2025-03-14 2025-03-21
"""

from dateutil.relativedelta import relativedelta
import datetime
from typing import Generator, Optional


# Generator[yield_type, send_type, return_type]
# yield_type: The type of values the generator yields
# send_type: The type of values that can be sent into the generator
# return_type: The type of value the generator returns when it ends (None if never ending)
def datecount(
    start: Optional[datetime.date] = None, step: str = "daily"
) -> Generator[datetime.date, None, None]:
    """
    A generator that yields dates based on a specified step interval.

    Args:
        start (Optional[datetime.date]): The starting date (defaults to today if None).
        step (str): The time interval for incrementing dates.
                    Options: 'daily', 'alternatively' (every other day), 'weekly', 'monthly', 'quarterly', 'yearly'.

    Yields:
        datetime.date: The next date based on the specified step.

    Notes:
        Using None as the default because Python evaluates default arguments only once at function definition. If start=datetime.date.today() were used as a default, it would be set at the time of definition, causing all subsequent calls to use the same initial date instead of dynamically updating to the current date

    """
    if start is None:
        start = datetime.date.today()

    step_dict = {
        "daily": 1,
        "alternatively": 2,
        "weekly": 7,
        "monthly": 1,
        "quarterly": 3,
        "yearly": 12,
    }

    # Raise error if wrong step entered
    try:
        step_n = step_dict[step]
    except KeyError:
        print(f"Invalid step '{step}'. Choose from: {list(step_dict.keys())}")

    if step in ["daily", "alternatively", "weekly"]:
        while True:
            start += datetime.timedelta(days=step_n)
            yield start
    elif step in ["monthly", "quarterly", "yearly"]:
        while True:
            start += relativedelta(months=step_n)
            yield start


def main() -> None:
    """
    Entry point of the script. Generates and prints dates for different step intervals.
    """
    steps = ["daily", "alternatively", "weekly", "monthly", "quarterly", "yearly"]

    for step in steps:
        print(f"\n{step.capitalize()}...\n")
        date_gen = datecount(step=step)
        # _ is a throwaway variable - used when the value is not needed
        for _ in range(10):
            print(next(date_gen))


if __name__ == "__main__":
    main()
