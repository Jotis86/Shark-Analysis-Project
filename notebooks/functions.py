# eliminar columnas

import pandas as pd
import re
import datetime
import numpy as np

def read_data(url): 
    df = pd.read_excel(url)
    return df


def drop_columns(df): 
    '''
    Drop useless columns
    '''
    
    df.drop(columns=["Case Number.1"], inplace=True)
    df.drop(columns=["Unnamed: 21"], inplace=True)
    df.drop(columns=["Unnamed: 11"], inplace=True)
    df.drop(columns=["Unnamed: 22"], inplace=True)
    df.drop(columns=["Case Number"], inplace=True)
    df.drop(columns=["href formula"], inplace=True)
    df.drop(columns=["href"], inplace=True)
    df.drop(columns=["pdf"], inplace=True)
    
    return df
    

# Clean and Standarize Date Formats

def clean_date(date_str):
    # Check if the input is NaT (Not a Time)
    if pd.isna(date_str):
        return pd.NaT
    
    # Convert datetime objects to string
    if isinstance(date_str, (pd.Timestamp, datetime.datetime)):
        date_str = date_str.strftime('%d %b %Y')
    
    # Ensure the input is a string
    if not isinstance(date_str, str):
        return date_str
    
    # Remove words like 'Reported', 'Ca.', 'Early', 'Late', 'Between', 'Before', 'After', 'Anniversary Day', 'No date', and extra spaces
    date_str = re.sub(r'Reported|Ca\.|Ca|Early|Late|Between|Before|After|Anniversary Day|No date|During the war|Before the war|Said to be|World War II|a few years before|early|late|between|before|after|anniversary day|no date|during the war|before the war|said to be|world war ii', '', date_str, flags=re.IGNORECASE).strip()
    
    # Remove suffixes like '.a' and '.b'
    date_str = re.sub(r'\.\w$', '', date_str).strip()
    
    # Replace inconsistent formats
    date_str = re.sub(r'(\d{2})-(\w+)-(\d{4})', r'\1 \2 \3', date_str)  # 09-Sep-2023 -> 09 Sep 2023
    date_str = re.sub(r'(\d{2}) (\w+)-(\d{4})', r'\1 \2 \3', date_str)  # 09 Sep-2023 -> 09 Sep 2023
    date_str = re.sub(r'(\d{2})-(\w+)-(\d{2})', r'\1 \2 20\3', date_str)  # 09-Sep-23 -> 09 Sep 2023
    date_str = re.sub(r'(\w+)-(\d{2})-(\d{4})', r'\2 \1 \3', date_str)  # Aug-24-1806 -> 24 Aug 1806
    
    # Handle year ranges (e.g., 1900-1905)
    date_str = re.sub(r'(\d{4})-(\d{4})', lambda m: f'01 Jan {(int(m.group(1)) + int(m.group(2))) // 2}', date_str)  # 1900-1905 -> 1902
    
    # Handle dates with only year (e.g., 1900)
    if re.match(r'^\d{4}$', date_str):
        date_str = f'01 Jan {date_str}'  # Convert to 01 Jan 1900
    
    # Handle dates with month and year (e.g., Jan 1900)
    if re.match(r'^\w+ \d{4}$', date_str):
        date_str = f'01 {date_str}'  # Convert to 01 Jan 1900
    
    # Handle dates with month and year in different format (e.g., Sep-1805)
    if re.match(r'^\w+-\d{4}$', date_str):
        date_str = f'01 {date_str.replace("-", " ")}'  # Convert to 01 Sep 1805
    
    # Handle dates with month name and year (e.g., October 1815)
    if re.match(r'^\w+ \d{4}$', date_str):
        date_str = f'01 {date_str}'  # Convert to 01 October 1815
    
    # Handle dates with "or" (e.g., 1990 or 1991)
    if re.match(r'^\d{4} or \d{4}$', date_str):
        date_str = date_str.split(' or ')[0]  # Take the first year
    
    # Handle dates with "B.C." (e.g., Ca. 214 B.C.)
    date_str = re.sub(r'B\.C\.', 'BC', date_str, flags=re.IGNORECASE)
    
    # Handle dates with "A.D." (e.g., Ca. 77 A.D.)
    date_str = re.sub(r'A\.D\.', 'AD', date_str, flags=re.IGNORECASE)
    
    # Handle dates with "Circa" or "Ca." (e.g., Circa 1855)
    date_str = re.sub(r'Circa|circa', '', date_str).strip()
    
    # Specific cases mapping
    specific_cases = {
        r'Before (\d{4})': lambda m: f'01 Jan {int(m.group(1)) - 1}',
        r'Before (\d{2})-(\w+)-(\d{4})': lambda m: f'{int(m.group(1)) - 1} {m.group(2)} {m.group(3)}',
        r'Between (\d{4}) & (\d{4})': lambda m: f'01 Jan {(int(m.group(1)) + int(m.group(2))) // 2}'
    }
    
    # Apply specific cases
    for pattern, func in specific_cases.items():
        date_str = re.sub(pattern, func, date_str)
    
    return date_str

def date_clean(df): 
    df['Date'] = df['Date'].apply(clean_date)
    return df 


#Type column 

def type_column(df): 
    
    # Step 1: Remove leading/trailing spaces
    df['Type'] = df['Type'].str.strip()
    
    # Step 2: Replace '?' and 'nan' with 'Unknown'
    df['Type'] = df['Type'].replace(['?', 'nan'], 'Unknown')
    
    # Step 3: Remplace 'Questionable', 'Unconfirmed', 'Invalid', 'Under investigation' with 'Unverified'
    
    df['Type'] = df['Type'].replace(['Questionable', 'Unverified', 'Invalid','Under investigation'], 'Unconfirmed')
    
    return df

def clean_country(country):
    if pd.isna(country):
        return country
    
    # Strip leading and trailing whitespace
    country = country.strip()
    
    # Convert to title case
    country = country.title()
    
    # Remove special characters
    country = re.sub(r'[^\w\s]', '', country)
    
    return country

def country_cleaned(df): 
    
    df['Country'] = df['Country'].apply(clean_country)
    
    return df




def state_cleaned(df): 
    
    df['State'] = df['State'].apply(clean_country)
    
    return df

def sex_clean(df): 
    
    df['Sex'] = df['Sex'].replace([' M', 'M ', 'M x 2' ], 'M')
    df['Sex'] = df['Sex'].replace(['lli', 'N', '.' ], 'undefined')
    
    return df


# Age

def clean_age(df): 
    
    df["Age"] = df["Age"].replace(['Middle Age', '(adult)', '"middle-age"', '50s', 'adult','Middle age'], 50)
    df['Age'] = df["Age"].replace(['20/30','20s', '28 & 22',  "20's", '28 & 26', '28, 23 & 30', '21 & ?', '23 & 20','20?', 'mid-20s','21 or 26','18 to 22','? & 19','23 & 26','25 or 28','"young"','young','17 & 35','18 or 20'],25)
    df["Age"] = df['Age'].replace(['40s', '45 and 15', '9 & 60', '46 & 34'], 45)
    df["Age"] = df['Age'].replace(['teen', 'Teen','a minor','Teens','?    &   14', '13 or 14','7      &    31', '16 to 18','13 or 18', '12 or 13'], 15)
    df["Age"] = df["Age"].replace('Both 11', 11)
    df["Age"] = df['Age'].replace(['a minor', '18 months', '9 months'], 1)
    df["Age"] = df['Age'].replace(['Elderly', '>50', "60's", '60s'], 65)
    df["Age"] = df['Age'].replace(['9 or 10', '10 or 12', '7 or 8','9 & 60','8 or 10'], 10)
    df["Age"] = df['Age'].replace(['mid-30s', '33 & 26', '31 or 33', '36 & 23','30 or 36','21, 34,24 & 35','Ca. 33','33 & 37','32 & 30','37, 67, 35, 27,  ? & 27','30 & 32','33 or 37'], 33)
    
    df['Age'] = df['Age'].str.split(" ").str[0].apply(pd.to_numeric, errors = "coerce")
    
    
    return df


# Time 

def clean_time_format(time_str):
   
    # Convertir el valor a cadena de texto
    time_str = str(time_str)
    
    # Manejar valores como NaN, "Not stated", "?"
    if pd.isna(time_str) or 'Not' in time_str or '?' in time_str or time_str == '' or time_str == ' ' or time_str ==  '':
        return np.nan
    
    if ('not advised' in time_str.lower() or 'not stated' in time_str.lower()): 
        return np.nan
    elif ('early morning' in time_str.lower() or 'morning' in time_str.lower() or 'just before noon' in time_str.lower() or 'am' in time_str.lower() or 'a.m.' in time_str.lower()
        or 'late morning' in time_str.lower() or 'noon' in time_str.lower() or 'mid morning' in time_str.lower() or 'mid-morning' in time_str.lower()
        or 'Sometime between 06h00 & 08hoo' in time_str or 'Between 11h00 & 12h00' in time_str or 'Before 10h30' in time_str): 
        return 'Morning'
    elif ('afternoon' in time_str.lower() or '"midday"' in time_str.lower() or 'early afternoon' in time_str.lower() or 'after noon' in time_str.lower() or
        'mid afternoon' in time_str.lower() or 'daytime' in time_str.lower() or '"after lunch"' in time_str.lower() or 'midday' in time_str.lower() or 
        'before daybreak' in time_str.lower() or '>17h30' in time_str or '17h00 Sunset' in time_str or 'Shortly before 13h00' in time_str): 
        return 'Afternoon'
    elif ('night' in time_str.lower() or '"evening"' in time_str.lower() or 'late afternoon' in time_str.lower() or 'sunset' in time_str.lower() or 'midnight' in time_str.lower()
        or 'lunchtime' in time_str.lower() or 'just before sundown' in time_str.lower() or 'shortly after midnight' in time_str.lower() or 'after dusk' in time_str.lower()
        or 'dusk' in time_str.lower() or '"night"' in time_str.lower() or 'nightfall' in time_str.lower() or 'just before dawn' in time_str.lower() or
        'dark' in time_str.lower() or '"shortly before dusk"' in time_str.lower() or 'After dusk' in time_str.lower() or 'after midnight' in time_str.lower() or 
        '"Early evening"' in time_str.lower() or 'After 04h00' in time_str or 'Ship aban-doned at 03h10' in time_str or '30 minutes after 1992.07.08.a' in time_str): 
        return 'Night'
    
    else: 
        # Tratar casos con "hr", "h", etc. y eliminar caracteres extra
        time_str = time_str.lower().replace('hr', 'h').replace('hoo', 'h').replace('jh', 'h')
        time_str = re.sub(r'[^\dh]', '', time_str)  # Eliminar caracteres no numéricos y letras extrañas
        
        # Eliminar 'h' al inicio o dobles h's incorrectas (como 'h12h00')
        time_str = re.sub(r'^h', '', time_str)  # Eliminar 'h' al inicio
        time_str = re.sub(r'h+', 'h', time_str)  # Asegurar que solo haya una 'h'

        
        
        # Tratar números como 1600 o 16h15, convertir a "HH:MM"
        match = re.match(r'(\d{1,2})h(\d{1,2})?', time_str)
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2)) if match.group(2) else 0
            return f'{hour:02d}:{minute:02d}'
        
        match_numeric = re.match(r'(\d{1,4})', time_str)
        if match_numeric:
            hour = int(match_numeric.group(1)[:2])
            minute = int(match_numeric.group(1)[2:]) if len(match_numeric.group(1)) > 2 else 0
            return f'{hour:02d}:{minute:02d}'
    
    return time_str


def categorize_time(cleaned_time):
    if pd.isna(cleaned_time):
        return np.nan
    if cleaned_time == 'Morning':
        return 'Morning'
    if cleaned_time == 'Afternoon':
        return 'Afternoon'
    if cleaned_time == 'Night':
        return 'Night'
    
    try:
        # Convertir a horas y minutos
        hour, minute = map(int, cleaned_time.split(':'))
        if 6 <= hour < 12:
            return 'Morning'
        elif 12 <= hour < 18:
            return 'Afternoon'
        else:
            return 'Night'
    except:
        return np.nan
    
    
def cleaned_time(df):
    
    df['Time'] = df['Time'].apply(clean_time_format)
    df['Time'] = df['Time'].replace('', np.nan)
    df['Time'] = df['Time'].apply(categorize_time)
    
    return df


def clean_location_column(df, column_name):

    def clean_location(location):
        if pd.isna(location):
            return None
        
        # Strip leading and trailing whitespace
        location = location.strip()
        
        # Convert to title case
        location = location.title()
        
        # Remove special characters (except commas and periods)
        location = re.sub(r'[^\w\s,\.]', '', location)
        
        return location
    
    df[column_name] = df[column_name].apply(clean_location)
    return df

def location_cleaned(df):
    df['Country'] = df['Country'].str.lower()
    return df



def clean_activity_column(df, column_name):

    def clean_activity(activity):
        if pd.isna(activity):
            return None
        
        # Strip leading and trailing whitespace
        activity = activity.strip()
        
        # Convert to title case
        activity = activity.title()
        
        # Remove special characters (except commas and periods)
        activity = re.sub(r'[^\w\s,\.]', '', activity)
        
        # Normalize common terms
        activity = activity.replace('Snorkelling', 'Snorkeling')
        activity = activity.replace('Boogie Boarding', 'Bodyboarding')
        activity = activity.replace('Stand-Up Paddleboarding', 'Stand-Up Paddleboarding')
        activity = activity.replace('Stand-Up Paddle Boarding', 'Stand-Up Paddleboarding')
        activity = activity.replace('Scuba Diving', 'Scuba Diving')
        activity = activity.replace('Free Diving', 'Freediving')
        activity = activity.replace('Spearfishing', 'Spearfishing')
        activity = activity.replace('Surfing', 'Surfing')
        activity = activity.replace('Swimming', 'Swimming')
        activity = activity.replace('Wading', 'Wading')
        activity = activity.replace('Fishing', 'Fishing')
        activity = activity.replace('Kayaking', 'Kayaking')
        activity = activity.replace('Paddle Boarding', 'Paddleboarding')
        activity = activity.replace('Body Boarding', 'Bodyboarding')
        activity = activity.replace('SurfSkiing', 'Surf Skiing')
        
        return activity
    
    df[column_name] = df[column_name].apply(clean_activity)
    return df

def activity_cleaned(df):
    df['Activity'] = df['Activity'].str.lower()
    return df



def clean_injury_column(df, column_name):
    
    def clean_injury(injury):
        if pd.isna(injury):
            return None
        
        # Strip leading and trailing whitespace
        injury = injury.strip()
        
        # Convert to sentence case
        injury = injury.capitalize()
        
        # Remove special characters (except commas and periods)
        injury = re.sub(r'[^\w\s,]', '', injury)
        
        # Remove text after a period
        if '.' in injury:
            injury = injury.split('.')[0]
        
        return injury.strip()
    
    df[column_name] = df[column_name].apply(clean_injury)
    return df

def injury_cleaned(df):
    df['Injury'] = df['Injury'].str.lower()
    return df



def clean_and_normalize_species2(df, column_name):
    """
    Limpia y normaliza la columna de especies en el DataFrame.
    
    Args:
    df (pd.DataFrame): El DataFrame que contiene la columna a limpiar.
    column_name (str): El nombre de la columna a limpiar.
    
    Returns:
    pd.DataFrame: El DataFrame con la columna limpiada y normalizada.
    """
    def replace_species(value, replacements):
        if pd.notna(value):  # Check if value is not NaN
            value_lower = value.lower()
            for key, replacement in replacements.items():
                if key in value_lower:
                    return replacement
        return value

    # Diccionario de términos y sus sustituciones
    replacements = {
        'white': 'White Shark',
        'tiger': 'Tiger Shark',
        'bull': 'Bull Shark',
        'nurse': 'Nurse Shark',
        'blacktip': 'Blacktip Shark',
        'hammerhead': 'Hammerhead Shark',
        'lemon': 'Lemon Shark',
        'blue': 'Blue Shark',
        'brown': 'Brown Shark',
        'raggedtooth': 'Raggedtooth Shark',
        'bronze': 'Bronze Shark',
        'caribbean': 'Caribbean Reef Shark',
        'mako': 'Mako Shark', 
        'reportedly a great white': 'White Shark', 
        'shall shark': 'Shall Shark', 
        'sandbar': 'Sandbar Shark', 
        'carribean': 'Carribean Reef Shark', 
        'raggedtooth': 'Raggedtooth Shark', 
        'broze': 'Bronze Shark', 
        'sevengill': 'Sevengill Shark', 
        'whitetip': 'White Shark', 
        'nurse': 'Nurse Shark', 
        'galapagos': 'Galapagos Shark', 
        'cookiecutter': 'Cookiecutter Shark', 
        'wfite': 'White Shark', 
        'wobbegong': 'Wobbegong Shark', 
        'horn': 'Horn Shark', 
        'mako': 'Mako Shark', 
        '"A small shark': 'Small Shark', 
        'epaulette': 'Epaulette Shark', 
        'spinner' : 'Spinner Shark', 
        'galapagos': 'Galapagos Shark', 
        'tope': 'Tope Shark', 
        '"Reef shark"': 'Reef Shark', 
        '"whitetip shark"': 'White Shark', 
        'broadnose': 'Broadnise Shark', 
        'reef': 'Reef Shark', 
        'sandtiger': 'Tiger Shark', 
        'spinner': 'Spinner Shark', 
        'stingray': 'Stringray Shark', 
        'toadfish': 'Toadfish Shark', 
        '"reef shark"': 'Reef Shark',
        'blue': 'Blue Shark', 
        'salmon': 'Salmon Shark', 
        'wobbegong': 'Wobbegong Shark', 
        'porbeagle': 'Porbeagle Shark', 
        'seven-gill' : 'Gill Shark', 
        'dogfish': 'Dogfish Shark', 
        'silky': 'Silky Shark', 
        'hammerhead': 'Hammmerhead Shark', 
        'raggedtooth': 'Raggedtooth Shark', 
        'goblin': 'Goblin Shark', 
        'angel': 'Angel Shark'
        
       
        
    }

    # Aplicar la función de sustitución a la columna 'Species'
    df[column_name] = df[column_name].apply(replace_species, replacements=replacements)

    
    mapping2 = {
        '"small sharks"' : 'Small Shark', 
        '"a small shark"' : 'Small Shark',
        'Large shark': 'Large Shark',
        '2.5m shark': 'Large Shark',
        "3' to 4' shark": 'Small Shark', 
        "8' shark": 'Large Shark', 
        "4' shark": 'Small Shark',
        "3' shark": 'Small Shark', 
        '1m shark': 'Small Shark', 
        '5m to 6m shark': 'Large Shark', 
        "5'shark": 'Large Shark', 
        '3m shark': 'Large Shark', 
        "6' shark": 'Large Shark', 
        "9' shark": 'Large Shark', 
        "5' shark": 'Large Shark', 
        "2' to 3' shark": 'Small Shark', 
        "7' to 8' shark": 'Large Shark', 
        '8 ft shark': 'Large Shark', 
        '5.5 ft shark': 'Large Shark', 
        '1.3m shark': 'Small Shark', 
        "3' to 5' shark": 'Small Shark', 
        '8" shark' : 'Large Shark', 
        '4m shark': 'Large Shark', 
        "4' to 5' shark": 'Small Shark', 
        '2 m shark': 'Large Shark', 
        "5' to 6' shark": 'Large Shark', 
        "7' shark": 'Large Shark', 
        "1+ m shark": 'Small Shark', 
        "6' to 7' shark": 'Large Shark',
        "2' shark": 'Small Shark', 
        "6.5' shark": 'Large Shark', 
        "10' to 12' shark": 'Large Shark', 
        "shark pup": 'White Shark', 
        "12' shark": 'Large Shark',
        "2.5 m shark": 'Large Shark', 
        "Reported as shark attacks but injuries caused by toadfish": 'not a shark', 
        "Reported as shark bite but injury caused by stingray": 'not a shark', 
        "5' to 8' shark": 'Large Shark', 
        "3 m shark": 'Large Shark', 
        "2m shark": 'Large Shark',
        "small shark": 'Small Shark', 
        "3m shark, probably a smooth hound": 'Large Shark', 
        'Shark involvement highly doubtful' : 'Small Shark', 
        'No shark invovlement - it ws a publicity stunt' : 'not a shark', 
        'Shark involvement prior to death not confirmed': 'Small Shark', 
        "10' shark": 'Large Shark', 
        'a small shark': 'Small Shark', 
        '3+ m shark': 'Large Shark', 
        "4' shark?": 'Small Shark', 
        '1m to 1.2 m shark': 'Small Shark', 
        '3- to 4-foot shark': 'Small Shark', 
        '3.5 to 4 m shark': 'Large Shark', 
        '2 m to  3 m shark': 'Large Shark', 
        '1.8 m shark': 'Large Shark', 
        '5 m shark': 'Large Shark', 
        '1.5 m shark': 'Small Shark', 
        '1 m shark': 'Small Shark', 
        "8' to 10' shark": 'Large Shark', 
        "4' to 6' shark" : 'Small Shark', 
        "4' tp 5' shark": 'Small Shark', 
        '1.8 metre shark': 'Large Shark',
        "6' to 8' shark": 'Large Shark', 
        'shark involvement not confirmed': 'Small Shark', 
        '"small sharks"': 'Small Shark', 
        'no shark involvement' : 'not a shark', 
        'no shark invovlement' : 'not a shark', 
        'No shark involvement' : 'not a shark',
        '1NAm NA] shark' : 'Large Shark',
        "4' toNA shark" : 'Small Shark',
        "4' shark" : 'Small Shark',
        "6' shark" : 'Large Shark',
        "4' toNA shark" : 'Small Shark',
        "2NAm NA] shark" : 'Large Shark',
        "3' shark" : 'Small Shark',
        "5' shark" : 'Small Shark', 
        "3' toNA shark" : 'Small Shark',
        "2 m shark" : 'Large Shark',
        "3 m NA'] shark": 'Large Shark',
        "3 m shark": 'Large Shark', 
        "1NAm toNA5 m NA toNA] shark": 'Large Shark',
        "3NAm NA'] shark": 'Large Shark',
        "7' shark": 'Large Shark', 
        "8' shark": 'Large Shark',
        "5' toNA shark": 'Large Shark',
        "2NAm shark": 'Small Shark',
        "2' toNA shark": 'Small Shark',
        "a small shark": 'Small Shark',
        "Shark involvement prior to death not confirmed": 'Shark Small',
        "1 m shark": 'Shark Small',   
        "Shark involvement not confirmed": 'Small Shark',
        "Shark involvement prior to death unconfirmed": 'Small Shark',
        "NA shark": 'Small Shark', 
        "3.5' to 4' shark": 'Small Shark',
        "14' to 18'shark": 'Large Shark', 
        "15' shark": 'Large Shark', 
        "2 to 2.5 m shark": 'Large Shark', 
        "1' to 2' shark": 'Small Shark', 
        '20 to 30kg shark': 'Small Shark', 
        "14' shark": 'Large Shark', 
        '2 m to 3 m shark': 'Large Shark', 
        '80 kg shark': 'Large Shark', 
        '2.6 m shark': 'Large Shark', 
        "+3' shark" : 'Small Shark', 
        "2' to 3' juvenile shark": 'Small Shark', 
        "3'  shark": 'Small Shark', 
        "2'  shark": 'Small Shark', 
        "4.5 to 5' shark": 'Small Shark', 
        "1.5' to 2' shark" : 'Small Shark', 
        "2.5' shark": 'Small Shark', 
        '"a small shark"': 'Small Shark', 
        'Not a shark attack; it was a hoax': 'not a shack' 
        
        
        
    }
    # Reemplazar valores no deseados con 'NA'
    mapping = {
        ' ' : 'NA',
        'no shark involvement' : 'NA',
        'no shark invovlement' : 'NA',
        'no shark invovlement - it ws a publicity stunt' : 'NA',
        'Invalid' : 'NA',
        'Invalid incident' : 'NA',
        'Questionable' :'NA',
        'Questionable incident' :'NA',
        'No shark involvement' : 'NA',
        '1NAm NA] shark' : 'NA',
        'Shark involvement prior to death was not confirmed' : 'NA',
        'Shark involvement not confirmed ' : 'NA',
        'NA shark ' : 'NA',
        '1NAm shark' : 'NA',
        "4' shark" : 'NA',
        "6' shark" : 'NA',
        "4' toNA shark" : 'NA',
        "2NAm NA] shark" : 'NA',
        "3' shark" : 'NA',
        "5' shark" : 'NA', 
        "3' toNA shark" : 'NA',
        "2 m shark" : 'NA',
        "3 m NA'] shark": 'NA',
        "3 m shark": 'NA', 
        "1NAm toNA5 m NA toNA] shark": 'NA',
        "3NAm NA'] shark": 'NA',
        "7' shark": 'NA', 
        "8' shark": 'NA',
        "5' toNA shark": 'NA',
        "2NAm shark": 'NA',
        "2' toNA shark": 'NA',
        "a small shark": 'NA',
        "Shark involvement prior to death not confirmed": 'NA',
        "1 m shark": 'NA',   
        "Shark involvement not confirmed": 'NA',
        "Shark involvement prior to death unconfirmed": 'NA',
        "NA shark": 'NA',
    }

    # Reemplazar valores no deseados en la columna 'Species'
    df[column_name] = df[column_name].replace(mapping)

    # Eliminar filas con 'NA' en la columna 'Species'
    df = df[df[column_name] != 'NA']
    
    return df

def clean_and_normalize_species(df, column_name):
    """
    Limpia y normaliza la columna de especies en el DataFrame.
    
    Args:
    df (pd.DataFrame): El DataFrame que contiene la columna a limpiar.
    column_name (str): El nombre de la columna a limpiar.
    
    Returns:
    pd.DataFrame: El DataFrame con la columna limpiada y normalizada.
    """
    def replace_species(value, replacements):
        if pd.notna(value):  # Check if value is not NaN
            value_lower = value.lower()
            for key, replacement in replacements.items():
                if key in value_lower:
                    return replacement
        return value

    # Diccionario de términos y sus sustituciones
    replacements = {
        'white': 'White Shark',
        'tiger': 'Tiger Shark',
        'bull': 'Bull Shark',
        'nurse': 'Nurse Shark',
        'blacktip': 'Blacktip Shark',
        'hammerhead': 'Hammerhead Shark',
        'lemon': 'Lemon Shark',
        'blue': 'Blue Shark',
        'brown': 'Brown Shark',
        'raggedtooth': 'Raggedtooth Shark',
        'bronze': 'Bronze Shark',
        'caribbean': 'Caribbean Reef Shark',
        'mako': 'Mako Shark', 
        'reportedly a great white': 'White Shark', 
        'shall shark': 'Shall Shark', 
        'sandbar': 'Sandbar Shark', 
        'carribean': 'Carribean Reef Shark', 
        'raggedtooth': 'Raggedtooth Shark', 
        'broze': 'Bronze Shark', 
        'sevengill': 'Sevengill Shark', 
        'whitetip': 'White Shark', 
        'nurse': 'Nurse Shark', 
        'galapagos': 'Galapagos Shark', 
        'cookiecutter': 'Cookiecutter Shark', 
        'wfite': 'White Shark', 
        'wobbegong': 'Wobbegong Shark', 
        'horn': 'Horn Shark', 
        'mako': 'Mako Shark', 
        '"A small shark': 'Small Shark', 
        'epaulette': 'Epaulette Shark', 
        'spinner' : 'Spinner Shark', 
        'galapagos': 'Galapagos Shark', 
        'tope': 'Tope Shark', 
        '"Reef shark"': 'Reef Shark', 
        '"whitetip shark"': 'White Shark', 
        'broadnose': 'Broadnise Shark', 
        'reef': 'Reef Shark', 
        'sandtiger': 'Tiger Shark', 
        'spinner': 'Spinner Shark', 
        'stingray': 'Stringray Shark', 
        'toadfish': 'Toadfish Shark', 
        '"reef shark"': 'Reef Shark',
        'blue': 'Blue Shark', 
        'salmon': 'Salmon Shark', 
        'wobbegong': 'Wobbegong Shark', 
        'porbeagle': 'Porbeagle Shark', 
        'seven-gill' : 'Gill Shark', 
        'dogfish': 'Dogfish Shark', 
        'silky': 'Silky Shark', 
        'hammerhead': 'Hammmerhead Shark', 
        'raggedtooth': 'Raggedtooth Shark', 
        'goblin': 'Goblin Shark', 
        'angel': 'Angel Shark', 
        'zambesi': 'Zambesi Shark',
        'spurdog': 'Spurdog Shark', 
        'smoothhound': 'Smoothhound Shark', 
        'basking': 'Basking Shark', 
        'sand': 'Sand Shark', 
        'silvertip': 'Silvertip Shark', 
        "on 8/13/2005 anglers from New Zealand":'Small Shark', 
        'copper': 'Copper Shark',
        'dusky': 'Dusky Shark',
        "grey-colored shark": 'Grey Shark',
        'cow': 'Cow Shark', 
        'small': 'Small Shark', 
        'juvenile': 'Small Shark', 
        'authentificated': 'unconfirmed',
        'whale': 'Whale Shark', 
        'unknown': 'unconfirmed', 
        '"red shark"': 'Red Shark', 
        'zambesi': 'Zambezi Shark', 
        'unconfirmed': 'unconfirmed', 
        'carpet': 'Carpet Shark', 
        '"spear-eye"': 'Spear-eye Shark', 
        'whale': 'Whale Shark', 
        'anglers from New Zealand': 'Large Shark', 
        '"black finned shark"': 'Finned Shark', 
        'soupfin': 'Soupfin Shark', 
        'leopard': 'Leopard Shark', 
        'grey': 'Grey Shark', 
        'gaffed': 'Gaffed Shark', 
        'shovelnose': 'Shovelnose Shark', 
        '"ground shark"': 'Ground Shark', 
        '>': 'Large Shark', 
        'zambezi': 'Zambezi Shark', 
        'albimarginatus': 'Albimarginatus Shark', 
        '<': 'Small Shark', 
        '500': 'Large Shark', 
        '136': 'Large Shark', 
        '193': 'Large Shark', 
        '"yellow belly"': 'Large Shark', 
        'rhizoprionodon': 'Gummy Shark',
        '"banjo shark"': 'Banjo Shark', 
        'not a shark': 'not a shark', 
        'shark captured': 'Large Shark', 
        'sharks': 'Large Shark', 
        '"a very flat head”': 'Large Shark', 
        '"gummy”': 'Gummy Shark', 
        '2 m': 'Large Shark', 
        'larger': 'Large Shark', 
        'hull': 'Hull Shark', 
        '4.5  m': 'Large Shark', 
        'bite': 'not a shark', 
        'cocktail': 'Cocktail Shark', 
        'carcharhinid': 'Carcharhinid Shark',
        'macrurus': 'C. Macrurus Shark', 
        '“spear-eye”': 'Spear-Eye Shark', 
        'bonita sharkk': 'Bonita Shark', 
        'anglers': 'Anglers Shark', 
        'tooth fragments': 'Large Shark', 
        'to involve a pinniped instead': 'not a shark', 
        'on turtle scraps': 'Small Shark', 
        'another shark nearby': 'Large Shark', 
        'dolphin': 'not a shark', 
        'shark known as': 'Old Tom Shark', 
        '13': 'Large Shark', 
        "7' to 8'": 'Large Shark', 
        'invovlement': 'not a shark', 
        'not confirmes': 'Small Shark', 
        "3.3 m [10'": 'Large Shark', 
        '60 cm': 'Small Shark', 
        "1.3 m [4'": 'Small Shark',
         "1.8 m [6']": 'Large Shark'
       }

    # Aplicar la función de sustitución a la columna 'Species'
    df[column_name] = df[column_name].apply(replace_species, replacements=replacements)

    
    mapping2 = {
        '"small sharks"' : 'Small Shark', 
        '"a small shark"' : 'Small Shark',
        'Large shark': 'Large Shark',
        '2.5m shark': 'Large Shark',
        "3' to 4' shark": 'Small Shark', 
        "8' shark": 'Large Shark', 
        "4' shark": 'Small Shark',
        "3' shark": 'Small Shark', 
        '1m shark': 'Small Shark', 
        '5m to 6m shark': 'Large Shark', 
        "5'shark": 'Large Shark', 
        '3m shark': 'Large Shark', 
        "6' shark": 'Large Shark', 
        "9' shark": 'Large Shark', 
        "5' shark": 'Large Shark', 
        "2' to 3' shark": 'Small Shark', 
        "7' to 8' shark": 'Large Shark', 
        '8 ft shark': 'Large Shark', 
        '5.5 ft shark': 'Large Shark', 
        '1.3m shark': 'Small Shark', 
        "3' to 5' shark": 'Small Shark', 
        '8" shark' : 'Large Shark', 
        '4m shark': 'Large Shark', 
        "4' to 5' shark": 'Small Shark', 
        '2 m shark': 'Large Shark', 
        "5' to 6' shark": 'Large Shark', 
        "7' shark": 'Large Shark', 
        "1+ m shark": 'Small Shark', 
        "6' to 7' shark": 'Large Shark',
        "2' shark": 'Small Shark', 
        "6.5' shark": 'Large Shark', 
        "10' to 12' shark": 'Large Shark', 
        "shark pup": 'White Shark', 
        "12' shark": 'Large Shark',
        "2.5 m shark": 'Large Shark', 
        "Reported as shark attacks but injuries caused by toadfish": 'not a shark', 
        "Reported as shark bite but injury caused by stingray": 'not a shark', 
        "5' to 8' shark": 'Large Shark', 
        "3 m shark": 'Large Shark', 
        "2m shark": 'Large Shark',
        "small shark": 'Small Shark', 
        "3m shark, probably a smooth hound": 'Large Shark', 
        'Shark involvement highly doubtful' : 'Small Shark', 
        'No shark invovlement - it ws a publicity stunt' : 'not a shark', 
        'Shark involvement prior to death not confirmed': 'Small Shark', 
        "10' shark": 'Large Shark', 
        'a small shark': 'Small Shark', 
        '3+ m shark': 'Large Shark', 
        "4' shark?": 'Small Shark', 
        '1m to 1.2 m shark': 'Small Shark', 
        '3- to 4-foot shark': 'Small Shark', 
        '3.5 to 4 m shark': 'Large Shark', 
        '2 m to  3 m shark': 'Large Shark', 
        '1.8 m shark': 'Large Shark', 
        '5 m shark': 'Large Shark', 
        '1.5 m shark': 'Small Shark', 
        '1 m shark': 'Small Shark', 
        "8' to 10' shark": 'Large Shark', 
        "4' to 6' shark" : 'Small Shark', 
        "4' tp 5' shark": 'Small Shark', 
        '1.8 metre shark': 'Large Shark',
        "6' to 8' shark": 'Large Shark', 
        'shark involvement not confirmed': 'Small Shark', 
        '"small sharks"': 'Small Shark', 
        'no shark involvement' : 'not a shark', 
        'no shark invovlement' : 'not a shark', 
        'No shark involvement' : 'not a shark',
        '1NAm NA] shark' : 'Large Shark',
        "4' toNA shark" : 'Small Shark',
        "4' shark" : 'Small Shark',
        "6' shark" : 'Large Shark',
        "4' toNA shark" : 'Small Shark',
        "2NAm NA] shark" : 'Large Shark',
        "3' shark" : 'Small Shark',
        "5' shark" : 'Small Shark', 
        "3' toNA shark" : 'Small Shark',
        "2 m shark" : 'Large Shark',
        "3 m NA'] shark": 'Large Shark',
        "3 m shark": 'Large Shark', 
        "1NAm toNA5 m NA toNA] shark": 'Large Shark',
        "3NAm NA'] shark": 'Large Shark',
        "7' shark": 'Large Shark', 
        "8' shark": 'Large Shark',
        "5' toNA shark": 'Large Shark',
        "2NAm shark": 'Small Shark',
        "2' toNA shark": 'Small Shark',
        "a small shark": 'Small Shark',
        "Shark involvement prior to death not confirmed": 'Shark Small',
        "1 m shark": 'Shark Small',   
        "Shark involvement not confirmed": 'Small Shark',
        "Shark involvement prior to death unconfirmed": 'Small Shark',
        "NA shark": 'Small Shark', 
        "3.5' to 4' shark": 'Small Shark',
        "14' to 18'shark": 'Large Shark', 
        "15' shark": 'Large Shark', 
        "2 to 2.5 m shark": 'Large Shark', 
        "1' to 2' shark": 'Small Shark', 
        '20 to 30kg shark': 'Small Shark', 
        "14' shark": 'Large Shark', 
        '2 m to 3 m shark': 'Large Shark', 
        '80 kg shark': 'Large Shark', 
        '2.6 m shark': 'Large Shark', 
        "+3' shark" : 'Small Shark', 
        "2' to 3' juvenile shark": 'Small Shark', 
        "3'  shark": 'Small Shark', 
        "2'  shark": 'Small Shark', 
        "4.5 to 5' shark": 'Small Shark', 
        "1.5' to 2' shark" : 'Small Shark', 
        "2.5' shark": 'Small Shark', 
        '"a small shark"': 'Small Shark', 
        'Not a shark attack; it was a hoax': 'not a shark', 
        '"A small shark"': 'Small Shark', 
        'Authorities report injury caused bya barracuda': 'not a shark', 
        'No shark invovlement': 'not a shark', 
        'A small shark': 'Small Shark', 
        "7' to 8' shark": 'Large Shark', 
        'Injuries not caused by a shark': 'not a shark', 
        'Shark involvement unconfirmed but considered probable': 'Small Shark', 
        'Shovelnose "shark" which is a ray, not a shark)': 'not a shark', 
        'Juvenile shark': 'Small Shark', 
        'Injury most likely caused by barracuda, not a shark':'not a shark', 
        'Shark involvement questionable': 'Small Shark', 
        " 6' to 8' shark": 'Large Shark', 
        "Said to involve an 8' shark but more likely damage caused by debris": 'not a shark', 
        'juvenile shark': 'Small Shark', 
        "Thought to involve a 3' to 4' shark, but shark involvement not confirmed": 'Small Shark', 
        'Shark involvement not cofirmed' : 'unconfirmed', 
        'Shark involvement not confirmed & highly unlikely': 'not a shark', 
        '7-gill shark?': 'Large Shark', 
        '7-gill shark': 'Large Shark', 
        '4.5 m shark': 'Large Shark', 
        '18" to 24" shark': 'Large Shark', 
        'Port Jackson shark, 1m': 'Small Shark', 
        '4 m shark': 'Large Shark', 
        '3 m to 4 m shark': 'Large Shark', 
        'Shark involvement probable, but not confirmed': 'Small Shark',
        'Reported by media as shark attack, but shark involvement prior to death was not confirmed': 'unconfirmed', 
        'Shark involvement not confirmed; thought to be a barracuda bite': 'not a shark', 
        '2.27 m shark': 'Large Shark', 
        '1.5 to 2 m shark': 'Small Shark', 
        "9.5' shark?": 'Large Shark', 
        "3' small spotted catshark, Scyliorhinus canicula": 'Small Shark', 
        'Questionable Incident': 'unconfirmed', 
        '2.4 m shark': 'Large Shark', 
        '24" to 30" shark': 'Large Shark', 
        '2.5 to 3 m shark': 'Large Shark', 
        '2 to 3 m shark': 'Large Shark', 
        "1' to 4' shark": 'Small Shark', 
         'small catsharks': 'Small Shark', 
         '3 m, 600-kg shark': 'Large Shark', 
         'Said to involve a 1.5 m shark': 'Small Shark', 
         "2 m [6.75'] shark, 200-kg shark T": 'Large Shark', 
         "[4.5' to 5'] shark": 'Small Shark', 
         "Unknown, but it was reported that a shark tooth was recovered from the wound": 'unconfirmed', 
         '"small shark"': 'Small Shark', 
         '18" to 36" shark': 'Large Shark', 
         "4 m [13'] shark": 'Large Shark', 
         "3 m [10'] shark": 'Large Shark', 
         "2.4 m [8'] shark": 'Large Shark', 
         "1.2 m [4'] shark": 'Small Shark', 
         "1.8 m [6'] shark": 'Small Shark', 
         "1.2 m to 1.5 m [4' to 5'] shark": 'Small Shark', 
         '2 sharks, 4.5 m & 3 m': 'Large Shark', 
         '"black tipped" shark': 'Tipped Shark', 
         "0.9 m to 1.5 m [3' to 5'] shark": 'Small Shark', 
         "2.4 m to 3.7 m [8' to 12'] shark": 'Large Shark', 
         'small sharks': 'Small Shark', 
         'Shark involvement doubtful': 'undefined', 
         'Unidentified species' : 'undefined', 
         "1.5 m to 1.8 m [5' to 6'] shark" : 'Small Shark', 
         "106 cm [3.5']  shark": 'Small Shark',
         "3.7 m to 4.3 m [12' to 14'] shark": 'Large Shark', 
         "0.9 m to 1.2 m [3' to 4'] shark": 'Small Shark', 
         'A “small” shark': 'Small Shark', 
         "60 cm [2'] captive shark": 'Small Shark', 
         'Species unidentified': 'unconfirmed', 
         "3.5' to 4.5' shark": 'Large Shark', 
         '"A pack of sharks"': 'Large Shark', 
         'Unknown, but the shark was caught and put on exhibition': 'unconfirmed', 
         '"a large shark"': 'Large Shark', 
        "Questionable incident, said to involve a 6' shark" : 'Large Shark', 
        '3 sharks': 'Large Shark', 
        'Not specified': 'undefined', 
        '6 ft shark': 'Large Shark', 
         '6ft shark': 'Large Shark', 
         'Bu.ll': 'undefined', 
         "7' to 8' shark": 'Large Shark', 
         ' ': 'not a shark', 
         "3' to 3.5' shark": 'Small Shark', 
         "5' to 7' shark": 'Large Shark', 
         '2 sharks, 4.5 m & 3 m': 'Large Shark', 
         '15 cm to 20 cm [6" to 8"] bite diameter just below left knee': 'Small Shark', 
         "2.4 m to 3 m [8' to 10'] grey colored shark": 'Large Shark', 
         "3 m to 3.7 m [10' to 12'] shark": 'Large Shark', 
         "0.9 m  to 1.2 m [3' to 4'] shark": 'Small Shark', 
         "0.9 m to 1.2 m [3' to 4'] shark; Tooth fragment recovered from hand": 'Small Shark', 
         '1 m  shark': 'Small Shark', 
         "2.1 m to 2.4 m [7' to 8'] shark": 'Large Shark', 
         "0.9 m [3'] shark": 'Small Shark', 
         'Shark involvement prior to death unconfired': 'Small Shark', 
         'C. leucas tooth fragment recovered from kayak': 'uncorfirmed', 
         'Questionable incident - shark bite may have precipitated drowning': 'unconfirmed', 
         'Unidentified': 'unconfirmed', 
         "2' to 3.5' shark": 'Small Shark', 
         "1.5 m [5'] shark": 'Small Shark', 
         "0.9 m  [3'] shark": 'Small Shark', 
         "1.2 m to 1.5 m [4.5' to 5'] shark": 'Small Shark', 
         "1.2 m to 1.8 m [4' to 6'] shark": 'Small Shark', 
         "2.1 to 2.4 m [7' to 8'] shark": 'Large Shark', 
         "60 cm to 90 cm [2' to 3'] shark": 'Small Shark', 
         "A 2' shark was seen in the area by witnesses": 'Small Shark', 
         'Shark involvement  not confirmed': 'unconfirmed', 
         'Shark involvement  questionable': 'unconfirmed', 
         '1.3 to 1.6 m shark': 'Small Shark', 
         '200 to 300 kg shark': 'Large Shark', 
         "4.5' to 5' shark": 'Small Shark', 
         '1.7 m shark': 'Small Shark', 
         'Shark involvement prior to death suspected but not confirmed': 'unconfirmed', 
         "1.8 m to 2.1 m [6' to 7'] shark": 'Large Shark', 
         '"a young shark"': 'Small Shark',
         "1.2 m to 1.5 m [4' to 5']   shark": 'Small Shark', 
         "1.5 to 1.8 m [5' to 6'] shark": 'Small Shark', 
         "Two 1.2 m to 1.5 m [4' to 5'] sharks":'Small Shark', 
         "2.1 m [7'] shark": 'Large Shark', 
         ">1.8 m [6'] shark": 'Large Shark', 
         "1.8 m to 2.4 m [6' to 8'] shark, tooth fragments recovered": 'Large Shark', 
         'Unidentified shark': 'unconfirmed', 
         '>2 m shark': 'Large Shark', 
         "5 m [16.5'] shark": 'Large Shark', 
         '1.8 m grey shark': 'Grey Shark', 
         "3 m [10'], 270- kg [595-lb] shark": 'Large Shark', 
         "7' female shark": 'Large Shark', 
         '"Shark had a very large girth"': 'Large Shark', 
         "1.8 m [6'] shark": 'Large Shark', 
         "1.8 m to 2.4 m [6' to 8'] shark": 'Large Shark', 
         '6 m, 600-kg shark':'Large Shark', 
         "Two sharks seen in vicinity: 2.4 m & 4.25 m  [8' & 14'] TL":'Large Shark', 
        '2 m to 2.5 m shark': 'Large Shark', 
        "1.5 m to 2 m [5' to 6.75'] shark": 'Large Shark', 
        '1 m "grey-colored" shark': 'Small Shark', 
        '"gray shark"': 'Grey Shark', 
        'a school of sharks': 'Large Shark', 
        '"Shark caught later"': 'Large Shark', 
        'Remains recovered from shark caught days later': 'unconfirmed', 
        '234-lb shark': 'Large Shark', 
        "Said to be a 7.6 m [25'] shark": 'Large Shark', 
        '"The fish was harpooned, dried, and presented to the sailor, who went round Europe exhibiting it  It was said to be 20 feet long.': 'Large Shark', 
        '70 kg shark': 'Small Shark', 
        '5m, 3500 kg female shark': 'Large Shark', 
        '"a school of sharks"': 'Large Shark', 
        '250-lb "dog shark"': 'Dog Shark', 
        '650-lb shark': 'Large Shark', 
        '2 days later a 600-lb shark was caught 100 yards from the site': 'Large Shark',
        "7' to 8' shark": 'Large Shark', 
        "3' to 3.5' shark": 'Small Shark', 
        "5' to 7' shark": 'Small Shark', 
        "12' to 18' shark" : 'Large Shark', 
        '2 sharks, 4.5 m & 3 m': 'Large Shark', 
        '15 cm to 20 cm [6" to 8"] bite diameter just below left knee': 'Small Shark', 
        "2.4 m to 3 m [8' to 10'] grey colored shark": 'Grey Shark', 
        "3 m to 3.7 m [10' to 12'] shark": 'Large Shark', 
        "0.9 m  to 1.2 m [3' to 4'] shark": 'Small Shark', 
        "0.9 m to 1.2 m [3' to 4'] shark; Tooth fragment recovered from hand": "Small Shark",
         "2 sharks": 'Large Shark', 
         'Identified as C. gangeticus by Dr. J. Fayrer': 'unconfirmed', 
         'Said to involve 2 sharks': 'Large Shark', 
         "Said to involve 2 sharks": 'Large Shark', 
         "4.7 m [15.5'] shark": 'Large Shark', 
         "16' shark": 'Large Shark', 
         "20' shark": 'Large Shark', 
         "1.8 m to 2.7 m [6' to 9'] shark": 'Large Shark', 
         "Fishermen recovered partial remains from shark a week later": 'unconfirmed', 
         'Remains recovered 5 days later': 'unconfirmed', 
         'Shark involvement probable': 'unconfirmed', 
         'Allegedly a 33-foot shark': 'Large Shark', 
         'Remains recovered from 3 sharks': 'Large Shark', 
         '18-foot shark': 'Large Shark', 
         "5.5' to 6' shark": 'Large Shark', 
         "Said to involve a 2.7 m [9'] shark": 'Large Shark', 
         "13' shark": 'Large Shark', 
         "3.7 m to 4.3 m [12' to 14']  shark": 'Large Shark', 
         "3.7 m [12'], 1200-lb shark. Shark caught & its jaw exhibited at the Carnegie Museum": 'Large Shark', 
         "15'": 'Large Shark', 
         '15* to 24" dog shark': 'Dog Shark', 
         "Comrades saw shark's tail appear about 5' away": 'Large Shark', 
         '"A pack of 6 sharks"': 'Large Shark', 
         "2.7 m [9'] shark later captured by Mitchell-Hedges": 'Large Shark', 
         '"a very large shark"': 'Large Shark', 
         "According to Carlsmith, the shark's mouth was 3' wide": 'Large Shark', 
         'Questionable, 2m shark suspected': 'Large Shark', 
         '"whiptail shark" (thresher shark?)': 'Whiptail Shark', 
         '"a dog shark"': 'Dog Shark', 
         '9-foot shark': 'Large Shark', 
         "7 shark's teeth found embedded in the woodwork of the boat": 'unconfirmed',
         "16' 800-lb shark": 'Large Shark', 
         "4.3 m [14'] shark seen in area previous week": 'Large Shark', 
         '100-lb shark': 'Large Shark', 
         "4.3 m [14'] shark seen in vicinity": 'Large Shark', 
         "0.9 m [3']  shark": 'Large Shark', 
         "18' shark": 'Large Shark', 
         "6 m [20']  shark": 'Large Shark', 
         "1.5 m, 45-kg shar": 'Large Shark', 
         "1.8 m to 2.4 m [6' to 8'] shark, tooth fragments recovered": 'Large Shark', 
         "1.8 m [6'] shark": 'Large Shark', 
         "6 m shark": 'Large Shark', 
         "2 m [6.75'] shark": 'Large Shark', 
         '40 to 50 sharks attacked survivors in the water': 'Large Shark', 
         '4.3 m shark': 'Large Shark', 
         "6', 100-lb shark": 'Large Shark', 
         '30-kg [66-lb] shark': 'Small Shark', 
         'Shark involvement not confirmed; officials considered barracua': 'not a shark', 
         '.5 m shark': 'Small Shark', 
         "4.5' shark": 'Small Shark', 
         "3 m to 4 m [10' to 13'] shark": 'Large Shark', 
         'Questionable incident; reported as shark attack but thought to involve a pinniped instead':'not a shark', 
         'Reported as a shark attack, the story was a hoax': 'not a shack', 
         "1.8 m [6'] shark, species identity questionable": 'Large Shark', 
         "13', 400-lb thresher shark": 'Large Shark', 
         'C. maculpinnis or C. limbatus': 'Maculpinnis Shark',
         "4' to 8' shark": 'Small Shark', 
         '2.2 m shark': 'Large Shark', 
         '270 kg shark': 'Large Shark', 
         "1.5 to 2 m [5' to 6.75'] shark": 'Large Shark', 
         "2.7 m  [9'] shark": 'Large Shark', 
         "12' to 14' shark": 'Large Shark', 
         "3.7 m [12'] sharks": 'Large Shark', 
         "2 m to 2.5 m [6.75'  to 8.25'] shark": 'Large Shark', 
         '1.5 m to 2 m shark': 'Large Shark', 
         '"Dog shark"': 'Dog Shark', 
         "7.5' shark": 'Large Shark', 
         'Considered a "Doubtful" incident': 'Unconfirmed', 
         "4m [13'] shark": 'Large Shark', 
         "1.5 m to 1.8m [5' to 6'] shark": 'Small Shark', 
         "3.7 m [12'] shark": 'Large Shark', 
         "A pack of 6 sharks": 'Large Sharks', 
         "1.5 m to 2.1 m  [5' to 7'] shark": 'Large Shark', 
         "4.6 m [15'] shark": 'Large Shark', 
         "1.8 m [6'], 180-lb shar": 'Large Shark', 
         '2 sharks involved': 'Large Shark', 
         '300-kg [662-lb] shark': 'Large Shark', 
         "1.8 m [6'], 136-kg [300-lb] shark": 'Large Shark', 
         "1.8 to 2.4 m [6' to 8'] shark": 'Large Shark', 
         "Less than 1.2 m [4']": 'Small Shark', 
         "1.7 m [5.5'] shark": 'Small Shark', 
         "2.1 m to 2.4 m  [7' to 8'] shark": 'Large Shark', 
         "1.8 m [6']  shark": 'Large Shark', 
         "4.3 m [14'], 1000-lb shark": 'Large Shark', 
         "500-lb shark": 'Large Shark', 
         "5.5 m [18'] shark": 'Large Shark', 
         "8 sharks": 'Large Shark', 
         "1.8 m to 2.4 m  [6' to 8'] shark": 'Large Shark', 
         "3.7 to 4.5 m [12' to 15'] shark seen in vicinity": 'Large Shark', 
         "Said to be 6.4 m [21'] shark": 'Large Shark', 
         '2 sharks, 4.5 m & 3 m': 'Large Shark', 
         "1.8 m [6'], 180-lb shark": 'Large Shark', 
         "2.7 m [9'] shark": 'Large Shark', 
         "2.5 m [8.25'] shark": 'Large Shark', 
         "4.3 m [14'] shark": 'Large Shark', 
         "3.5 m shark": 'Large Shark', 
         "2.7 m to 3 m [9' to 10'] sharks": 'Large Shark', 
         "4.9 m [16']shark": 'Large Shark', 
         "1.2 m  [4'] shark": 'Large Shark', 
         "Next morning a 3 m [10'] shark was caught that had Andrews' leg in its gut": 'Large Shark', 
         "Two shark's teeth recovered from canoe": 'unconfirmed', 
         "1.5 m to 1.8 m  [5' to 6'] shark": 'Small Shark', 
         '43" shark': 'Small Shark', 
         "2.4 m [8'], 600-lb shark": 'Large Shark', 
         '80-lb hooked shark': 'Small Shark', 
         '200-lb shark': 'Large Shark', 
         "7' to 8' shark": 'Large Shark', 
         'Injury believed caused by an eel, not a shark': 'not a shark',
         "3.5 m [11.5']shark": 'Large Shark', 
         "[4' to 5']": 'Large Shark', 
         "2 sharks, 4.5 m & 3 m": 'Large Shark', 
         "6 m [20'] shark": 'Large Shark', 
         "3.7 m to 4.6 m [12' to 15'] shark seen in the vicinity": 'Large Shark', 
         "1.8 m to 2.4 m [6' to 8'] shark, tooth fragments recovered": 'Large Shark', 
         "1.8 m [6'] shark": 'Large Shark', 
         "150-lb shark": 'Large Shark', 
         "1.6 m shark": 'Small Shark', 
         'Questionable incident; reported as shark attack but thought to involve a pinniped instead': 'unconfirmed', 
         "1.5 m [5']  shark": 'Small Shark', 
         "1.2 m to 1.8 m [4' to 6'] shark observed in area": 'Small Shark', 
         '90-kg "blackfin" shark': 'Blackfin Shark', 
         '60 cm  shark': 'Small Shark', 
         '36"  shark': 'Small Shark', 
         "2.7 m [9']shark":'Large Shark', 
         "1.2 m [4'], possibly  larger shark": 'Small Shark', 
         "Two 2.1 m [7'] sharks": 'Large Shark',
         "3.7 m to 4.6 m [12' to 15'] shark": 'Large Shark', 
         "2.7 m [9']  shark": 'Large Shark', 
         "3.5 m [11.5'] shark": 'Large Shark', 
         "3 m to 4.3 m [10' to 14'] shark": 'Large Shark', 
         "5.5' shark": 'Small Shark', 
         "20 kg shark": 'Small Shark', 
         "1.8 to 2.1 m [6' to 7'] shark": 'Large Shark', 
         "Bitten by several 1.8 m [6'] sharks": 'Large Shark', 
         'Injury believed caused by an eel, not a shark': 'not a shark', 
         '2 sharks, 4.5 m & 3 m': 'Large Shark', 
         "1.2 m [4'], possibly  larger shark": 'Large Shark', 
         "Two 2.1 m [7'] sharks": 'Large Shark', 
         'Shark involvement prior to deaths was not confirmed': 'Small Shark', 
         "3.5 m [11.5'] shark": 'Large Shark', 
         "6 m [20'] shark": 'Large Shark', 
         "20 kg shark": 'Small Shark', 
         "1.8 to 2.1 m [6' to 7'] shark": 'Large Shark', 
         "Said to involve 2 sharks: 5.2 m & 6 m [17' & 20']": 'Large Shark', 
         "Sharks averaged 1.8 m [6'] in length": 'Large Shark', 
         '8-lb shark': 'Small Shark', 
         "2.4 m [8']  shark": 'Large Shark', 
         "4 m [13'] shark x 6": 'Large Shark', 
         "Reported as  a shark bite but toothmarks appear to be those of a dolphin": 'not a shark', 
         "0.7 m [2.5'] shark": 'Small Shark', 
         "2.13 m shark": 'Large Shark', 
         "Possibly C. leucas": "C. leucas Shark", 
         "1.5 m, 45-kg shark": 'Small Shark', 
         "2.3 m [7'] shark": 'Large Shark', 
         "3.7 [12'] shark": 'Large Shark', 
         "3 m [10'] shark seen in vicinity": 'Large Shark', 
         "1,100-lb shark": 'Large Shark', 
         '1.5 m, 45-kg shark': 'Small Shark', 
         '60 cm  shark': 'Small Shark', 
         "1.4 m [4.5'] shark": 'Small Shark', 
         '5m shark': 'Large Shark', 
         "2.6 m [8.5'] shark landed 2 hours later": 'Large Shark', 
         "2.6 m [8.5'] shark": 'Large Shark', 
         "4.4 m [14'] shark": 'Large Shark', 
         '68" shark': 'Small Shark', 
         'Description of shark does not ring true': 'unconfirmed', 
         "1.8 m [6'] shark": 'Large Shark'
         
         
         
         
        
        
    }
    
    df[column_name] = df[column_name].replace(mapping2)
    # Reemplazar valores no deseados con 'NA'
    mapping = {
        ' ' : 'NA',
        'no shark involvement' : 'NA',
        'no shark invovlement' : 'NA',
        'no shark invovlement - it ws a publicity stunt' : 'NA',
        'Invalid' : 'NA',
        'Invalid incident' : 'NA',
        'Questionable' :'NA',
        'Questionable incident' :'NA',
        'No shark involvement' : 'NA',
        '1NAm NA] shark' : 'NA',
        'Shark involvement prior to death was not confirmed' : 'NA',
        'Shark involvement not confirmed ' : 'NA',
        'NA shark ' : 'NA',
        '1NAm shark' : 'NA',
        "4' shark" : 'NA',
        "6' shark" : 'NA',
        "4' toNA shark" : 'NA',
        "2NAm NA] shark" : 'NA',
        "3' shark" : 'NA',
        "5' shark" : 'NA', 
        "3' toNA shark" : 'NA',
        "2 m shark" : 'NA',
        "3 m NA'] shark": 'NA',
        "3 m shark": 'NA', 
        "1NAm toNA5 m NA toNA] shark": 'NA',
        "3NAm NA'] shark": 'NA',
        "7' shark": 'NA', 
        "8' shark": 'NA',
        "5' toNA shark": 'NA',
        "2NAm shark": 'NA',
        "2' toNA shark": 'NA',
        "a small shark": 'NA',
        "Shark involvement prior to death not confirmed": 'NA',
        "1 m shark": 'NA',   
        "Shark involvement not confirmed": 'NA',
        "Shark involvement prior to death unconfirmed": 'NA',
        'Shark involvement prior to death could not be determined': 'NA',
        'Shark involvement suspected but not confirmed': 'NA', 
        "NA shark": 'NA',
    }

    # Reemplazar valores no deseados en la columna 'Species'
    df[column_name] = df[column_name].replace(mapping)

    # Eliminar filas con 'NA' en la columna 'Species'
    df = df[df[column_name] != 'NA']
    df = df[df[column_name] != 'Unconfirmed']
    df = df[df[column_name] != 'undefined']
    df = df[df[column_name] != 'Not authenticated']
    df = df[df[column_name] != 'uncorfirmed']
    df = df[df[column_name] != 'unconfirmed']
    df = df[df[column_name] != 'not a shark']
    df = df[df[column_name] != 'not a shack']
    df = df[df[column_name] != ' ']
    df = df.dropna(subset=[column_name])
    return df

def add_oceans_column(df, country_column, new_column):
    """
    Añade una columna de océanos y mares al DataFrame basada en el país.
    
    Args:
    df (pd.DataFrame): El DataFrame que contiene la columna de países.
    country_column (str): El nombre de la columna de países.
    new_column (str): El nombre de la nueva columna a añadir.
    
    Returns:
    pd.DataFrame: El DataFrame con la nueva columna añadida.
    """
    countries_oceans = {
        'morocco': 'Atlantic Ocean',
        'jamaica': 'Caribbean Sea',
        'belize': 'Caribbean Sea',
        'australia': 'Indian Ocean and Pacific Ocean',
        'usa': 'Atlantic Ocean and Pacific Ocean',
        'maldive islands': 'Indian Ocean',
        'turks and caicos': 'Atlantic Ocean',
        'french polynesia': 'Pacific Ocean',
        'tobago': 'Caribbean Sea',
        'bahamas': 'Atlantic Ocean',
        'india': 'Indian Ocean',
        'trinidad': 'Caribbean Sea',
        'south africa': 'Atlantic Ocean and Indian Ocean',
        'mexico': 'Pacific Ocean and Gulf of Mexico',
        'new zealand': 'Pacific Ocean',
        'egypt': 'Red Sea',
        'spain': 'Atlantic Ocean and Mediterranean Sea',
        'portugal': 'Atlantic Ocean',
        'samoa': 'Pacific Ocean',
        'colombia': 'Pacific Ocean and Caribbean Sea',
        'ecuador': 'Pacific Ocean',
        'cuba': 'Caribbean Sea',
        'brazil': 'Atlantic Ocean',
        'seychelles': 'Indian Ocean',
        'new caledonia': 'Pacific Ocean',
        'argentina': 'Atlantic Ocean',
        'fiji': 'Pacific Ocean',
        'maldives': 'Indian Ocean',
        'england': 'Atlantic Ocean',
        'japan': 'Pacific Ocean',
        'indonesia': 'Indian Ocean and Pacific Ocean',
        'thailand': 'Indian Ocean and Andaman Sea',
        'costa rica': 'Pacific Ocean and Caribbean Sea',
        'canada': 'Atlantic Ocean, Pacific Ocean, and Arctic Ocean',
        'jordan': 'Red Sea',
        'papua new guinea': 'Pacific Ocean',
        'reunion island': 'Indian Ocean',
        'china': 'Pacific Ocean',
        'ireland': 'Atlantic Ocean',
        'italy': 'Mediterranean Sea',
        'malaysia': 'Indian Ocean and South China Sea',
        'mauritius': 'Indian Ocean',
        'solomon islands': 'Pacific Ocean',
        'united kingdom': 'Atlantic Ocean',
        'united arab emirates': 'Persian Gulf',
        'philippines': 'Pacific Ocean',
        'cape verde': 'Atlantic Ocean',
        'dominican republic': 'Caribbean Sea',
        'cayman islands': 'Caribbean Sea',
        'aruba': 'Caribbean Sea',
        'mozambique': 'Indian Ocean',
        'puerto rico': 'Caribbean Sea',
        'greece': 'Mediterranean Sea',
        'france': 'Atlantic Ocean and Mediterranean Sea',
        'kiribati': 'Pacific Ocean',
        'taiwan': 'Pacific Ocean',
        'guam': 'Pacific Ocean',
        'nigeria': 'Atlantic Ocean',
        'tonga': 'Pacific Ocean',
        'scotland': 'Atlantic Ocean',
        'croatia': 'Adriatic Sea',
        'saudi arabia': 'Red Sea and Persian Gulf',
        'chile': 'Pacific Ocean',
        'kenya': 'Indian Ocean',
        'russia': 'Arctic Ocean and Pacific Ocean',
        'south korea': 'Pacific Ocean',
        'malta': 'Mediterranean Sea',
        'vietnam': 'South China Sea',
        'madagascar': 'Indian Ocean',
        'panama': 'Pacific Ocean and Caribbean Sea',
        'somalia': 'Indian Ocean',
        'norway': 'Atlantic Ocean and Arctic Ocean',
        'senegal': 'Atlantic Ocean',
        'yemen': 'Red Sea and Gulf of Aden',
        'sri lanka': 'Indian Ocean',
        'uruguay': 'Atlantic Ocean',
        'micronesia': 'Pacific Ocean',
        'tanzania': 'Indian Ocean',
        'marshall islands': 'Pacific Ocean',
        'hong kong': 'Pacific Ocean',
        'el salvador': 'Pacific Ocean',
        'bermuda': 'Atlantic Ocean',
        'montenegro': 'Adriatic Sea',
        'iran': 'Persian Gulf and Caspian Sea',
        'tunisia': 'Mediterranean Sea',
        'namibia': 'Atlantic Ocean',
        'bangladesh': 'Bay of Bengal',
        'western samoa': 'Pacific Ocean',
        'palau': 'Pacific Ocean',
        'grenada': 'Caribbean Sea',
        'turkey': 'Mediterranean Sea and Black Sea',
        'singapore': 'Indian Ocean',
        'sudan': 'Red Sea',
        'nicaragua': 'Pacific Ocean and Caribbean Sea',
        'american samoa': 'Pacific Ocean',
        'guatemala': 'Pacific Ocean and Caribbean Sea',
        'netherlands antilles': 'Caribbean Sea',
        'iceland': 'Atlantic Ocean',
        'barbados': 'Caribbean Sea',
        'guyana': 'Atlantic Ocean',
        'haiti': 'Caribbean Sea',
        'kuwait': 'Persian Gulf',
        'cyprus': 'Mediterranean Sea',
        'lebanon': 'Mediterranean Sea',
        'martinique': 'Caribbean Sea',
        'paraguay': 'Landlocked',
        'peru': 'Pacific Ocean',
        'ghana': 'Atlantic Ocean',
        'greenland': 'Atlantic Ocean and Arctic Ocean',
        'sweden': 'Baltic Sea',
        'djibouti': 'Red Sea and Gulf of Aden'
    }

    # Convertir los nombres de los países a minúsculas y eliminar espacios adicionales
    df[country_column] = df[country_column].str.lower().str.strip()
    
    # Convertir las claves del diccionario a minúsculas y eliminar espacios adicionales
    countries_oceans = {k.lower().strip(): v for k, v in countries_oceans.items()}
    
    # Imprimir algunos valores intermedios para depuración
    print("Valores únicos de la columna de países después de convertir a minúsculas y eliminar espacios:")
    print(df[country_column].unique())
    
    df[new_column] = df[country_column].map(countries_oceans)
    
    # Imprimir algunos valores del DataFrame después de añadir la nueva columna
    print("Valores del DataFrame después de añadir la columna de océanos y mares:")
    print(df[[country_column, new_column]].head(20))
    
    return df
