# app.py
from flask import Flask, request, jsonify, send_from_directory
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)

# Replace with your AWS credentials and bucket information
AWS_ACCESS_KEY_ID = 'AKIA5FTZCPHEM6Z5BLVI'
AWS_SECRET_ACCESS_KEY = 'tQHNVgC0dATjKWCzHlZaDHg5Aoa/SYDDHzD8P1sO'
BUCKET_NAME = 'django-static-1335'

s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

@app.route('/')
def index():
    return open('index.html').read()

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    try:
        s3.upload_fileobj(file, BUCKET_NAME, file.filename, ExtraArgs={'ACL': 'public-read'})
        return jsonify({'message': 'File uploaded successfully'})
    except ClientError as e:
        return jsonify({'error': e.response['Error']['Message']}), 500

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)
