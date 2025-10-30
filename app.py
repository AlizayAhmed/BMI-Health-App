import streamlit as st
import math
from fpdf import FPDF
import time
import random

# -------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------
st.set_page_config(page_title="BMI & Health Calculators", page_icon="💪", layout="centered")

# -------------------------------------------
# THEME SETTINGS
# -------------------------------------------
if "theme" not in st.session_state:
    st.session_state.theme = "light"

def set_theme():
    if st.session_state.theme == "light":
        st.markdown("""
            <style>
            body { background-color: #f9f9f9; color: #000; }
            .stTabs [role="tablist"] { justify-content: center; }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
            body { background-color: #1e1e1e; color: #fff; }
            .stTabs [role="tablist"] { justify-content: center; }
            </style>
        """, unsafe_allow_html=True)

def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

set_theme()

# -------------------------------------------
# HEADER SECTION
# -------------------------------------------
col1, col2 = st.columns([6,1])
with col1:
    st.title("💪 BMI & Health Calculators")
with col2:
    if st.button("🌗 Toggle Theme"):
        toggle_theme()
        st.rerun()

# -------------------------------------------
# PDF GENERATION FUNCTION
# -------------------------------------------
def generate_pdf(results):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "BMI & Health Report", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.ln(10)
    for key, value in results.items():
        pdf.cell(0, 10, f"{key}: {value}", ln=True)
    pdf.output("health_report.pdf")
    return "health_report.pdf"

# -------------------------------------------
# HEALTH TIPS
# -------------------------------------------
tips = [
    "🥦 Eat a balanced diet rich in fruits and vegetables.",
    "🚶 Walk at least 30 minutes daily.",
    "💧 Drink 8 glasses of water every day.",
    "😴 Sleep at least 7 hours each night.",
    "🧘‍♀️ Stretch for 5 minutes every hour.",
    "🏃 Stay active and keep moving!",
]
tip = random.choice(tips)
st.info(f"💡 Health Tip: {tip}")

# -------------------------------------------
# TABS FOR CALCULATORS
# -------------------------------------------
tabs = st.tabs(["🏋️ BMI Calculator", "🔥 BMR Calculator", "📉 Body Fat %", "⚖️ Ideal Weight"])

# -------------------------------------------
# 1. BMI CALCULATOR
# -------------------------------------------
with tabs[0]:
    st.subheader("🏋️ BMI Calculator")
    height_unit = st.selectbox("Height Unit", ["cm", "ft/in"])
    if height_unit == "cm":
        height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=170.0)
    else:
        ft = st.number_input("Height (ft)", min_value=1.0, max_value=8.0, value=5.0)
        inch = st.number_input("Height (in)", min_value=0.0, max_value=11.0, value=7.0)
        height = ft * 30.48 + inch * 2.54

    weight_unit = st.selectbox("Weight Unit", ["kg", "lbs"])
    weight = st.number_input(f"Weight ({weight_unit})", min_value=10.0, max_value=300.0, value=65.0)
    if weight_unit == "lbs":
        weight *= 0.453592

    if st.button("Calculate BMI"):
        bmi = weight / ((height / 100) ** 2)
        category = (
            "Underweight" if bmi < 18.5 else
            "Normal weight" if bmi < 25 else
            "Overweight" if bmi < 30 else
            "Obese"
        )
        st.success(f"Your BMI is **{bmi:.2f}**, Category: **{category}**")
        if category == "Underweight":
            st.info("Eat nutrient-rich foods and increase calorie intake gradually.")
        elif category == "Normal weight":
            st.success("Great! Maintain your balanced diet and regular exercise.")
        elif category == "Overweight":
            st.warning("Try regular exercise and a balanced, lower-calorie diet.")
        else:
            st.error("Consult a doctor for personalized advice on weight management.")
        st.balloons()

# -------------------------------------------
# 2. BMR CALCULATOR
# -------------------------------------------
with tabs[1]:
    st.subheader("🔥 BMR (Basal Metabolic Rate) Calculator")
    gender = st.selectbox("Gender", ["Male", "Female"])
    age = st.number_input("Age", min_value=10, max_value=100, value=25)
    height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=170.0)
    weight = st.number_input("Weight (kg)", min_value=10.0, max_value=300.0, value=65.0)
    activity = st.selectbox("Activity Level", ["Sedentary", "Light", "Moderate", "Active", "Very Active"])

    if st.button("Calculate BMR"):
        if gender == "Male":
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        else:
            bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

        multiplier = {
            "Sedentary": 1.2,
            "Light": 1.375,
            "Moderate": 1.55,
            "Active": 1.725,
            "Very Active": 1.9
        }[activity]

        daily_calories = bmr * multiplier
        st.success(f"Your BMR is **{bmr:.2f} kcal/day**.")
        st.info(f"To maintain your weight, you need approximately **{daily_calories:.0f} calories/day**.")
        st.snow()

# -------------------------------------------
# 3. BODY FAT PERCENTAGE
# -------------------------------------------
with tabs[2]:
    st.subheader("📉 Body Fat Percentage Estimator")
    gender = st.selectbox("Gender", ["Male", "Female"], key="bodyfat_gender")
    age = st.number_input("Age", min_value=10, max_value=100, value=25, key="bodyfat_age")
    weight = st.number_input("Weight (kg)", min_value=10.0, max_value=300.0, value=65.0, key="bodyfat_weight")
    height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=170.0, key="bodyfat_height")
    waist = st.number_input("Waist (cm)", min_value=30.0, max_value=200.0, value=70.0, key="bodyfat_waist")
    neck = st.number_input("Neck (cm)", min_value=20.0, max_value=100.0, value=35.0, key="bodyfat_neck")
    hip = st.number_input("Hip (cm) (optional for females)", min_value=30.0, max_value=200.0, value=90.0, key="bodyfat_hip")

    if st.button("Calculate Body Fat %"):
        if gender == "Male":
            body_fat = 495 / (1.0324 - 0.19077 * math.log10(waist - neck) + 0.15456 * math.log10(height)) - 450
        else:
            body_fat = 495 / (1.29579 - 0.35004 * math.log10(waist + hip - neck) + 0.22100 * math.log10(height)) - 450

        st.success(f"Your estimated body fat is **{body_fat:.2f}%**")

        if body_fat < 6:
            st.info("Essential fat level.")
        elif body_fat < 14:
            st.success("Athlete level.")
        elif body_fat < 21:
            st.info("Fit range.")
        elif body_fat < 25:
            st.warning("Average range.")
        else:
            st.error("Obese range. Consult a physician for advice.")

# -------------------------------------------
# 4. IDEAL WEIGHT
# -------------------------------------------
with tabs[3]:
    st.subheader("⚖️ Ideal Weight Calculator")
    gender = st.selectbox("Gender", ["Male", "Female"], key="ideal_gender")
    height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=170.0, key="ideal_height")

    if st.button("Calculate Ideal Weight"):
        if gender == "Male":
            ideal = 50 + 0.9 * (height - 152)
        else:
            ideal = 45.5 + 0.9 * (height - 152)
        range_low = ideal - 5
        range_high = ideal + 5
        st.success(f"Your ideal weight range is **{range_low:.1f} – {range_high:.1f} kg**")

# -------------------------------------------
# DOWNLOAD REPORT
# -------------------------------------------
st.divider()
st.subheader("🧾 Download Your Health Report")
if st.button("Generate PDF Summary"):
    results = {
        "BMI": "Calculated above if used",
        "BMR": "Calculated above if used",
        "Body Fat %": "Calculated above if used",
        "Ideal Weight": "Calculated above if used"
    }
    pdf_file = generate_pdf(results)
    with open(pdf_file, "rb") as file:
        st.download_button("⬇️ Download Report", file, file_name="Health_Report.pdf")
