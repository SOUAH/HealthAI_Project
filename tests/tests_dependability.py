import requests

# The URL of the Dockerized API
URL = "http://localhost:8000/predict"

def run_test(name, text, expected_status):
    print(f"--- Running Test: {name} ---")
    payload = {"text": text}
    response = requests.post(URL, json=payload)
    data = response.json()
    
    print(f"Input: {text[:50]}...")
    print(f"System Response: {data}")
    
    if data['status'] == expected_status:
        print(f"RESULT: PASS\n")
    else:
        print(f"RESULT: FAIL (Expected {expected_status})\n")

#SAFETY GATE TEST (Checking the 'Innovation' Boundary)
#To ensure the system rejects data that is too short to be safe.
run_test(
    "Safety Boundary Test", 
    "I am sad.", 
    "Rejected"
)

#METAMORPHIC TEST (Checking Fairness)
note_a = "I have been feeling very hopeless and tired lately. I cannot sleep."
note_b = "My name is John. I have been feeling very hopeless and tired lately. I cannot sleep."

print("Running Metamorphic Fairness Test")
res_a = requests.post(URL, json={"text": note_a}).json()
res_b = requests.post(URL, json={"text": note_b}).json()

if res_a['risk_label'] == res_b['risk_label']:
    print(f"Risk A: {res_a['risk_label']}, Risk B: {res_b['risk_label']}")
    print("RESULT: PASS (Model is Fair)\n")
else:
    print("RESULT: FAIL (Model is Biased!)\n")