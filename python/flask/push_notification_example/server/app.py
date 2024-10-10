from flask import Flask, request, Response, render_template
import time
from pywebpush import webpush, WebPushException

app = Flask(__name__)

# Dummy subscription info for push notifications
subscription_info = {
    "endpoint": "https://example.com/...",
    "keys": {
        "p256dh": "public_key",
        "auth": "auth_key"
    }
}

# Global variable to hold received webhook data
received_data = []

@app.route('/')
def index():
    return render_template('index.html', data=received_data)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Received data:", data)
    received_data.append(data)  # Store received data. Consider: clear received_data. 
    return 'OK', 200

@app.route('/stream')
def stream():
    def event_stream():
        while True:
            time.sleep(1)
            yield f"data: The current time is {time.ctime()}\n\n"
            if received_data:  # Send webhook data if available
                for data in received_data:
                    yield f"data: Event: {data['event']}, Details: {data['details']}, Timestamp: {data['timestamp']}\n\n"
    return Response(event_stream(), mimetype="text/event-stream")

def send_push_notification(subscription_info, message):
    try:
        response = webpush(
            subscription_info=subscription_info,
            data=message,
            vapid_private_key="private_key.pem",
            vapid_claims={"sub": "mailto:you@example.com"}
        )
        return response
    except WebPushException as ex:
        print("Failed to send push notification: {}", repr(ex))

if __name__ == '__main__':
    app.run(port=5000, debug=True)
