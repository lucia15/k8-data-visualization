import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pandas as pd
import datetime as dt
from datetime import datetime
import re
import calendar


# Include this path if working in Google Colab
#d = '/content/gdrive/My Drive/p2-p-data-visualization-Pappaterra-Lucia/'
# If not
d = ''


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def gsheet_api_check(SCOPES):
    """
    Check credentials, if none, request access.

    :param SCOPES: scopes
    :return: credentials
    """
    creds = None
    if os.path.exists(d + 'token.pickle'):
        with open(d + 'token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                d + 'modules/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open(d + 'token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


def pull_sheet_data(SPREADSHEET_ID, RANGE_NAME, SCOPES=SCOPES):
    """
    Pull data from google spreadsheet.

    :param SPREADSHEET_ID: spreadsheet id
    :param RANGE_NAME: sheet name
    :param SCOPES: scopes
    :return: pandas dataframe with the imported information
    """
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
    """
    Filters pandas dataframe with google spreadsheet information for specific date,
    also pre-process dataframe and sort projects by priority.

    :param data: dataframe with google spreadsheet data
    :param date: string with date
    :return: curated pandas dataframe
    """
    if date == 'today':
        date = pd.to_datetime(date).strftime('%m/%d/%Y')

    date = format_date(date)

    # get previous day
    day = datetime.strptime(date, '%m/%d/%Y')
    previous_day = day - dt.timedelta(days=1)
    previous_date = pd.to_datetime(previous_day).strftime('%m/%d/%Y')

    previous_date = format_date(previous_date)

    # get week day
    w_d = day.weekday()
    week_day = calendar.day_name[w_d]

    # get month name
    m = int(date.split('/')[0])
    month_name = calendar.month_name[m]

    date_text = week_day + ', ' + date.split('/')[1] + ' ' + month_name
    #date_text = week_day[:3] + ', ' + date.split('/')[1] + ' ' + month_name[:3]

    df = pd.DataFrame(data, columns=data[0])

    df = df.assign(Date=date_text)

    df['Timestamp'] = df['Timestamp'].apply(
        lambda s: s.split(' ')[0] if isinstance(s, str) else s)

    df = df[df['Timestamp'].isin([date, previous_date])]

    df['Project'] = df['Project'].apply(
        lambda s: remove_chars(s) if isinstance(
            s, str) else s)
    df.replace(float('NaN'), '', inplace=True)

    df['Team members'] = df['Team members'].apply(
        lambda s: remove_parenthesis(
            remove_chars(
                flat(s))) if isinstance(
            s, str) else s)
            
    df['Onboarding'] = df['Onboarding'].apply(
        lambda s: remove_parenthesis(
            remove_chars(
                flat(s))) if isinstance(
            s, str) else s)
            
    df['Offboarding'] = df['Offboarding'].apply(
        lambda s: remove_parenthesis(
            remove_chars(
                flat(s))) if isinstance(
            s, str) else s)

    for col in ['Issues in progress', 'Closed issues', 'Major issues']:
        df[col] = df[col].apply(lambda s: flat(s) if isinstance(s, str) else s)

    df['Next Release/ Important dates'] = df['Next Release/ Important dates'].apply(
        lambda s: s.replace('Release', '') if isinstance(s, str) else s)

    # sort by priority
    df['Priority'] = pd.Categorical(
        df['Priority'], categories=[
            'P1', 'P2', 'P3', ''], ordered=True)
    df = df.sort_values('Priority')

    df = df.drop_duplicates(subset=['Project'], keep='last')

    return df


def format_date(date):
    """
    Delete '0' from month in date string.

    :param mystring: string
    :return: string
    """
    if date[3] == '0':
        date = date[:3] + date[4:]
    return date


def remove_parenthesis(mystring):
    """
    Delete substring between parenthesis from string.

    :param mystring: string
    :return: string
    """
    regex = re.compile(r".*?\((.*?)\)")
    text = re.findall(regex, mystring)

    for i in range(len(text)):
        substring = '(' + text[i] + ')'
        mystring = mystring.replace(substring, '')

    return mystring


def remove_chars(mystring):
    """
    Removes @, -, # chars from string, replace double spaces by single space 
    and removes any trailing characters.

    :param mystring: string
    :return: string
    """
    return mystring.replace(
        '@',
        '').replace(
        '-',
        '').replace(
            '#',
            '').replace(
                '  ',
        ' ').rstrip('\n')


def flat(mystring):
    """
    Replace line breaks by commas.

    :param mystring: string
    :return: string
    """
    return mystring.replace('\n', ', ')
