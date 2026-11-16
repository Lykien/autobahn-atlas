# Rechtlicher und technischer Prüfstand – 16.11.2026

Prüfumfang: Quellcode, bereitgestelltes Manifest, npm-Lizenzmaterial und veröffentlichte Konfiguration. Kein anwaltliches Gutachten, keine Freigabe als rechtssicher, kein visueller Browser-/Cookie-Netzwerktest. Betreiberangabe: privates Hobby ohne Werbung/Einnahmen; keine Freigabe persönlicher Kontaktdaten.

## Offene Punkte vor einer rechtlichen Freigabe

1. **Anbieterkennzeichnung:** Auf der aktuellen Website fehlt ein Impressum. Eine an die Allgemeinheit gerichtete Informationskarte dürfte über ausschließlich persönliche/familiäre Zwecke hinausgehen. § 18 Abs. 1 MStV spricht deshalb auch ohne Einnahmen für Name und ladungsfähige Anschrift. Ob zusätzlich § 5 DDG oder bei redaktionellem Ausbau § 18 Abs. 2 MStV eingreift, ist einzelfallabhängig. Ein GitHub-Nutzername, ein Disclaimer oder eine E-Mail ersetzen die erforderliche Anschrift nicht.
2. **Privatanschrift schützen:** Eine tatsächlich zustellfähige Geschäfts- oder geeignete c/o-Adresse kann je nach Gestaltung verwendbar sein. Bei Impressumsdiensten gerichtliche Zustellung, Empfangsvollmacht, Nutzungsrecht, tatsächliche Erreichbarkeit und Vertragsbedingungen individuell prüfen; ein Postfach oder eine reine Briefweiterleitung reicht nicht automatisch. Keine Empfehlung eines ungeprüften Anbieters. Andere Stelle kann nur dann Betreiber sein, wenn sie das Angebot tatsächlich verantwortet.
3. **Datenschutzinformation:** Es fehlt eine leicht erreichbare, zum tatsächlichen Betrieb passende Erklärung nach Art. 13 DSGVO. Verantwortlicher, Kontakt, Zwecke, Rechtsgrundlagen, Empfänger, Speicherdauer/-kriterien, Betroffenenrechte, zuständige Aufsicht und gegebenenfalls Drittlandtransfers müssen geklärt werden. Die öffentliche Karte nicht pauschal als DSGVO-freie Haushaltstätigkeit behandeln.
4. **GitHub Pages:** GitHub protokolliert laut eigener Dokumentation Besucher-IP-Adressen zur Sicherheit. Internationale Verarbeitung ist laut GitHub-Erklärung möglich; Betreiberrolle, anwendbare Hosting-Vertragsbedingungen und ggf. Anforderungen aus Art. 28/44 ff. DSGVO gesondert prüfen. Keine erfundene Aufbewahrungsdauer und keine pauschale Behauptung, ein AV-Vertrag sei abgeschlossen. Falls dies nicht passend abbildbar ist, Hosting bei einem geeigneten EU-Anbieter mit passenden Vertragsbedingungen erwägen.
5. **Externe Hintergrundkarte:** OSM-Kacheln werden derzeit direkt beim Seitenaufruf geladen. Dabei erhalten OSMF bzw. ihre Infrastruktur IP-Adresse, Browser-/Verbindungsdaten, Referrer und angefragte Kachelkoordinaten. Keine GPS-Ortung der Besucher implementiert; Kachelkoordinaten sind der angezeigte Kartenausschnitt. Rechtsgrundlage und Informationen dazu dokumentieren. Eine Zwei-Klick-Lösung oder selbst gehostete Hintergrundkarte kann Datenflüsse verringern, ersetzt aber nicht die Betreiber-/Hostingprüfung.
6. **Cookies/Tracking:** Im eigenen Anwendungscode keine Analytics, Werbung, Trackingpixel, Local-/Session-Storage oder Cookie-Schreibzugriffe gefunden. Deshalb kein pauschaler Bedarf für ein Marketing-Cookiebanner aus dem Code ableitbar. Providerverhalten wurde nicht im Browser gemessen. § 25 TDDDG ist von der allgemeinen Rechtmäßigkeit der personenbezogenen Datenverarbeitung nach DSGVO zu unterscheiden; „keine Cookies“ heißt nicht „keine Datenverarbeitung“.
7. **Haftung/Qualität:** Der sichtbare Hinweis zu Verkehrszeichen und fehlender Amtlichkeit ist sinnvoll, aber kein vollständiger Haftungsausschluss. Keine verbindliche Aussage zur tatsächlichen Zulässigkeit einer Geschwindigkeit, keine Vollständigkeits-/Aktualitätsgarantie. Die Kategorien bleiben technische, evidenzbasierte Auswertungen; die Regeln und der regionale Umfang sind offengelegt. Weiterhin unsichere Daten konservativ behandeln.
8. **Name/Marken:** Keine Marken-/Titelschutzrecherche für „freie fahrt“ vorgenommen. Keine fremden Logos oder amtlichen Wappen eingebunden. Vor kommerziellem Ausbau gesondert prüfen.

## Technische Verbesserungen in diesem Änderungsstand

- Google-Fonts-Import entfernt, ausschließlich lokale Systemschriften: keine vom Projekt veranlassten Schriftabrufe an Google mehr.
- OSM-Attribution in MapLibre explizit nicht eingeklappt; zusätzliche ausgeschriebene Namensnennung auf der Karte.
- ODbL-Notice im Datenverzeichnis mit Herkunft, Bearbeitung und Link zur vollständigen abgeleiteten GeoJSON-Datenbank.
- Vollständige Lizenz-/Copyrightmaterialien der npm-Laufzeitabhängigkeiten automatisch in `public/THIRD_PARTY_NOTICES.txt`, bei jedem Build neu erzeugt und auf der Website verlinkt.
- Keine persönliche Anschrift oder E-Mail aus Kontoprofilen übernommen und keine unvollständige Muster-Datenschutzerklärung als fertige Erklärung veröffentlicht.

Die Ergänzungen reduzieren konkrete technische/Lizenzlücken. Sie schließen die offenen Betreiber- und Datenschutzfragen nicht. Eine fertige Anbieterkennzeichnung kann erst mit einer tatsächlich geeigneten und ausdrücklich freigegebenen Adresse ergänzt werden.

## Primärquellen

- § 18 MStV: https://www.gesetze-bayern.de/Content/Document/MStV-18
- Medienaufsicht zur Impressumspflicht: https://www.ma-hsh.de/aufsicht/impressumspflicht.html
- Ladungsfähige Anschrift: https://www.lfk.de/service/dokumente-rechtsgrundlagen/leitfaden-zur-impressumspflicht-im-internet
- IHK zu möglicher c/o-Adresse (branchenspezifische Erläuterung, kein pauschaler Freibrief): https://www.ihk.de/berlin/service-und-beratung/recht-und-steuern/gewerberecht/erlaubnis-registrierungsverfahren-ihk/impressum-6179844
- § 5 DDG: https://www.gesetze-im-internet.de/ddg/__5.html
- DSGVO: https://eur-lex.europa.eu/eli/reg/2016/679/oj
- § 25 TDDDG: https://www.gesetze-im-internet.de/ttdsg/__25.html
- GitHub Pages/IP-Protokollierung: https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages
- GitHub-Datenschutz: https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement
- OSMF-Datenschutz: https://osmfoundation.org/wiki/Privacy_Policy
- OSM-Kachelnutzungsbedingungen: https://operations.osmfoundation.org/policies/tiles/
- OSM-Attribution: https://osmfoundation.org/wiki/Licence/Attribution_Guidelines
- ODbL: https://opendatacommons.org/licenses/odbl/1-0/
