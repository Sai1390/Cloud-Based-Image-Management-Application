from flask import Flask, render_template, request, redirect, send_file
import boto3
from cryptography.fernet import Fernet
import io

app = Flask(__name__)

# Initialize S3 client with correct region and signature version
s3 = boto3.client(
    's3',
    region_name='eu-north-1',  # Use your actual region
    config=boto3.session.Config(signature_version='s3v4')
)

BUCKET_NAME = 'my-image-management-bucket'  # Replace with your S3 bucket name

# Route for displaying the upload form and uploading images
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    
    # Check if the user wants to encrypt the image
    if 'encrypt' in request.form:
        file_data = file.read()  # Read the file data
        encryption_key = Fernet.generate_key()  # Generate a new key for each file
        cipher = Fernet(encryption_key)
        encrypted_data = cipher.encrypt(file_data)  # Encrypt the data
        s3.put_object(Bucket=BUCKET_NAME, Key=file.filename + '.encrypted', Body=encrypted_data)

        # Display the encryption key to the user
        return f"Image encrypted and uploaded successfully! Use this key to decrypt: {encryption_key.decode()}"
    else:
        s3.upload_fileobj(file, BUCKET_NAME, file.filename)
        return 'Image uploaded successfully!'

# Route for listing images stored in the S3 bucket
@app.route('/list', methods=['GET'])
def list_images():
    objects = s3.list_objects_v2(Bucket=BUCKET_NAME)

    files = []
    if 'Contents' in objects:
        for obj in objects['Contents']:
            if 'encrypted' in request.args and request.args['encrypted'] == 'on':
                if obj['Key'].endswith('.encrypted'):  # Filter encrypted files
                    files.append(obj['Key'])
            else:
                files.append(obj['Key'])
                
    return render_template('list.html', files=files)

# Route for downloading an image
@app.route('/download/<filename>')
def download_image(filename):
    # Generate a presigned URL to download the file from S3
    file_url = s3.generate_presigned_url('get_object',
                                         Params={'Bucket': BUCKET_NAME, 'Key': filename},
                                         ExpiresIn=3600)  # Link valid for 1 hour
    return redirect(file_url)

# Route for decrypting and downloading an encrypted image
@app.route('/decrypt/<filename>', methods=['GET', 'POST'])
def decrypt_image(filename):
    if request.method == 'POST':
        key = request.form['key']  # Get the decryption key from user input

        # Download the encrypted file from S3
        response = s3.get_object(Bucket=BUCKET_NAME, Key=filename)
        encrypted_data = response['Body'].read()

        # Decrypt the file using the provided key
        try:
            cipher = Fernet(key.encode())
            decrypted_data = cipher.decrypt(encrypted_data)
        except Exception as e:
            return f"Decryption failed: {str(e)}"

        # Serve the decrypted file to the user without storing it on the server
        return send_file(
            io.BytesIO(decrypted_data),
            as_attachment=True,
            download_name=filename.replace('.encrypted', '')  # Replaced attachment_filename with download_name
        )

    # If GET, show a form for key input
    return '''
    <form method="POST">
        <label for="key">Enter decryption key:</label><br>
        <input type="text" id="key" name="key" required><br><br>
        <button type="submit">Decrypt and Download</button>
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
