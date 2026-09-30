"""Read a Journal v15 export; write private aggregates without journal prose."""
import json
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime
from zoneinfo import ZoneInfo

def analyze(data):
    tz = ZoneInfo('America/New_York')
    units = {u['id']: u for u in data.get('customUnits', [])}
    events = [i for e in data['experiences'] for i in e.get('ingestions', [])]
    own = [i for i in events if i.get('consumerName') is None]
    rows = []
    for i in own:
        u = units.get(i.get('customUnitId'), {})
        if u.get('name') not in ('Adderall XR', 'Adderall IR'):
            continue
        components = u.get('doseComponents', [])
        c = components[0] if len(components) == 1 else {}
        valid = (c.get('substanceName') == 'Amphetamine' and c.get('substanceUnit') == 'mg'
                 and isinstance(c.get('dose'), (int, float)) and isinstance(i.get('dose'), (int, float)))
        stamp = datetime.fromtimestamp(i['time']/1000, tz)
        rows.append({'date': stamp.date().isoformat(), 'month': stamp.strftime('%Y-%m'),
                     'hour': stamp.hour + stamp.minute/60, 'time': i['time'],
                     'form': u['name'].split()[-1], 'route': i['administrationRoute'],
                     'mg': i['dose'] * c['dose'] if valid else None,
                     'estimated': bool(i.get('isDoseAnEstimate') or c.get('isEstimate'))})
    dates = sorted({r['date'] for r in rows})
    byday = defaultdict(list)
    for r in rows: byday[r['date']].append(r)
    months = defaultdict(lambda: {'XR':0, 'IR':0, 'XR_count':0, 'IR_count':0})
    for r in rows:
        months[r['month']][r['form']+'_count'] += 1
        if r['mg'] is not None: months[r['month']][r['form']] += r['mg']
    both = sum({r['form'] for r in rs} == {'XR','IR'} for rs in byday.values())
    names = Counter(units.get(i.get('customUnitId'), {}).get('name') or i.get('substanceName') or 'Unresolved' for i in own)
    stats = {'exportSource':data.get('exportSource'), 'experiences':len(data['experiences']),
        'allIngestions':len(events), 'ownIngestions':len(own), 'otherIngestions':len(events)-len(own),
        'ratings':sum(len(e.get('ratings',[])) for e in data['experiences']),
        'timedNotes':sum(len(e.get('timedNotes',[])) for e in data['experiences']),
        'adderallEvents':len(rows), 'adderallDays':len(dates), 'bothDays':both,
        'first': dates[0] if dates else None, 'last':dates[-1] if dates else None, 'unknownDose':sum(r['mg'] is None for r in rows),
        'estimated':sum(r['estimated'] for r in rows), 'forms':dict(Counter(r['form'] for r in rows)),
        'routes':dict(Counter(r['route'] for r in rows)), 'topProducts':names.most_common(10),
        'monthly':[{'month':m, **v} for m,v in sorted(months.items())],
        'recentDays':[{'date':d,'events':byday[d]} for d in dates[-14:]]}
    return stats

if __name__ == '__main__':
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument('input', nargs='?', default='private/journal.json')
    p.add_argument('--output', default='private/summary.json')
    args=p.parse_args()
    result=analyze(json.loads(Path(args.input).read_text(encoding='utf-8-sig')))
    Path(args.output).write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('monthly','recentDays','topProducts')},indent=2))
