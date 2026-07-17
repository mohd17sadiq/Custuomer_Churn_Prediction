from flask import Flask, render_template, request
import pandas as pd
import pickle
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "model", "customer_churn_model.pkl"), "rb") as f:
    model_data = pickle.load(f)

model = model_data["model"]
feature_names = model_data["features_names"]

with open(os.path.join(BASE_DIR, "model", "encoders.pkl"), "rb") as f:
    encoders = pickle.load(f)


def encode_input(data):
    input_df = pd.DataFrame([data])

    for column, encoder in encoders.items():
        input_df[column] = encoder.transform(input_df[column])

    return input_df[feature_names]


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    probability = None
    error = None

    if request.method == "POST":
        try:
            input_data = {
                "gender": request.form["gender"],
                "SeniorCitizen": int(request.form["SeniorCitizen"]),
                "Partner": request.form["Partner"],
                "Dependents": request.form["Dependents"],
                "tenure": float(request.form["tenure"]),
                "PhoneService": request.form["PhoneService"],
                "MultipleLines": request.form["MultipleLines"],
                "InternetService": request.form["InternetService"],
                "OnlineSecurity": request.form["OnlineSecurity"],
                "OnlineBackup": request.form["OnlineBackup"],
                "DeviceProtection": request.form["DeviceProtection"],
                "TechSupport": request.form["TechSupport"],
                "StreamingTV": request.form["StreamingTV"],
                "StreamingMovies": request.form["StreamingMovies"],
                "Contract": request.form["Contract"],
                "PaperlessBilling": request.form["PaperlessBilling"],
                "PaymentMethod": request.form["PaymentMethod"],
                "MonthlyCharges": float(request.form["MonthlyCharges"]),
                "TotalCharges": float(request.form["TotalCharges"]),
            }

            input_df = encode_input(input_data)
            prediction = model.predict(input_df)[0]
            probabilities = model.predict_proba(input_df)[0]

            result = "Customer Likely to Churn" if prediction == 1 else "Customer Likely to Stay"
            probability = round(float(probabilities[prediction]) * 100, 2)

        except Exception as e:
            error = f"Prediction failed: {str(e)}"

    return render_template(
        "index.html",
        result=result,
        probability=probability,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)
