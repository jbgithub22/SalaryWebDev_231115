import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map

def clean_experience(x):
    if x == 'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)

def clean_country(x):
    if x == 'United States of America':
        return 'United States'
    if x == 'United Kingdom of Great Britain and Northern Ireland':
        return 'United Kingdom'
    return x

@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\Users\jbarcc\Desktop\Hobby\CS - ML_Local\SalaryWebDev_231115\datasets\stack-overflow-developer-survey-2023\survey_results_public.csv")

    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedCompYearly"]]
    df = df.rename({"ConvertedCompYearly": "Salary"}, axis=1)
    df = df[df["Salary"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed, full-time"]
    df = df.drop("Employment", axis=1)

    country_map = shorten_categories(df.Country.value_counts(), 400)
    df['Country'] = df['Country'].map(country_map)

    df = df[df["Salary"] <= 350000]
    df = df[df["Salary"] >= 10000]
    df = df[df['Country'] != 'Other']

    df['YearsCodePro'] = df['YearsCodePro'].apply(clean_experience)
    df['Country'] = df['Country'].apply(clean_country)

    return df

df = load_data()

def show_explore_page():
    st.title("Explore Software Engineer Salaries")
    st.write("""### Stack Overflow Developer Survey 2020""")

#|| Pie Chart -----------------------------------------------------

    st.write("""#### Number of Data from different countries""")

    data = df["Country"].value_counts()

    fig1, ax1 = plt.subplots()
    patches, labels, pct_texts = ax1.pie(data, 
                                        labels=data.index, 
                                        autopct="%1.1f%%", 
                                        pctdistance = 1.15,
                                        rotatelabels = True,
                                        labeldistance = 1.3,
                                        startangle=90
                                        )
    for label, pct_text in zip(labels, pct_texts):
        pct_text.set_rotation(label.get_rotation())
    ax1.axis("equal") # Equal aspect ratio ensures that pie is drawn as a circle

    st.pyplot(fig1)

#|| Bar Chart -----------------------------------------------------

    st.write("""### Mean Salary Based on Country""")

    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    
    st.bar_chart(data)

#|| Line Chart -----------------------------------------------------

    st.write("""### Mean Salary Based on Experience""")

    data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
   
    st.line_chart(data)

#|| Box Plot -----------------------------------------------------

    st.write("""### Box plot of Salary against Country""")

    fig4, ax = plt.subplots(1,1, figsize=(12,7))
    df.boxplot('Salary', 'Country', ax=ax)
    plt.suptitle('Salary (US$) vs Country')
    plt.title('')
    plt.ylabel('Salary')
    plt.xticks(rotation=90)

    st.pyplot(fig4)

    