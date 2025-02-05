from dateutil.relativedelta import relativedelta
import datetime


def datecount(start=datetime.date.today(), step="daily"):

    step_dict = {
        "daily": 1,
        "alternatively": 2,
        "weekly": 7,
        "monthly": 1,
        "quarterly": 3,
        "yearly": 12,
    }

    step = step_dict[step]

    if step in ["daily", "alternatively", "weekly"]:
        while True:
            step = step_dict[step]
            yield start
            start += datetime.timedelta(days=step)

    # elif step in ["monthly", "quarterly", "yearly"]:
    #     while True:
    #         step = step_dict[step]
    #         yield start
    #         start += relativedelta(months=step)


daily_gen = datecount(step="daily")
alt_gen = datecount(step="alternatively")
weekly_gen = datecount(step="weekly")
monthly_gen = datecount(step="monthly")
quarterly_gen = datecount(step="quarterly")
yearly_gen = datecount(step="yearly")

for i in range(10):
    print(next(daily_gen))
# for i in range(10):
#     print(next(alt_gen))
# for i in range(10):
#     print(next(weekly_gen))
# for i in range(10):
#     print(next(monthly_gen))
# for i in range(10):
#     print(next(quarterly_gen))
# for i in range(10):
#     print(next(yearly_gen))
