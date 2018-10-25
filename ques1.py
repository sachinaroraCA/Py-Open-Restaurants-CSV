import pandas as pd


def find_open_restaurants(filename,  day,  time):

    headers = ["name", "timing"]
    data = pd.read_csv(filename, names=headers)
    open_restourants = []
    index = 0
    for column in data["timing"]:
        timings = column.split("/")

        for timing in timings:
            total_days = []
            time_string = ""
            day_string = timing.strip().split(" ")[0]
            if "-" in day_string:
                day_indexes = get_day_indexes(day_string)
                total_days.extend(day_indexes)
            else:
                day_index = get_day_index(day_string)
                total_days.append(day_index)

            check_time = timing.replace(day_string, "").strip()
            if not check_time[0].isdigit():
                day_string = check_time.split(" ")[0]
                if "-" in day_string:
                    day_indexes = get_day_indexes(day_string)
                    total_days.extend(day_indexes)
                else:
                    day_index = get_day_index(day_string)
                    total_days.append(day_index)

                time_string = check_time.replace(day_string, ""  ).strip()
            else:
                time_string = timing.strip().replace(day_string, "")

            # print(total_days, time_string )
            time_instance = time_string.split(" - ")
            to_time = get_time_instance(time_instance[1])
            from_time = get_time_instance(time_instance[0])

            final_result_indexes = []
            queried_time = get_time_instance(time)
            if "-" in day:
                queried_day_range = day.split("-")
                queried_from_day = get_day_index(queried_day_range[0])
                queried_to_day = get_day_index(queried_day_range[1])
                queried_days = [ index for index in range(queried_from_day, queried_to_day+1)]

                if compare_days_lists(queried_days, total_days) and queried_time <= to_time and queried_time >= from_time:
                    open_restourants.append(data["name"][index])
            else:
                queried_day = get_day_index(day)

                if queried_day in total_days and queried_time <= to_time and queried_time >= from_time:
                    open_restourants.append(data["name"][index])

        index = index+1
    [print(item) for item in open_restourants]


def get_days(days_string):
    days = days_string.split("-")
    return days


def get_day_index(day):
    days_dict = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4, "Sat": 5, "Sun": 6}
    try:
        day_index = days_dict[day]
    except:
        day_index = False

    return day_index


def get_time_instance(time_str):
    import datetime
    from datetime import timedelta
    time_str = time_str.strip()
    if len(time_str) == 4 or len(time_str) == 5:
        time_stamp = datetime.datetime.strptime(time_str, "%H %p")
    else:
        time_stamp = datetime.datetime.strptime(time_str, "%H:%M %p")

    if "PM" in time_str.upper():
        time_stamp = time_stamp + timedelta(hours=12)

    return time_stamp.time()


def compare_days_lists(list1, list2):
    for item in list1:
        if item not in list2:
            return False
    return True


def get_day_indexes(day_string):
    days = get_days(day_string)
    from_day = days[0]
    to_day = days[1].replace(",", "")
    day_indexes = [index for index in range(get_day_index(from_day), get_day_index(to_day) + 1)]
    return day_indexes


find_open_restaurants(filename="restaurant_hours.csv",
                      day="Mon-Fri",
                      time="02:00 PM")