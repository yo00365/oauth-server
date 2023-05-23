import requests

"""
The 'requests' module allows sending HTTP requests in Python.
It provides convenient methods for making GET, POST, PUT, DELETE, and other HTTP requests.
"""

def request_token(client_id, client_secret, redirect_uri, authorization_code):
    """
    Requests an access token from the OAuth server using the provided parameters.

    Args:
        client_id (str): The client ID for authentication.
        client_secret (str): The client secret for authentication.
        redirect_uri (str): The redirect URI for handling the authorization callback.
        authorization_code (str): The authorization code obtained from the user.

    Returns:
        tuple: A tuple containing the access token (str), token type (str), and expires in (str).
               If the request fails, returns (None, None, None).
    """

    token_endpoint = 'http://localhost:8000/token'
    token_params = {
        'code': authorization_code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri
    }
    response = requests.post(token_endpoint, data=token_params)

    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get('access_token')
        token_type = token_data.get('token_type')
        expires_in = token_data.get('expires_in')
        return access_token, token_type, expires_in
    else:
        return None, None, None

def get_resources(access_token):
    """
    Retrieves resources from a resource server using the provided access token.

    Args:
        access_token (str): The access token for authorization.

    Returns:
        dict or None: The JSON response from the resource server if the request is successful.
                      Returns None if the request fails.
    """

    resource_server_url = 'http://localhost:5000/resource'
    headers = {'Authorization': 'Bearer ' + access_token}
    resource_response = requests.get(resource_server_url, headers=headers)

    if resource_response.status_code == 200:
        return resource_response.json()
    else:
        return None

def request_oauth_token():
    """
    Requests an OAuth token using the client ID, client secret, and redirect URI.

    This function represents the main flow of the OAuth authentication process.

    Steps:
    1. Redirect the user to the authorization endpoint.
    2. Receive the authorization code from the callback URL.
    3. Exchange the authorization code for an access token.
    4. OAuth sends the access token to the client.
    5. The client sends the token and requests resources from the resource server.
    6. The resource server sends resources to the client.

    Returns:
        None
    """

    client_id = 'your_client_id'
    client_secret = 'your_client_secret'
    redirect_uri = 'http://localhost:8000/callback'
    authorization_endpoint = 'http://localhost:8000/authorize'

    # Redirect the user to the authorization endpoint
    authorization_url = 'http://localhost:8000/authorize?response_type=code&client_id=your_client_id&redirect_uri=http://localhost:8000/callback'
    print("Please visit the following URL and provide consent:")
    print(authorization_url)

    # Receive the authorization code from the callback URL
    authorization_code = input("Enter the authorization code: ")

    # Exchange the authorization code for an access token
    access_token, token_type, expires_in = request_token(client_id, client_secret, redirect_uri, authorization_code)

    if access_token is not None:
        # Step 4: OAuth sends the access token to the client
        print("Access token:", access_token)

        # Step 5: The client sends the token and requests resources from the resource server
        resources = get_resources(access_token)

        if resources is not None:
            # Step 7: The resource server sends resources to the client
            print("Resources:")
            print(resources)
        else:
            print("Error accessing resources")
    else:
        print("Error requesting access token")

# Execute the main function
request_oauth_token()



