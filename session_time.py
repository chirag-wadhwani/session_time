import sys
from datetime import datetime
from collections import defaultdict

def sanitize_line(line):
    """
    Sanitize the line by removing the additional spaces and validate the date, username, and marker fetched from the sanitized line
    """
    line_parts = line.strip().split(" ")
    line_parts = [line_part.strip() for line_part in line_parts]

    if len(line_parts) == 3:
        try:
            date = datetime.strptime(line_parts[0], "%H:%M:%S")
            line_parts[0] = date
        except:
            return None
        username = line_parts[1]
        session_state = line_parts[2]
        if not username.isalnum() or session_state not in ["Start", "End"]:
            return None

        return line_parts
    else:
        return None

def calculate_session(file_path):
    """
    Calculate number of sessions and total seconds
    """
    try:
        f = open(file_path, "r")
    except Exception as e:
        print("Error occured while reading the file: {}".format(e))
        return None

    earliest_time = None
    latest_time = None
    session_dict = defaultdict(lambda: [[], 0, 0])

    for line in f:
        line_parts = sanitize_line(line)
        if line_parts:
            date = line_parts[0]
            username = line_parts[1]
            session_state = line_parts[2]
            if not earliest_time:
                earliest_time = date
            if session_state == "Start":
                session_dict[username][0].append(date)
            else:
                if session_dict.get(username, [[]])[0]:
                    start_date = session_dict[username][0].pop(0)
                else:
                    start_date = earliest_time
                difference_seconds = (date - start_date).total_seconds()
                session_dict[username][1] += 1
                session_dict[username][2] += difference_seconds

            latest_time = date

    for username, details in session_dict.items():
        for start_time in details[0]:
            difference_seconds = (latest_time - start_time).total_seconds()
            session_dict[username][1] += 1
            session_dict[username][2] += difference_seconds

        session_dict[username][0] = []
        print("{} {} {}".format(username, details[1], details[2]))

    f.close()

if __name__ == "__main__":

    total_args = len(sys.argv)
    if total_args < 2:
        print("Please provide a file path to logs")
    else:
        file_path = sys.argv[1]
        calculate_session(file_path)