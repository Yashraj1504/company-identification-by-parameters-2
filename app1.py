from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load company data from Excel file
def load_data():
    try:
        df = pd.read_excel("static/processed_data_.xlsx")
        return df
    except Exception as e:
        print(f"Error loading file: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error

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
      #  month = request.form.get("Month", "").strip()
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
    months = df["Month"].dropna().unique().tolist()
    
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
