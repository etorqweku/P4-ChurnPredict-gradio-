import joblib
import gradio as gr
import pandas as pd

# Load trained model and other resources
model= joblib.load("H:/New folder (4)/P4-ChurnPredict-Pro/src/model/rf_model.joblib")
imputer=joblib.load("H:/New folder (4)/P4-ChurnPredict-Pro/src/model/imputer.joblib")
preprocessor=joblib.load("H:/New folder (4)/P4-ChurnPredict-Pro/src/model/preprocessor.joblib")


# Define the classify function
def classify(num):
    if num == 0:
        return "Customer will not Churn"
    else:
        return "Customer will churn"

# Define the prediction function
def predict_churn(SeniorCitizen, Partner, Dependents, tenure, InternetService,
                   OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport,
                   StreamingTV, StreamingMovies, Contract, PaperlessBilling,
                   PaymentMethod, MonthlyCharges, TotalCharges, gender, PhoneService, MultipleLines):

    # Create input data list
    input_data = [
        SeniorCitizen, Partner, Dependents, tenure, InternetService,
        OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport,
        StreamingTV, StreamingMovies, Contract, PaperlessBilling,
        PaymentMethod, MonthlyCharges, TotalCharges, gender, PhoneService, MultipleLines
    ]

    # Convert input data to a DataFrame
    input_df = pd.DataFrame([input_data], columns=[
        "SeniorCitizen", "Partner", "Dependents", "tenure", "InternetService",
        "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport",
        "StreamingTV", "StreamingMovies", "Contract", "PaperlessBilling",
        "PaymentMethod", "MonthlyCharges", "TotalCharges", "gender", "PhoneService", "MultipleLines"
    ])
    print(input_df)
    
    input_df['TotalCharges']=imputer.transform(input_df[['TotalCharges']])

    # Apply preprocessing
    prep_data = preprocessor.transform(input_df)
    print("r")
    print(prep_data)

    # Make a prediction
    pred = model.predict(prep_data)

    # Get the classification
    output = classify(pred[0])

    return [(pred[0], output)]

# Create Gradio interface
iface = gr.Interface(
    fn=predict_churn,
    inputs=[
        gr.inputs.Slider(minimum=0, maximum= 1, step=1, label="SeniorCitizen: Select 1 for Yes and 0 for No"),
        gr.inputs.Radio(["Yes", "No"], label="Partner: Do You Have a Partner?"),
        gr.inputs.Radio(["Yes", "No"], label="Dependents: Do You Have a Dependent?"),
        gr.inputs.Number(label="tenure: How Long Have You Been with Vodafone in Months?"),
        gr.inputs.Radio(["DSL", "Fiber optic", "No"], label="What Internet Service Do You Use?"),
        gr.inputs.Radio(["Yes", "No", "No internet service"], label="Do You Have Online Security?"),
        gr.inputs.Radio(["Yes", "No", "No internet service"], label="Do You Have Any Online Backup Service?"),
        gr.inputs.Radio(["Yes", "No", "No internet service"], label="Do You Use Any Device Protection?"),
        gr.inputs.Radio(["Yes", "No", "No internet service"], label="Do You Use TechSupport?"),
        gr.inputs.Radio(["Yes", "No", "No internet service"], label="Do You Stream TV?"),
        gr.inputs.Radio(["Yes", "No", "No internet service"], label="Do You Stream Movies?"),
        gr.inputs.Radio(["Month-to-month", "One year", "Two year"], label="What Is Your Contract Type?"),
        gr.inputs.Radio(["Yes", "No"], label=" Do You Use Paperless Billing?"),
        gr.inputs.Radio([
             "Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"
         ], label="What Payment Method Do You Use?"),
        gr.inputs.Number(label="What is you Monthly Charges?"),
        gr.inputs.Number(label="How Much Is Your Total Charges?"),
        gr.inputs.Radio(["Male","Female"],label="Gender"),
        gr.inputs.Radio(["Yes", "No"], label="PhoneService: Do You Have a Phone Service?"),
        gr.inputs.Radio(["Yes", "No"], label="MultipleLines: Do You use Multiple Lines?")
    ],
    outputs=gr.outputs.HighlightedText(color_map={
        "Customer will not Churn": "green",
        "Customer will churn": "red"
    }, label="Your Output") 
)

# Launch the interface
iface.launch(share=True, debug=True)
