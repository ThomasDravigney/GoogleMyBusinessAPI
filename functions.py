from time import time
import os.path
import pickle
import requests
import pandas as pd
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


account_id = '112578893942190553010'


def timer(func):
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s')
        return result
    return wrap_func


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


@timer
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


@timer
def get_locations_metrics(metrics, start_date, end_date):
    locations_list = get_locations_list()

    metrics_list = []
    for metric in metrics:
        metrics_list.append({
            "metric": metric,
            "options": [
                "AGGREGATED_DAILY"
            ]
        }, )

    my_headers = {'Authorization': 'Bearer {0}'.format(get_token())}
    my_json = {
                "locationNames": [],
                "basicRequest": {
                    "metricRequests": metrics_list,
                    "timeRange": {
                        "startTime": start_date + "T00:00:00Z",  # format : AAAA-MM-JJ
                        "endTime": end_date + "T00:00:00Z"  # format : AAAA-MM-JJ
                    }
                }
            }

    res = []
    location_id_list = []
    i = 0
    for loc_id in locations_list:
        location_id_list.append("accounts/" + account_id + "/locations/" + loc_id)
        i += 1

        if i%10 == 0 or i == len(locations_list):
            my_json['locationNames'] = location_id_list

            response = requests.post('https://mybusiness.googleapis.com/v4/accounts/112578893942190553010/locations:reportInsights',
                                     headers=my_headers,
                                     json=my_json
                                    )

            res.append(response.json())

            location_id_list = []

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


@timer
def create_dataframe(data):  # data from get_location_metrics()
    df = pd.DataFrame(columns=['DATE', 'LOCATION_ID', 'METRIC', 'VALUE'])

    for location in data:
        for i in range(len(location['locationMetrics'])):
            try:
                location_id = location['locationMetrics'][i]['locationName'].split('/')[-1]
                for metric in location['locationMetrics'][i]['metricValues']:
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
            except KeyError:
                pass

    return df
