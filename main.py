# Google client library Quickstart : https://developers.google.com/people/quickstart/python
# Building and calling a service : https://googleapis.github.io/google-api-python-client/docs/start.html => N/A
# Building API requests with python : https://www.nylas.com/blog/use-python-requests-module-rest-apis/
# Google My Business API methods : https://developers.google.com/my-business/reference/rest?hl=fr
# Google My Business, location metrics : https://developers.google.com/my-business/reference/rest/v4/Metric?hl=fr


from functions import get_location_metrics
import pandas as pd


def main():
    df = pd.DataFrame(columns=['DATE', 'LOCATION_ID', 'METRIC', 'VALUE'])

    for location in get_location_metrics()['locationMetrics']:
        x, y, z, location_id = location['locationName'].split('/')
        for metric in location['metricValues']:
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

    print(df)


if __name__ == '__main__':
    main()
