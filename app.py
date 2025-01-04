from flask import Flask, render_template, request#,flash
import joblib #,os
import numpy as np

app = Flask(__name__)
#app.secret_key = os.urandom(16).hex()  # Add a secret key for session management

# Load the trained model and scaler
model = joblib.load("loan_eligibility_model.pkl")
scaler = joblib.load("numerical_features_scaler.pkl")

def calculate_emi(principal, rate, term_months):
    monthly_rate = rate / (12 * 100)
    emi = (principal * monthly_rate * (1 + monthly_rate)**term_months) / ((1 + monthly_rate)**term_months - 1)
    return round(emi, 2)

# Define numerical and encoded categorical feature names
numerical_features = [
    'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term',
    'DTI', 'Income_per_Family_Member', 'Loan_to_Income_Ratio'
]
encoded_categorical_features = [
    'Gender_Male', 'Married_Yes', 'Education_Not Graduate', 
    'Self_Employed_Yes', 'Property_Area_Semiurban', 
    'Property_Area_Urban', 'Credit_History'
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            # Get user inputs
            applicant_income = float(request.form['ApplicantIncome'])
            # Handle coapplicant income based on checkbox
            coapplicant_income = 0.0
            if 'CoapplicantAvailable' in request.form:  # If coapplicant is available
                coapplicant_income = float(request.form['CoapplicantIncome'])
            loan_amount = float(request.form['LoanAmount'])
            loan_amount_term = float(request.form['Loan_Amount_Term'])
            credit_history = int(request.form['Credit_History'])
            gender = int(request.form['Gender'])
            married = int(request.form['Married'])
            dependents = int(request.form['Dependents'])
            self_employed = int(request.form['Self_Employed'])
            education = int(request.form['Education'])
            property_area = int(request.form['Property_Area'])

            # Calculate derived features
            dti = (loan_amount * 1000) / (applicant_income + coapplicant_income)
            income_per_family_member = applicant_income / (dependents + 1)
            loan_to_income_ratio = (loan_amount * 1000) / applicant_income

            # Prepare scaled numerical data
            numerical_data = [
                applicant_income, coapplicant_income, loan_amount, loan_amount_term,
                dti, income_per_family_member, loan_to_income_ratio
            ]
            numerical_data_scaled = scaler.transform([numerical_data])[0]

            # Prepare encoded categorical data
            categorical_data = [
                gender, married, 1 - education, self_employed, 
                1 if property_area == 1 else 0, 1 if property_area == 2 else 0,
                credit_history
            ]

            # Combine data
            final_input = np.concatenate((numerical_data_scaled, categorical_data))

            # Prediction
            prediction = model.predict([final_input])[0]

            if prediction == 1:  # Loan Approved
                loan_amount += loan_amount * 1000 # the loan amount entering in terms of thousands
                interest_rate = 8.5  # Example interest rate
                monthly_installment = calculate_emi(loan_amount, interest_rate, loan_amount_term)

                prediction_text = [
                    f"Loan Approved! Here are your details:",
                    f" - DTI Ratio: {dti:.2f}",
                    f" - Monthly Installment (at {interest_rate}% interest): INR {monthly_installment}",
                    f" - Loan Term: {loan_amount_term} months"
                ]
            else:  # Loan Not Approved
                rejection_reason = [
                    "Loan Not Approved! Possible reasons:",
                    f" - DTI Ratio: {dti:.2f} (Risk threshold exceeded)",
                    " - Consider lowering the loan amount or increasing your income to qualify."
                ]
                suggestion_text = [
                    "We suggest applying for a smaller loan amount to improve eligibility."
                ]
                prediction_text = rejection_reason + suggestion_text

        except Exception as e:
            prediction_text = [f"Error: {e}"]

        return render_template('index.html', prediction_text=prediction_text)

    # For GET request, set prediction_text to empty
    return render_template('index.html', prediction_text=[])


if __name__ == '__main__':
    app.run(debug=True)
