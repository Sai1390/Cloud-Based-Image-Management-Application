# Cloud-Based-Image-Management-Application

A cloud-based Image Management Application using Python (Flask) and AWS. Users can upload images to an S3 bucket, with optional encryption. The app allows listing, downloading, and decrypting images. It is hosted on an EC2 instance and uses Boto3 for AWS services and Fernet for encryption.

---

## Overview
This project is a cloud-based Image Management Application built using **Python** and **Amazon Web Services (AWS)**. The application allows users to:
- Upload images to an **S3 bucket**.
- Optionally **encrypt** images before uploading.
- View a list of uploaded images.
- Download images, including decrypting encrypted images.
- Decrypt and download encrypted images using a provided decryption key.

The project is hosted on an **AWS EC2 instance** and interacts with **AWS S3** for image storage.

## Features
- **Image Upload**: Users can upload images via the web interface.
- **Optional Encryption**: Images can be encrypted before uploading, using the **Fernet** encryption method.
- **List Images**: Users can view a list of images stored in the S3 bucket.
- **Download**: Images can be downloaded from the S3 bucket, including a decrypt option for encrypted images.
- **Decryption**: Users can input the encryption key to decrypt images before downloading.

## Architecture
The application is built using:
- **Python** (Flask framework)
- **Amazon S3** for image storage
- **Amazon EC2** for hosting
- **Boto3** for interaction with AWS services
- **Cryptography** library for encryption and decryption

## Setup and Installation

### Prerequisites
- An AWS account with permissions to create and manage S3 buckets and EC2 instances.
- **Python 3.x** installed on your local machine.
- The following Python libraries:
  - Flask
  - Boto3
  - Cryptography

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   ```

2. **Install Dependencies**:
   Install the required Python libraries:
   - Flask
  - Boto3
  - Cryptography

3. **AWS Configuration**:
   - Set up an **S3 bucket** to store images.
   - Launch an **EC2 instance** and configure it to allow HTTP/HTTPS traffic.
   - Ensure your EC2 instance has the necessary **IAM roles** for accessing the S3 bucket.

4. **Run the Application**:
   Start the Flask application by connecting to your EC2 instance:
   ```bash
   ssh -i "D:\Commvault\Commvault.pem" ec2-user@ec2-13-60-222-86.eu-north-1.compute.amazonaws.com
   ```
   Once connected, navigate to the project directory and run:
   ```bash
   python3 app.py
   ```

5. **Access the Application**:
   - The application is now running on your EC2 instance and can be accessed via the EC2 public IP:
     ```
     http://ec2-13-60-222-86.eu-north-1.compute.amazonaws.com:5000
     ```

## How to Use

### 1. Upload Images
- Navigate to the **Upload Images** page.
- Select an image to upload and choose whether to encrypt it by checking the "Encrypt images while uploading" checkbox.
- Upon successful upload, the encryption key will be displayed if the image was encrypted. Save this key to decrypt the image later.

### 2. List and Download Images
- Navigate to the **List of Images** page.
- You can view all uploaded images and filter by encrypted images using the "Show only encrypted images" checkbox.
- You can download any image directly or use the **"Decrypt and Download"** option for encrypted images.

### 3. Decrypting Images
- For encrypted images, click **"Decrypt and Download"**.
- Enter the encryption key that was provided during the upload process to decrypt the image.

## Security Considerations
- **Encryption Key Management**: For testing, encryption keys are displayed to the user after upload. In a real-world scenario, keys should be securely stored in a key management service like **AWS KMS** or **AWS Secrets Manager**.
- **HTTPS**: Use HTTPS in production environments to secure communication between users and the server.

## Future Improvements
- Implement **user authentication** with login and signup functionalities.
- Store encryption keys securely using a key management service.
- Use HTTPS for secure communication.
