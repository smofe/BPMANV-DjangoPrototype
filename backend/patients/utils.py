from datetime import datetime
import json


def json_has_attributes_of(superset_json, subset_json):
    """
    Checks if a superset_json contains all attributes of a subset_json
    :param superset_json: a json dictionary
    :param subset_json: a json dictionary
    :return: boolean
    """
    try:
        for attribute, value in subset_json.items():
            superset_json[attribute]
    except KeyError:
        return False
    return True


def json_are_all_values_positive(json):
    """
    Checks if all attributes of the given json have positive values
    :param json: a json dictionary
    :return: boolean
    """
    for attribute, value in json.items():
        if json[attribute] < 0:
            return False
    return True


def json_is_subset_of(subset_json, superset_json):
    """
    Checks if a superset json contains more of each attribute than a subset json
    :param superset_json: The json representing the super set
    :param subset_json: The json representing the sub set
    :return: boolean
    """
    if json_has_attributes_of(superset_json, subset_json):
        for attribute, value in subset_json.items():
            if superset_json[attribute] < value:
                return False
        return True
    else:
        raise Exception("Json format mismatch")


def json_subtract_subset(superset_json, subset_json):
    """
    Subtracts all attributes of subset_json from the superset_json. (Call by reference)
    Should have checked if subset_json is a valid subset (json_is_subset_of)
    :param superset_json: the json set that will be subtracted from
    :param subset_json: the json set that defines what is subtracted
    :return: returns the modified superset_json
    """
    if json_has_attributes_of(superset_json, subset_json):
        for attribute, value in subset_json.items():
            superset_json[attribute] -= value
        return superset_json
    else:
        raise Exception("Json format mismatch")


def json_add_subset(receiver_json, sender_json):
    """
    Adds all attributes of sender_json to the receiver_json. (Call by reference)
    :param receiver_json: json to be added to
    :param sender_json: json to be added from
    :return: returns the modified receiver_json
    """
    if json_has_attributes_of(receiver_json, sender_json):
        for attribute, value in sender_json.items():
            receiver_json[attribute] += value
        return receiver_json
    else:
        raise Exception("Json format mismatch")


def save_to_event_log(string):
    text_file = open("user_event_log.txt", "a")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text_file.write( "\n" + str(current_time) + " | " + string)
    text_file.close()


def save_json_to_log(request):
    """
    takes a request and parses it into a json to be stored in a log file
    :param request: Request
    :return:
    """
    new_request = {
        "user": str(request.user),
        "path": str(request.path),
        "data": str(request.data),
        "method": str(request.method),
        "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    with open('data.json') as file:
            data = file.read()
    try:
        dic = json.loads(data)
    except:
        dic = {
            "requests": []
        }
    dic["requests"].append(new_request)
    with open('data.json', 'w') as file:
        json.dump(dic, file, ensure_ascii=False, indent=4)






