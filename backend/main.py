from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

# Load the saved model and vectorizer at startup [cite: 160, 236]
model = joblib.load('backend/model.pkl')
vectorizer = joblib.load('backend/vectorizer.pkl')

def run_safety_checks(text: str):
    words = text.split()
    #Rejecting data that is too short to ensures "Correctness and Rigor"[cite: 107].
    if len(words) < 10:
        return False, "Input too short for safe clinical assessment."
    return True, "Safe"

@app.route("/predict", methods=['POST'])
def predict_depression():
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({"status": "Error", "reason": "Missing 'text' field"}), 400
    
    input_text = data['text']
    
    #Safety Boundary Check
    is_safe, message = run_safety_checks(input_text)
    if not is_safe:
        return jsonify({"status": "Rejected", "reason": message})

    #Real AI Inference [cite: 231, 239]
    processed_text = vectorizer.transform([input_text])
    prediction = model.predict(processed_text)[0]
    probability = model.predict_proba(processed_text)[0][1]
    
    #Probabilistic Output
    # Use probability threshold: if prob is high, it's high risk (suicide class) (Preserves "Human Decision Authority")
    risk_label = "High Risk" if probability >= 0.5 else "Low Risk"
    
    return jsonify({
        "status": "Success",
        "risk_label": risk_label,
        "probability_score": round(float(probability), 2),
        "disclaimer": "This is a decision signal for clinicians only. Not a diagnosis."
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)