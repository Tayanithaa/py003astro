# AstroGuy AI — Vedic Astrology Web App

## Run (Windows)

### 1) Create and activate virtual environment
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 2) Install dependencies
```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 3) Configure environment variables
Create `.env` in project root:
```env
SECRET_KEY=change-this-to-a-long-random-value
DATABASE_URL=sqlite:///astroguy.db
FLASK_DEBUG=True
```

### 4) (Optional but recommended) initialize migrations
```powershell
python -m flask db init
python -m flask db migrate -m "initial"
python -m flask db upgrade
```

### 5) Train chatbot model (run once)
```powershell
python train_model.py
```

### 6) Start application
```powershell
python app.py
```

Open: http://localhost:5000

## Quick rerun (after first setup)
```powershell
.\venv\Scripts\activate
python app.py
```

## Features
- Birth Chart (Jathagam) with interactive SVG
- Daily Panchangam (Tithi, Vara, Nakshatra, Yoga, Karana, Rahu Kalam)
- Marriage Compatibility (Ashtakoota — 8 Kootas, 36 points)
- Horoscope Predictions (12 Rasis, Tamil + English)
- Personality Quiz (ML-powered)
- Planetary Wellness Tracker
- Shareable Cosmic Card (Canvas → PNG download)
- Finance Astrology
- Vedic Remedies (9 Planets)
- ML Chatbot (TF-IDF + Naive Bayes, 15 intents)
- Tamil + English bilingual throughout

## Included in current build
- SQLAlchemy models (`User`, `BirthChart`, `CompatibilityReport`, `Feedback`)
- Authentication (register/login/logout/profile/password reset token flow)
- Precision astro calculations (geopy + ephem fallback logic)
- Vimshottari Dasha + transit API
- Enhanced Panchangam (sunrise/sunset, Rahu Kalam, Yamagandam, Gulika)
- Personalized chatbot responses (dasha/transit/remedies)
- 2-page downloadable PDF chart report
- Help/FAQ + feedback submission endpoint
- Dark mode support
