from .models import UsersCheckedIn
from datetime import datetime, date


def mycheck_in(user):
    user_has_checked_in = False
    checked_in_user = UsersCheckedIn.objects.filter(user=user).order_by('-check_date')[:1]
    checkin_dates = []
    for i in checked_in_user.all():
        checkin_dates.append(i.check_date)
        if i.check_date == date.today():
            user_has_checked_in = True
        else:
            user_has_checked_in = False

    checkin_context = {
        "user_has_checked_in": user_has_checked_in
    }

    return checkin_context
