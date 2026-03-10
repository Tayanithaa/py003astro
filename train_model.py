"""
AstroGuy AI — ML Chatbot Model Trainer
=======================================
Run this ONCE to train and save the model:

    python train_model.py

What this does:
  1. Loads data/chatbot_dataset.json  (your labeled training data)
  2. Preprocesses text (lowercasing, stemming with NLTK if available)
  3. Trains TF-IDF + Naive Bayes classifier (scikit-learn)
  4. Saves trained model to utils/chatbot_model.pkl
  5. Prints accuracy score and classification report
"""

import json
import pickle
import os
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# ── Optional NLTK stemming (better accuracy if installed) ──────────────────
try:
    import nltk
    from nltk.stem import PorterStemmer
    nltk.download('punkt',     quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt_tab', quiet=True)
    _stemmer = PorterStemmer()
    USE_NLTK = True
    print("NLTK found — using stemming for better accuracy.\n")
except ImportError:
    USE_NLTK = False
    _stemmer = None
    print("INFO: NLTK not found. Using basic preprocessing.")
    print("      Install with: pip install nltk\n")

# ── Paths ──────────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
DATA_PATH  = os.path.join(BASE_DIR, 'data',  'chatbot_dataset.json')
MODEL_PATH = os.path.join(BASE_DIR, 'utils', 'chatbot_model.pkl')

# ── Text preprocessing ─────────────────────────────────────────────────────
def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    tokens = text.split()
    if USE_NLTK and _stemmer:
        tokens = [_stemmer.stem(t) for t in tokens if len(t) > 1]
    else:
        tokens = [t for t in tokens if len(t) > 1]
    return ' '.join(tokens)

# ── Load dataset ───────────────────────────────────────────────────────────
print("=" * 55)
print("  AstroGuy AI — ML Chatbot Trainer")
print("=" * 55)

with open(DATA_PATH, 'r', encoding='utf-8') as f:
    dataset = json.load(f)

X_raw, y = [], []
for intent in dataset['intents']:
    for pattern in intent['patterns']:
        X_raw.append(pattern)
        y.append(intent['tag'])

print(f"\nDataset loaded:")
print(f"   Samples : {len(X_raw)}")
print(f"   Intents : {len(set(y))}")
print(f"   Classes : {sorted(set(y))}\n")

# ── Preprocess ─────────────────────────────────────────────────────────────
X = [preprocess(t) for t in X_raw]

# ── Train / test split ─────────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"Split  →  Train: {len(X_train)}  |  Test: {len(X_test)}\n")

# ── Build & train pipeline ─────────────────────────────────────────────────
#   TF-IDF converts raw text to numerical feature vectors
#   MultinomialNB classifies intent from those vectors
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(
        ngram_range=(1, 2),   # unigrams + bigrams
        max_features=3000,    # top 3000 features
        min_df=1,
        sublinear_tf=True     # log normalization
    )),
    ('clf', MultinomialNB(alpha=0.1))
])

print("Training TF-IDF + Naive Bayes model...")
pipeline.fit(X_train, y_train)
print("Done.\n")

# ── Evaluate ───────────────────────────────────────────────────────────────
y_pred   = pipeline.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Accuracy: {accuracy * 100:.1f}%\n")
print("Classification Report:")
print(classification_report(y_test, y_pred))

# ── Save (pipeline + responses — no function objects) ─────────────────────
responses_map = {
    intent['tag']: intent['responses']
    for intent in dataset['intents']
}

model_data = {
    'pipeline':    pipeline,
    'responses':   responses_map,
    'intent_tags': sorted(set(y)),
    'accuracy':    accuracy,
}

os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
with open(MODEL_PATH, 'wb') as f:
    pickle.dump(model_data, f)

print(f"Model saved → {MODEL_PATH}  ({os.path.getsize(MODEL_PATH)/1024:.1f} KB)")
print("\nAll done! Run: python app.py")
print("=" * 55)
