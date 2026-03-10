"""
AstroGuy AI — South Indian Birth Chart SVG Generator
=====================================================
CORRECT South Indian chart rules:
- 12 signs are FIXED in their boxes (Pisces always top-left, clockwise)
- Fixed layout: Pi Ar Ta Ge / Aq [  ] Ca / Cp [  ] Le / Sg Sc Li Vi
- Lagna (ascendant) is marked with diagonal lines in its sign box
- Houses are counted clockwise FROM the Lagna sign
- Planets go in their actual sign box (not house number box)
"""
from typing import Dict, List

# ── Fixed South Indian grid layout ──────────────────────────────────────────
# Sign numbers (1=Aries...12=Pisces) in grid position (col, row), 0-indexed
# Top row L→R:    Pisces(12) Aries(1)  Taurus(2)  Gemini(3)
# Right col T→B:  Cancer(4)  Leo(5)    Virgo(6)
# Bot row R→L:    Libra(7)   Scorpio(8) Sagittarius(9) Capricorn(10)
# Left col B→T:   Aquarius(11)
SIGN_POSITIONS = {
    12: (0,0),  1: (1,0),  2: (2,0),  3: (3,0),
    11: (0,1),                          4: (3,1),
    10: (0,2),                          5: (3,2),
     9: (0,3),  8: (1,3),  7: (2,3),  6: (3,3),
}

RASI_EN = {
    1:'Mesham',2:'Rishabam',3:'Midhunam',4:'Katakam',
    5:'Simmam',6:'Kanni',7:'Thulam',8:'Viruchigam',
    9:'Dhanusu',10:'Makaram',11:'Kumbam',12:'Meenam'
}
RASI_TA = {
    1:'மேஷம்',2:'ரிஷபம்',3:'மிதுனம்',4:'கடகம்',
    5:'சிம்மம்',6:'கன்னி',7:'துலாம்',8:'விருச்சிகம்',
    9:'தனுசு',10:'மகரம்',11:'கும்பம்',12:'மீனம்'
}
PLANET_SYM = {
    'Sun':'Su','Moon':'Mo','Mars':'Ma','Mercury':'Me',
    'Jupiter':'Ju','Venus':'Ve','Saturn':'Sa',
    'Rahu':'Ra','Ketu':'Ke','Lagna':'Lg'
}
PLANET_COL = {
    'Sun':'#FF8C00','Moon':'#C0C0FF','Mars':'#FF4444',
    'Mercury':'#44BB44','Jupiter':'#FFD700','Venus':'#FF69B4',
    'Saturn':'#8888FF','Rahu':'#AA44AA','Ketu':'#AA8844',
    'Lagna':'#00FFCC'
}
PLANET_INFO = {
    'Sun':    'Soul, ego, father, authority, vitality, government service.',
    'Moon':   'Mind, emotions, mother, water, public life, intuition.',
    'Mars':   'Energy, courage, siblings, property, engineering, surgery.',
    'Mercury':'Intelligence, communication, business, education, writing.',
    'Jupiter':'Wisdom, wealth, children, religion, teaching, expansion.',
    'Venus':  'Love, beauty, luxury, arts, marriage, vehicles, comfort.',
    'Saturn': 'Karma, discipline, longevity, service, delays, hard work.',
    'Rahu':   'Obsession, foreign, technology, sudden gains/losses, illusion.',
    'Ketu':   'Spirituality, liberation, past life, detachment, mysticism.',
    'Lagna':  'Ascendant — your body, personality, and life direction.',
}
HOUSE_MEANINGS = {
    1:'Self, personality, body, health, appearance',
    2:'Wealth, family, speech, food, early education',
    3:'Siblings, courage, communication, short journeys',
    4:'Mother, home, property, vehicles, education',
    5:'Children, intelligence, creativity, romance, past life merit',
    6:'Enemies, health issues, debts, service, daily routine',
    7:'Marriage, partnerships, business, foreign travel',
    8:'Longevity, transformation, secrets, inheritance, occult',
    9:'Luck, religion, father, higher education, dharma',
    10:'Career, status, reputation, government, public life',
    11:'Gains, income, elder siblings, social network, desires',
    12:'Expenses, liberation, foreign land, sleep, spirituality',
}


def _house_num(lagna_rasi: int, sign: int) -> int:
    """Return the house number for a given sign, counting clockwise from lagna."""
    return ((sign - lagna_rasi) % 12) + 1


def generate_birth_chart_svg(chart: Dict, size: int = 420) -> str:
    cell = size // 4
    pad  = 6
    svg  = []

    lagna_rasi = chart.get('lagna', {}).get('number', 1)

    # Build sign → list of planets
    sign_planets: Dict[int, List[str]] = {s: [] for s in range(1, 13)}
    sign_planets[lagna_rasi].append('Lagna')

    # Planet → sign number from chart dict
    def _rasi(key):
        v = chart.get(key)
        if isinstance(v, dict): return v.get('rasi', 0)
        return 0

    sign_planets[_rasi('sun') or chart.get('sun',{}).get('rasi',0)].append('Sun') if (_rasi('sun') or chart.get('sun',{}).get('rasi',0)) else None
    sign_planets[chart.get('rasi',{}).get('number',0)].append('Moon') if chart.get('rasi',{}).get('number',0) else None
    sign_planets[chart.get('mars',{}).get('rasi',0)].append('Mars') if chart.get('mars',{}).get('rasi',0) else None
    sign_planets[chart.get('mercury',{}).get('rasi',0)].append('Mercury') if chart.get('mercury',{}).get('rasi',0) else None
    sign_planets[chart.get('jupiter',{}).get('rasi',0)].append('Jupiter') if chart.get('jupiter',{}).get('rasi',0) else None
    sign_planets[chart.get('venus',{}).get('rasi',0)].append('Venus') if chart.get('venus',{}).get('rasi',0) else None
    sign_planets[chart.get('saturn',{}).get('rasi',0)].append('Saturn') if chart.get('saturn',{}).get('rasi',0) else None
    sign_planets[chart.get('rahu',{}).get('rasi',0)].append('Rahu') if chart.get('rahu',{}).get('rasi',0) else None
    sign_planets[chart.get('ketu',{}).get('rasi',0)].append('Ketu') if chart.get('ketu',{}).get('rasi',0) else None

    # Remove 0 entries
    sign_planets.pop(0, None)

    fs = int(cell * 0.16)  # font size

    svg.append(f'''<svg xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 {size} {size}" width="{size}" height="{size}"
      style="font-family:sans-serif;cursor:pointer" id="birthChartSvg">
  <defs><style>
    .hc{{fill:rgba(255,255,255,.04);stroke:rgba(255,215,0,.35);stroke-width:1.5;transition:fill .2s}}
    .hc:hover{{fill:rgba(255,215,0,.10)}}
    .hn{{fill:rgba(255,215,0,.45);font-size:{int(fs*.85)}px}}
    .rn{{fill:rgba(255,255,255,.55);font-size:{int(fs*.9)}px}}
    .pt{{font-size:{fs}px;font-weight:700}}
    .cb{{fill:rgba(0,0,0,.35);stroke:rgba(255,215,0,.2);stroke-width:1}}
    .ct{{fill:#FFD700;font-size:{int(fs*1.1)}px;font-weight:700;text-anchor:middle}}
    .cs{{fill:rgba(255,255,255,.45);font-size:{int(fs*.8)}px;text-anchor:middle}}
  </style></defs>''')

    for sign_num, (col, row) in SIGN_POSITIONS.items():
        x = col * cell
        y = row * cell
        house = _house_num(lagna_rasi, sign_num)
        planets = [p for p in sign_planets.get(sign_num, []) if p]
        is_lagna = (sign_num == lagna_rasi)

        hmean = HOUSE_MEANINGS[house].replace("'","\\'")
        rasi_en = RASI_EN[sign_num]
        planet_str = ', '.join(p for p in planets if p != 'Lagna') or 'Empty'
        onclick = f"showHouseInfo({house},'{rasi_en}',{house},'{planet_str}','{hmean}')"

        svg.append(f'  <g onclick="{onclick}">')
        # Cell background
        lagna_stroke = 'rgba(0,255,204,.6)' if is_lagna else 'rgba(255,215,0,.35)'
        lagna_fill   = 'rgba(0,255,204,.06)' if is_lagna else 'rgba(255,255,255,.04)'
        svg.append(f'    <rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" class="hc" style="fill:{lagna_fill};stroke:{lagna_stroke}"/>')

        # Lagna diagonal lines
        if is_lagna:
            svg.append(f'    <line x1="{x}" y1="{y}" x2="{x+cell}" y2="{y+cell}" stroke="rgba(0,255,204,.4)" stroke-width="1"/>')
            svg.append(f'    <line x1="{x+cell}" y1="{y}" x2="{x}" y2="{y+cell}" stroke="rgba(0,255,204,.4)" stroke-width="1"/>')

        # House number (small, top-left)
        svg.append(f'    <text x="{x+4}" y="{y+int(fs*1.1)}" class="hn">{house}</text>')

        # Rasi name (small, bottom-center)
        svg.append(f'    <text x="{x+cell//2}" y="{y+cell-5}" class="rn" text-anchor="middle">{RASI_TA[sign_num]}</text>')

        # Planets
        non_lagna = [p for p in planets if p != 'Lagna']
        for i, planet in enumerate(non_lagna[:4]):
            px = x + pad + (i % 2) * (cell // 2 - pad + 2)
            py = y + int(cell * 0.35) + (i // 2) * int(cell * 0.26)
            color = PLANET_COL.get(planet, '#FFF')
            sym   = PLANET_SYM.get(planet, planet[:2])
            svg.append(f'    <text x="{px}" y="{py}" class="pt" fill="{color}">{sym}</text>')

        # Show "Lg" label if lagna
        if is_lagna:
            svg.append(f'    <text x="{x+cell-4}" y="{y+int(fs*1.1)}" class="hn" text-anchor="end" style="fill:rgba(0,255,204,.8)">Lg</text>')

        svg.append('  </g>')

    # Center 2x2 box
    cx, cy = cell, cell
    svg.append(f'''  <rect x="{cx}" y="{cy}" width="{cell*2}" height="{cell*2}" class="cb" rx="4"/>
  <text x="{cx+cell}" y="{cy+int(cell*.42)}" class="ct">🪐</text>
  <text x="{cx+cell}" y="{cy+int(cell*.62)}" class="ct">AstroGuy</text>
  <text x="{cx+cell}" y="{cy+int(cell*.78)}" class="cs">Vedic Birth Chart</text>
  <text x="{cx+cell}" y="{cy+int(cell*.93)}" class="cs">{RASI_EN.get(lagna_rasi,'')} Lagna</text>
  <text x="{cx+cell}" y="{cy+int(cell*1.07)}" class="cs" style="fill:rgba(0,255,204,.6)">Houses count clockwise ↻</text>''')

    svg.append('</svg>')
    return '\n'.join(svg)


def get_planet_house_data(chart: Dict) -> List[Dict]:
    """Return planets with house positions for sidebar display."""
    lagna_rasi = chart.get('lagna', {}).get('number', 1)
    result = []
    planet_sign_map = {
        'Sun':     chart.get('sun',{}).get('rasi',0),
        'Moon':    chart.get('rasi',{}).get('number',0),
        'Mars':    chart.get('mars',{}).get('rasi',0),
        'Mercury': chart.get('mercury',{}).get('rasi',0),
        'Jupiter': chart.get('jupiter',{}).get('rasi',0),
        'Venus':   chart.get('venus',{}).get('rasi',0),
        'Saturn':  chart.get('saturn',{}).get('rasi',0),
        'Rahu':    chart.get('rahu',{}).get('rasi',0),
        'Ketu':    chart.get('ketu',{}).get('rasi',0),
        'Lagna':   lagna_rasi,
    }
    for planet, sign in planet_sign_map.items():
        if not sign: continue
        house = _house_num(lagna_rasi, sign)
        result.append({
            'name':   planet,
            'symbol': PLANET_SYM.get(planet, planet[:2]),
            'color':  PLANET_COL.get(planet, '#FFF'),
            'sign':   RASI_EN.get(sign, ''),
            'sign_ta':RASI_TA.get(sign, ''),
            'house':  house,
            'info':   PLANET_INFO.get(planet, ''),
        })
    return result
