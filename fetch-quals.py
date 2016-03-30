import bs4, json, sys
if sys.version[0] == '2':
    from urllib2 import urlopen
else:
    from urllib.request import urlopen
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
print(json.dumps(data))
