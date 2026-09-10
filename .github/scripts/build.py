"""Regenerate README.md and assets/ for the profile repo.

    pip install fonttools uharfbuzz
    python .github/scripts/build.py

Edit content.py (projects, wins, stack, about) or palettes.py (colours) and re-run.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))       # repo root
sys.path.insert(0, HERE)
from style_theme import Theme

S = Theme()
assets = S.build()
os.makedirs(f"{ROOT}/assets", exist_ok=True)
for name, svg in assets.items():
    # stats/langs/activity are owned by gen_stats.py once the workflow has run; only seed them if missing
    if name in ("stats.svg", "langs.svg", "activity.svg") and os.path.exists(f"{ROOT}/assets/{name}") and "--force" not in sys.argv:
        continue
    open(f"{ROOT}/assets/{name}", "w").write(svg)
open(f"{ROOT}/README.md", "w").write(S.readme())
print(f"wrote README.md + {len(assets)} assets -> {ROOT}")
