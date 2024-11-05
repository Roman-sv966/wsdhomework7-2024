import sys
import qrcode
from dotenv import load_dotenv
import logging.config
from pathlib import Path
import os
import argparse
from datetime import datetime
import validators  # Import the validators package

# Load environment variables
load_dotenv()

# Environment Variables for Configuration
QR_DIRECTORY = os.getenv('QR_CODE_DIR', 'qr_codes')  # Directory for saving QR code
FILL_COLOR = os.getenv('FILL_COLOR', 'blue')  # Fill color for the QR code
BACK_COLOR = os.getenv('BACK_COLOR', 'white')  # Background color for the QR code

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
        ]
    )

def create_directory(path: Path):
    logging.info(f"Checking if directory {path} exists or needs to be created.")
    try:
        path.mkdir(parents=True, exist_ok=True)
        logging.info(f"Directory {path} is ready for use.")
    except Exception as e:
        logging.error(f"Failed to create directory {path}: {e}")
        exit(1)

def is_valid_url(url):
    logging.info(f"Validating URL: {url}")
    if validators.url(url):
        logging.info(f"URL is valid: {url}")
        return True
    else:
        logging.error(f"Invalid URL provided: {url}")
        return False

def generate_qr_code(data, path, fill_color='red', back_color='white'):
    if not is_valid_url(data):
        return  # Exit the function if the URL is not valid

    try:
        logging.info("Starting QR code generation process.")
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color=fill_color, back_color=back_color)

        with path.open('wb') as qr_file:
            img.save(qr_file)
            logging.info(f"QR code image saved to {path}")
        logging.info("QR code generation process completed successfully.")

    except Exception as e:
        logging.error(f"An error occurred while generating or saving the QR code: {e}")

def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Generate a QR code.')
    parser.add_argument('--url', help='The URL to encode in the QR code', default='https://github.com/Roman-sv966')
    args = parser.parse_args()

    # Initial logging setup
    setup_logging()
    logging.info("QR Code generation script started.")

    # Generate a timestamped filename for the QR code
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    qr_filename = f"QRCode_{timestamp}.png"
    logging.info(f"Generated filename for QR code: {qr_filename}")

    # Create the full path for the QR code file
    qr_code_full_path = Path.cwd() / QR_DIRECTORY / qr_filename
    logging.info(f"Full path for QR code file: {qr_code_full_path}")

    # Ensure the QR code directory exists
    create_directory(Path.cwd() / QR_DIRECTORY)

    # Generate and save the QR code
    generate_qr_code(args.url, qr_code_full_path, FILL_COLOR, BACK_COLOR)
    logging.info("QR Code generation script completed.")

if __name__ == "__main__":
    main()
