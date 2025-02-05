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

    step_n = step_dict[step]

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
