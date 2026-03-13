"""
AstroGuy AI — Daily Panchangam Calculator
==========================================
Calculates the 5 elements of Hindu Panchangam:
  1. Tithi   — Lunar day (1-30)
  2. Vara    — Weekday (with ruling planet)
  3. Nakshatra — Moon's current star
  4. Yoga    — Sun+Moon combination (1-27)
  5. Karana  — Half-tithi (1-11)

Also calculates:
  - Rahu Kalam  (inauspicious period)
  - Abhijit Muhurta (most auspicious period)
  - Moon phase
  - Current planetary info

All calculations use Lahiri ayanamsa (same as rest of app).
No external API needed — 100% Python math.
"""

import math
from datetime import datetime, timedelta
from typing import Dict


# ── Constants ──────────────────────────────────────────────────────────────
J2000          = 2451545.0
AYANAMSA_2000  = 23.8581
AYANAMSA_RATE  = 0.013976


# ── Core astronomy helpers ─────────────────────────────────────────────────
def _to_rad(d): return d * math.pi / 180
def _norm360(d): return d % 360

def _julian_day(year, month, day, hour=12, minute=0):
    y, m = year, month
    if m <= 2: y -= 1; m += 12
    A = int(y / 100)
    B = 2 - A + int(A / 4)
    return int(365.25*(y+4716)) + int(30.6001*(m+1)) + day + (hour + minute/60)/24 + B - 1524.5

def _ayanamsa(year):
    return AYANAMSA_2000 + (year - 2000) * AYANAMSA_RATE

def _moon_longitude(jd):
    T  = (jd - J2000) / 36525.0
    L  = 218.3164477 + 481267.88123421*T - 0.0015786*T*T + T**3/538841
    M  = 134.9633964 + 477198.8675055*T  + 0.0087414*T*T
    D  = 297.8501921 + 445267.1114034*T  - 0.0018819*T*T
    Ms = 357.5291092 + 35999.0502909*T   - 0.0001536*T*T
    F  = 93.2720950  + 483202.0175233*T  - 0.0036539*T*T
    dL = (6.289*math.sin(_to_rad(M))
        + 1.274*math.sin(_to_rad(2*D-M))
        + 0.658*math.sin(_to_rad(2*D))
        + 0.214*math.sin(_to_rad(2*M))
        - 0.186*math.sin(_to_rad(Ms))
        - 0.114*math.sin(_to_rad(2*F)))
    return _norm360(L + dL)

def _sun_longitude(jd):
    T  = (jd - J2000) / 36525.0
    L0 = 280.46646 + 36000.76983*T
    M  = 357.52911 + 35999.05029*T
    C  = ((1.914602 - 0.004817*T)*math.sin(_to_rad(M))
        + 0.019993*math.sin(_to_rad(2*M))
        + 0.000289*math.sin(_to_rad(3*M)))
    return _norm360(L0 + C)


# ── Panchangam data ────────────────────────────────────────────────────────
TITHIS = [
    "Pratipada","Dwitiya","Tritiya","Chaturthi","Panchami",
    "Shashthi","Saptami","Ashtami","Navami","Dashami",
    "Ekadashi","Dwadashi","Trayodashi","Chaturdashi","Purnima/Amavasya"
]
TITHI_TAMIL = [
    "பிரதமை","துவிதியை","திரிதியை","சதுர்த்தி","பஞ்சமி",
    "சஷ்டி","சப்தமி","அஷ்டமி","நவமி","தசமி",
    "ஏகாதசி","துவாதசி","த்ரயோதசி","சதுர்தசி","பௌர்ணமி/அமாவாசை"
]
TITHI_TYPE = [
    "Nanda","Bhadra","Jaya","Rikta","Purna",
    "Nanda","Bhadra","Jaya","Rikta","Purna",
    "Nanda","Bhadra","Jaya","Rikta","Purna"
]

VARAS = [
    {"en":"Sunday",   "ta":"ஞாயிறு",    "planet":"Sun",    "symbol":"☀️", "color":"#FF6B35"},
    {"en":"Monday",   "ta":"திங்கள்",   "planet":"Moon",   "symbol":"🌙", "color":"#C0C0C0"},
    {"en":"Tuesday",  "ta":"செவ்வாய்",  "planet":"Mars",   "symbol":"♂",  "color":"#FF4444"},
    {"en":"Wednesday","ta":"புதன்",      "planet":"Mercury","symbol":"☿",  "color":"#44BB44"},
    {"en":"Thursday", "ta":"வியாழன்",   "planet":"Jupiter","symbol":"♃",  "color":"#FFD700"},
    {"en":"Friday",   "ta":"வெள்ளி",    "planet":"Venus",  "symbol":"♀",  "color":"#FF69B4"},
    {"en":"Saturday", "ta":"சனி",       "planet":"Saturn", "symbol":"♄",  "color":"#4444FF"},
]

NAKSHATRAS_27 = [
    ("Ashwini","அஸ்வினி"),("Bharani","பரணி"),("Krittika","கிருத்திகை"),
    ("Rohini","ரோகிணி"),("Mrigashira","மிருகசீரிஷம்"),("Ardra","திருவாதிரை"),
    ("Punarvasu","புனர்பூசம்"),("Pushya","பூசம்"),("Ashlesha","ஆயில்யம்"),
    ("Magha","மகம்"),("Purva Phalguni","பூரம்"),("Uttara Phalguni","உத்திரம்"),
    ("Hasta","ஹஸ்தம்"),("Chitra","சித்திரை"),("Swati","சுவாதி"),
    ("Vishakha","விசாகம்"),("Anuradha","அனுஷம்"),("Jyeshtha","கேட்டை"),
    ("Mula","மூலம்"),("Purva Ashadha","பூராடம்"),("Uttara Ashadha","உத்திராடம்"),
    ("Shravana","திருவோணம்"),("Dhanishta","அவிட்டம்"),("Shatabhisha","சதயம்"),
    ("Purva Bhadrapada","பூரட்டாதி"),("Uttara Bhadrapada","உத்திரட்டாதி"),
    ("Revati","ரேவதி"),
]

YOGAS = [
    ("Vishkambha","விஷ்கம்ப"),("Priti","ப்ரீதி"),("Ayushman","ஆயுஷ்மான்"),
    ("Saubhagya","சௌபாக்கிய"),("Shobhana","சோபன"),("Atiganda","அதிகண்ட"),
    ("Sukarma","சுகர்ம"),("Dhriti","திருதி"),("Shula","சூல"),
    ("Ganda","கண்ட"),("Vriddhi","விருத்தி"),("Dhruva","திருவ"),
    ("Vyaghata","வியாகாத"),("Harshana","ஹர்ஷண"),("Vajra","வஜ்ர"),
    ("Siddhi","சித்தி"),("Vyatipata","வியதீபாத"),("Variyana","வரீயான்"),
    ("Parigha","பரிக"),("Shiva","சிவ"),("Siddha","சித்த"),
    ("Sadhya","சாத்ய"),("Shubha","சுப"),("Shukla","சுக்ல"),
    ("Brahma","பிரம்ம"),("Indra","இந்திர"),("Vaidhriti","வைத்ருதி"),
]
YOGA_QUALITY = [
    "Inauspicious","Auspicious","Auspicious","Auspicious","Auspicious",
    "Inauspicious","Auspicious","Auspicious","Inauspicious","Inauspicious",
    "Auspicious","Auspicious","Inauspicious","Auspicious","Inauspicious",
    "Auspicious","Inauspicious","Auspicious","Inauspicious","Auspicious",
    "Auspicious","Auspicious","Auspicious","Auspicious","Auspicious",
    "Auspicious","Inauspicious",
]

KARANAS = [
    "Bava","Balava","Kaulava","Taitila","Garija",
    "Vanija","Vishti","Shakuni","Chatushpada","Naga","Kimstughna"
]
KARANA_TAMIL = [
    "பவ","பாலவ","கௌலவ","தைதில","கரஜ",
    "வணிஜ","விஷ்டி","சகுனி","சதுஷ்பாத","நாக","கிம்ஸ்துக்ன"
]

# Rahu Kalam by weekday (fraction of day: start, end out of 8 parts)
RAHU_KALAM_PARTS = [8, 2, 7, 5, 6, 4, 3]  # Sun=8th part, Mon=2nd, etc.

MOON_PHASES = [
    (0,   "🌑 New Moon",        "New Moon — Amavasya"),
    (45,  "🌒 Waxing Crescent", "Waxing Crescent"),
    (90,  "🌓 First Quarter",   "First Quarter"),
    (135, "🌔 Waxing Gibbous",  "Waxing Gibbous"),
    (180, "🌕 Full Moon",       "Full Moon — Purnima"),
    (225, "🌖 Waning Gibbous",  "Waning Gibbous"),
    (270, "🌗 Last Quarter",    "Last Quarter"),
    (315, "🌘 Waning Crescent", "Waning Crescent"),
]

# Regional festival dates (Tamil Nadu / South India) — format: (month, day)
FESTIVALS = {
    (1, 14): {"en": "Pongal / Makar Sankranti", "ta": "பொங்கல் / மகர சங்கராந்தி"},
    (1, 15): {"en": "Mattu Pongal", "ta": "மாட்டுப் பொங்கல்"},
    (1, 26): {"en": "Republic Day", "ta": "குடியரசு தினம்"},
    (3, 14): {"en": "Holi", "ta": "ஹோலி"},
    (4, 14): {"en": "Tamil New Year (Puthandu)", "ta": "தமிழ் புத்தாண்டு (புத்தாண்டு)"},
    (8, 15): {"en": "Independence Day", "ta": "சுதந்திர தினம்"},
    (10, 2): {"en": "Gandhi Jayanti", "ta": "காந்தி ஜெயந்தி"},
}

# ── Ephem sunrise/sunset ───────────────────────────────────────────────────
try:
    import ephem
    _EPHEM = True
except ImportError:
    _EPHEM = False


def _get_sunrise_sunset(year: int, month: int, day: int,
                        lat: float, lon: float) -> tuple:
    """Return (sunrise_hour, sunset_hour) as decimal hours (local time)."""
    if _EPHEM:
        try:
            obs = ephem.Observer()
            obs.lat   = str(lat)
            obs.lon   = str(lon)
            obs.date  = f"{year}/{month}/{day} 00:00:00"
            obs.horizon = '-0:34'  # account for refraction

            sun = ephem.Sun()
            # Convert ephem UTC time to local decimal hours using longitude offset
            tz_offset = lon / 15.0  # rough hours offset from UTC

            rise_utc = ephem.localtime(obs.next_rising(sun)).hour + \
                       ephem.localtime(obs.next_rising(sun)).minute / 60
            set_utc  = ephem.localtime(obs.next_setting(sun)).hour + \
                       ephem.localtime(obs.next_setting(sun)).minute / 60

            # Clamp to sensible range
            sunrise = max(4.0, min(10.0, rise_utc))
            sunset  = max(16.0, min(21.0, set_utc))
            return sunrise, sunset
        except Exception:
            pass  # fall through to approximation

    # Approximate sunrise/sunset using solar declination
    # More accurate than fixed 6/18
    from math import radians, degrees, sin, cos, acos, tan
    day_of_year = (datetime(year, month, day) - datetime(year, 1, 1)).days + 1
    B = radians(360 / 365 * (day_of_year - 81))
    # Equation of time (minutes)
    eot = 9.87 * math.sin(2 * B) - 7.53 * math.cos(B) - 1.5 * math.sin(B)
    # Solar declination
    decl = radians(23.45 * math.sin(B))
    lat_r = radians(abs(lat))
    try:
        cos_h = -math.tan(lat_r) * math.tan(decl)
        cos_h = max(-1, min(1, cos_h))
        half_day = math.degrees(math.acos(cos_h)) / 15
    except Exception:
        half_day = 6.0
    solar_noon = 12 - (lon - round(lon / 15) * 15) / 15 - eot / 60
    sunrise = solar_noon - half_day
    sunset  = solar_noon + half_day
    return max(4.0, sunrise), min(21.0, sunset)


# ── Main calculator ────────────────────────────────────────────────────────
def get_panchangam(date: datetime = None, lat: float = 13.0827,
                   lon: float = 80.2707) -> Dict:
    """
    Calculate full Panchangam for a given date and location.
    Defaults to today, Chennai coordinates.
    Uses ephem for precise sunrise/sunset when available.
    """
    if date is None:
        date = datetime.now()

    year, month, day = date.year, date.month, date.day
    hour             = date.hour + date.minute / 60

    jd       = _julian_day(year, month, day, hour)
    ayanamsa = _ayanamsa(year + (month-1)/12 + day/365)

    # Sidereal longitudes
    moon_trop = _moon_longitude(jd)
    sun_trop  = _sun_longitude(jd)
    moon_sid  = _norm360(moon_trop - ayanamsa)
    sun_sid   = _norm360(sun_trop  - ayanamsa)

    # ── 1. Tithi ──────────────────────────────────────────────────────────
    moon_sun_diff = _norm360(moon_trop - sun_trop)
    tithi_index   = int(moon_sun_diff / 12)        # 0-29
    tithi_display = tithi_index % 15               # 0-14
    tithi_elapsed = (moon_sun_diff % 12) / 12 * 100

    paksha = "Shukla Paksha (Waxing)" if tithi_index < 15 else "Krishna Paksha (Waning)"
    paksha_ta = "சுக்ல பக்ஷம்" if tithi_index < 15 else "கிருஷ்ண பக்ஷம்"

    # ── 2. Vara (weekday) ─────────────────────────────────────────────────
    weekday  = date.weekday()          # Mon=0 … Sun=6
    vara_idx = (weekday + 1) % 7       # Sun=0 … Sat=6
    vara     = VARAS[vara_idx]

    # ── 3. Nakshatra ──────────────────────────────────────────────────────
    nak_index = int(moon_sid / 13.3333) % 27
    nak_pada  = int((moon_sid % 13.3333) / 3.3333) + 1
    nak_elapsed = ((moon_sid % 13.3333) / 13.3333) * 100

    # ── 4. Yoga ───────────────────────────────────────────────────────────
    yoga_long  = _norm360(moon_sid + sun_sid)
    yoga_index = int(yoga_long / 13.3333) % 27

    # ── 5. Karana ─────────────────────────────────────────────────────────
    karana_index = int(moon_sun_diff / 6) % 11

    # ── Location-specific Sunrise/Sunset & Rahu Kalam ────────────────────
    sunrise_h, sunset_h = _get_sunrise_sunset(year, month, day, lat, lon)
    day_dur   = sunset_h - sunrise_h
    part_dur  = day_dur / 8           # each of 8 equal parts

    rk_part    = RAHU_KALAM_PARTS[vara_idx] - 1
    rk_start_h = sunrise_h + rk_part * part_dur
    rk_end_h   = rk_start_h + part_dur

    def _fmt_time(h):
        hr  = int(h) % 24
        mn  = int(round((h - int(h)) * 60))
        if mn >= 60: hr, mn = hr + 1, mn - 60
        ap  = "AM" if hr < 12 else "PM"
        hr12 = hr if hr <= 12 else hr - 12
        if hr12 == 0: hr12 = 12
        return f"{hr12}:{mn:02d} {ap}"

    rahu_kalam = {
        "start": _fmt_time(rk_start_h),
        "end":   _fmt_time(rk_end_h),
        "avoid": True
    }

    # ── Yamagandam ────────────────────────────────────────────────────────
    # Yamagandam parts by weekday (1-indexed part of day): Sun=5,Mon=4,Tue=3,Wed=2,Thu=1,Fri=7,Sat=6
    YAMA_PARTS = [5, 4, 3, 2, 1, 7, 6]
    ym_part    = YAMA_PARTS[vara_idx] - 1
    ym_start   = sunrise_h + ym_part * part_dur
    yamagandam = {"start": _fmt_time(ym_start), "end": _fmt_time(ym_start + part_dur)}

    # ── Gulika Kalam ──────────────────────────────────────────────────────
    GULIKA_PARTS = [7, 6, 5, 4, 3, 2, 1]
    gl_part      = GULIKA_PARTS[vara_idx] - 1
    gl_start     = sunrise_h + gl_part * part_dur
    gulika_kalam = {"start": _fmt_time(gl_start), "end": _fmt_time(gl_start + part_dur)}

    # ── Abhijit Muhurta ───────────────────────────────────────────────────
    midday    = (sunrise_h + sunset_h) / 2
    abh_start = midday - 0.4
    abh_end   = midday + 0.4
    abhijit   = {"start": _fmt_time(abh_start), "end": _fmt_time(abh_end)}

    # ── Moon phase ────────────────────────────────────────────────────────
    phase_angle = moon_sun_diff
    phase_label = MOON_PHASES[-1][1]
    phase_name  = MOON_PHASES[-1][2]
    for threshold, label, name in MOON_PHASES:
        if phase_angle >= threshold:
            phase_label = label
            phase_name  = name

    # ── Regional festival check ───────────────────────────────────────────
    festival = FESTIVALS.get((month, day))

    # ── Is today auspicious? ──────────────────────────────────────────────
    yoga_good = YOGA_QUALITY[yoga_index] == "Auspicious"
    is_vishti = KARANAS[karana_index] == "Vishti"   # Vishti = inauspicious
    overall   = "Auspicious ✨" if yoga_good and not is_vishti else "Moderate" if yoga_good or not is_vishti else "Inauspicious ⚠️"

    return {
        "date": date.strftime("%A, %d %B %Y"),
        "date_ta": f"{vara['ta']}, {date.strftime('%d %B %Y')}",

        "tithi": {
            "number":   tithi_index + 1,
            "name":     TITHIS[tithi_display],
            "name_ta":  TITHI_TAMIL[tithi_display],
            "type":     TITHI_TYPE[tithi_display],
            "paksha":   paksha,
            "paksha_ta":paksha_ta,
            "elapsed":  round(tithi_elapsed, 1),
        },
        "vara": {
            "en":     vara["en"],
            "ta":     vara["ta"],
            "planet": vara["planet"],
            "symbol": vara["symbol"],
            "color":  vara["color"],
        },
        "nakshatra": {
            "name":     NAKSHATRAS_27[nak_index][0],
            "name_ta":  NAKSHATRAS_27[nak_index][1],
            "pada":     nak_pada,
            "elapsed":  round(nak_elapsed, 1),
        },
        "yoga": {
            "name":    YOGAS[yoga_index][0],
            "name_ta": YOGAS[yoga_index][1],
            "quality": YOGA_QUALITY[yoga_index],
        },
        "karana": {
            "name":    KARANAS[karana_index],
            "name_ta": KARANA_TAMIL[karana_index],
        },
        "sunrise":    _fmt_time(sunrise_h),
        "sunset":     _fmt_time(sunset_h),
        "rahu_kalam": rahu_kalam,
        "yamagandam": yamagandam,
        "gulika_kalam": gulika_kalam,
        "abhijit":    abhijit,
        "moon_phase": {
            "label": phase_label,
            "name":  phase_name,
            "angle": round(phase_angle, 1),
        },
        "auspicious":  overall,
        "festival":    festival,
        "sun_long":    round(sun_sid,  2),
        "moon_long":   round(moon_sid, 2),
        "ayanamsa":    round(ayanamsa, 4),
        "location":    {"lat": lat, "lon": lon},
    }

    """
    Calculate full Panchangam for a given date and location.
    Defaults to today, Chennai coordinates.

    Returns a dict with all 5 elements + extras.
    """
    if date is None:
        date = datetime.now()

    year, month, day = date.year, date.month, date.day
    hour             = date.hour + date.minute / 60

    jd       = _julian_day(year, month, day, hour)
    ayanamsa = _ayanamsa(year + (month-1)/12 + day/365)

    # Sidereal longitudes
    moon_trop = _moon_longitude(jd)
    sun_trop  = _sun_longitude(jd)
    moon_sid  = _norm360(moon_trop - ayanamsa)
    sun_sid   = _norm360(sun_trop  - ayanamsa)

    # ── 1. Tithi ──────────────────────────────────────────────────────────
    moon_sun_diff = _norm360(moon_trop - sun_trop)
    tithi_index   = int(moon_sun_diff / 12)        # 0-29
    tithi_display = tithi_index % 15               # 0-14
    tithi_elapsed = (moon_sun_diff % 12) / 12 * 100

    paksha = "Shukla Paksha (Waxing)" if tithi_index < 15 else "Krishna Paksha (Waning)"
    paksha_ta = "சுக்ல பக்ஷம்" if tithi_index < 15 else "கிருஷ்ண பக்ஷம்"

    # ── 2. Vara (weekday) ─────────────────────────────────────────────────
    weekday  = date.weekday()          # Mon=0 … Sun=6
    vara_idx = (weekday + 1) % 7       # Sun=0 … Sat=6
    vara     = VARAS[vara_idx]

    # ── 3. Nakshatra ──────────────────────────────────────────────────────
    nak_index = int(moon_sid / 13.3333) % 27
    nak_pada  = int((moon_sid % 13.3333) / 3.3333) + 1
    nak_elapsed = ((moon_sid % 13.3333) / 13.3333) * 100

    # ── 4. Yoga ───────────────────────────────────────────────────────────
    yoga_long  = _norm360(moon_sid + sun_sid)
    yoga_index = int(yoga_long / 13.3333) % 27

    # ── 5. Karana ─────────────────────────────────────────────────────────
    karana_index = int(moon_sun_diff / 6) % 11

    # ── Rahu Kalam ────────────────────────────────────────────────────────
    sunrise_h  = 6.0   # approx 6:00 AM
    sunset_h   = 18.0  # approx 6:00 PM
    day_dur    = sunset_h - sunrise_h
    part_dur   = day_dur / 8           # each part ~90 min

    rk_part    = RAHU_KALAM_PARTS[vara_idx] - 1
    rk_start_h = sunrise_h + rk_part * part_dur
    rk_end_h   = rk_start_h + part_dur

    def _fmt_time(h):
        hr  = int(h)
        mn  = int((h - hr) * 60)
        ap  = "AM" if hr < 12 else "PM"
        hr12 = hr if hr <= 12 else hr - 12
        if hr12 == 0: hr12 = 12
        return f"{hr12}:{mn:02d} {ap}"

    rahu_kalam = {
        "start": _fmt_time(rk_start_h),
        "end":   _fmt_time(rk_end_h),
        "avoid": True
    }

    # ── Abhijit Muhurta ───────────────────────────────────────────────────
    midday    = (sunrise_h + sunset_h) / 2
    abh_start = midday - 0.4
    abh_end   = midday + 0.4
    abhijit   = {"start": _fmt_time(abh_start), "end": _fmt_time(abh_end)}

    # ── Moon phase ────────────────────────────────────────────────────────
    phase_angle = moon_sun_diff
    phase_label = MOON_PHASES[-1][1]
    phase_name  = MOON_PHASES[-1][2]
    for threshold, label, name in MOON_PHASES:
        if phase_angle >= threshold:
            phase_label = label
            phase_name  = name

    # ── Is today auspicious? ──────────────────────────────────────────────
    yoga_good = YOGA_QUALITY[yoga_index] == "Auspicious"
    is_vishti = KARANAS[karana_index] == "Vishti"   # Vishti = inauspicious
    overall   = "Auspicious ✨" if yoga_good and not is_vishti else "Moderate" if yoga_good or not is_vishti else "Inauspicious ⚠️"

    return {
        "date": date.strftime("%A, %d %B %Y"),
        "date_ta": f"{vara['ta']}, {date.strftime('%d %B %Y')}",

        "tithi": {
            "number":   tithi_index + 1,
            "name":     TITHIS[tithi_display],
            "name_ta":  TITHI_TAMIL[tithi_display],
            "type":     TITHI_TYPE[tithi_display],
            "paksha":   paksha,
            "paksha_ta":paksha_ta,
            "elapsed":  round(tithi_elapsed, 1),
        },
        "vara": {
            "en":     vara["en"],
            "ta":     vara["ta"],
            "planet": vara["planet"],
            "symbol": vara["symbol"],
            "color":  vara["color"],
        },
        "nakshatra": {
            "name":     NAKSHATRAS_27[nak_index][0],
            "name_ta":  NAKSHATRAS_27[nak_index][1],
            "pada":     nak_pada,
            "elapsed":  round(nak_elapsed, 1),
        },
        "yoga": {
            "name":    YOGAS[yoga_index][0],
            "name_ta": YOGAS[yoga_index][1],
            "quality": YOGA_QUALITY[yoga_index],
        },
        "karana": {
            "name":    KARANAS[karana_index],
            "name_ta": KARANA_TAMIL[karana_index],
        },
        "rahu_kalam": rahu_kalam,
        "abhijit":    abhijit,
        "moon_phase": {
            "label": phase_label,
            "name":  phase_name,
            "angle": round(phase_angle, 1),
        },
        "auspicious":  overall,
        "sun_long":    round(sun_sid,  2),
        "moon_long":   round(moon_sid, 2),
        "ayanamsa":    round(ayanamsa, 4),
    }
