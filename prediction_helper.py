import pandas as pd
from joblib import load

model_young = load("artifacts/model_young.joblib")
model_rest = load("artifacts/model_rest.joblib")

scaler_young = load("artifacts/scaler_young")
scaler_rest = load("artifacts/scaler_rest.joblib")


def calculate_normalized_risk_score(medical_history):
    risk_scores = {
        "diabetes": 6,
        "heart disease": 8,
        "high blood pressure": 6,
        "thyroid": 5,
        "no disease": 0,
        "none": 0
    }

    diseases = medical_history.lower().split(" & ")
    total_risk_score = 0
    for disease in diseases:
        total_risk_score += risk_scores.get(disease, 0)
    max_score = 14
    min_score = 0

    normalized_risk_score = (total_risk_score - min_score)/(max_score-min_score)

    return normalized_risk_score


def preprocessing(input_dict):
    expected_columns =("age","number_of_dependants","income_lakhs","insurance_plan","genetical_risk","normalized_risk_score",
                       "gender_Male","region_Northwest","region_Southeast","region_Southwest","marital_status_Unmarried",
                       "bmi_category_Obesity","bmi_category_Overweight","bmi_category_Underweight","smoking_status_Occasional",
                       "smoking_status_Regular", "employment_status_Salaried" ,"employment_status_Self-Employed")



    df = pd.DataFrame(0 ,columns = expected_columns , index = [0])
    insurance_plan_encoding = {
        'Bronze': 1,
        'Silver':2 ,
        'Gold':3
    }
    for key , value in input_dict.items():
        if key == "Gender" and value=="Male":
            df["gender_Male"] = 1
        elif key  == "Region":
            if value =="Northwest":
                df["region_Northwest"]=1
            elif value =="Southeast":
                df["region_Southeast"]=1
            elif value =="Southwest":
                df["region_Southwest"]=1
        elif key == "Marital Status"and value == "Unmarried":
            df["marital_status_Unmarried"]=1
        elif key == "BMI Category":
            if value == "Obesity":
                df["bmi_category_Obesity"]=1
            elif value == "Overweight":
                df["bmi_category_Overweight"]=1
            elif value == "Underweight":
                df["bmi_category_Underweight"]=1
        elif key == "Smoking Status":
            if value == "Occasional":
                df["smoking_status_Occasional"]=1
            elif value == "Regular":
                df[ "smoking_status_Regular"]=1
        elif key == "Employment Status":
            if value == "Salaried":
                df["employment_status_Salaried"]=1
            if value == "Self-Employed":
                df["employment_status_Self-Employed"]=1
        elif key == "Insurance Plan":
            df["insurance_plan"]= insurance_plan_encoding.get(value,1)
        elif key =="Age":
            df["age"]=value
        elif key =="Genetical Risk":
            df["genetical_risk"]= value
        elif key == "Number of Dependants":
            df["number_of_dependants"]=value
        elif key == "Income in Lakhs":
            df["income_lakhs"]= value

    df["normalized_risk_score"] =calculate_normalized_risk_score(input_dict["Medical History"])


    df = handle_scaling((input_dict["Age"]), df)
    return df

def handle_scaling(age, df):
    if age <= 25:
       scaler_object = scaler_young
    else:
       scaler_object = scaler_rest

    scaling_columns = scaler_object["scaling_columns"]
    scaler = scaler_object["scaler"]

    df["income_level"]=None
    df[scaling_columns]=scaler.transform(df[scaling_columns])
    df.drop("income_level" , axis = 1 , inplace =True)
    return df

def predict(input_dict):
    input_df = preprocessing(input_dict)

    if input_dict["Age"]<=25:
        prediction =model_young.predict(input_df)
    else:
        prediction = model_rest.predict(input_df)

    return int(prediction)