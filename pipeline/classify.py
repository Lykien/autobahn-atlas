"""Conservative classification of explicit OSM evidence, per travel direction."""
import re

CATEGORIES = ('unlimited_confirmed', 'limited_confirmed', 'unlimited_candidate', 'unknown')

def classify(tags, direction='forward'):
    def result(status, reason):
        return {'classification': status, 'reason': reason}
    value = tags.get('maxspeed:' + direction, tags.get('maxspeed', '')).strip().lower()
    conditional = tags.get('maxspeed:' + direction + ':conditional', tags.get('maxspeed:conditional', ''))
    temporary = any(k.startswith(('maxspeed:temporary', 'temporary:maxspeed', 'construction:maxspeed')) for k in tags) or tags.get('temporary') == 'yes' or tags.get('construction') not in (None, 'no')
    variable = value in ('signals', 'variable') or tags.get('maxspeed:variable') not in (None, 'no')
    lanes = tags.get('maxspeed:lanes:' + direction, tags.get('maxspeed:lanes', ''))
    if lanes and any(x.strip() != value for x in lanes.split('|')):
        return result('unknown', 'Widersprüchliche oder abweichende Fahrstreifenangaben')
    if temporary:
        return result('unknown', 'Temporäre Beschränkung/Baustelle: Grundzustand nicht unabhängig belegt')
    if value == 'none':
        if conditional and not re.fullmatch(r'\s*\d+(?:\s*km/h)?\s*@\s*\([^;]+\)(?:\s*;\s*\d+(?:\s*km/h)?\s*@\s*\([^;]+\))*\s*', conditional):
            return result('unlimited_candidate', 'Unbegrenzter Grundwert, komplexe Bedingung ungeprüft')
        return result('unlimited_confirmed', 'Explizites maxspeed=none; Bedingungen können zeitweise begrenzen')
    if variable:
        return result('unlimited_candidate', 'Wechselverkehrszeichen; ausgeschalteter Grundzustand nicht belegt')
    if re.fullmatch(r'[1-9]\d{0,2}(?:\s*km/h)?', value):
        if conditional:
            return result('unknown', 'Numerischer Grundwert mit bedingter Ausnahme: Regelzustand prüfen')
        return result('limited_confirmed', 'Expliziter numerischer Grundwert ohne Hinweis auf temporäre Geltung')
    return result('unknown', 'Kein eindeutiger expliziter Grundwert; keine Ableitung aus fehlenden Tags')
