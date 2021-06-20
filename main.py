# Google client library Quickstart : https://developers.google.com/people/quickstart/python
# Building and calling a service : https://googleapis.github.io/google-api-python-client/docs/start.html => N/A
# Building API requests with python : https://www.nylas.com/blog/use-python-requests-module-rest-apis/
# Google My Business API methods : https://developers.google.com/my-business/reference/rest?hl=fr
# Google My Business, location metrics : https://developers.google.com/my-business/reference/rest/v4/Metric?hl=fr


from functions import get_location_metrics, save_local_data, get_local_data, clear_local_data, create_dataframe, timer


@timer
def main():
    try:
        data = get_local_data()
        print(data)
    except (FileNotFoundError, UnboundLocalError):
        save_local_data(get_location_metrics())
        print('local_data file has been created. Rerun to get expected result.')

    # df.to_csv(r'C:\Users\dravi\Downloads\data gmb.csv', index=False)


if __name__ == '__main__':
    main()
