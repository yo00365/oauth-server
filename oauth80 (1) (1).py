from flask import Flask, jsonify, request
import secrets
import string

app = Flask(__name__)

# Store authorization codes
stored_authorization_codes = {}

# Store access tokens
stored_access_tokens = {}

# Step 2: OAuth verifies the client
@app.route('/authorize', methods=['GET'])
def authorize():
    """
    Step 2: OAuth verifies the client.

    Verifies the client ID and displays a consent page to the user.

    Returns:
        str: The HTML content of the consent page.

    Raises:
        None
    """
    client_id = request.args.get('client_id')

    # Verify the client
    if client_id == 'your_client_id':
        # Step 3: User consent
        return '''
        <html>
        <head>
            <title>Consent page</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                }}
                h1 {{
                    color: #333;
                }}
                .container {{
                    max-width: 400px;
                    margin: 0 auto;
                    padding: 20px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    background-color: #f9f9f9;
                }}
                .btn {{
                    display: inline-block;
                    padding: 8px 16px;
                    font-size: 14px;
                    font-weight: bold;
                    text-decoration: none;
                    color: #fff;
                    background-color: #007bff;
                    border-radius: 5px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Consent page</h1>
                <p>Click the "Verify" button to authorize.</p>
                <form action="/callback" method="post">
                    <input type="hidden" name="client_id" value="{0}">
                    <input class="btn" type="submit" value="Verify">
                </form>
            </div>
        </body>
        </html>
        '''.format(client_id)
    else:
        return jsonify({'error': 'Invalid client'}), 401

# Step 4: Handle callback and provide authorization code
@app.route('/callback', methods=['POST'])
def callback():
    """
    Step 4: Handle callback and provide authorization code.

    Generates an authorization code and stores it for the client.

    Returns:
        str: The HTML content displaying the authorization code.

    Raises:
        None
    """
    client_id = request.form.get('client_id')

    # Generate authorization code
    authorization_code = generate_authorization_code()

    # Store authorization code
    stored_authorization_codes[client_id] = authorization_code

    return '''
    <html>
    <head>
        <title>Authorization Code</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
            }}
            h1 {{
                color: #333;
            }}
            .container {{
                max-width: 400px;
                margin: 0 auto;
                padding: 20px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #f9f9f9;
            }}
            .code-label {{
                font-size: 16px;
                margin-bottom: 10px;
            }}
            .code-value {{
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
                background-color: #f1f1f1;
                border-radius: 5px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Authorization Code</h1>
            <p>Your authorization code is:</p>
            <div class="code-value">{0}</div>
        </div>
    </body>
    </html>
    '''.format(authorization_code)

# Step 6: Exchange authorization code for access token
@app.route('/token', methods=['POST'])
def exchange_token():
    """
    Step 6: Exchange authorization code for access token.

    Exchanges the authorization code for an access token.

    Returns:
        dict: The access token response as a JSON object.

    Raises:
        None
    """
    authorization_code = request.form.get('code')
    client_id = request.form.get('client_id')
    client_secret = request.form.get('client_secret')

    if client_id != 'your_client_id' or client_secret != 'your_client_secret':
        return jsonify({'error': 'Invalid client credentials'}), 401

    stored_auth_code = stored_authorization_codes.get(client_id)
    if stored_auth_code != authorization_code:
        return jsonify({'error': 'Invalid authorization code'}), 400

    def generate_access_token(length=32):
        """
        Generates an access token.

        Args:
            length (int, optional): The length of the access token. Defaults to 32.

        Returns:
            str: The generated access token.

        Raises:
            None
        """
        # Define the characters that can be used in the token
        characters = string.ascii_letters + string.digits

        # Generate a random string of characters
        token = ''.join(secrets.choice(characters) for _ in range(length))

        return token

    def generate_token_response():
        """
        Generates the access token response.

        Generates an access token, stores it, and constructs the response.

        Returns:
            dict: The access token response as a JSON object.

        Raises:
            None
        """
        access_token = generate_access_token()
        token_type = 'bearer'
        expires_in = 3600

        # Store access token
        stored_access_tokens[access_token] = {
            'client_id': client_id,
            'expires_in': expires_in
        }

        return jsonify({'access_token': access_token, 'token_type': token_type, 'expires_in': expires_in})

    # Generate and return access token response
    response = generate_token_response()
    return response

# New endpoint to validate access token
@app.route('/validate_token', methods=['POST'])
def validate_token():
    """
    Validates an access token.

    Validates whether the provided access token is valid.

    Returns:
        dict: The validation status as a JSON object.

    Raises:
        None
    """
    access_token = request.json.get('access_token')

    if access_token in stored_access_tokens:
        return jsonify({'status': 'valid'}), 200
    else:
        return jsonify({'status': 'invalid'}), 401


def generate_authorization_code(length=16):
    """
    Generates an authorization code.

    Args:
        length (int, optional): The length of the authorization code. Defaults to 16.

    Returns:
        str: The generated authorization code.

    Raises:
        None
    """
    # Define the characters that can be used in the code
    characters = string.ascii_letters + string.digits

    # Generate a random string of characters
    code = ''.join(secrets.choice(characters) for _ in range(length))

    return code

if __name__ == '__main__':
    app.run(port=8000)


