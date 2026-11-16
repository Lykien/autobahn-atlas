# Freie Fahrt – Autobahn-Atlas

Statische, responsive Deutschlandkarte des **regulären**, nicht aktuellen Geschwindigkeitsstatus. React, TypeScript, Vite, MapLibre; Streaming-Datenpipeline mit Python/pyosmium. Keine API-Schlüssel, kein eigener Server.

## Lokal starten

Node 22+, Python 3.12+, für PBF-Verarbeitung ausreichend freier Speicher (Deutschland: mehrere GB Download, zusätzlicher Plattenplatz für Node-Index und Ausgabe; 20–40 GB einplanen).

```bash
npm ci
npm run dev
# http://localhost:5173
npm test
npm run build
npm run preview
```

Der ausgelieferte Datenumfang ist im `public/data/manifest.json` sichtbar. Ein regionaler Startdatensatz ist **keine vollständige Deutschlandauswertung**. Es werden keine Geschwindigkeitsdaten erfunden. Die Startansicht umfasst Deutschland, auch wenn der Datensatz nur eine Region enthält.

## Deutschlanddaten erzeugen

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# Debian/Ubuntu: sudo apt-get install osmium-tool
bash pipeline/update.sh
npm run build
```

Das Skript lädt Geofabriks Deutschland-PBF. Der `Last-Modified`-Header dokumentiert den Extraktstand (kein minutengenauer OSM-Änderungsstand). Download und Zwischenprodukte bleiben in `.cache`, nie in Git. Alternativ:

```bash
python -m pipeline.build /pfad/germany.osm.pbf --snapshot 2026-11-15T21:00:00Z --output public/data
```

Nur `highway=motorway`, keine Anschlussrampen, keine im Bau befindlichen neuen Autobahnen. OSM-Wege werden je Fahrtrichtung klassifiziert; Standard bei Autobahnen ist `oneway=yes`, `-1` und `no` werden berücksichtigt. Der Geofabrik-Extrakt definiert den Umfang; Randgeometrien können über die Grenze hinausreichen. Kein exakter administrativer Grenzschnitt. Keine Bundeslandzuordnung ohne gesonderte geprüfte Grenzdaten.

GeoJSON wird gestreamt geschrieben. Es enthält nur Autobahnen statt des gesamten PBF. MapLibre kachelt die geladene Quelle intern. Deutschlandweite GeoJSON-Größe und mobiler Speicherverbrauch sind vor produktiver Veröffentlichung zu messen; für hohe Last/zu große Dateien ist eine Umstellung auf PMTiles sinnvoll. Diese Version behauptet keine getestete Vollnetz-Performance.

## Manuelle Prüfung

Abschnitt anklicken, Prüfvorlage herunterladen, Felder `source` (öffentlich belegbare URL), `reason`, `reviewed_at` (ISO-Datum) ausfüllen. Eintrag in `data/overrides.json` aufnehmen und Pipeline erneut ausführen. Die Vorlage allein ist **keine** gültige Korrektur. IDs sind `OSM-Way-ID:forward` bzw. `:backward`. Der SHA-256 der geprüften Tags muss übereinstimmen; veränderte Tags setzen den Abschnitt auf `unknown`. Geometrieänderungen bei gleichen Tags werden derzeit nicht erkannt: regelmäßige Nachprüfung erforderlich. Entfernte/geteilte Ways führen bei verwaisten Overrides zum Abbruch. Quellen und Begründung bleiben in der veröffentlichten abgeleiteten Datenbank erhalten. Korrekturen werden nicht durch Updates überschrieben.

## GitHub Pages

1. Projekt samt `package-lock.json` in ein GitHub-Repository auf Branch `main` übertragen.
2. Settings → Pages → Source: **GitHub Actions** auswählen.
3. Workflow `Validate and deploy Pages` ausführen. Jeder veröffentlichende Lauf erzeugt zuerst Deutschlanddaten; Pull Requests verwenden den regionalen Datensatz.
4. Den vom Deployment-Job ausgegebenen Link öffnen.

`BASE_PATH` wird aus dem Repositorynamen gesetzt; für eine eigene Domain bzw. ein `user.github.io`-Repository auf `/` ändern. Pull Requests bauen und testen ohne Deployment. Montags läuft die Deutschlandpipeline erneut. Ein fehlgeschlagener Build/Datenlauf löst kein Deployment aus; die zuvor veröffentlichte Version bleibt bestehen. Neue Daten werden als Bestandteil des Pages-Artefakts veröffentlicht, nicht automatisch in Git committed. Auch Pushes und manuell gestartete Deployments erzeugen Deutschlanddaten neu; damit überschreibt kein regionaler Startdatensatz ein veröffentlichtes Vollnetz. Dies erfordert je Deployment einen größeren Download. Updates sind über GitHub-Workflowlogs und das Manifest nachvollziehbar. Keine Behauptung einer unveränderlichen Datenhistorie; für wissenschaftliche Reproduzierbarkeit PBF mit Hash extern archivieren.

## Daten, Nutzungsbedingungen und Grenzen

Details: [Klassifikation und Quellen](docs/DATA.md). `public/data/audit.jsonl` protokolliert ungeklärte/verwor­fene Fälle. Statistik berechnet Fahrtrichtungskilometer, **keine physische Autobahnlänge**. Beide getrennten Fahrbahnen zählen jeweils; `oneway=no` zählt jede Richtung einmal. Keine fingierte Halbierung.

Hintergrund: Standard-OSM-Rastertiles, sichtbare Attribution, keine Offline-/Bulk-Downloads. Nutzung nur im Rahmen von https://operations.osmfoundation.org/policies/tiles/ ; keine Verfügbarkeitsgarantie. Bei stärkerem Publikumsverkehr eigenen geeigneten Tile-Anbieter bzw. selbst statisch gehostete Kacheln einsetzen. Schriftarten sind lokale Systemschriften; es werden keine Google Fonts geladen. Die Segmentdaten funktionieren unabhängig von den Hintergrundtiles.

OSM-Daten © OpenStreetMap-Mitwirkende, ODbL 1.0 (https://www.openstreetmap.org/copyright). Abgeleitete Datenbank steht unter ODbL 1.0; GeoJSON und Manifest sind auf der Website herunterladbar. Änderungen/Korrekturen sind mit Quellen dokumentiert. Software: MIT (LICENSE). Rechtliche Hinweise sind Bestandteil der Oberfläche.

Der reale Saarland-Startdatensatz kann mit `bash pipeline/sample.sh` reproduziert werden (jeweils neuester Extrakt; den exakten historischen Stand mit dem im Manifest dokumentierten Input-Hash separat archivieren).

Die Deutschlandpipeline benötigt zusätzlich die CLI `osmium` (Debian/Ubuntu-Paket `osmium-tool`). Vor dem Aufbau des Knotenindex reduziert `osmium tags-filter` den Extrakt auf Autobahnen mit referenzierten Knoten. Der Input-Hash im Manifest bezieht sich auf diese gefilterte PBF-Datei.

Für eine schnelle erste Ansicht kann der manuelle Workflow **Publish regional preview** den mitgelieferten, sichtbar als regional gekennzeichneten Saarland-Datensatz veröffentlichen. Er ersetzt die dann veröffentlichte Karte; nur bewusst ausführen. Der reguläre Deutschlandworkflow veröffentlicht nach erfolgreichem Datenimport das vollständige Netz.

## Rechtlicher Prüfstand

Siehe [Prüfbericht](docs/LEGAL_REVIEW.md). Anbieterkennzeichnung und vollständige Datenschutzangaben sind noch offen; privater Hobbybetrieb ist keine pauschale Befreiung. Das Projekt wird nicht als rechtssicher freigegeben. Die technischen Verbesserungen übernehmen keine persönlichen Kontaktdaten.
