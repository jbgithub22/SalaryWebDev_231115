import streamlit as st
import pickle
import numpy as np

def load_model():
    with open('save_steps.pkl', 'rb') as file:
       data = pickle.load(file)
    return data

data = load_model()

regressor= data["model"]
le_country = data["le_country"]
le_education = data["le_education"]

def show_predict_page():
    st.title("Software Developer Salary Prediction")

    st.write("""### We need some information to predict the salary""")

    countries = (
        'United States of America',
        'United Kingdom of Great Britain and Northern Ireland',
        'Australia', 
        'Netherlands', 
        'Germany', 
        'Sweden', 
        'France', 
        'Spain',
        'Brazil', 
        'Italy', 
        'Canada', 
        'Switzerland', 
        'India', 
        'Norway',
        'Denmark', 
        'Israel', 
        'Poland',
    )

    education = (
        "Bachelor’s degree (B.A., B.S., B.Eng., etc.)",
        'Some college/university study without earning a degree',
        "Master’s degree (M.A., M.S., M.Eng., MBA, etc.)",
        'Professional degree (JD, MD, Ph.D, Ed.D, etc.)',
        'Associate degree (A.A., A.S., etc.)',
        'Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)',
        'Primary/elementary school', 
        'Something else',
    )

    selected_country = st.selectbox("Country", countries)
    selected_education = st.selectbox("Education Level", education)
    selected_experience = st.slider("Years of Experience", 0, 50, 3)

    ok = st.button("Calculate Salary")
    if ok:
        X = np.array([[selected_country, selected_education, selected_experience]])
        X[:, 0] = le_country.transform(X[:, 0])
        X[:, 1] = le_education.transform(X[:, 1])
        X = X.astype(float)

        salary = regressor.predict(X)
        st.subheader(f"The estimated salary is ${salary[0]:.2f}")


        