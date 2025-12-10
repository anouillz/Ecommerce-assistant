import fitz  
from pyzbar.pyzbar import decode
from PIL import Image
import io
from config import PDF_FOLDER_PATH
import os

def extract_qr_from_page(pdf_path, page_number):
    "Open a pdf and extract the qr code from a given page number (0-indexed)."
    try:
        doc = fitz.open(pdf_path)
        page = doc.load_page(page_number) 
        
        image_list = page.get_images(full=True)
        
        # no images found
        if not image_list:
            return None

        for img_index, img in enumerate(image_list):
            i = img[0]
            base_image = doc.extract_image(i)
            image_bytes = base_image["image"]
            
            # convert image to PIL format
            image = Image.open(io.BytesIO(image_bytes))
            
            # see if it contains a QR code
            decoded_objects = decode(image)
            for obj in decoded_objects:
                if obj.type == 'QRCODE':
                    url = obj.data.decode('utf-8')
                    return url
                    
        return None
    except Exception as e:
        print(f"QR Error: {e}")
        return None

# Quick test
if __name__ == "__main__":
    pdf = os.path.join(PDF_FOLDER_PATH, "vins_2021.pdf")
    # Test on page 3 (which has a YouTube QR code for Soleil du Valais)
    print(extract_qr_from_page(pdf, 2))