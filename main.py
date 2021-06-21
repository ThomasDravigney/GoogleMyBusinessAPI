# Google client library Quickstart : https://developers.google.com/people/quickstart/python
# Building and calling a service : https://googleapis.github.io/google-api-python-client/docs/start.html => N/A
# Building API requests with python : https://www.nylas.com/blog/use-python-requests-module-rest-apis/
# Google My Business API methods : https://developers.google.com/my-business/reference/rest?hl=fr
# Google My Business, location metrics : https://developers.google.com/my-business/reference/rest/v4/Metric?hl=fr


from functions import get_location_metrics, save_local_data, get_local_data, clear_local_data, create_dataframe, timer


metrics = ["QUERIES_DIRECT", "QUERIES_INDIRECT"]
start_date = '2021-06-17'
end_date = '2021-06-18'


@timer
def main():
    try:
        data = get_local_data()
        df = create_dataframe(data)
        print(df)
    except (FileNotFoundError, UnboundLocalError):
        save_local_data(get_location_metrics(metrics, start_date, end_date))
        print('local_data file has been created. Rerun to get expected result.')

    # df.to_csv(r'C:\Users\dravi\Downloads\data gmb.csv', index=False)


if __name__ == '__main__':
    main()
