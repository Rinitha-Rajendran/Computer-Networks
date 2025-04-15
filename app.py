from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import socket
import time
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

HOST = '192.168.169.243'
PORT = 1234
SCREENSHOT_PATH = 'screenshot.png'

def receive_image(client_socket, file_path):
    """Receives an image file in chunks and saves it to the specified path."""
    with open(file_path, 'wb') as f:
        while True:
            data = client_socket.recv(4096)  # Receiving in 4 KB chunks
            if not data:
                break
            f.write(data)
    return "Screenshot saved successfully."

def send_socket_request(url, option, email=None):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
        # Prepare the message format for the server
        if option == '3' and email:
            message = f"{url}|{option}|{email}"
        else:
            message = f"{url}|{option}"
        client.sendall(message.encode('utf-8'))
        
        # For screenshot option, receive and save the screenshot file
        if option == '2':
            result = receive_image(client, SCREENSHOT_PATH)
            return result
        else:
            response = client.recv(1024)
            return response.decode('utf-8')

    except socket.error as e:
        return f"Error: {str(e)}"
    finally:
        client.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    url = request.form['url']
    option = request.form['option']
    email = request.form.get('email', '')

    if option == '3' and not email:
        flash("Email is required for option 3!")
        return redirect(url_for('index'))

    result = send_socket_request(url, option, email)
    flash(result)

    # For option 2, redirect to display the screenshot after processing
    if option == '2' and os.path.exists(SCREENSHOT_PATH):
        return redirect(url_for('display_screenshot'))

    return redirect(url_for('index'))

@app.route('/screenshot')
def display_screenshot():
    # Check if screenshot exists before displaying it
    if os.path.exists(SCREENSHOT_PATH):
        return send_file(SCREENSHOT_PATH, mimetype='image/png')
    else:
        flash("Screenshot not available.")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)