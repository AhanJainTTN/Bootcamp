"""
Read about itertools.count(start=0, step=1) function which accepts options arguments start and end Based on this, implement a similar `datecount([start, step])` where start is a `datetime.date` object and step can we string values 'alternative', 'daily', 'weekly', 'monthly', 'Quarterly', 'yearly' (ignore case) example execution: >> dc = datecount(step='weekly') >> for i in range(10): print (next(dc)) Output: 2025-01-17 2025-01-24 2025-01-31 2025-02-07 2025-02-14 2025-02-21 2025-02-28 2025-03-07 2025-03-14 2025-03-21
"""

from dateutil.relativedelta import relativedelta
import datetime


def datecount(start=None, step="daily"):

    # Using None as default otherwise start is evaluated once at function definition and all subsequent calls use the date when the function is defined as default
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

    # Catch error if wrong step entered
    try:
        step_n = step_dict[step]
    except KeyError:
        print("Enter correct step")

    while step in ["daily", "alternatively", "weekly"]:
        yield start
        start += datetime.timedelta(days=step_n)

    while step in ["monthly", "quarterly", "yearly"]:
        yield start
        start += relativedelta(months=step_n)


# daily generator
daily_gen = datecount(step="daily")
print("Every Day...\n")
for i in range(10):
    print(next(daily_gen))

# alternative generator
alt_gen = datecount(step="alternatively")
print("\nEvery Other Day...\n")
for i in range(10):
    print(next(alt_gen))

# weekly generator
weekly_gen = datecount(step="weekly")
print("\nEvery Week...\n")
for i in range(10):
    print(next(weekly_gen))

# monthly generator
monthly_gen = datecount(step="monthly")
print("\nEvery Month...\n")
for i in range(10):
    print(next(monthly_gen))

# quarterly generator
quarterly_gen = datecount(step="quarterly")
print("\nEvery Quarter...\n")
for i in range(10):
    print(next(quarterly_gen))

# yearly generator
yearly_gen = datecount(step="yearly")
print("\nEvery Year...\n")
for i in range(10):
    print(next(yearly_gen))
