import os.path
import pickle
import requests
import pandas as pd
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


account_id = '112578893942190553010'
start_date = '2021-01-01'
end_date = '2021-01-02'


def get_token():
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/business.manage']

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds.token


def get_locations_list():
    locations_list = []
    page_token = None

    while page_token != '':
        my_headers = {'Authorization': 'Bearer {0}'.format(get_token())}
        query = {'orderBy': 'storeCode',
                 'pageToken': page_token}

        response = requests.get('https://mybusiness.googleapis.com/v4/accounts/{0}/locations'.format(account_id),
                                headers=my_headers,
                                params=query)

        for row in response.json()['locations']:
            x, y, z, location_id = row['name'].split('/')
            locations_list.append(location_id)

        try:
            page_token = response.json()['nextPageToken']
        except KeyError:
            page_token = ''

    return locations_list


def get_location_metrics():
    res = []
    for location_id in get_locations_list():
        my_headers = {'Authorization': 'Bearer {0}'.format(get_token())}
        my_json = {
                "locationNames": [
                    "accounts/112578893942190553010/locations/" + location_id
                ],
                "basicRequest": {
                    "metricRequests": [
                        {
                            "metric": "ALL",
                            "options": [
                                "AGGREGATED_DAILY"
                            ]
                        },
                    ],
                    "timeRange": {
                        "startTime": start_date + "T01:01:23.045123456Z",   # format : AAAA-MM-JJ
                        "endTime": end_date + "T23:59:59.045123456Z"        # format : AAAA-MM-JJ
                    }
                }
            }

        response = requests.post(
            'https://mybusiness.googleapis.com/v4/accounts/112578893942190553010/locations:reportInsights',
            headers=my_headers,
            json=my_json)

        res.append(response.json())

    return res


def save_local_data(data):
    with open('local_data', 'wb') as file:
        my_pickler = pickle.Pickler(file)
        my_pickler.dump(data)


def get_local_data():
    with open('local_data', 'rb') as file:
        my_unpickler = pickle.Unpickler(file)
        local_data = my_unpickler.load()

    return local_data


def clear_local_data():
    with open('local_data', 'wb') as file:
        my_pickler = pickle.Pickler(file)
        my_pickler.dump([])


def create_dataframe(data):     # data from get_location_metrics()
    df = pd.DataFrame(columns=['DATE', 'LOCATION_ID', 'METRIC', 'VALUE'])

    for location in data:
        x, y, z, location_id = location['locationMetrics'][0]['locationName'].split('/')
        for metric in location['locationMetrics'][0]['metricValues']:
            for date in metric['dimensionalValues']:
                try:
                    row = {
                        'DATE': date['timeDimension']['timeRange']['startTime'],
                        'LOCATION_ID': location_id,
                        'METRIC': metric['metric'],
                        'VALUE': date['value']}
                    df = df.append(row, ignore_index=True)
                except KeyError:
                    pass

    return df

