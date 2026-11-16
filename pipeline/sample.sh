#!/usr/bin/env bash
set -euo pipefail
mkdir -p .cache
curl --fail --location --retry 3 https://download.geofabrik.de/europe/germany/saarland-latest.osm.pbf -o .cache/saarland.osm.pbf
snapshot=$(python -c "import osmium; r=osmium.io.Reader('.cache/saarland.osm.pbf'); print(r.header().get('osmosis_replication_timestamp')); r.close()")
python -m pipeline.build .cache/saarland.osm.pbf --snapshot "$snapshot" --source https://download.geofabrik.de/europe/germany/saarland.html --scope 'Regionaler Testdatensatz · Saarland' --output public/data
