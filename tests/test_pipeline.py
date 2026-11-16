import unittest
import tempfile
import json
from pathlib import Path
from pipeline.classify import classify
from pipeline.build import process_way, valid_geometry, length_km, load_overrides, tag_hash, validate_totals

class ClassificationTests(unittest.TestCase):
    def test_cases(self):
        cases=[({},'unknown'),({'maxspeed':'none'},'unlimited_confirmed'),({'maxspeed':'120'},'limited_confirmed'),({'maxspeed':'signals'},'unlimited_candidate'),({'maxspeed:conditional':'none @ (22:00-06:00)'},'unknown'),({'maxspeed':'none','maxspeed:conditional':'100 @ (wet)'},'unlimited_confirmed'),({'maxspeed':'120','temporary':'yes'},'unknown'),({'maxspeed':'none','construction':'motorway'},'unknown'),({'maxspeed':'80','construction:maxspeed':'80'},'unknown'),({'maxspeed':'none','maxspeed:conditional':'signals @ (traffic)'},'unlimited_candidate'),({'maxspeed':'120','maxspeed:conditional':'none @ (22:00-06:00)'},'unknown'),({'maxspeed':'DE:motorway'},'unknown'),({'maxspeed':'none','maxspeed:lanes':'none|100'},'unknown')]
        for tags,want in cases:
            with self.subTest(tags=tags): self.assertEqual(classify(tags)['classification'],want)
    def test_directions(self):
        t={'maxspeed':'120','maxspeed:forward':'none','oneway':'no'}
        f=process_way(1,t,[[10,50],[10.01,50]],'2026-01-01',{})
        self.assertEqual([x['properties']['classification'] for x in f],['unlimited_confirmed','limited_confirmed'])
        t['oneway']='-1'; self.assertEqual(process_way(1,t,[[10,50],[10.01,50]],'',{})[0]['properties']['direction'],'backward')
    def test_geometry(self):
        for p in ([],[[10,50]],[[10,50],[10,50]],[[200,50],[10,50]],[[float('nan'),50],[10,50]]): self.assertFalse(valid_geometry(p))
        self.assertAlmostEqual(length_km([[0,0],[1,0]]),111.195,places=2)
    def test_override_staleness(self):
        t={'maxspeed':'80','temporary':'yes'}
        o={'1:forward':{'classification':'unlimited_confirmed','reason':'Beleg','tags_sha256':tag_hash(t)}}
        f=process_way(1,t,[[10,50],[11,50]],'',o)[0]
        self.assertEqual(f['properties']['verification'],'Manuell geprüft')
        t['maxspeed']='60'
        self.assertEqual(process_way(1,t,[[10,50],[11,50]],'',o)[0]['properties']['classification'],'unknown')
    def test_override_requires_provenance(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'o.json'; p.write_text(json.dumps([{'id':'1:forward'}]))
            with self.assertRaises(ValueError): load_overrides(p)

    def test_total_guard(self):
        with self.assertRaises(ValueError): validate_totals(2,0,{'unknown':3},'Deutschland (Geofabrik-Extrakt)')
        with self.assertRaises(ValueError): validate_totals(100,10,{'unknown':20000},'Deutschland (Geofabrik-Extrakt)')
        validate_totals(10000,0,{'unknown':27000},'Deutschland (Geofabrik-Extrakt)')
    def test_directional_conditions(self):
        t={'maxspeed':'none','maxspeed:forward:conditional':'signals @ (traffic)','maxspeed:backward':'100'}
        self.assertEqual(classify(t,'forward')['classification'],'unlimited_candidate')
        self.assertEqual(classify(t,'backward')['classification'],'limited_confirmed')
