import streamlit as st
import pandas as pd
import re
from datetime import date, datetime

import database as db
import ai_helper as ai

st.set_page_config(
    page_title="MIRA - Health Prediction System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .header-banner {
        background: linear-gradient(135deg, #1e3a5f 0%, #2e86ab 100%);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    .header-banner h1 { margin: 0; font-size: 2rem; }
    .header-banner p  { margin: 0.3rem 0 0; opacity: 0.85; font-size: 0.95rem; }
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07);
        text-align: center;
    }
    .metric-card h3 { margin: 0; color: #2e86ab; font-size: 1.8rem; }
    .metric-card p  { margin: 0.2rem 0 0; color: #64748b; font-size: 0.85rem; }
    .remark-box {
        background: #f0f9ff;
        border-left: 4px solid #2e86ab;
        padding: 0.8rem 1rem;
        border-radius: 0 8px 8px 0;
        font-size: 0.9rem;
        color: #1e3a5f;
        margin-top: 0.5rem;
    }
    .success-msg { background: #d1fae5; color: #065f46; padding: 0.6rem 1rem; border-radius: 8px; font-weight: 500; }
    .error-msg   { background: #fee2e2; color: #991b1b; padding: 0.6rem 1rem; border-radius: 8px; font-weight: 500; }
    .section-title { font-size: 1.1rem; font-weight: 600; color: #1e3a5f; margin-bottom: 0.8rem; padding-bottom: 0.4rem; border-bottom: 2px solid #e2e8f0; }
</style>
""", unsafe_allow_html=True)

db.create_table()

st.markdown("""
<div class="header-banner">
    <h1>🏥 MIRA - Medical Intelligence Robotic Automation</h1>
    <p>AI-Powered Health Prediction System | Patient Blood Test Management</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🧭 Navigation")
    page = st.radio(
        "Select a page:",
        ["📊 Dashboard", "➕ Add Patient", "✏️ Edit Patient", "🗑️ Delete Patient", "🔍 Search Records"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    MIRA uses the **Claude AI API** to analyse patient blood test results and generate intelligent health predictions.

    **Normal Ranges:**
    - Glucose: 70-99 mg/dL
    - Haemoglobin: 12-17.5 g/dL
    - Cholesterol: < 200 mg/dL
    """)

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    return bool(re.match(pattern, email))

def is_valid_dob(dob):
    return dob < date.today()

def validate_patient_form(full_name, dob, email, glucose, haemoglobin, cholesterol):
    if not full_name or len(full_name.strip()) < 2:
        return False, "Full name must be at least 2 characters."
    if not is_valid_dob(dob):
        return False, "Date of birth cannot be today or a future date."
    if not is_valid_email(email):
        return False, "Please enter a valid email address (e.g. user@example.com)."
    if not (0 < glucose < 1000):
        return False, "Glucose must be a positive numeric value (0-1000 mg/dL)."
    if not (0 < haemoglobin < 50):
        return False, "Haemoglobin must be a positive numeric value (0-50 g/dL)."
    if not (0 < cholesterol < 1000):
        return False, "Cholesterol must be a positive numeric value (0-1000 mg/dL)."
    return True, ""

if page == "📊 Dashboard":
    st.markdown('<p class="section-title">📊 Patient Records Overview</p>', unsafe_allow_html=True)
    patients = db.fetch_all_patients()
    total = len(patients)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card"><h3>{total}</h3><p>Total Patients</p></div>', unsafe_allow_html=True)
    with col2:
        high_glucose = sum(1 for p in patients if p["glucose"] > 99)
        st.markdown(f'<div class="metric-card"><h3>{high_glucose}</h3><p>High Glucose</p></div>', unsafe_allow_html=True)
    with col3:
        low_haemo = sum(1 for p in patients if p["haemoglobin"] < 12)
        st.markdown(f'<div class="metric-card"><h3>{low_haemo}</h3><p>Low Haemoglobin</p></div>', unsafe_allow_html=True)
    with col4:
        high_chol = sum(1 for p in patients if p["cholesterol"] > 200)
        st.markdown(f'<div class="metric-card"><h3>{high_chol}</h3><p>High Cholesterol</p></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if not patients:
        st.info("📭 No patient records found. Use Add Patient to get started.")
    else:
        df = pd.DataFrame(patients)
        df = df.rename(columns={
            "id": "ID", "full_name": "Full Name", "dob": "Date of Birth",
            "email": "Email", "glucose": "Glucose (mg/dL)",
            "haemoglobin": "Haemoglobin (g/dL)", "cholesterol": "Cholesterol (mg/dL)",
            "remarks": "AI Health Remarks", "created_at": "Added On"
        })
        df = df.drop(columns=["Added On"])
        st.dataframe(df, use_container_width=True, height=400)
        st.caption(f"Showing {total} patient record(s).")
        st.markdown("---")
        st.markdown("**View Full AI Remarks for a Patient:**")
        selected_id = st.selectbox(
            "Select Patient ID",
            options=[p["id"] for p in patients],
            format_func=lambda x: f"ID {x} — {next(p['full_name'] for p in patients if p['id'] == x)}"
        )
        if selected_id:
            patient = db.fetch_patient_by_id(selected_id)
            if patient and patient.get("remarks"):
                st.markdown(f'<div class="remark-box">🤖 <strong>AI Health Prediction:</strong><br><br>{patient["remarks"]}</div>', unsafe_allow_html=True)

elif page == "➕ Add Patient":
    st.markdown('<p class="section-title">➕ Add New Patient Record</p>', unsafe_allow_html=True)
    st.markdown("Fill in the patient details below. AI health prediction will be generated automatically.")
    st.markdown("<br>", unsafe_allow_html=True)
    with st.form("add_patient_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**👤 Personal Information**")
            full_name = st.text_input("Full Name *", placeholder="e.g. John Smith")
            dob = st.date_input("Date of Birth *", min_value=date(1900, 1, 1), max_value=date.today(), value=date(1990, 1, 1))
            email = st.text_input("Email Address *", placeholder="e.g. john@example.com")
        with col2:
            st.markdown("**🩸 Blood Test Results**")
            glucose = st.number_input("Glucose (mg/dL) *", min_value=0.0, max_value=999.0, value=90.0, step=0.1, help="Normal fasting range: 70-99 mg/dL")
            haemoglobin = st.number_input("Haemoglobin (g/dL) *", min_value=0.0, max_value=50.0, value=13.5, step=0.1, help="Normal: Men 13.5-17.5, Women 12.0-15.5 g/dL")
            cholesterol = st.number_input("Cholesterol (mg/dL) *", min_value=0.0, max_value=999.0, value=180.0, step=0.1, help="Desirable: Below 200 mg/dL")
        st.markdown("---")
        submit = st.form_submit_button("🤖 Save & Generate AI Prediction", use_container_width=True)
    if submit:
        is_valid, error_msg = validate_patient_form(full_name, dob, email, glucose, haemoglobin, cholesterol)
        if not is_valid:
            st.markdown(f'<div class="error-msg">❌ {error_msg}</div>', unsafe_allow_html=True)
        else:
            with st.spinner("🤖 Generating AI health prediction via Claude API..."):
                remarks = ai.get_health_prediction(full_name=full_name, dob=str(dob), glucose=glucose, haemoglobin=haemoglobin, cholesterol=cholesterol)
            success, message = db.insert_patient(full_name=full_name.strip(), dob=str(dob), email=email.strip().lower(), glucose=glucose, haemoglobin=haemoglobin, cholesterol=cholesterol, remarks=remarks)
            if success:
                st.markdown(f'<div class="success-msg">✅ {message}</div>', unsafe_allow_html=True)
                st.markdown("**🤖 AI Health Prediction:**")
                st.markdown(f'<div class="remark-box">{remarks}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="error-msg">❌ {message}</div>', unsafe_allow_html=True)

elif page == "✏️ Edit Patient":
    st.markdown('<p class="section-title">✏️ Edit Patient Record</p>', unsafe_allow_html=True)
    patients = db.fetch_all_patients()
    if not patients:
        st.info("📭 No records available to edit. Add a patient first.")
    else:
        selected_id = st.selectbox(
            "Select Patient to Edit:",
            options=[p["id"] for p in patients],
            format_func=lambda x: f"ID {x} — {next(p['full_name'] for p in patients if p['id'] == x)}"
        )
        patient = db.fetch_patient_by_id(selected_id)
        if patient:
            st.markdown(f"**Editing record for:** `{patient['full_name']}`")
            st.markdown("<br>", unsafe_allow_html=True)
            with st.form("edit_patient_form"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**👤 Personal Information**")
                    full_name = st.text_input("Full Name *", value=patient["full_name"])
                    dob = st.date_input("Date of Birth *", value=datetime.strptime(patient["dob"], "%Y-%m-%d").date(), min_value=date(1900, 1, 1), max_value=date.today())
                    email = st.text_input("Email Address *", value=patient["email"])
                with col2:
                    st.markdown("**🩸 Blood Test Results**")
                    glucose = st.number_input("Glucose (mg/dL) *", value=float(patient["glucose"]), min_value=0.0, max_value=999.0, step=0.1)
                    haemoglobin = st.number_input("Haemoglobin (g/dL) *", value=float(patient["haemoglobin"]), min_value=0.0, max_value=50.0, step=0.1)
                    cholesterol = st.number_input("Cholesterol (mg/dL) *", value=float(patient["cholesterol"]), min_value=0.0, max_value=999.0, step=0.1)
                regenerate = st.checkbox("🔄 Regenerate AI Prediction", value=False)
                st.markdown("---")
                update_btn = st.form_submit_button("💾 Update Record", use_container_width=True)
            if update_btn:
                is_valid, error_msg = validate_patient_form(full_name, dob, email, glucose, haemoglobin, cholesterol)
                if not is_valid:
                    st.markdown(f'<div class="error-msg">❌ {error_msg}</div>', unsafe_allow_html=True)
                else:
                    if regenerate:
                        with st.spinner("🤖 Regenerating AI health prediction..."):
                            remarks = ai.get_health_prediction(full_name=full_name, dob=str(dob), glucose=glucose, haemoglobin=haemoglobin, cholesterol=cholesterol)
                    else:
                        remarks = patient["remarks"]
                    success, message = db.update_patient(patient_id=selected_id, full_name=full_name.strip(), dob=str(dob), email=email.strip().lower(), glucose=glucose, haemoglobin=haemoglobin, cholesterol=cholesterol, remarks=remarks)
                    if success:
                        st.markdown(f'<div class="success-msg">✅ {message}</div>', unsafe_allow_html=True)
                        if regenerate:
                            st.markdown(f'<div class="remark-box">{remarks}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="error-msg">❌ {message}</div>', unsafe_allow_html=True)

elif page == "🗑️ Delete Patient":
    st.markdown('<p class="section-title">🗑️ Delete Patient Record</p>', unsafe_allow_html=True)
    st.warning("⚠️ Deleting a record is permanent and cannot be undone.")
    patients = db.fetch_all_patients()
    if not patients:
        st.info("📭 No records available to delete.")
    else:
        selected_id = st.selectbox(
            "Select Patient to Delete:",
            options=[p["id"] for p in patients],
            format_func=lambda x: f"ID {x} — {next(p['full_name'] for p in patients if p['id'] == x)}"
        )
        patient = db.fetch_patient_by_id(selected_id)
        if patient:
            col1, col2, col3 = st.columns(3)
            col1.metric("Name", patient["full_name"])
            col2.metric("Email", patient["email"])
            col3.metric("Date of Birth", patient["dob"])
            st.markdown("<br>", unsafe_allow_html=True)
            confirm = st.checkbox(f"✅ I confirm I want to permanently delete this record.")
            if confirm:
                if st.button("🗑️ Delete Record", type="primary"):
                    success, message = db.delete_patient(selected_id)
                    if success:
                        st.markdown(f'<div class="success-msg">✅ {message}</div>', unsafe_allow_html=True)
                        st.rerun()
                    else:
                        st.markdown(f'<div class="error-msg">❌ {message}</div>', unsafe_allow_html=True)

elif page == "🔍 Search Records":
    st.markdown('<p class="section-title">🔍 Search Patient Records</p>', unsafe_allow_html=True)
    query = st.text_input("Search by Name or Email:", placeholder="e.g. John or john@example.com")
    if query:
        results = db.search_patients(query)
        if not results:
            st.info(f"🔍 No patients found matching '{query}'.")
        else:
            st.success(f"✅ Found {len(results)} matching record(s).")
            df = pd.DataFrame(results)
            df = df.rename(columns={
                "id": "ID", "full_name": "Full Name", "dob": "Date of Birth",
                "email": "Email", "glucose": "Glucose", "haemoglobin": "Haemoglobin",
                "cholesterol": "Cholesterol", "remarks": "AI Remarks", "created_at": "Added On"
            })
            df = df.drop(columns=["Added On"])
            st.dataframe(df, use_container_width=True)
            sel = st.selectbox("View full AI remarks for:", options=[r["id"] for r in results],
                                format_func=lambda x: f"ID {x} — {next(r['full_name'] for r in results if r['id'] == x)}")
            p = next((r for r in results if r["id"] == sel), None)
            if p and p.get("remarks"):
                st.markdown(f'<div class="remark-box">🤖 {p["remarks"]}</div>', unsafe_allow_html=True)
    else:
        st.info("Type a name or email above to search records.")

st.markdown("---")
st.markdown("<p style='text-align:center; color:#94a3b8; font-size:0.8rem;'>MIRA – Medical Intelligence Robotic Automation | Powered by Claude AI (Anthropic) | Built with Python & Streamlit</p>", unsafe_allow_html=True)