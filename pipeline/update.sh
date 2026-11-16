#!/usr/bin/env bash
set -euo pipefail
mkdir -p .cache
# Geofabrik headers record the authoritative extract timestamp.
curl --fail --location --retry 3 --dump-header .cache/headers.txt https://download.geofabrik.de/europe/germany-latest.osm.pbf -o .cache/germany.osm.pbf.part
mv .cache/germany.osm.pbf.part .cache/germany.osm.pbf
snapshot=$(python -c "from email.utils import parsedate_to_datetime; from pathlib import Path; h=Path('.cache/headers.txt').read_text(); print(parsedate_to_datetime([x.split(':',1)[1].strip() for x in h.splitlines() if x.lower().startswith('last-modified:')][-1]).isoformat())")
python -m pipeline.build .cache/germany.osm.pbf --snapshot "$snapshot" --output .cache/output
# Publish only a complete successful generation.
python -c "import shutil; from pathlib import Path; p=Path('public/data'); p.mkdir(parents=True,exist_ok=True); [shutil.copy2(f,p/f.name) for f in Path('.cache/output').iterdir() if f.is_file()]"
