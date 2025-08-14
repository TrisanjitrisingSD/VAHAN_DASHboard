# Vehicle Registration Dashboard

## Setup Instructions

- Install Dependencies: Run `pip install -r requirements.txt` to install required packages.
- Prepare Data: Place raw Excel files (e.g., "makers_monthwise_2023.xlsx", "makers_monthwise_2024.xlsx", "makers_monthwise_2025.xlsx") in the `data/raw/` folder. Ensure filenames include a 4-digit year.
- Process Data: Execute `python src/process_data.py` to generate the processed dataset in `data/processed/vehicle_data.csv`.
- Run Dashboard: Start the app with `streamlit run src/app.py`.


## Data Assumptions

- Source: Data is manually exported  from the Vahan dashboard with filters set to "Electric(Battery)" fuel type, vehicle classes (e.g., "Two Wheeler", "Three Wheeler", "Motor Car"), "Month Wise", "Maker Wise", and "Calendar Year".
- Structure: Excel files have a header row, month sub-header, and registration data per maker, covering January to August 2025 (as of August 14, 2025).
- Categories: 2W (two-wheelers), 3W (three-wheelers), 4W (four-wheelers) are mapped based on maker research. Unknown makers default to NaN and are filtered out.
- Processing: No SQL or scraping; Pandas handles in-memory processing. Non-numeric registration values are coerced to 0.

## Feature Roadmap

- Automation: Integrate API access if Vahan provides one for real-time updates.
- Granularity: Add state-level filters if data expands.
- Export: Enable PDF export of dashboard views.
- Forecasting: Add machine learning for registration trends.

