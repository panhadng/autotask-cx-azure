# Autotask API Integration Server

This is a Flask-based REST API server that integrates with the Autotask API to manage tickets and company information.

## Setup

1. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

2. Install required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Fill in your Autotask API credentials and other configuration values
   ```bash
   cp .env.example .env
   ```

## Running the Server

1. Start the server:
   ```bash
   gunicorn --config gunicorn.conf.py app:app
   ```
   The server will start on `http://localhost:8000` by default.

## API Endpoints

### Tickets

- `GET /api/tickets` - Get all tickets
- `GET /api/tickets/<ticket_id>` - Get specific ticket
- `POST /api/tickets` - Create new ticket
- `PUT /api/tickets/<ticket_id>` - Update ticket
- `DELETE /api/tickets/<ticket_id>` - Delete ticket

### Companies

- `GET /api/companies` - Get all companies
- `GET /api/companies/<company_id>` - Get specific company
