# Run from command line as:
# python fetch_event_schedule.py <match_url> <event_name>
# URLs should come from http://frc-events.usfirst.org/...
# example: "http://frc-events.usfirst.org/2016/MILAK/qualifications"

import bs4, json, sys, os
if sys.version[0] == '2':
    from urllib2 import urlopen
else:
    from urllib.request import urlopen

if len(sys.argv) != 3:
    print("Requires 2 command line arguments (schedule url, event name): %i given" %(len(sys.argv)-1))
    sys.exit()

save_path = os.path.join('match_schedules',sys.argv[2]+'.json')
if os.path.exists(save_path):
    print("An event schedule with that name already exists. Choose a different event name")
    sys.exit()

if sys.argv[1].startswith('http'):
    src = urlopen(sys.argv[1]).read()
else:
    src = open(sys.argv[1]).read()
b = bs4.BeautifulSoup(src,'html.parser')
rows = b.find_all('tr', class_='hidden-xs')
# assert len(rows) == 80
data = {}
for i, r in enumerate(rows):
    match_id = i + 1
    data[match_id] = {}
    for j, td in enumerate(r.find_all('td', class_='danger')):
        data[match_id]['Red ' + str(j + 1)] = int(td.text)
    for j, td in enumerate(r.find_all('td', class_='info')):
        data[match_id]['Blue ' + str(j + 1)] = int(td.text)

if data == {}:
    print("No schedule data found on this URL. Check that it is in the format 'http://frc-events.usfirst.org/.../qualifications'")
    sys.exit()
with open(save_path, 'w') as f:
    f.write(json.dumps(data))
