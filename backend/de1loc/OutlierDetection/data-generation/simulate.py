from schedule_creator import Day, Event, loadWeekly, Weekly, DAYS_OF_WEEK
import numpy as np

STANDARD_DEV = 10/60

class Week:
    def __init__(self, num):
        self.num = num
        self.days = []

class Schedule:
    def __init__(self, name):
        self.name = name
        self.weeks = []

def generateWeek(weekly, num):
    week = Week(num)
    for day in weekly.days:
        randDay = Day(day.day)
        for event in day.events:
            mean = event.time
            randTime = np.random.normal(mean, STANDARD_DEV)
            randEvent = Event(event.isUnlocking, randTime)
            randDay.events.append(randEvent)
        week.days.append(randDay)
    return week

def generateSchedule(weekly, num_weeks):
    schedule = Schedule(weekly.name)
    for i in range(num_weeks):
        week = generateWeek(weekly, i)
        schedule.weeks.append(week)
    return schedule

def scheduleToNumpy(schedule, user=0):
    X = []
    for week in schedule.weeks:
        for day in week.days:
            for event in day.events:
                num = week.num
                isUnlck = int(event.isUnlocking)
                weekday = (DAYS_OF_WEEK.index(day.day) if event.time < 24 else DAYS_OF_WEEK.index+1) % 7
                time = event.time % 24
                X.append([user, num, isUnlck, weekday, time])
    return np.array(X)


def printWeek(week):
    print(f"Week Number: {week.num}")
    for day in week.days:
        print(f"    {day.day}")
        for event in day.events:
            print("---")
            print(f"        isUnlocking: {event.isUnlocking}")
            print(f"        time: {event.time}")
            print("---")

def printSchedule(schedule):
    print(f"Schedule name: {schedule.name}")
    for week in schedule.weeks:
        printWeek(week)

if __name__ == '__main__':
    test = loadWeekly("weeklys/Declan")
    s = generateSchedule(test, 4)
    n =scheduleToNumpy(s)
    print(n)
    



        
    



