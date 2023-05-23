from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Step 6: Resource server receives a request with an access token and validates it
@app.route('/resource', methods=['GET'])
def resource():
    """
    Endpoint that handles resource requests.

    Retrieves the access token from the request headers and validates it.
    If the token is valid, returns the requested resources.
    Otherwise, returns an error response.

    Returns:
        JSON response containing the requested resources or an error message.
    """
    access_token = request.headers.get('Authorization').split(' ')[1]

    # Validate the access token
    if validate_access_token(access_token):
        # Step 7: The resource server sends resources to the client
        return jsonify({'resources': ['youssef', 'essam']}), 200
    else:
        return jsonify({'error': 'Invalid token'}), 401


def validate_access_token(access_token):
    """
    Validates the access token by sending a request to the OAuth server.

    Args:
        access_token (str): The access token to validate.

    Returns:
        bool: True if the access token is valid, False otherwise.
    """
    # Send a request to the OAuth server to validate the access token
    oauth_server_url = 'http://localhost:8000/validate_token'  # Replace with the actual OAuth server URL
    response = requests.post(oauth_server_url, json={'access_token': access_token})

    if response.status_code == 200:
        return True
    else:
        return False


if __name__ == '__main__':
    app.run(port=5000)



