import requests

def register_user(api_url, username, email, stock_id, invitation_code, phone_number=None):
    """
    Registers a user with the given details.

    :param api_url: The base URL of the registration API (e.g., http://localhost:8000/register).
    :param username: The username of the user.
    :param email: The email of the user.
    :param stock_id: The stock ID the user is interested in.
    :param invitation_code: The invitation code for registration.
    :param phone_number: (Optional) The phone number of the user.
    :return: The response from the server.
    """
    payload = {
        "username": username,
        "email": email,
        "phone_number": phone_number,
        "stock_id": stock_id,
        "invitation_code": invitation_code,
    }

    try:
        # Send the POST request
        response = requests.post(api_url, json=payload)

        # Check the response status
        if response.status_code == 201:
            return {"success": True, "message": "Registration successful."}
        else:
            return {"success": False, "message": response.json().get("error", "Unknown error.")}
    except requests.exceptions.RequestException as e:
        return {"success": False, "message": f"Request failed: {str(e)}"}

if __name__ == "__main__":
    # Example usage
    API_URL = "http://localhost:8000/register"
    
    # Replace with actual values
    username = "JohnDoe"
    email = "johndoe@example.com"
    stock_id = "AAPL"
    invitation_code = "INV12345"
    phone_number = "1234567890"  # Optional
    
    # Register the user
    result = register_user(API_URL, username, email, stock_id, invitation_code, phone_number)
    print(result)
