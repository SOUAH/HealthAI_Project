import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, f1_score
import joblib

def train_solo_model():
    #Load the new lightweight dataset
    df = pd.read_csv('data/Suicide_Detection.csv')
    
    #Split into Training and Testing(To evaluate 'Generalization)
    X_train, X_test, y_train, y_test = train_test_split(df['text'], df['class'], test_size=0.2)

    #Vectorize and Train
    vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
    X_train_vec = vectorizer.fit_transform(X_train)
    
    model = MultinomialNB()
    model.fit(X_train_vec, y_train)

    #Evaluate on test set
    X_test_vec = vectorizer.transform(X_test)
    y_pred = model.predict(X_test_vec)
    
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    print("Training Complete!")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"F1 Score: {f1:.4f}")

    #Save for API
    joblib.dump(model, 'backend/model.pkl')
    joblib.dump(vectorizer, 'backend/vectorizer.pkl')

if __name__ == '__main__':
    train_solo_model()