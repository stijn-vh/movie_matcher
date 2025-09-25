import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
import sqlite3
import pandas as pd
import pickle

nlp = spacy.load("en_core_web_sm")

conn = sqlite3.connect('mm_api/movies.db')
c = conn.cursor()

def preprocess_text(text):
    doc = nlp(text)
    return " ".join(token.lemma_ for token in doc if not token.is_stop and not token.is_punct)


c.execute('SELECT Name, Description FROM Movie')
movies = c.fetchall()

names = [row[0] for row in movies]
texts = [row[1] for row in movies]

processed_texts = [preprocess_text(text) for text in texts]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(processed_texts)

from sklearn.cluster import KMeans

K = [40, 60, 80]

for k in K:
    model = KMeans(n_clusters=k, random_state=1)
    model.fit(X)

    labels = model.labels_

    c.execute('ALTER TABLE Movie ADD COLUMN Category' + str(k) + 'Cluster INT')

    for i in range(len(names)):
        c.execute('UPDATE Movie SET Category' + str(k) + 'Cluster = ? WHERE Name = ?', (int(labels[i]), names[i]))
    
    conn.commit()
