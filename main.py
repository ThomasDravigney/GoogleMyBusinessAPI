# Google client library Quickstart : https://developers.google.com/people/quickstart/python
# Building and calling a service : https://googleapis.github.io/google-api-python-client/docs/start.html => N/A
# Building API requests with python : https://www.nylas.com/blog/use-python-requests-module-rest-apis/
# Google My Business API methods : https://developers.google.com/my-business/reference/rest?hl=fr
# Google My Business, location metrics : https://developers.google.com/my-business/reference/rest/v4/Metric?hl=fr


from functions import get_location_metrics, save_local_data, get_local_data, clear_local_data, create_dataframe


def main():
    #save_local_data(get_location_metrics())
    data = get_local_data()

    print(create_dataframe(data))


if __name__ == '__main__':
    main()
