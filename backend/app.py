import streamlit as st
import requests
import jwt
import datetime
import time
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

#DATABASE CONFIGURATION [cite: 125, 127]
client = MongoClient("mongodb://localhost:27017/")
db = client["safe_guard_db"]
users_col = db["psychologists"]
sessions_col = db["clinical_sessions"]

SECRET_KEY = "clinical_ai_secret_key" 

#AUTH & JWT UTILS [cite: 130]
def create_token(user_data):
    payload = {
        "username": user_data["username"],
        "name": user_data["name"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except:
        return None

#PAGE CONFIGURATION
st.set_page_config(page_title="Safe-Guard AI | Secure Portal", layout="wide")

# I REMOVED THE CUSTOM CSS BLOCK THAT CAUSED THE WHITE SQUARE
st.markdown("""
    <style>
    .stInfo { border-left: 5px solid #007bff; }
    </style>
    """, unsafe_allow_html=True)

#LOGIN & REGISTRATION UI
if "token" not in st.session_state:
    st.session_state.token = None

if not st.session_state.token:
    _, col_form, _ = st.columns([1, 1, 1])
    
    with col_form:
        tab1, tab2 = st.tabs(["Login", "Register Clinician"])
        
        with tab1:
            st.subheader("Clinician Login")
            l_user = st.text_input("Username", key="l_user")
            l_pass = st.text_input("Password", type="password", key="l_pass")
            if st.button("Secure Login", use_container_width=True):
                user = users_col.find_one({"username": l_user})
                if user and check_password_hash(user["password"], l_pass):
                    st.session_state.token = create_token(user)
                    st.success("Authenticated successfully!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Invalid credentials.")

        with tab2:
            st.subheader("New Clinician Registration")
            reg_name = st.text_input("Full Name (e.g., Dr. Souha Aouididi)")
            reg_user = st.text_input("Create Username")
            reg_pass = st.text_input("Create Password", type="password")
            if st.button("Register", use_container_width=True):
                if users_col.find_one({"username": reg_user}):
                    st.error("Username already exists.")
                else:
                    hashed_pw = generate_password_hash(reg_pass)
                    users_col.insert_one({"name": reg_name, "username": reg_user, "password": hashed_pw})
                    st.success("Registration complete! Please login.")

#MAIN CLINICAL DASHBOARD [cite: 134, 136]
else:
    user_info = decode_token(st.session_state.token)
    if not user_info:
        st.session_state.token = None
        st.rerun()

    with st.sidebar:
        st.write(f"Logged in as: **{user_info['name']}**")
        if st.button("Logout"):
            st.session_state.token = None
            st.rerun()
        st.write("---")
        st.subheader("Recent Patient History")
        history = list(sessions_col.find().sort("timestamp", -1).limit(5))
        for h in history:
            st.caption(f"{h['patient_id']} | {h['risk_label']} | {h['date']}")

    st.title("Safe-Guard: Decision Support System")
    st.info("**Safety Warning:** AI indicators are for decision support only[cite: 152].")

    st.write("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.text_input("Psychologist", value=user_info['name'], disabled=True)
    with c2:
        patient_id = st.text_input("Patient ID", placeholder="Enter ID...")
    with c3:
        session_date = st.date_input("Session Date")

    st.write("---")

    l_col, r_col = st.columns([2, 1])

    with l_col:
        st.subheader("Session Notes")
        note = st.text_area("Input clinical text:", height=250)
        analyze_btn = st.button("Analyze Risk", use_container_width=True)
        
        if analyze_btn:
            words = note.split()
            if len(words) < 15:
                st.error("INPUT REJECTED: Min 15 words required for safety[cite: 152].")
            else:
                try:
                    response = requests.post("http://localhost:5000/predict", json={"text": note})
                    data = response.json()
                    
                    if data['status'] == "Success":
                        prob = data['probability_score'] * 100
                        risk = data['risk_label']
                        
                        with r_col:
                            st.metric("Depression Risk Probability", f"{prob:.1f}%")
                            if "High" in risk:
                                st.error(f"Suggested Risk: **{risk}**")
                                st.warning("**Clinician Action Required** [cite: 152]")
                            else:
                                st.success(f"Suggested Risk: **{risk}**")
                        
                        sessions_col.insert_one({
                            "clinician": user_info['name'],
                            "patient_id": patient_id,
                            "date": str(session_date),
                            "risk_label": risk,
                            "probability": prob,
                            "timestamp": datetime.datetime.now()
                        })
                        st.toast("Record saved to MongoDB[cite: 124].")
                except:
                    st.error("Connection Error: Is the API running? [cite: 113]")

    if not analyze_btn:
        with r_col:
            st.write("Awaiting session input...")