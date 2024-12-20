from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
# Allow CORS for all domains on all routes
CORS(app, resources={r"/*": {"origins": os.getenv('CORS_ORIGIN')}})


@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify(message="Hello from Flask!")


@app.route('/api/companies', methods=['GET'])
def get_companies():
    # Define the API endpoint
    url = os.getenv('AT_BASE_URL') + "/Companies/query"

    # Define the query parameters
    params = {
        "search": '{ "filter":[{"op" : "exist", "field" : "id" }]}'
    }

    # Define the headers
    headers = {
        "ApiIntegrationCode": os.getenv('AT_API_INTEGRATION_CODE'),
        "UserName": os.getenv('AT_USERNAME'),
        "Secret": os.getenv('AT_SECRET'),
        "Content-Type": "application/json"
    }

    try:
        # Make the GET request
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Return the JSON response
        fullData = response.json()['items']
        data = [
            {
                'id': item['id'],
                'companyName': item['companyName'],
                'phone': item['phone'],
                'webAddress': item['webAddress'],
                'isActive': item['isActive'],
                'city': item['city']
            }
            for item in fullData
        ]
        return jsonify(data)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/tickets', methods=['POST'])
def create_ticket():
    # Get the request data
    ticket_data = request.get_json()

    # Define the API endpoint for ticket creation
    url = os.getenv('AT_BASE_URL') + "/Tickets"

    # Define the headers
    headers = {
        "ApiIntegrationCode": os.getenv('AT_API_INTEGRATION_CODE'),
        "UserName": os.getenv('AT_USERNAME'),
        "Secret": os.getenv('AT_SECRET'),
        "Content-Type": "application/json"
    }

    email_mapping = {
        "flyonit.com.au": 0,
    }

    email = ticket_data.get('email').split('@')[1]
    title = ticket_data.get('title')
    description = ticket_data.get('description')
    company_id = email_mapping.get(
        email, None)

    # Prepare the ticket payload
    ticket_payload = {
        "companyID": company_id,
        "QueueID": 5,
        "dueDateTime": "2024-12-31T23:59:59",
        "priority": 2,
        "status": 1,
        "title": title,
        "description": description
    }

    try:
        # Make the POST request
        response = requests.post(url, headers=headers, json=ticket_payload)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Return the created ticket data
        return jsonify(response.json()), 201

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/company/<int:company_id>/tickets', methods=['GET'])
def get_tickets(company_id):
    # Define the API endpoint for ticket query
    url = os.getenv('AT_BASE_URL') + "/Tickets/query"
    params = {
        "search": '{ "filter":[{"op" : "noteq", "field" : "Status", "value": 5},{"op" : "eq", "field" : "CompanyID", "value": ' + str(company_id) + '}]}'
    }

    # Define the headers
    headers = {
        "ApiIntegrationCode": os.getenv('AT_API_INTEGRATION_CODE'),
        "UserName": os.getenv('AT_USERNAME'),
        "Secret": os.getenv('AT_SECRET'),
        "Content-Type": "application/json"
    }

    try:
        # Make the GET request
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Return the JSON response
        fullData = response.json()['items']
        data = [
            {
                'id': item['id'],
                'title': item['title'],
                'status': item['status'],
                'priority': item['priority'],
                'description': item['description'],
                'createDate': item['createDate'],
                'dueDateTime': item['dueDateTime'],
                'ticketNumber': item['ticketNumber']
            }
            for item in fullData
        ]
        return jsonify(data)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
