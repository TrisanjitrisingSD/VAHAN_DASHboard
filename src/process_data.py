import pandas as pd
import os
from glob import glob
import re

def process_data(raw_dir='data/raw', processed_dir='data/processed'):
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)

    data_frames = []
    files = glob(os.path.join(raw_dir, '*.xlsx'))
    
    if not files:
        raise ValueError("No Excel files found in data/raw directory. Ensure files are placed there and named with a 4-digit year (e.g., makers_monthwise_2023.xlsx).")
    
    
    category_map = {
        '3EV INDUSTRIES PVT LTD': '3W',
        '3S INDUSTRIES PRIVATE LIMITED': '3W',
        '3SI INDUSTRIES PRIVATE LIMITED': '3W',
        'A1 HEAVY EQUIPMENTS DEVELOPER': '4W',
        'A-1 SUREJA INDUSTRIES': '3W',
        'AADHYA ENTERPRISES': '3W',
        'AADITYA EMOTORS INDIA PVT LTD': '2W',
        'AADITYA GARBAGE PRODUCTS PVT LTD': '3W',
        'AAHANA COMMERCE PVT LTD': '3W',
        'AAKK AUTO PVT LTD': '4W',
        'AARGEE ELECTRIC': '2W',
        'AARON INDUSTRIES': '3W',
        'A.B. AGRO ENGINEERING WORKS': '4W',
        'A.B. AGRO ENGINEERING WORKS&ENTERPRISESAP11815428': '4W',
        'AB EXCAVATORS & EARTHMOVERS PVT LTD': '4W',
        'AB N DHRUV AUTOCRAFT (INDIA) PVT LTD': '4W',
        'AB DHRUV AUTOCRAFT (INDIA) PVT LTD': '4W',
        'ABZO MOTORS PVT LTD': '2W',
        'ACCPL INFRA FABTECH PVT LTD': '4W',
        'ACCRETION POWER AUTOS': '3W',
        'ACTION CONSTRUCTION EQUIPMENT LTD.': '4W',
        'A D AGRO WORKS': '4W',
        'ADAPT MOTORS PVT LTD': '3W',
        'ADICO ESCORTS AGRI EQUIPMENTS PVT. LTD.': '4W',
        'ADIDEV TECHNOA PVT LTD': '3W',
        'ADISHAKTI TRACTORS': '4W',
        'ADISHWAR AUTO RIDE INDIA PVT.LTD.': '3W',
        'ADISHWAR AUTO RIDE INDIA PVT LTD': '3W',
        'ADITYA AGRO INDUSTRIES': '4W',
        'ADITYA ENTERPRISES': '3W',
        'ADITYA SAI INDUSTRIES': '3W',
        'ADM TECHNOLOGIES PVT. LTD.': '3W',
        'ADRIS ELECTRIC PVT LTD': '2W',
        'AERODRIVE PVT LTD': '3W',
        'AEROEAGLE AUTOMOBILES PVT LTD': '3W',
        'AFKON AUTOMOTIVES PVT LTD': '3W',
        'AFTEK MOTORS INDIA PVT LTD': '3W',
        'AFZAL ENGG WORKS,JUNAGARH': '4W',
        'AGP ENGINEERING PRODUCTS': '4W',
        'AGRAWAL RENEWABLE ENERGY PVT LTD': '3W',
        'AGRI KING TRACTORS & EQUIPMENTS PVT LTD': '4W',
        'AGRO INDUSTRIES': '4W',
        'AGRO TRAILERS AP312870751': '4W',
        'AHMED MOTORS': '3W',
        'AJANTA KRUSHI YANTRA': '4W',
        'AJAX ENGINEERING LTD': '4W',
        'AJAX FIORI ENGINEERING PVT LTD': '4W',
        'AJAY AGRO ENTERPRISES,SBP': '4W',
        'AJAY ENGINEERING AND AGRICULTURAL EQUIPMENT CO.': '4W',
        'AJAY ENTERPRISES': '3W',
        'AJAY MOTORS PRIVATE LIMITED': '3W',
        'A.J ENTERPRISES': '3W',
        'AKAL AGRO INDUSTRY': '4W',
        'AKASH EQUIPMENTS & MACHINERIES (P) LTD.': '4W',
        'AKASH TRAILOR': '4W',
        'A.K.AUTO ELECTRICAL': '3W',
        'A K AUTTO ELECTRICAL': '3W',
        'AKG INTERNATIONAL': '3W',
        'A K GUPTA & CO.': '3W',
        'AKMAAN MULTI MECH MACHINE': '4W',
        'OLA ELECTRIC': '2W',
        'ATHER ENERGY': '2W',
        'TVS MOTOR COMPANY': '2W',
        'BAJAJ AUTO': '2W',
        'HERO ELECTRIC': '2W',
        'AMPERE VEHICLES': '2W',
        'REVOLT MOTORS': '2W',
        'OKINAWA AUTOTECH': '2W',
        'PURE EV': '2W',
        'KINETIC GREEN': '2W',
        'TORK MOTORS': '2W',
        'WARDWIZARD INNOVATIONS': '2W',
        'BGAUSS': '2W',
        'ULTRAVIOLETTE AUTOMOTIVE': '2W',
        'MAHINDRA LAST MILE MOBILITY LTD': '3W',
        'PIAGGIO VEHICLES': '3W',
        'ATUL AUTO': '3W',
        'SAERA ELECTRIC': '3W',
        'YC ELECTRIC VEHICLE': '3W',
        'OMEGA SEIKI MOBILITY': '3W',
        'ALTIGREEN PROPULSION LABS': '3W',
        'EULER MOTORS': '3W',
        'GAYAM MOTOR WORKS': '3W',
        'MONTRA ELECTRIC': '3W',
        'TATA MOTORS': '4W',
        'MAHINDRA ELECTRIC': '4W',
        'MG MOTOR INDIA': '4W',
        'HYUNDAI': '4W',
        'BYD INDIA': '4W',
        'MARUTI SUZUKI': '4W',
        'KIA': '4W',
        'ASHOK LEYLAND': '4W',
        'JBM AUTO': '4W',
        'OLECTRA GREENTECH': '4W',
    }

    for file in files:
        
        match = re.search(r'(\d{4})', os.path.basename(file))
        if not match:
            raise ValueError(f"No 4-digit year found in filename: {file}. Ensure filenames include the year (e.g., 2023).")
        year = int(match.group(1))
        
        
        df = pd.read_excel(file, header=1)
        
        # Month names are in row 3 (df.iloc[1, 2:-1])
        month_names = df.iloc[1, 2:-1].tolist()
        
        # Data starts from row 4 (df.iloc[2:])
        df = df.iloc[2:].reset_index(drop=True)
        
        # Set columns
        df.columns = ['S No', 'Maker'] + month_names + ['TOTAL']
        
        # Drop unnecessary columns
        df = df.drop(['S No', 'TOTAL'], axis=1)
        
        # Clean Maker
        df['Maker'] = df['Maker'].str.strip().str.replace(r'[\xa0\s]+', ' ', regex=True)
        
        # Melt months to long format (filter non-NaN months for 2025)
        month_cols = [col for col in df.columns if col != 'Maker' and pd.notna(col)]
        df = df.melt(id_vars=['Maker'], value_vars=month_cols, var_name='Month', value_name='Registrations')
        
        # Convert Registrations to numeric, coercing errors to NaN
        df['Registrations'] = pd.to_numeric(df['Registrations'], errors='coerce')
        
        # Add year
        df['Year'] = year
        
        # Map category
        df['Category'] = df['Maker'].map(category_map)
        
        data_frames.append(df)
    
    all_data = pd.concat(data_frames, ignore_index=True)
    
    # Save to processed
    all_data.to_csv(os.path.join(processed_dir, 'vehicle_data.csv'), index=False)
    print("Data processed and saved to data/processed/vehicle_data.csv")

if __name__ == '__main__':
    process_data()