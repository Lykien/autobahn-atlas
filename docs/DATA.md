# Klassifikationsregeln und Datenquellen

## Evidenz und Priorität

1. Geometrie muss aus mindestens zwei gültigen WGS84-Punkten bestehen und eine positive Länge haben. Fehlerhafte Ways werden protokolliert; >200 km pro Way bricht den Lauf ab.
2. Richtungsbezogene Werte überschreiben generische Angaben. Abweichende Fahrstreifenangaben bleiben `unknown`.
3. Explizite temporäre/Baustellenmarker erzwingen `unknown`, solange keine unabhängige manuelle Evidenz für den Grundzustand vorliegt. Ein numerischer aktueller Wert wird niemals durch Vermutung in `none` umgewandelt.
4. `maxspeed=none` bestätigt den unbegrenzten Grundwert. Einfache numerische Bedingungen `100 @ (wet)` oder Zeitbedingungen ändern die Basisklassifikation nicht. Komplexe/nicht unterstützte Bedingungen ergeben `unlimited_candidate`. Die Syntaxprüfung interpretiert Bedingungen nicht als aktuellen Verkehrsstatus.
5. `signals`, `variable` oder `maxspeed:variable` ohne expliziten eindeutigen Grundwert ergeben `unlimited_candidate`, keine bestätigte unbegrenzte Strecke.
6. Numerischer Grundwert ohne temporäre Marker/bedingte Ausnahmen ergibt `limited_confirmed`. Mit bedingten Ausnahmen ergibt er konservativ `unknown`.
7. Fehlende Werte, `DE:motorway`, unklare Werte, nur bedingte Angaben: `unknown`. Die deutsche Rechtslage ersetzt keinen expliziten Beleg. Keine Klassifikation anhand von `source:maxspeed` allein.
8. Dokumentierte manuelle Prüfung kann die automatisierte Klassifikation überschreiben. Geänderte Tags invalidieren sie. Verwaiste IDs stoppen den Lauf.

`limited_confirmed` bedeutet auf Basis vorhandener OSM-Tags belegt, keine amtliche Verifikation. Nicht als temporär getaggte Baustellen können aus einem numerischen OSM-Tag nicht erkannt werden. Das ist eine bekannte Datenlücke, keine Aussage über die tatsächliche Anordnung.

## Quellenprüfung

- Geofabrik Deutschland: https://download.geofabrik.de/europe/germany.html – effiziente landesweite PBF-Quelle; pyosmium liest streamend, Locations werden mit plattenbasiertem Node-Index aufgelöst. PBF-Quelle/Snapshot und Ausgabedatei-Hash im Manifest.
- OSM-Schema: https://wiki.openstreetmap.org/wiki/Key:maxspeed , https://wiki.openstreetmap.org/wiki/Key:maxspeed:conditional , https://wiki.openstreetmap.org/wiki/Conditional_restrictions . Tags sind nicht überall vollständig oder konsistent.
- OSM-Historie: https://wiki.openstreetmap.org/wiki/OSM_history – Way-Historie kann frühere `none`-Werte zeigen, beweist aber ohne aktuelle Prüfung weder das Ende einer Baustelle noch einen unveränderten Regelzustand. Geofabrik-Latest ist kein History-Extrakt. Keine automatische Rückprojektion historischer Werte.
- Autobahn-Verkehrs-/Baustellenmeldungen (https://verkehr.autobahn.de/) beschreiben aktuelle Ereignisse; keine hier nachgewiesene flächendeckende Quelle für den unbegrenzten Grundzustand. Deshalb keine ungeprüfte Verschneidung und kein frei erfundener historischer Status. Konkrete öffentlich belegbare Angaben können manuell geprüft werden.

## Grenzen

Wechselverkehrszeichen im ausgeschalteten Zustand, verdeckte temporäre numerische Tags, Baustellen ohne Grundwert, komplexe Bedingungen, historische Way-Splits und veraltete OSM-Tags benötigen zusätzliche Evidenz. Keine Liveverkehrsdaten, keine amtliche Rechtsauskunft, keine garantierte Aktualität. Die Richtgeschwindigkeit 130 km/h wird nicht als Dauerlimit abgeleitet. Numerisch explizites `maxspeed=130` wird dagegen als angeordnetes Limit interpretiert.

Länge: Haversine-Summe über ursprüngliche OSM-Knoten (Radius 6371,0088 km), vor jeder Visualisierung. Kein vereinfachtes Kartenmaß und keine doppelte Addition identischer Way-ID/Richtung. Gegenläufige Fahrbahnen sind bewusst getrennte Einheiten. Die Gesamtsumme des Vollnetzes sollte vor einem Release mit unabhängigen Fahrbahnlängen verglichen werden; unterschiedliche Definitionen verhindern einen pauschalen Vergleich mit physischer Netzlänge.

Die Deutschlandpipeline akzeptiert als grobe Fehlererkennung nur 15.000–50.000 Fahrtrichtungskilometer und bricht bei mehr als 1 % (mindestens sechs) verworfenen Geometrien ab. Diese großzügigen technischen Schranken ersetzen keine fachliche Vollständigkeitsprüfung.
