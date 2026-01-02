import pandas as pd
import streamlit as st
from prediction_helper import predict

st.title("Health Insurance Premium Prediction ")

# Creating columns
categorical_columns = {
    'gender': ['Male', 'Female'],
    'region': ['Northwest', 'Southeast', 'Northeast', 'Southwest'],
    'marital_status': ['Unmarried', 'Married'],
    'bmi_category': ['Underweight', 'Normal', 'Overweight', 'Obesity'],
    'smoking_status': [
        'Does Not Smoke',
        'Occasional',
        'Regular'
    ],
    'employment_status': ['Salaried', 'Self-Employed', 'Freelancer'],
    'income_level': ['<10L', '10L - 25L', '25L - 40L', '> 40L'],
    'medical_history': [
        'No Disease',
        'Diabetes',
        'High blood pressure',
        'Thyroid',
        'Heart disease',
        'Diabetes & High blood pressure',
        'Diabetes & Thyroid',
        'Diabetes & Heart disease',
        'High blood pressure & Heart disease'
    ],
    'insurance_plan': ['Bronze', 'Silver', 'Gold']
}

# Creating rows

row1 = st.columns(3)
row2 = st.columns(3)
row3 = st.columns(3)
row4 = st.columns(3)

# Assigning inputs to the columns in rows

with row1[0]:
    age = st.number_input("Age" , min_value =18 , max_value = 100 , step=1)
with row1[1]:
    number_of_dependants = st.number_input("Number of Dependants" , min_value=0 , max_value=20 , step=1)
with row1[2]:
    income_lakhs = st.number_input("Income in Lakhs" , min_value=1 , max_value =200 , step=1)


with row2[0]:
    genetical_risk = st.number_input("Genetical Risk", min_value=0 , max_value = 5 , step=1)
with row2[1]:
    insurance_plan = st.selectbox("Insurance Plan",categorical_columns['insurance_plan'])
with row2[2]:
    employment_status = st.selectbox("Employment Status",categorical_columns["employment_status"])

with row3[0]:
    marital_status = st.selectbox("Marital Status" , categorical_columns['marital_status'])
with row3[1]:
    bmi_category = st.selectbox("BMI Category",categorical_columns['bmi_category'])
with row3[2]:
    gender = st.selectbox("Gender", categorical_columns['gender'])


with row4[0]:
    region = st.selectbox("Region", categorical_columns['region'])
with row4[1]:
    smoking_status =st.selectbox("Smoking status",categorical_columns['smoking_status'])
with row4[2]:
    medical_history = st.selectbox("Medical History", categorical_columns['medical_history'])

# Creating a dictionary for input values

input_dict={
    "Age":age,
    "Number of Dependants":number_of_dependants,
    "Income in Lakhs"  :income_lakhs,
    "Genetical Risk" : genetical_risk,
    "Insurance Plan": insurance_plan,
    "Employment Status":employment_status,
    "Marital Status":marital_status,
    "BMI Category" :bmi_category,
    "Gender": gender,
    "Region": region,
    "Smoking Status": smoking_status,
    "Medical History" : medical_history
}
input_df = pd.DataFrame([input_dict])

if st.button("Predict"):
   prediction= predict(input_dict)

   st.success(f"Premium Predicted : {prediction}")
