"""Stream Germany PBF; write validated per-direction GeoJSON and audit manifest atomically."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
from datetime import datetime, timezone, date
from pipeline.classify import classify, CATEGORIES

def length_km(points):
    total = 0
    for (a,b),(c,d) in zip(points, points[1:]):
        x,y=math.radians(d-b),math.radians(c-a)
        h=math.sin(x/2)**2+math.cos(math.radians(b))*math.cos(math.radians(d))*math.sin(y/2)**2
        total += 6371.0088*2*math.asin(min(1,math.sqrt(h)))
    return total

def valid_geometry(points):
    return len(points)>1 and all(len(p)==2 and all(math.isfinite(v) for v in p) and -180<=p[0]<=180 and -90<=p[1]<=90 for p in points) and length_km(points)>0

def load_overrides(path):
    entries=json.loads(Path(path).read_text()); out={}
    for e in entries:
        required=('id','classification','source','reason','reviewed_at','tags_sha256')
        if any(not e.get(k) for k in required) or e['classification'] not in CATEGORIES:
            raise ValueError('Unvollständige manuelle Korrektur')
        if not e['source'].startswith(('https://','http://')) or date.fromisoformat(e['reviewed_at'])>date.today():
            raise ValueError('Ungültige Quelle/Prüfdatum')
        if e['id'] in out: raise ValueError('Doppelte Korrektur')
        out[e['id']]=e
    return out

def tag_hash(tags):
    return hashlib.sha256(json.dumps(tags,sort_keys=True,ensure_ascii=False).encode()).hexdigest()

def process_way(way_id, tags, points, snapshot, overrides):
    if not valid_geometry(points): raise ValueError('Leere/ungültige Geometrie')
    directions=['backward'] if tags.get('oneway')=='-1' else ['forward','backward'] if tags.get('oneway')=='no' else ['forward']
    features=[]
    for direction in directions:
        ident=f'{way_id}:{direction}'; verdict=classify(tags,direction); override=overrides.get(ident)
        verification='OSM-Auswertung'
        if override:
            if override['tags_sha256'] != tag_hash(tags):
                verdict={'classification':'unknown','reason':'Manuelle Prüfung durch geänderte OSM-Tags veraltet'}
                verification='Erneute Prüfung erforderlich'
            else:
                verdict={k:override[k] for k in ('classification','reason')}; verification='Manuell geprüft'
        props={'id':ident,'osm_id':str(way_id),'ref':tags.get('ref','Ohne Nummer'),'direction':direction,'length_km':round(length_km(points),5),'tags':tags,'tags_sha256':tag_hash(tags),'snapshot':snapshot,'verification':verification,'override':override,**verdict}
        features.append({'type':'Feature','id':ident,'properties':props,'geometry':{'type':'LineString','coordinates':points}})
    return features

def file_hash(path):
    with open(path,'rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()

def validate_totals(count, rejected, lengths, scope):
    total=sum(lengths.values())
    if rejected > max(5,count*.01): raise ValueError('Zu viele ungültige Geometrien')
    if count<1 or total<1: raise ValueError('Leerer/unplausibler Datensatz')
    if scope == 'Deutschland (Geofabrik-Extrakt)' and not 15000 <= total <= 50000:
        raise ValueError('Deutschland-Fahrtrichtungslänge außerhalb großzügigem Plausibilitätsbereich 15.000–50.000 km')

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('pbf'); parser.add_argument('--snapshot',required=True,help='UTC extract snapshot, ISO 8601'); parser.add_argument('--source',default='https://download.geofabrik.de/europe/germany.html'); parser.add_argument('--scope',default='Deutschland (Geofabrik-Extrakt)'); parser.add_argument('--output',default='public/data'); parser.add_argument('--overrides',default='data/overrides.json'); args=parser.parse_args()
    datetime.fromisoformat(args.snapshot.replace('Z','+00:00'))
    import osmium
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    overrides=load_overrides(args.overrides); used=set(); counts={k:0 for k in CATEGORIES}; lengths={k:0.0 for k in CATEGORIES}; count=0; rejected=0
    geo=out/'segments.geojson.tmp'; audit=out/'audit.jsonl.tmp'
    with geo.open('w') as stream, audit.open('w') as log:
        stream.write('{"type":"FeatureCollection","features":[')
        class Handler(osmium.SimpleHandler):
            def way(self,w):
                nonlocal count,rejected
                tags=dict(w.tags)
                if tags.get('highway')!='motorway': return
                try:
                    points=[[round(n.lon,6),round(n.lat,6)] for n in w.nodes]
                    features=process_way(w.id,tags,points,args.snapshot,overrides)
                except (ValueError,osmium.InvalidLocationError) as exc:
                    rejected+=1; log.write(json.dumps({'osm_id':w.id,'error':str(exc)})+'\n'); return
                for feature in features:
                    p=feature['properties']; used.add(p['id']); counts[p['classification']]+=1; lengths[p['classification']]+=p['length_km']
                    if p['length_km']>200: raise ValueError('Unplausible Way-Länge >200 km')
                    if count: stream.write(',')
                    stream.write(json.dumps(feature,ensure_ascii=False,separators=(',',':'))); count+=1
                    if p['classification'] in ('unknown','unlimited_candidate'): log.write(json.dumps(p,ensure_ascii=False)+'\n')
        Handler().apply_file(args.pbf,locations=True,idx='sparse_file_array,'+str(out/'node-index.tmp'))
        stream.write(']}')
    validate_totals(count,rejected,lengths,args.scope)
    if set(overrides)-used: raise ValueError('Verwaiste manuelle Korrekturen: '+str(set(overrides)-used))
    manifest={'mode':'osm','snapshot':args.snapshot,'generated_at':datetime.now(timezone.utc).isoformat(),'source':args.source,'scope':args.scope,'license':'ODbL-1.0','length_unit':'Fahrtrichtungskilometer','counts':counts,'lengths_km':lengths,'rejected':rejected,'sha256':hashlib.sha256(geo.read_bytes()).hexdigest(),'input_sha256':file_hash(args.pbf)}
    (out/'manifest.json.tmp').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
    for name in ('segments.geojson','audit.jsonl','manifest.json'): os.replace(out/(name+'.tmp'),out/name)
    (out/'node-index.tmp').unlink(missing_ok=True)
if __name__=='__main__': main()
