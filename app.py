import streamlit as st
import math
from fpdf import FPDF
import random

# ------------------------- PAGE CONFIG -------------------------
st.set_page_config(page_title="BMI & Health Calculators", page_icon="💪", layout="centered")

# ------------------------- THEME HANDLER -------------------------
if "theme" not in st.session_state:
    st.session_state.theme = "light"

def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

def apply_theme():
    if st.session_state.theme == "dark":
        st.markdown("""
            <style>
            body { background-color: #121212; color: #fff; }
            .stTabs [role="tablist"] { justify-content: center; }
            .stButton>button { background-color: #262730; color: white; border: none; }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
            body { background-color: #f8f9fa; color: #000; }
            .stTabs [role="tablist"] { justify-content: center; }
            .stButton>button { background-color: #90ee90; color: black; border: none; }
            </style>
        """, unsafe_allow_html=True)

apply_theme()

# ------------------------- HEADER -------------------------
col1, col2 = st.columns([6, 1])
with col1:
    st.title("💪 BMI & Health Calculators")
with col2:
    if st.button("🌗 Theme"):
        toggle_theme()
        st.rerun()

st.markdown("---")

# ------------------------- HEALTH TIPS -------------------------
tips = [
    "🥦 Eat a balanced diet rich in fruits and veggies.",
    "🚶 Walk 30 minutes daily for better metabolism.",
    "💧 Drink at least 8 glasses of water daily.",
    "😴 Sleep 7–8 hours for good recovery.",
    "🧘‍♀️ Stretch every hour if you work long hours.",
    "🏋️ Stay active — consistency beats intensity!"
]
st.info(f"💡 Health Tip: {random.choice(tips)}")

# ------------------------- PDF GENERATION -------------------------
def create_pdf(results):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 18)
    pdf.cell(190, 10, "Health Report", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.ln(10)
    for key, value in results.items():
        pdf.cell(0, 10, f"{key}: {value}", ln=True)
    pdf.output("health_report.pdf")
    return "health_report.pdf"

# ------------------------- MAIN APP TABS -------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🏋️ BMI", "🔥 BMR", "📉 Body Fat %", "⚖️ Ideal Weight"
])

# ------------------------- BMI CALCULATOR -------------------------
with tab1:
    st.subheader("🏋️ BMI Calculator")
    height_unit = st.selectbox("Height Unit", ["cm", "ft/in"])
    if height_unit == "cm":
        height = st.number_input("Height (cm)", 50.0, 250.0, 170.0)
    else:
        ft = st.number_input("Height (ft)", 1.0, 8.0, 5.0)
        inch = st.number_input("Height (in)", 0.0, 11.0, 7.0)
        height = ft * 30.48 + inch * 2.54

    weight_unit = st.selectbox("Weight Unit", ["kg", "lbs"])
    weight = st.number_input(f"Weight ({weight_unit})", 10.0, 300.0, 65.0)
    if weight_unit == "lbs":
        weight *= 0.453592

    if st.button("Calculate BMI"):
        bmi = weight / ((height / 100) ** 2)
        category = (
            "Underweight" if bmi < 18.5 else
            "Normal" if bmi < 25 else
            "Overweight" if bmi < 30 else
            "Obese"
        )
        st.success(f"Your BMI: **{bmi:.2f}** — {category}")
        if category == "Normal":
            st.balloons()
        elif category == "Overweight":
            st.warning("Try adding daily exercise and monitor your diet.")
        elif category == "Obese":
            st.error("Consult a healthcare professional for personalized advice.")

# ------------------------- BMR CALCULATOR -------------------------
with tab2:
    st.subheader("🔥 BMR Calculator")
    gender = st.radio("Gender", ["Male", "Female"])
    age = st.number_input("Age", 10, 100, 25)
    height = st.number_input("Height (cm)", 50.0, 250.0, 170.0)
    weight = st.number_input("Weight (kg)", 10.0, 300.0, 65.0)
    activity = st.selectbox("Activity Level", ["Sedentary", "Light", "Moderate", "Active", "Very Active"])

    if st.button("Calculate BMR"):
        if gender == "Male":
            bmr = 88.36 + (13.4 * weight) + (4.8 * height) - (5.7 * age)
        else:
            bmr = 447.6 + (9.2 * weight) + (3.1 * height) - (4.3 * age)

        activity_multiplier = {
            "Sedentary": 1.2,
            "Light": 1.375,
            "Moderate": 1.55,
            "Active": 1.725,
            "Very Active": 1.9
        }
        calories = bmr * activity_multiplier[activity]
        st.success(f"Your BMR is **{bmr:.1f} kcal/day**")
        st.info(f"To maintain your weight, consume around **{calories:.0f} kcal/day**")
        st.snow()

# ------------------------- BODY FAT -------------------------
with tab3:
    st.subheader("📉 Body Fat % Estimation")
    gender = st.selectbox("Gender", ["Male", "Female"], key="bf_gender")
    waist = st.number_input("Waist (cm)", 30.0, 200.0, 70.0)
    neck = st.number_input("Neck (cm)", 20.0, 100.0, 35.0)
    height = st.number_input("Height (cm)", 50.0, 250.0, 170.0)
    hip = st.number_input("Hip (cm) [Females only]", 30.0, 200.0, 90.0)

    if st.button("Calculate Body Fat %"):
        if gender == "Male":
            bf = 495 / (1.0324 - 0.19077 * math.log10(waist - neck) + 0.15456 * math.log10(height)) - 450
        else:
            bf = 495 / (1.29579 - 0.35004 * math.log10(waist + hip - neck) + 0.22100 * math.log10(height)) - 450
        st.success(f"Your estimated Body Fat %: **{bf:.2f}%**")

# ------------------------- IDEAL WEIGHT -------------------------
with tab4:
    st.subheader("⚖️ Ideal Weight Calculator")
    gender = st.selectbox("Gender", ["Male", "Female"], key="ideal_gender")
    height = st.number_input("Height (cm)", 50.0, 250.0, 170.0, key="ideal_height")

    if st.button("Calculate Ideal Weight"):
        ideal = 50 + 0.9 * (height - 152) if gender == "Male" else 45.5 + 0.9 * (height - 152)
        st.success(f"Your Ideal Weight: **{ideal:.1f} kg**")

# ------------------------- DOWNLOAD REPORT -------------------------
st.markdown("---")
st.subheader("🧾 Download Health Report")
if st.button("Generate PDF"):
    results = {
        "BMI": "See tab 1",
        "BMR": "See tab 2",
        "Body Fat %": "See tab 3",
        "Ideal Weight": "See tab 4",
    }
    file_path = create_pdf(results)
    with open(file_path, "rb") as f:
        st.download_button("⬇️ Download PDF", f, file_name="Health_Report.pdf")
