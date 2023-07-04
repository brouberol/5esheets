def assert_status_and_return_data(client_method, url, status_code, *args, **kwargs):
    response = client_method(url, *args, **kwargs)
    assert (
        response.status_code == status_code
    ), f"Expected: {status_code}, got: {response.status_code}"
    return response.json()
