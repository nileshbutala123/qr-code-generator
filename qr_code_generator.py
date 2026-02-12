#!/usr/bin/env python3

import qrcode
import os
import sys
import uuid
import shutil
from io import BytesIO
from datetime import datetime, timedelta
from pathlib import Path

class QRCodeGenerator:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.qr_folder = os.path.join(self.base_dir, "QR code")
        self._ensure_qr_folder_exists()

    def _ensure_qr_folder_exists(self):
        """Create the QR code folder if it doesn't exist"""
        os.makedirs(self.qr_folder, exist_ok=True)

    def generate(self, url, cleanup_on_generate=True):
        """
        Generate a QR code for the given URL in a dedicated subfolder

        Args:
            url (str): The URL to encode in the QR code
            cleanup_on_generate (bool): Whether to cleanup old QR codes during generation

        Returns:
            dict: Dictionary with 'success' (bool), 'path' (str), 'folder' (str), and 'message' (str)
        """
        try:
            # Validate URL
            if not url:
                return {
                    'success': False,
                    'path': None,
                    'folder': None,
                    'message': 'URL cannot be empty'
                }

            # Add https:// prefix if needed
            if not (url.startswith('http://') or url.startswith('https://')):
                url = 'https://' + url

            # Create a unique subfolder for this QR code
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_id = str(uuid.uuid4())[:8]
            folder_name = f"qr_{timestamp}_{unique_id}"
            qr_subfolder = os.path.join(self.qr_folder, folder_name)
            os.makedirs(qr_subfolder, exist_ok=True)

            # Generate the QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(url)
            qr.make(fit=True)

            # Create image
            img = qr.make_image(fill_color="black", back_color="white")

            # Save to the subfolder
            output_file = os.path.join(qr_subfolder, "qrcode.png")
            img.save(output_file)

            # Save metadata
            metadata = {
                'url': url,
                'created': datetime.now().isoformat(),
                'expires': (datetime.now() + timedelta(days=1)).isoformat(),
                'filename': 'qrcode.png'
            }
            metadata_file = os.path.join(qr_subfolder, "metadata.txt")
            with open(metadata_file, 'w') as f:
                for key, value in metadata.items():
                    f.write(f"{key}: {value}\n")

            # Cleanup old QR codes if requested
            if cleanup_on_generate:
                self.cleanup_old_qrcodes()

            result = {
                'success': True,
                'path': output_file,
                'folder': qr_subfolder,
                'message': f'QR code generated successfully for URL: {url}'
            }
            print(f"[OK] QR code saved to: {output_file}")
            print(f"  Folder: {qr_subfolder}")
            return result

        except Exception as e:
            return {
                'success': False,
                'path': None,
                'folder': None,
                'message': f'Error generating QR code: {str(e)}'
            }

    def cleanup_old_qrcodes(self, days=1):
        """
        Delete QR code folders older than the specified number of days

        Args:
            days (int): Number of days after which to delete QR codes (default: 1)

        Returns:
            dict: Statistics about cleaned up folders
        """
        if not os.path.exists(self.qr_folder):
            return {'success': True, 'deleted_count': 0, 'message': 'QR folder does not exist'}

        try:
            current_time = datetime.now()
            cutoff_time = current_time - timedelta(days=days)
            deleted_count = 0

            for folder_name in os.listdir(self.qr_folder):
                folder_path = os.path.join(self.qr_folder, folder_name)

                if not os.path.isdir(folder_path):
                    continue

                # Get folder creation time
                folder_stat = os.stat(folder_path)
                folder_creation_time = datetime.fromtimestamp(folder_stat.st_ctime)

                # If folder is older than cutoff, delete it
                if folder_creation_time < cutoff_time:
                    shutil.rmtree(folder_path)
                    deleted_count += 1
                    print(f"[OK] Deleted old QR code folder: {folder_name}")

            return {
                'success': True,
                'deleted_count': deleted_count,
                'message': f'Cleanup complete. Deleted {deleted_count} old QR code folder(s).'
            }

        except Exception as e:
            return {
                'success': False,
                'deleted_count': 0,
                'message': f'Error during cleanup: {str(e)}'
            }




if __name__ == "__main__":
    # Example usage
    generator = QRCodeGenerator()

    # Generate a QR code
    result = generator.generate("https://nfl.com")
    print(result['message'])

    if result['success']:
        print(f"QR Code Path: {result['path']}")
        print(f"Folder: {result['folder']}")

    # Manual cleanup (optional - cleanup is already called during generation)
    cleanup_result = generator.cleanup_old_qrcodes(days=1)
    print(cleanup_result['message'])


                'message': f'Error during cleanup: {str(e)}'
            }




if __name__ == "__main__":
    # Example usage
    generator = QRCodeGenerator()

    # Generate a QR code
    result = generator.generate("https://example.com")
    print(result['message'])

    if result['success']:
        print(f"QR Code Path: {result['path']}")
        print(f"Folder: {result['folder']}")

    # Manual cleanup (optional - cleanup is already called during generation)
    cleanup_result = generator.cleanup_old_qrcodes(days=1)
    print(cleanup_result['message'])

