import dash
from dash import dcc, html, Input, Output
import pandas as pd
import re
from collections import Counter
import plotly.express as px
from wordcloud import WordCloud
import numpy as np
from dash.dash_table import DataTable

# Load the dataset
data = pd.read_csv("convdata.csv", nrows=3000)

# Function to extract symptoms, diseases, and other information
def extract_information(conversation):
    symptoms_keywords = [
        "fever", "cough", "dyspnea", "difficulty breathing", "fatigue", "headache", "nausea", "vomiting", "diarrhea", "abdominal pain",
        "chest pain", "shortness of breath", "sore throat", "muscle aches", "loss of taste or smell", "rash", "swelling", "joint pain"
    ]
    diseases_keywords = [
        "COVID-19", "ARDS", "heart disease", "diabetes", "hypertension", "asthma", "malaria", "tuberculosis", "pneumonia", "flu",
        "kidney disease", "liver disease", "stroke", "depression", "anxiety", "cancer", "arthritis", "diarrhea", "gastritis", "IBS"
    ]

    symptoms = []
    diseases = []

    for symptom in symptoms_keywords:
        if re.search(symptom, conversation, re.IGNORECASE):
            symptoms.append(symptom)

    for disease in diseases_keywords:
        if re.search(disease, conversation, re.IGNORECASE):
            diseases.append(disease)

    return {
        "symptoms": symptoms,
        "diseases": diseases
    }

# Function to extract gender information
def extract_gender(conversation):
    gender_keywords = ["male", "female"]
    
    for gender in gender_keywords:
        if re.search(gender, conversation, re.IGNORECASE):
            return gender.capitalize()
    return "Unknown"

# Apply the extraction functions
data["extracted"] = data["conversation"].apply(extract_information)
data["symptoms"] = data["extracted"].apply(lambda x: x["symptoms"])
data["diseases"] = data["extracted"].apply(lambda x: x["diseases"])
data["gender"] = data["conversation"].apply(extract_gender)
data.drop(columns=["extracted"], inplace=True)

# Flatten lists
all_symptoms = [symptom for sublist in data["symptoms"] for symptom in sublist]
all_diseases = [disease for sublist in data["diseases"] for disease in sublist]

# Count occurrences
symptom_counts = Counter(all_symptoms)
disease_counts = Counter(all_diseases)

# Risk Categorization
def calculate_risk(conversation):
    high_risk_terms = ["dyspnea", "difficulty breathing", "ARDS"]
    moderate_risk_terms = ["fever", "fatigue", "COVID-19"]
    
    if any(term in conversation for term in high_risk_terms):
        return "High"
    elif any(term in conversation for term in moderate_risk_terms):
        return "Moderate"
    else:
        return "Low"

data["risk_level"] = data["conversation"].apply(calculate_risk)

# Dash Application
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Doctor-Patient Conversation Analysis Dashboard", style={"textAlign": "center"}),

    # Highlighted Points
    html.Div([
        html.Div([
            html.H3(f"{len(data)}"),
            html.P("Total Conversations")
        ], className="highlight"),

        html.Div([
            html.H3(f"{len(set(all_symptoms))}"),
            html.P("Unique Symptoms")
        ], className="highlight"),

        html.Div([
            html.H3(f"{len(set(all_diseases))}"),
            html.P("Unique Diseases")
        ], className="highlight"),
    ], className="highlights-row"),

    # Toggle for Graph Selection
    html.Div([
        html.Label("Select Visualization:"),
        dcc.Dropdown(
            id="graph-toggle",
            options=[
                {"label": "Disease Distribution", "value": "disease_dist"},
                {"label": "Risk Levels", "value": "risk_dist"},
                {"label": "Word Cloud", "value": "wordcloud"},
                {"label": "Symptom-Disease Heatmap", "value": "heatmap"},
                {"label": "Conversation Length Distribution", "value": "conv_length"},
                {"label": "Gender Distribution", "value": "gender_dist"}
            ],
            value="disease_dist",
            clearable=False
        )
    ], className="toggle-dropdown"),

    # Dynamic Graph
    dcc.Graph(id="dynamic-graph")
], className="container")

# Callbacks for Dynamic Graph
@app.callback(
    Output("dynamic-graph", "figure"),
    [Input("graph-toggle", "value")]
)
def update_graph(selected_graph):
    if selected_graph == "disease_dist":
        fig = px.bar(
            x=list(disease_counts.keys()), y=list(disease_counts.values()),
            labels={"x": "Diseases", "y": "Frequency"}, title="Disease Distribution",
            color_discrete_sequence=["#636EFA"]
        )
    elif selected_graph == "risk_dist":
        fig = px.pie(
            data_frame=data, names="risk_level", title="Risk Level Distribution",
            color_discrete_sequence=px.colors.sequential.RdBu
        )
    elif selected_graph == "wordcloud":
        all_conversations = " ".join(data["conversation"])
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(all_conversations)
        fig = px.imshow(wordcloud, template="plotly_white", title="Word Cloud of Conversations")
    elif selected_graph == "heatmap":
        cooccurrence_matrix = pd.crosstab(
            pd.Series(all_symptoms, name="Symptoms"), pd.Series(all_diseases, name="Diseases")
        )
        fig = px.imshow(
            cooccurrence_matrix, text_auto=True, title="Symptom-Disease Co-occurrence Heatmap",
            color_continuous_scale="Viridis"
        )
    elif selected_graph == "conv_length":
        data["conversation_length"] = data["conversation"].apply(len)
        fig = px.histogram(
            data, x="conversation_length", nbins=30, title="Conversation Length Distribution",
            labels={"conversation_length": "Length of Conversation"}, color_discrete_sequence=["#00CC96"]
        )
    elif selected_graph == "gender_dist":
        fig = px.pie(
            data_frame=data, names="gender", title="Gender Distribution",
            color_discrete_sequence=px.colors.sequential.PuRd
        )
    return fig

# Run the Application
if __name__ == "__main__":
    app.run_server(debug=True)
