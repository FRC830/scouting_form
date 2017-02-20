# Run from command line as:
# python fetch_event_schedule.py <match_url> <event_name>
# URLs should come from http://frc-events.usfirst.org/...
# example: "http://frc-events.usfirst.org/2016/MILAK/qualifications"

import requests, json, sys, os

HEADER = {"X-TBA-App-Id":"frc830:scoutingform:v2017"}
URL = "https://www.thebluealliance.com/api/v2/event/%s/matches"

class FetchError(Exception):
    pass

def fetch(source, filename):
    try:
        if '\\' in filename:
            raise FetchError("Illegal character in filename: \\")

        save_path = os.path.join('match_schedules',filename+'.json')
        if os.path.exists(save_path):
            raise FetchError("A file with that name already exists")
        if not filename:
            raise FetchError("A file name must be provided")

        r = requests.get(URL %source, headers = HEADER)
        data = r.json()
        schedule = {}

        for match in data:
        	if match["comp_level"] != "qm":
        		continue
        	red = match["alliances"]["red"]["teams"]
        	blue = match["alliances"]["blue"]["teams"]
        	teams = {}
        	for i in range (3):
        		teams["Blue " + str(i+1)] = blue[i][3:]
        		teams["Red " + str(i+1)] = red[i][3: ]
        	schedule[match["match_number"]] = teams

        if schedule == {}:
            raise FetchError("No schedule data found on this URL.")
        try:
            with open(save_path, 'w') as f:
                f.write(json.dumps(schedule))
        except OSError:
            raise FetchError("Invalid filename")
    except FetchError as e:
        return str(e), False
    except Exception as e:
        return "An unknown error occurred: [" + type(e).__name__ + "] " + str(e), False
    else:
        return "Success! Schedule saved to: "+save_path, True

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Requires 2 command line arguments (event code, event name): %i given" %(len(sys.argv)-1))
        sys.exit()
    print(fetch(sys.argv[1], sys.argv[2])[0])
