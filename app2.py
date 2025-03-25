from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load company data from Excel file
def load_data():
    try:
        df = pd.read_excel("static/processed_data_5.xlsx")
        return df
    except Exception as e:
        print(f"Error loading file: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error

# Function to sort months in calendar order
def get_sorted_months(df):
    month_order = {
        "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
        "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12
    }

    # Extract unique months from the column
    unique_months = df["Month"].dropna().unique().tolist()

    # Sort the months in the correct order
    sorted_months = sorted(unique_months, key=lambda x: month_order.get(x, 999))  
    return sorted_months

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    company_details = None
    not_found = False
    df = load_data()

    # Ensure the dataframe is not empty
    if df.empty:
        return "Error: Unable to load company data."

    # Fill NaN values with empty strings to prevent errors
    df = df.fillna('')

    if request.method == 'POST':
        industry = [com_sta.strip() for com_sta in request.form.getlist("Company_Status")]
        location = [loc.strip() for loc in request.form.getlist("location")]
        roc = [roc.strip() for roc in request.form.getlist("ROC")]
        selected_months = [month.strip() for month in request.form.getlist("Month")]

        # Apply filtering only when user input is provided
        result = df[
            (df["Company Status"].isin(industry)) &
            (df["State"].isin(location)) &
            (df["ROC"].isin(roc)) &
            (df["Month"].isin(selected_months))
        ]
        print(len(result))
        if not result.empty:
            company_details = result.to_dict(orient='records')
        else:
            not_found = True

    # Extract unique values for dropdown options
    company_statuses = df["Company Status"].dropna().unique().tolist()
    locations = df["State"].dropna().unique().tolist()
    rocs = df["ROC"].dropna().unique().tolist()
    months = get_sorted_months(df)  # Sort months in calendar order

    return render_template(
        'index.html',
        company_details=company_details,
        not_found=not_found,
        company_statuses=company_statuses,
        locations=locations,
        rocs=rocs,
        months=months
    )

if __name__ == '__main__':
    app.run(debug=True)
