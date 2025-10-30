import streamlit as st
from fpdf import FPDF

# --- APP CONFIG ---
st.set_page_config(page_title="BMI & Health Calculator", layout="centered")

# --- THEME SWITCH ---
st.sidebar.title("🌓 Theme Settings")
theme = st.sidebar.radio("Choose Theme", ["🌙 Dark Mode", "☀️ Light Mode"])

if theme == "🌙 Dark Mode":
    st.markdown(
        """
        <style>
        body, .stApp {background-color: #0e1117; color: #f5f5f5;}
        div[data-testid="stSidebar"] {background-color: #1a1d23;}
        .stButton>button {background-color: #4CAF50; color: white;}
        </style>
        """, unsafe_allow_html=True)
else:
    st.markdown(
        """
        <style>
        body, .stApp {background-color: #ffffff; color: #000000;}
        div[data-testid="stSidebar"] {background-color: #f7f7f7;}
        .stButton>button {background-color: #2196F3; color: white;}
        </style>
        """, unsafe_allow_html=True)

# --- HEADER ---
st.title("🏋️ BMI & Health Calculator")
st.markdown("Calculate your **Body Mass Index (BMI)** and get a quick health summary.")

# --- INPUTS ---
st.header("Enter Your Details")
col1, col2 = st.columns(2)
with col1:
    height = st.number_input("Height (cm):", min_value=50.0, max_value=250.0, value=170.0, key="height")
with col2:
    weight = st.number_input("Weight (kg):", min_value=10.0, max_value=300.0, value=70.0, key="weight")

age = st.number_input("Age:", min_value=5, max_value=120, value=25, key="age")
gender = st.radio("Gender:", ["Male", "Female"], horizontal=True, key="gender")

# --- CALCULATE BMI ---
if st.button("Calculate BMI", key="calc_bmi"):
    bmi = round(weight / ((height / 100) ** 2), 2)
    if bmi < 18.5:
        status = "Underweight"
    elif bmi < 24.9:
        status = "Normal"
    elif bmi < 29.9:
        status = "Overweight"
    else:
        status = "Obese"

    st.success(f"Your BMI is **{bmi}**, which is considered **{status}**.")

    # --- HEALTH TIPS ---
    st.markdown("### 💡 Health Tips:")
    tips = {
        "Underweight": "Increase calorie intake and include protein-rich foods.",
        "Normal": "Maintain a balanced diet and regular exercise.",
        "Overweight": "Add cardio workouts and reduce sugar/fat intake.",
        "Obese": "Consult a dietitian and follow a structured workout plan."
    }
    st.info(tips[status])

    # --- PDF GENERATION ---
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="BMI & Health Report", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Height: {height} cm", ln=True)
    pdf.cell(200, 10, txt=f"Weight: {weight} kg", ln=True)
    pdf.cell(200, 10, txt=f"Age: {age}", ln=True)
    pdf.cell(200, 10, txt=f"Gender: {gender}", ln=True)
    pdf.cell(200, 10, txt=f"BMI: {bmi}", ln=True)
    pdf.cell(200, 10, txt=f"Health Status: {status}", ln=True)
    pdf.ln(5)
    pdf.multi_cell(0, 10, f"Health Tip: {tips[status]}")

    pdf_file = "BMI_Report.pdf"
    pdf.output(pdf_file)
    with open(pdf_file, "rb") as f:
        st.download_button("📄 Download PDF Report", f, file_name=pdf_file)

# --- FOOTER ---
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("💻 Developed with ❤️ using Streamlit", unsafe_allow_html=True)
