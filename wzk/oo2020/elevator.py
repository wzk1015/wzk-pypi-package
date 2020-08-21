from random import *
from numpy.random import permutation
import re


def hw5_generator(length, time_max):
    id = []
    ans = []

    for i in range(length):
        # generate time
        ans.append([time_max * random()])
        # generate id
        new_id = randint(0, 100)
        while new_id in id:
            new_id = randint(0, 100)
        id.append(new_id)

    ans.sort()
    min_time = min(ans)[0] - random()

    for i in range(length):
        ans[i][0] -= min_time
        ans[i].append(id[i])
        # generate floor
        ans[i].append(randint(1, 15))
        ans[i].append(randint(1, 15))
        while ans[i][2] == ans[i][3]:
            ans[i][3] = randint(1, 15)
    for i in range(length):
        ans[i] = "[{0:.1f}]{1}-FROM-{2}-TO-{3}\n".format(ans[i][0], ans[i][1], ans[i][2], ans[i][3])

    return ans


def hw6_generator(length, num_elevator, time_max):
    id = []
    ans = []
    # ans: time id from to

    for i in range(length):
        # generate time
        ans.append([time_max * random()])
        # generate id
        id.append(i + 1)

    ans.sort()
    min_time = min(ans)[0] - random() - 1

    for i in range(length):
        ans[i][0] -= min_time
        ans[i].append(id[i])
        # generate floor
        floors = list(range(1, 16))
        floors.extend([-1, -2, -3])
        ans[i].append(choice(floors))
        ans[i].append(choice(floors))
        while ans[i][2] == ans[i][3]:
            ans[i][3] = randint(1, 15)

    for i in range(length):
        ans[i] = "[{0:.1f}]{1}-FROM-{2}-TO-{3}\n".format(ans[i][0], ans[i][1], ans[i][2], ans[i][3])
    ans.insert(0, "[0.0]{}\n".format(num_elevator))
    return ans


def hw7_generator(length, num_new_elevator, time_max):
    id = []
    ans = []
    add_elev_index = 0
    add_elev_time = []
    order = permutation([1, 2, 3])
    if num_new_elevator == -1:
        num_new_elevator = randint(0, 3)
    for i in range(num_new_elevator):
        add_elev_time.append(randint(0, length - 1))
    # ans: time id from to

    for i in range(length):
        # generate time
        ans.append([time_max * random()])
        # generate id
        id.append(i + 1)

    ans.sort()
    min_time = min(ans)[0] - random() - 1

    for i in range(length):
        ans[i][0] -= min_time
        ans[i].append(id[i])
        # generate floor
        floors = list(range(1, 21))
        floors.extend([-1, -2, -3])
        ans[i].append(choice(floors))
        ans[i].append(choice(floors))
        while ans[i][2] == ans[i][3]:
            ans[i][3] = choice(floors)

    for i in range(length):
        if i not in add_elev_time:
            ans[i] = "[{0:.1f}]{1}-FROM-{2}-TO-{3}\n".format(ans[i][0], ans[i][1], ans[i][2], ans[i][3])
        else:
            ans[i] = "[{0:.1f}]{1}-ADD-ELEVATOR-{2}\n".format(ans[i][0], "X" + str(order[add_elev_index]),
                                                              choice(["A", "B", "C"]))
            add_elev_index += 1
    return ans


def hw7_generator_coverage():
    ans = ["[1.0]X1-ADD-ELEVATOR-A\n", "[1.0]X2-ADD-ELEVATOR-B\n", "[1.0]X3-ADD-ELEVATOR-C\n"]
    count = 1
    floors = [-3, -2, -1]
    floors.extend(list(range(1, 21)))
    for i in floors:
        for j in floors:
            if i == j:
                continue
            ans.append("[2.0]{}-FROM-{}-TO-{}\n".format(count, i, j))
            count += 1
    return ans


def hw7_judge(data, lines):
    #print(data)
    actions, people, requests, elevators = _hw7_process(lines, data)
    floors_range = list(range(1, 21))
    floors_range.extend([-1, -2, -3])

    for id in requests.keys():
        if id not in people.keys():
            print("Person not found!" + str(id))
            return False

    for action in actions:
        if action["floor"] not in floors_range:
            print("Floor out of range!")
            return False

        if "id" in action.keys() and action["id"] not in people.keys():
            print("Wrong ID!")
            return False

    if not _hw7_check_people_in_elevator(actions, elevators):
        return False
    if not _hw7_check_time_and_floor(actions, elevators):
        return False
    if not _hw7_check_people(people, requests):
        return False

    return True


def _hw7_process(lines, data):
    actions = []
    people = {}
    elevators = {"A": "A", "B": "B", "C": "C"}
    requests = {}

    for line in data:
        if line == "END\n":
            break
        if line.find("ADD-ELEVATOR") != -1:
            split_list = line.split("-")
            id = split_list[0].split("]")[1]
            type = split_list[-1].strip("\n")
            elevators[id] = type
        else:
            line = line.replace("--", "-$")
            split_list = line.split("-")
            id = int(split_list[0].split("]")[1])
            time = float(line[1:].split(']')[0])
            fro = int(split_list[2].replace("$", "-"))
            to = int(split_list[4].replace("$", "-"))
            requests[id] = {"from": fro, "to": to, "time": time}

    for i in range(len(lines)):
        #print(lines[i], end="")
        line = lines[i].replace("--", "-$").strip()
        new_dict = {'time': float(line.split("]")[0].strip("[").strip())}
        split_list = line.split("-")
        new_dict["action"] = split_list[0].split("]")[1]

        new_dict["floor"] = int(split_list[-2].replace("$", "-"))
        new_dict["elevator"] = split_list[-1]
        if new_dict["action"] in ["IN", "OUT"]:
            new_dict["id"] = int(split_list[-3])
            if new_dict["id"] not in people:
                people[new_dict["id"]] = [new_dict]
            else:
                people[new_dict["id"]].append(new_dict)
        actions.append(new_dict)

    return actions, people, requests, elevators


def _hw7_check_people_in_elevator(actions, elevators):
    passengers = {"A": [], "B": [], "C": [], "X1": [], "X2": [], "X3": []}
    max_size = {"A": 6, "B": 8, "C": 7}
    for action in actions:
        elev = action["elevator"].strip()

        if action["action"] == "IN":
            if action["id"] in passengers[elev]:
                print("In twice!")
                return False
            passengers[elev].append(action["id"])
            if len(passengers[elev]) > max_size[elevators[elev]]:
                print("Too Many People in elevator {}!".format(elev))
                return False
        elif action["action"] == "OUT":
            if action["id"] not in passengers[elev]:
                print("Out from nowhere!")
                return False
            passengers[elev].remove(action["id"])
    return True


def _hw7_check_time_and_floor(actions, elevators):
    elevator_dict = {"A": [], "B": [], "C": [], "X1": [], "X2": [], "X3": []}
    arrive_time = {"A": 0.4, "B": 0.5, "C": 0.6}
    arrive_floors = {"A": [-3, -2, -1, 1, 15, 16, 17, 18, 19, 20],
                     "B": [-2, -1, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                     "C": [1, 3, 5, 7, 9, 11, 13, 15]}

    for action in actions:
        elevator_dict[action["elevator"]].append(action)

    for elev in elevator_dict.keys():
        actions_elev = elevator_dict[elev]
        for i in range(len(actions_elev) - 1):
            if actions_elev[i]["action"] == "ARRIVE" and actions_elev[i + 1]["action"] == "ARRIVE":
                if actions_elev[i + 1]["time"] - actions_elev[i]["time"] < arrive_time[elevators[elev]] - 0.00001:
                    print("Arrive too fast!")
                    return False
            if actions_elev[i]["action"] == "OPEN":
                for j in range(i + 1, len(actions_elev)):
                    if actions_elev[j]["action"] == "CLOSE":
                        if actions_elev[j]["time"] - actions_elev[i]["time"] < 0.399999:
                            print("Close too fast!")
                            return False
                        break
            if actions_elev[i]["action"] == "CLOSE":
                for j in range(i + 1, len(actions_elev)):
                    if actions_elev[j]["action"] == "ARRIVE":
                        if actions_elev[j]["time"] - actions_elev[i]["time"] < arrive_time[elevators[elev]] - 0.00001:
                            print("Arrive after close too fast!")
                            return False
                        break
            if (actions_elev[i + 1]["floor"] - actions_elev[i]["floor"] > 1 and
                actions_elev[i]["floor"] != -1) or \
                    (actions_elev[i + 1]["floor"] - actions_elev[i]["floor"] < -1 and
                     actions_elev[i + 1]["floor"] != -1):
                print("Wrong floor movement! " + str(actions_elev[i + 1]))
                return False

        for i in range(len(actions_elev)):
            if actions_elev[i]["action"] != "ARRIVE" and actions_elev[i]["floor"] not in arrive_floors[elevators[elev]]:
                print("Stop at wrong floor! floor:" + str(actions_elev[i]["floor"]) + "elev: " + str(actions_elev[i]))
                return False

    return True


def _hw7_check_people(people, requests):
    for id in people.keys():
        source = requests[id]["from"]
        target = requests[id]["to"]
        movements = people[id]
        if len(movements) % 2 == 1:
            print("Person movements are odd number! person" + str(id))
            return False
        i = 0
        while i < len(movements) - 1:
            if movements[i]["action"] != "IN" or movements[i + 1]["action"] != "OUT":
                print("In and out movements mismatch! person" + str(id))
                return False
            if movements[i]["elevator"] != movements[i + 1]["elevator"]:
                print("In and out elevator mismatch! person" + str(id))
                return False
            if i + 1 != len(movements) - 1:
                if movements[i + 1]["floor"] != movements[i + 2]["floor"]:
                    print("Transfer floor mismatch! person" + str(id))
                    return False
            i += 2
        if movements[-1]["floor"] != target:
            print("Wrong target! person" + str(id))
            return False
        if movements[0]["floor"] != source:
            print("Wrong source! person" + str(id))
            return False
    return True


def hw6_judge(data, lines):
    actions, people, requests = _hw6_process(lines, data)
    floors_range = list(range(1, 17))
    floors_range.extend([-1, -2, -3])

    for id in requests.keys():
        if id not in people.keys():
            print("Person not found!" + str(id))
            return False
        if "OUT" not in people[id].keys() or people[id]["OUT"] != requests[id]["to"]:
            print("Wrong destination!" + str(id))
            return False
        if "IN" not in people[id].keys() or people[id]["IN"] != requests[id]["from"]:
            print("Wrong start point!" + str(id))
            return False

    for action in actions:
        if action["floor"] not in floors_range:
            print("Floor out of range!")
            return False
        if "id" in action.keys() and action["id"] not in people.keys():
            print("Wrong ID!")
            return False

    if not _hw6_check_people_in_elevator(actions):
        return False
    if not _hw6_check_time(actions):
        return False
    return True


def _hw6_process(lines, data):
    actions = []
    people = {}
    for i in range(len(lines)):
        line = lines[i].replace("--", "-$").strip()
        new_dict = {}
        new_dict["time"] = float(line.split("]")[0].strip("[").strip())
        split_list = line.split("-")
        new_dict["action"] = split_list[0].split("]")[1]
        new_dict["floor"] = int(split_list[-2].replace("$", "-"))
        new_dict["elevator"] = split_list[-1]
        if new_dict["action"] in ["IN", "OUT"]:
            new_dict["id"] = int(split_list[-3])
            if new_dict["id"] not in people:
                people[new_dict["id"]] = {new_dict["action"]: new_dict["floor"]}
            else:
                people[new_dict["id"]][new_dict["action"]] = new_dict["floor"]
        actions.append(new_dict)

    requests = {}
    for line in data:
        if line.startswith("[0.0]"):
            continue
        if line == "END\n":
            break
        line = line.replace("--", "-$")
        split_list = line.split("-")
        id = int(split_list[0].split("]")[1])
        time = float(line[1:].split(']')[0])
        fro = int(split_list[2].replace("$", "-"))
        to = int(split_list[4].replace("$", "-"))
        requests[id] = {"from": fro, "to": to, "time": time}

    return actions, people, requests


def _hw6_check_people_in_elevator(actions):
    passengers = {"A": [], "B": [], "C": [], "D": [], "E": []}
    for action in actions:
        elev = action["elevator"]
        if action["action"] == "IN":
            if action["id"] in passengers[elev]:
                print("In twice!")
                return False
            passengers[elev].append(action["id"])
            if len(passengers[elev]) > 7:
                print("Too Many People in elevator {}!".format(elev))
                return False
        elif action["action"] == "OUT":
            if action["id"] not in passengers[elev]:
                print("Out from nowhere!")
                return False
            passengers[elev].remove(action["id"])
    return True


def _hw6_check_time(actions):
    elevator_dict = {"A": [], "B": [], "C": [], "D": [], "E": []}
    for action in actions:
        elevator_dict[action["elevator"]].append(action)

    for elev in elevator_dict.keys():
        actions_elev = elevator_dict[elev]
        for i in range(len(actions_elev) - 1):
            if actions_elev[i]["action"] == "ARRIVE" and actions_elev[i + 1]["action"] == "ARRIVE":
                if actions_elev[i + 1]["time"] - actions_elev[i]["time"] < 0.399999:
                    print("Arrive too fast!")
                    return False
            if actions_elev[i]["action"] == "OPEN":
                for j in range(i + 1, len(actions_elev)):
                    if actions_elev[j]["action"] == "CLOSE":
                        if actions_elev[j]["time"] - actions_elev[i]["time"] < 0.399999:
                            print("Close too fast!")
                            return False
                        break
            if actions_elev[i]["action"] == "CLOSE":
                for j in range(i + 1, len(actions_elev)):
                    if actions_elev[j]["action"] == "ARRIVE":
                        if actions_elev[j]["time"] - actions_elev[i]["time"] < 0.399999:
                            print("Arrive after close too fast!")
                            return False
                        break
            if (actions_elev[i + 1]["floor"] - actions_elev[i]["floor"] > 1 and
                actions_elev[i]["floor"] != -1) or \
                    (actions_elev[i + 1]["floor"] - actions_elev[i]["floor"] < -1 and
                     actions_elev[i + 1]["floor"] != -1):
                print("Wrong floor movement!" + str(actions_elev[i + 1]))
                return False
    return True


def hw5_judge(lines, data):
    actions, people, string, floors, requests = _hw5_process(lines, data)
    for id in requests.keys():
        if id not in people.keys():
            print("Person not found!" + str(id))
            return False
        if "OUT" not in people[id].keys() or people[id]["OUT"] != requests[id]["to"]:
            print("Wrong destination!" + str(id))
            return False
        if "IN" not in people[id].keys() or people[id]["IN"] != requests[id]["from"]:
            print("Wrong start point!" + str(id))
            return False

    for action in actions:
        if action["floor"] not in range(1, 16):
            print("Floor out of range!")
            return False

        if "id" in action.keys() and action["id"] not in people.keys():
            print("Wrong ID!")
            return False

        for i in range(len(floors) - 1):
            if floors[i + 1] - floors[i] > 1 or floors[i + 1] - floors[i] < -1:
                print("Wrong floor movement!")
                return False

        if not re.match("(A*(O[io]*C))*", string):
            print("Wrong action sequence!")
            return False

        if not _hw5_check_people_in_elevator(actions):
            return False
        if not _hw5_check_time(actions):
            return False

    return True


def _hw5_process(lines, data):
    actions = []
    string = ""
    floors = []
    people = {}
    for i in range(len(lines)):
        new_dict = {"time": float(lines[i].split("]")[0].strip("[").strip())}
        split_list = lines[i].split("-")
        new_dict["action"] = split_list[0].split("]")[1]
        new_dict["floor"] = int(split_list[-1])
        floors.append(new_dict["floor"])
        if new_dict["action"] in ["IN", "OUT"]:
            new_dict["id"] = int(split_list[-2])
            string += new_dict["action"][0].lower()
            if new_dict["id"] not in people:
                people[new_dict["id"]] = {new_dict["action"]: new_dict["floor"]}
            else:
                people[new_dict["id"]][new_dict["action"]] = new_dict["floor"]
        else:
            string += new_dict["action"][0]
        actions.append(new_dict)

    requests = {}
    for line in data:
        if line == "END\n":
            break
        split_list = line.split("-")
        id = int(split_list[0].split("]")[1])
        time = float(line[1:].split(']')[0])
        fro = int(split_list[2])
        to = int(split_list[4])
        requests[id] = {"from": fro, "to": to, "time": time}

    return actions, people, string, floors, requests


def _hw5_check_people_in_elevator(actions):
    passengers = []
    for action in actions:
        if action["action"] == "IN":
            if action["id"] in passengers:
                print("In twice!")
                return False
            passengers.append(action["id"])
        elif action["action"] == "OUT":
            if action["id"] not in passengers:
                print("Out from nowhere!")
                return False
            passengers.remove(action["id"])
    return True


def _hw5_check_time(actions):
    for i in range(len(actions) - 1):
        if actions[i]["action"] == "ARRIVE" and actions[i + 1]["action"] == "ARRIVE":
            if actions[i + 1]["time"] - actions[i]["time"] < 0.399999:
                print("Arrive too fast!")
                print(actions[i + 1]["time"])
                print(actions[i]["time"])
                return False
        if actions[i]["action"] == "OPEN":
            for j in range(i + 1, len(actions)):
                if actions[j]["action"] == "CLOSE":
                    if actions[j]["time"] - actions[i]["time"] < 0.399999:
                        print("Close too fast!")
                        return False
                    break
    return True