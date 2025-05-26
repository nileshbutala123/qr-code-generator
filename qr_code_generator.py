#!/usr/bin/env python3

import qrcode
import os
import sys
import webbrowser
import base64
import uuid
import json
import subprocess
from io import BytesIO
from datetime import datetime

# AWS S3 imports - boto3 will be installed if not present
try:
    import boto3
    from botocore.exceptions import ClientError
except ImportError:
    boto3 = None

class QRCodeGenerator:
    def __init__(self):
        self.output_dir = os.path.dirname(os.path.abspath(__file__))
        self.s3_client = None
        self.s3_bucket = None

    def configure_aws(self, bucket_name, region='us-east-1',
                     aws_access_key=None, aws_secret_key=None):
        """
        Configure AWS credentials and S3 bucket for deployment

        Args:
            bucket_name (str): Name of the S3 bucket
            region (str): AWS region
            aws_access_key (str, optional): AWS access key
            aws_secret_key (str, optional): AWS secret key

        Returns:
            bool: True if configuration successful, False otherwise
        """
        # Ensure boto3 is installed
        if boto3 is None:
            print("Installing AWS SDK (boto3)...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "boto3"])
                import boto3
                from botocore.exceptions import ClientError
                print("AWS SDK (boto3) installed successfully!")
            except Exception as e:
                print(f"Error installing boto3: {e}")
                return False

        try:
            # Initialize S3 client
            if aws_access_key and aws_secret_key:
                self.s3_client = boto3.client(
                    's3',
                    region_name=region,
                    aws_access_key_id=aws_access_key,
                    aws_secret_access_key=aws_secret_key
                )
            else:
                # Use credentials from ~/.aws/credentials or environment variables
                self.s3_client = boto3.client('s3', region_name=region)

            # Check if bucket exists, create if it doesn't
            self.s3_bucket = bucket_name
            self._ensure_bucket_exists(region)

            # Set bucket website configuration
            self._configure_bucket_website()

            print(f"AWS S3 configured successfully with bucket: {bucket_name}")
            return True

        except Exception as e:
            print(f"Error configuring AWS: {e}")
            return False

    def _ensure_bucket_exists(self, region):
        """Create the S3 bucket if it doesn't exist"""
        try:
            self.s3_client.head_bucket(Bucket=self.s3_bucket)
            print(f"S3 bucket '{self.s3_bucket}' already exists")
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':
                # Bucket doesn't exist, create it
                if region == 'us-east-1':
                    self.s3_client.create_bucket(Bucket=self.s3_bucket)
                else:
                    location = {'LocationConstraint': region}
                    self.s3_client.create_bucket(
                        Bucket=self.s3_bucket,
                        CreateBucketConfiguration=location
                    )
                print(f"Created S3 bucket: {self.s3_bucket}")

                # Set bucket public access policy
                self.s3_client.put_public_access_block(
                    Bucket=self.s3_bucket,
                    PublicAccessBlockConfiguration={
                        'BlockPublicAcls': False,
                        'IgnorePublicAcls': False,
                        'BlockPublicPolicy': False,
                        'RestrictPublicBuckets': False
                    }
                )

                # Create bucket policy for public read access
                bucket_policy = {
                    'Version': '2012-10-17',
                    'Statement': [{
                        'Sid': 'PublicReadGetObject',
                        'Effect': 'Allow',
                        'Principal': '*',
                        'Action': ['s3:GetObject'],
                        'Resource': [f'arn:aws:s3:::{self.s3_bucket}/*']
                    }]
                }

                # Apply the bucket policy
                self.s3_client.put_bucket_policy(
                    Bucket=self.s3_bucket,
                    Policy=json.dumps(bucket_policy)
                )
            else:
                # Some other error occurred
                raise

    def _configure_bucket_website(self):
        """Configure the S3 bucket for static website hosting"""
        try:
            self.s3_client.put_bucket_website(
                Bucket=self.s3_bucket,
                WebsiteConfiguration={
                    'ErrorDocument': {'Key': 'error.html'},
                    'IndexDocument': {'Suffix': 'index.html'},
                }
            )
            print(f"Configured S3 bucket for static website hosting")
        except Exception as e:
            print(f"Error configuring bucket for website hosting: {e}")

    def generate(self, url, output_file=None, deploy_to_s3=False):
        """
        Generate a QR code for the given URL

        Args:
            url (str): The URL to encode in the QR code
            output_file (str, optional): The filename to save the QR code
            deploy_to_s3 (bool): Whether to deploy to S3

        Returns:
            str: The path to the generated QR code file or S3 URL
        """
        # Validate URL
        if not url:
            raise ValueError("URL cannot be empty")

        # Add https:// prefix if needed
        if not (url.startswith('http://') or url.startswith('https://')):
            url = 'https://' + url
            print(f"Added https:// prefix. URL is now: {url}")

        # Generate filename if not provided
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"qrcode_{timestamp}.png"
        elif not output_file.lower().endswith('.png'):
            output_file += '.png'

        # Create full path
        output_path = os.path.join(self.output_dir, output_file)

        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        # Create image and save
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(output_path)

        print(f"\nQR code successfully generated!")
        print(f"URL: {url}")
        print(f"Saved to: {output_path}")

        # Deploy to S3 if requested
        s3_url = None
        if deploy_to_s3 and self.s3_client and self.s3_bucket:
            s3_url = self.deploy_to_s3(url, output_path)
            if s3_url:
                print(f"QR code deployed to S3: {s3_url}")
                return s3_url

        # Open QR code in browser (local file if not deployed to S3)
        self.open_in_browser(url, output_path)

        return output_path

    def open_in_browser(self, url, image_path):
        """
        Opens the generated QR code in a web browser

        Args:
            url (str): The URL encoded in the QR code
            image_path (str): Path to the QR code image file
        """
        # Read the image and convert to base64
        with open(image_path, "rb") as img_file:
            img_data = img_file.read()

        img_base64 = base64.b64encode(img_data).decode('utf-8')

        # Create HTML content with the QR code
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>QR Code for {url}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    text-align: center;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                }}
                h1 {{
                    color: #333;
                    font-size: 24px;
                }}
                .qr-container {{
                    margin: 30px 0;
                }}
                .qr-image {{
                    max-width: 300px;
                    height: auto;
                }}
                .url {{
                    word-break: break-all;
                    margin: 20px 0;
                    padding: 10px;
                    background-color: #f0f0f0;
                    border-radius: 5px;
                }}
                .button {{
                    display: inline-block;
                    padding: 10px 20px;
                    background-color: #4CAF50;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    font-weight: bold;
                    margin-top: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>QR Code Generated</h1>
                <div class="qr-container">
                    <img src="data:image/png;base64,{img_base64}" alt="QR Code" class="qr-image">
                </div>
                <p>This QR code links to:</p>
                <div class="url">{url}</div>
                <p>You can scan this QR code with any QR code scanner app on your mobile device.</p>
                <a href="{url}" class="button" target="_blank">Open URL</a>
            </div>
        </body>
        </html>
        """

        # Generate a temporary HTML file
        html_path = os.path.join(self.output_dir, "qr_display.html")
        with open(html_path, "w") as html_file:
            html_file.write(html_content)

        # Open the HTML file in the browser
        print(f"Opening QR code in browser...")
        webbrowser.open('file://' + os.path.abspath(html_path))

    def deploy_to_s3(self, url, image_path):
        """
        Deploy QR code and HTML viewer to S3

        Args:
            url (str): The URL encoded in the QR code
            image_path (str): Path to the QR code image file

        Returns:
            str: The S3 URL to the deployed QR code viewer
        """
        if not self.s3_client or not self.s3_bucket:
            print("S3 is not configured. Use configure_aws() first.")
            return None

        try:
            # Generate unique ID for this QR code
            qr_id = str(uuid.uuid4())[:8]

            # Upload the QR code image
            image_key = f"qrcodes/{qr_id}/{os.path.basename(image_path)}"
            self.s3_client.upload_file(
                Filename=image_path,
                Bucket=self.s3_bucket,
                Key=image_key,
                ExtraArgs={'ContentType': 'image/png', 'ACL': 'public-read'}
            )

            # Get the S3 URL for the image
            region = self.s3_client.meta.region_name
            s3_image_url = f"https://{self.s3_bucket}.s3.{region}.amazonaws.com/{image_key}"

            # Create HTML content for S3
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>QR Code for {url}</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        text-align: center;
                        padding: 20px;
                        background-color: #f5f5f5;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        background-color: white;
                        padding: 30px;
                        border-radius: 10px;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    }}
                    h1 {{
                        color: #333;
                        font-size: 24px;
                    }}
                    .qr-container {{
                        margin: 30px 0;
                    }}
                    .qr-image {{
                        max-width: 300px;
                        height: auto;
                    }}
                    .url {{
                        word-break: break-all;
                        margin: 20px 0;
                        padding: 10px;
                        background-color: #f0f0f0;
                        border-radius: 5px;
                    }}
                    .button {{
                        display: inline-block;
                        padding: 10px 20px;
                        background-color: #4CAF50;
                        color: white;
                        text-decoration: none;
                        border-radius: 5px;
                        font-weight: bold;
                        margin-top: 20px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>QR Code Generated</h1>
                    <div class="qr-container">
                        <img src="{s3_image_url}" alt="QR Code" class="qr-image">
                    </div>
                    <p>This QR code links to:</p>
                    <div class="url">{url}</div>
                    <p>You can scan this QR code with any QR code scanner app on your mobile device.</p>
                    <a href="{url}" class="button" target="_blank">Open URL</a>
                </div>
            </body>
            </html>
            """

            # Upload the HTML file
            html_key = f"qrcodes/{qr_id}/index.html"
            self.s3_client.put_object(
                Body=html_content,
                Bucket=self.s3_bucket,
                Key=html_key,
                ContentType='text/html',
                ACL='public-read'
            )

            # Get the website URL
            website_url = f"http://{self.s3_bucket}.s3-website-{region}.amazonaws.com/qrcodes/{qr_id}/"

            return website_url

        except Exception as e:
            print(f"Error deploying to S3: {e}")
            return None


def print_banner():
    """Print a fancy banner for the app"""
    print("\n" + "=" * 50)
    print("QR CODE GENERATOR".center(50))
    print("=" * 50)
    print("\nThis tool generates QR codes from URLs.")
    print("The QR codes can be scanned with any QR code scanner app.")
    print("\nFeatures:")
    print("1. Generate QR codes for any URL")
    print("2. View QR codes in your browser")
    print("3. Deploy QR codes to AWS S3 for sharing")
    print("\nInstructions:")
    print("1. Enter a URL (with or without http/https)")
    print("2. Optionally specify a filename (default: auto-generated)")
    print("3. Choose to deploy to AWS S3 (if configured)")
    print("4. The QR code will be displayed in your browser")
    print("-" * 50)

def main():
    """Main function to run the QR code generator"""
    print_banner()

    generator = QRCodeGenerator()

    # Check if user wants to configure AWS S3
    print("\nDo you want to enable AWS S3 deployment? (y/n)")
    aws_choice = input("> ").strip().lower()

    if aws_choice == 'y':
        # Get AWS configuration
        print("\nAWS S3 Configuration:")
        bucket_name = input("Enter S3 bucket name: ").strip()
        region = input("Enter AWS region (default: us-east-1): ").strip() or "us-east-1"

        print("\nDo you want to enter AWS credentials? (y/n)")
        print("Note: If 'n', AWS SDK will use credentials from ~/.aws/credentials or environment variables")
        creds_choice = input("> ").strip().lower()

        aws_key = aws_secret = None
        if creds_choice == 'y':
            aws_key = input("Enter AWS Access Key ID: ").strip()
            aws_secret = input("Enter AWS Secret Access Key: ").strip()

        # Configure AWS
        if generator.configure_aws(bucket_name, region, aws_key, aws_secret):
            print("\nAWS S3 configured successfully!")
        else:
            print("\nAWS S3 configuration failed. Continuing in local mode only.")

    while True:
        try:
            print("\nEnter a URL to generate a QR code (or 'q' to quit):")
            url = input("> ").strip()

            if url.lower() in ('q', 'quit', 'exit'):
                print("\nThank you for using the QR Code Generator!\n")
                break

            print("\nEnter a filename (or press Enter for auto-generated name):")
            filename = input("> ").strip()

            # Ask about deployment if AWS is configured
            deploy_to_s3 = False
            if generator.s3_client and generator.s3_bucket:
                print("\nDo you want to deploy this QR code to AWS S3? (y/n)")
                deploy_choice = input("> ").strip().lower()
                deploy_to_s3 = deploy_choice == 'y'

            # Generate QR code
            generator.generate(url, filename, deploy_to_s3)

            # Ask if user wants to create another
            print("\nDo you want to generate another QR code? (y/n)")
            choice = input("> ").strip().lower()
            if choice != 'y':
                print("\nThank you for using the QR Code Generator!\n")
                break

        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again.")

if __name__ == "__main__":
    main()
