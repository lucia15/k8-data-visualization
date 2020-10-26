import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pandas as pd
import datetime as dt
from datetime import datetime
import re


# Include this path if working in Google Colab    
#d = '/content/gdrive/My Drive/p2-p-data-visualization-Pappaterra-Lucia/'
# If not 
d = ''


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def gsheet_api_check(SCOPES):
    creds = None
    if os.path.exists(d+'token.pickle'):
        with open(d+'token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                d+'modules/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open(d+'token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds
    
    
def pull_sheet_data(SPREADSHEET_ID, RANGE_NAME, SCOPES=SCOPES):
    creds = gsheet_api_check(SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME).execute()
    values = result.get('values', [])
    
    if not values:
        print('No data found.')
    else:
        rows = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                  range=RANGE_NAME).execute()
        data = rows.get('values')
        print("COMPLETE: Data copied")
        return data
        
        
def sheet_to_df(data, date='today'):
    
    if date == 'today':
        date = pd.to_datetime(date).strftime('%m/%d/%Y')
    
    date = format_date(date)     
    
    # get previous day   
    day = datetime.strptime(date, '%m/%d/%Y')
    previous_day = day - dt.timedelta(days=1)
    previous_date = pd.to_datetime(previous_day).strftime('%m/%d/%Y')
    
    previous_date = format_date(previous_date)
        
    df = pd.DataFrame(data, columns=data[0])
    
    df['Timestamp'] = df['Timestamp'].apply(lambda s: s.split(' ')[0] if isinstance(s, str) else s)

    df = df[df['Timestamp'].isin([date, previous_date])]
    
    df['Project'] = df['Project'].apply(lambda s: remove_chars(s) if isinstance(s, str) else s)
    df.replace(float('NaN'), '', inplace=True)
    
    df['Team members'] = df['Team members'].apply(lambda s: remove_parenthesis(remove_chars(flat(s))) if isinstance(s, str) else s)
    df['Onboarding'] = df['Onboarding'].apply(lambda s: remove_parenthesis(remove_chars(flat(s))) if isinstance(s, str) else s)
    df['Offboarding'] = df['Offboarding'].apply(lambda s: remove_parenthesis(remove_chars(flat(s))) if isinstance(s, str) else s)
    
    for col in ['Issues in progress', 'Closed issues', 'Major issues']:
        df[col] = df[col].apply(lambda s: flat(s) if isinstance(s, str) else s)
    
    df['Next Release/ Important dates'] = df['Next Release/ Important dates'].apply(lambda s: s.replace('Release', '') if isinstance(s, str) else s)

    # sort by priority
    df['Priority'] = pd.Categorical(df['Priority'], categories=['P1','P2','P3',''], ordered=True)                   
    df = df.sort_values('Priority')

    df = df.drop_duplicates(subset=['Project'], keep='last')

    return df
    

def format_date(date):
    if date[3]=='0': 
        date = date[:3] + date[4:]  
    return date
    

def remove_parenthesis(mystring):
    """
    Delete substring between parenthesis from string
    """
    regex = re.compile(".*?\((.*?)\)")
    text = re.findall(regex, mystring)
    
    for i in range(len(text)):
        substring = '('+text[i]+')'
        mystring = mystring.replace(substring, '')

    return mystring
    

def remove_chars(mystring):
    return mystring.replace('@', '').replace('-', '').replace('#', '').replace('  ', ' ').rstrip('\n')
    
    
def flat(mystring):
    """
    Replace line breaks by commas
    """
    return mystring.replace('\n', ', ')
          