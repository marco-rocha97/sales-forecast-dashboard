# 📊 Sales Forecast Dashboard

An interactive **Streamlit application** for **time series sales forecasting** using **PyCaret**.

The app allows you to explore daily sales, train regression models, and visualize forecasts against actual sales.

---

## ✨ Features

- 🗂️ Data Integration
    - Sales data (sales.csv)
    - SKU master data (sku_data.csv)
    - Location data (location_data.csv)

- 🧹 Data Preprocessing
    - Resampling sales to daily frequency
    - Calendar feature engineering (weekday, weekend, week-of-year, etc.)
    - Target encoding for categorical variables (location, sku)

- 🤖 Model Training
    - Powered by PyCaret
    - Automatically compares multiple regression models:
        - Linear Regression
        - AdaBoost
        - XGBoost
        - LightGBM

- 📈 Forecasting
    - Train/Test split by user-defined date
    - Predicts future sales quantities
    - Interactive visualization of Actual vs Forecasted sales

- 🎨 Dashboard UI
    - Built with Streamlit
    - Interactive filters for Warehouse and Material
    - Altair charts with optional vertical split line
    - Clear error and warning messages for empty datasets

---

## 🚀 Demo

1. Select a Warehouse and Material

2. Pick a Train/Test Split Date

3. View:
    - Raw historical sales
    - Best performing model
    - Forecast vs Actual sales

---

## ⚙️ Setup Instructions

### 1. Clone this repository
```powershell
git clone https://github.com/marco-rocha97/sales-forecast-dashboard.git
cd sales-forecast-dashboard
```

### 2. Create and activate a virtual environment
```powershell
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
```

### 3. Install dependencies
```powershell
pip install -r requirements.txt
```

---

## ▶️ Usage

Run the Streamlit app
```powershell
streamlit run app.py
```
Open the app in your browser: http://localhost:8501

Or use the Hugging Face link: https://huggingface.co/spaces/marcorocha97/sales-forecast-dashboard

---

## 📂 Data Requirements

- sales.csv

    Required columns:
    - date (format: %d/%m/%Y)
    - location
    - sku
    - quantity

- sku_data.csv

    Required columns:
    - SKU
    - Material

- location_data.csv

    Required columns:
    - Location
    - Warehouse

---

## 📊 Example Output

### Raw Sales

Daily sales with vertical line at train/test split date.

### Forecast vs Actual

Line chart comparing forecasted sales vs actual sales.

---

## 📦 Tech Stack

- [Streamlit](https://streamlit.io/) – Dashboard UI

- [Pandas](https://pandas.pydata.org/) – Data manipulation

- [Altair](https://altair-viz.github.io/) – Visualization

- [PyCaret](https://pycaret.org/) – Model training & forecasting

- [Category Encoders](https://contrib.scikit-learn.org/category_encoders/) – Target encoding

---
👤 Author: Marco Rocha

📅 Python Version: 3.11.9