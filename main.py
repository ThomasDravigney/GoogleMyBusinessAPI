# Google client library Quickstart : https://developers.google.com/people/quickstart/python
# Building and calling a service : https://googleapis.github.io/google-api-python-client/docs/start.html => N/A
# Building API requests with python : https://www.nylas.com/blog/use-python-requests-module-rest-apis/
# Google My Business API methods : https://developers.google.com/my-business/reference/rest?hl=fr
# Google My Business, location metrics : https://developers.google.com/my-business/reference/rest/v4/Metric?hl=fr

import pandas as pd
from functions import get_locations_metrics, save_local_data, get_local_data, clear_local_data, create_dataframe, timer
from datetime import date
from datetime import timedelta


metrics = ["ALL"]
start_date = date.isoformat(date.today() - timedelta(days=3))
end_date = date.isoformat(date.today() - timedelta(days=2))


@timer
def main():
    try:
        data = get_local_data()
        df = create_dataframe(data)
        print(df)
        df.to_csv(r'C:\Users\dravi\Downloads\GMB_STATISTICS_{0}_{1}.csv'.format(start_date, end_date), index=False)

    except (FileNotFoundError, UnboundLocalError):
        save_local_data(get_locations_metrics(metrics, start_date, end_date))
        print('local_data file has been created. Rerun to get expected result.')


if __name__ == '__main__':
    main()
