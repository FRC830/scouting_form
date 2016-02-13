import csv, os, threading

fields = [
	"match_id",
    "team_id",
    "auton_start",
    "auton_breach",
    "auton_score",
    "lb_breach",
    "pc_breach",
    "cf_breach",
    "mo_breach",
    "rp_breach",
    "db_breach",
    "sp_breach",
    "rw_breach",
    "rt_breach",
    "breach_count",
    "high_scores",
    "high_misses",
    "low_scores",
    "fouls",
    "tech_fouls",
    "defense",
    "hang",
    "comments"
]

def getlines(f):
	return list(filter(len, map(lambda line: line.rstrip('\r\n'), f.readlines())))

_export_lock = threading.Lock()
def save_data(data, path):
    with _export_lock:
        add_headers = False
        if not os.path.exists(path):
            add_headers = True
            contents = ''
        else:
            with open(path, 'r') as f:
                lines = getlines(f)
                if not len(lines) or not lines[0].startswith(fields[0]):
                    add_headers = True
                    contents = '\n'.join(lines) + '\n'
        if add_headers:
            with open(path, 'w') as f:
                writer = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
                writer.writeheader()
                f.write(contents)
        with open(path, 'a') as f:
            writer = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
            writer.writerow(data)
        lines = []
        with open(path, 'r') as f:
            lines = getlines(f)
        if len(lines) > 2 and lines[-1] == lines[-2]:
            with open(path, 'w') as f:
                f.write('\n'.join(lines[:-1]))
                f.write('\n')

def process(data):
    for f in fields:
        if f not in data:
            data[f] = 0
    return data