import pickle as pkl
DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    


class Event:
    def __init__(self, isUnlocking, time):
        self.isUnlocking = isUnlocking
        self.time = time

class Day:
    def __init__(self, day):
        self.day = day
        self.events = []

class Weekly:
    def __init__(self, name):
        self.name = name
        self.days = []

def generateWeekly():
    name = input("Please enter your name: ")
    weekly = Weekly(name)
    for day in DAYS_OF_WEEK:
        curr = Day(day)
        while(1):

            response = input(f"Do you wish to add another event to {curr.day}? (Y/N): ")
            if response == "Y":
                while(1):
                    unlocking = input("Are you unlocking? (Y/N): ")
                    if unlocking == "Y" or unlocking == "N":
                        break
                unlocking = True if unlocking == "Y" else False
                hour = input("What hour? Answer in 24 hour format: ")
                minute = input("What minute: ")
                time = int(hour) + int(minute)/60
                event = Event(unlocking, time)
                curr.events.append(event)
            if response == "N":
                break
            else:
                continue
        weekly.days.append(curr)
    print(weekly)
    return weekly

def saveWeekly(weekly):
    file = open(f"{weekly.name}.pkl", "wb")
    pkl.dump(weekly, file)
    file.close()

def loadWeekly(name):
    file = open(f"{name}.pkl","rb")
    weekly = pkl.load(file)
    file.close()
    return weekly


def printWeekly(weekly):
    print(f"Weekly name: {weekly.name}")
    for day in weekly.days:
        print(f"    {day.day}")
        for event in day.events:
            print("---")
            print(f"        isUnlocking: {event.isUnlocking}")
            print(f"        time: {event.time}")
            print("---")



if __name__ == '__main__':
    w = generateWeekly()
    saveWeekly(w)
    # w = loadWeekly("Declan")
    # printWeekly(w)
