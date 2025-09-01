# Grafana Alert Webhook → SMS Notifier

This project provides a simple Flask-based webhook that listens for Grafana alert notifications, processes the alert data, matches it with services, and sends SMS alerts using an external SMS gateway API.

### 📌 Features

*   Receives Grafana alert webhooks on a custom endpoint.
*   Extracts: IP addresses of affected nodes, service names from a `servers.txt` file, and alert values (threshold breaches).
*   Formats and maps alerts into human-readable messages.
*   Sends alerts via HTTP API calls to predefined phone numbers.

### 📂 Directory Structure

Use code with caution.

grafana-alert-webhook/
├── app.py # Main Flask application (the webhook logic)
├── servers.txt # File containing IP → Service name mappings
├── requirements.txt # Python dependencies
├── README.md # Documentation

### 📜 Example `servers.txt`

Each line contains: `<ip>,<service_name>`

Example:
*.*.*.157,Database
*.*.*.170,Web Server
*.*.*.180,Application Server

### ⚙️ Installation

1.  Clone this repository
    ```sh
    git clone https://github.com/<your-username>/grafana-alert-webhook.git
    cd grafana-alert-webhook
    ```
2.  Install dependencies
    ```sh
    pip install -r requirements.txt
    ```
3.  Run the Flask app
    ```sh
    python app.py
    ```
    By default, the app runs on `http://localhost:5000`.

### 📡 Grafana Configuration

1.  Go to Grafana → Alerting → Contact Points.
2.  Add a new **Webhook** contact point:
    *   **URL:** `http://<your-server-ip>:5000/sendsms?number=<your-phone-number>`
    *   **Method:** `POST`
    *   **Send Full JSON Alert.**
3.  Add this contact point to your notification policies.

### 📥 Example Alert Flow

Grafana sends webhook → Flask app receives → Parses alert → Looks up IP in `servers.txt` → Builds SMS → Sends via API.

Example message sent via SMS:
Grafana_Alert High CPU Usage
*.*.*.157 "Database" is 95

### 📤 SMS Gateway

This webhook integrates with an HTTP SMS API (Kannel in this example):
`http://<sms-gateway>:13013/cgi-bin/sendsms?username=USER&password=PASS&from=5188&to=<MSISDN>&text=<ALERT_MESSAGE>&MT&charset=utf-8`

You can update the `noc` list in `app.py` with your desired phone numbers.

### 🔒 Security Notes

*   Restrict access to the Flask port (e.g., firewall to allow only Grafana).
*   Don’t hardcode SMS credentials in code for production.
*   Run Flask with a production server like `gunicorn` or behind `nginx`.

### 🚀 To-Do

*   Dockerize the webhook.
*   Add retry logic if SMS gateway fails.
*   Add logging & monitoring of SMS sends.