import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import joblib
import os

def train_solo_model():
    file_path = 'data/Suicide_Detection.csv'
    
    if not os.path.exists(file_path):
        print(f"ERROR: File not found at {file_path}. Check your folders!")
        return

    print("Loading dataset...")
    df = pd.read_csv(file_path)
    
    # preprocessing: Cleaning data before training
    df = df[['text', 'class']].dropna()
    
    # Split data for evaluation (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(df['text'], df['class'], test_size=0.2)

    print("Training model")
    vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
    X_train_vec = vectorizer.fit_transform(X_train)
    
    model = MultinomialNB()
    model.fit(X_train_vec, y_train)

    #So the FastAPI service can load them without re-training 
    joblib.dump(model, 'backend/model.pkl')
    joblib.dump(vectorizer, 'backend/vectorizer.pkl')
    print("SUCCESS: Model 'brain' saved to backend/model.pkl")

if __name__ == "__main__":
    train_solo_model()