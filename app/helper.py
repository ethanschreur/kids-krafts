import calendar

def get_prev_month(month):
    """Given a month (1-12), it returns the previous month number."""
    prev_month = month - 1
    if prev_month == 0:
        prev_month = 12
    return prev_month

def get_next_month(month):
    """Given a month (1-12), it returns the next month number."""
    next_month = month + 1
    if (next_month == 13):
        next_month = 1
    return next_month

def get_prev_year(month, year):
    """Given a year int ex. 21 or 20 it returns the previous month's year number."""
    prev_month = get_prev_month(month)
    prev_year = year
    if prev_month == 12:
        prev_year = prev_year - 1
    return prev_year

def get_next_year(month, year):
    """Given a year int ex. 21 or 20, it returns the next month's year number."""
    next_month = get_next_month(month)
    next_year = year
    if (next_month == 1):
        next_year = next_year + 1;
    return next_year

def get_two_weeks_options(month, year):
    """Generates the two options for the two week time ranges that there can be during each month."""
    prev_month = get_prev_month(month)
    curr_month = month
    next_month = get_next_month(month)
    prev_year = get_prev_year(month, year)
    curr_year = year
    next_year = get_next_year(month, year)
    first_range = [calendar.monthcalendar(2000 + prev_year, prev_month)[-1], calendar.monthcalendar(2000 + curr_year, curr_month)[0]]
    second_range = [calendar.monthcalendar(2000 + curr_year, curr_month)[-1], calendar.monthcalendar(2000 + next_year, next_month)[0]]
    if (first_range[0].count(0) == 7 - first_range[1].count(0)):
        if first_range[0].count(0) < 4:
            first_range[1] = calendar.monthcalendar(2000 + curr_year, curr_month)[1]
        else:
            first_range[0] = calendar.monthcalendar(2000+ prev_year, prev_month)[-2]
    if (second_range[0].count(0) == 7 - second_range[1].count(0)):
        if second_range[0].count(0) < 4:
            second_range[1] = calendar.monthcalendar(2000 + next_year, next_month)[1]
        else:
            second_range[0] = calendar.monthcalendar(2000+ curr_year, curr_month)[-2]

    first_two_weeks = {'months': [prev_month, curr_month], 'years': [prev_year, curr_year], 'range': first_range}
    second_two_weeks = {'months': [curr_month, next_month], 'years': [curr_year, next_year], 'range': second_range}
    return [first_two_weeks, second_two_weeks];


def whichOption(today, two_weeks_options):
    """Looks at the two week options and decides which one to go with."""
    if (today <= two_weeks_options[0]['range'][1][-1]):
        return "first"
    else: 
        return "second"


def get_last_week(which, two_weeks_options):
    """Returns the last week of the first month for the two week time range."""
    if which == "first":
        return two_weeks_options[0]['range'][0]
    else:
        return two_weeks_options[1]['range'][0]

def get_first_week(which, two_weeks_options):
    """Returns the first week of the second month for the two week time range."""
    if which == "first":
        return two_weeks_options[0]['range'][1]
    else:
        return two_weeks_options[1]['range'][1]

def get_total_month_days(which, two_weeks_options):
    """Gets the total number of days for a specific month and year."""
    if which == "first":
        return (calendar.monthrange(2000 + two_weeks_options[0]['years'][0], two_weeks_options[0]['months'][0])[1])
    else: 
        return (calendar.monthrange(2000 + two_weeks_options[1]['years'][0], two_weeks_options[1]['months'][0])[1])

def get_new_last_week(last_week, which, two_weeks_options):
    """Transforms a list of the last week's days to replace any zeros with their respective actual number representations."""
    total_month_days = get_total_month_days(which, two_weeks_options)
    if (0 in last_week):
        new_last_week = []
        count_up = 1
        for index in last_week:
            if (index == 0):
                new_last_week.append(count_up)
                count_up = count_up + 1
            else:
                new_last_week.append(last_week[len(new_last_week)])
        return new_last_week
    else:
        return last_week

def get_new_first_week(first_week, which, two_weeks_options):
    """Transforms a list of the first week's days to replace any zeros with their respective actual number representations."""
    total_month_days = get_total_month_days(which, two_weeks_options)
    if (0 in first_week):
        new_first_week = []
        number_zeros = first_week.count(0)
        for val in first_week:
            if (val == 0):
                new_first_week.append(total_month_days - number_zeros + 1)
                number_zeros = number_zeros - 1
            else:
                new_first_week.append(val)
        return new_first_week
    else:
        return first_week

def get_first_month(which, prev_month, curr_month):
    """Returns the first month's number representation for the two week range."""
    if which == "first":
        first_month = prev_month
    else:
        first_month = curr_month
    return first_month

def get_second_month(which, curr_month, next_month):
    """Returns the second month's number representation for the two week range."""
    if which == "first":
        second_month = curr_month
    else:
        second_month = next_month
    return second_month

def get_month_header(which, prev_month, curr_month, next_month, last_week, first_week):
    """Generates the header that will go above the calendar that displays the two week range."""
    if which == "first":
        month_header = f"{prev_month} {last_week[0]} - {curr_month} {first_week[-1]}"
    else:
        month_header = f"{curr_month} {last_week[0]} - {next_month} {first_week[-1]}"
    return month_header 

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}