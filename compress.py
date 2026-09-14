import fitz  # PyMuPDF
import io
import os
from PIL import Image

def compress_pdf_to_target(
    input_pdf: str, 
    output_pdf: str, 
    target_dpi: int = 110,      # Dropping DPI slightly for massive size reduction
    jpeg_quality: int = 35,     # 30-40% is optimal for scanned handwritten notes
    max_dimension: int = 1200   # Limits max image resolution to 1200px
):
    """
    Compresses scanned image PDFs down to ~20MB by optimizing DPI and JPEG quality.
    """
    if not os.path.exists(input_pdf):
        print(f"❌ Error: File '{input_pdf}' not found!")
        return

    print(f"📦 Starting target compression for '{input_pdf}'...")
    doc = fitz.open(input_pdf)
    new_doc = fitz.open()

    total_pages = len(doc)

    for page_num in range(total_pages):
        page = doc[page_num]

        # Render page at 110 DPI (sufficient for handwritten text, drastically smaller)
        pix = page.get_pixmap(dpi=target_dpi)
        img = Image.open(io.BytesIO(pix.tobytes("jpeg")))

        # Resize if dimensions exceed max_dimension
        if max(img.width, img.height) > max_dimension:
            img.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)

        # Convert to RGB (or Grayscale 'L' for even smaller size)
        if img.mode != "RGB":
            img = img.convert("RGB")

        # Compress image buffer as JPEG
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="JPEG", quality=jpeg_quality, optimize=True)
        img_bytes.seek(0)

        # Create new PDF page with exact matching dimensions
        rect = page.rect
        new_page = new_doc.new_page(width=rect.width, height=rect.height)
        new_page.insert_image(rect, stream=img_bytes.getvalue())

        if (page_num + 1) % 10 == 0 or page_num + 1 == total_pages:
            print(f"   -> Processed page {page_num + 1} of {total_pages}...")

    # Save with full deflation
    new_doc.save(output_pdf, garbage=4, deflate=True)
    new_doc.close()
    doc.close()

    orig_size = os.path.getsize(input_pdf) / (1024 * 1024)
    comp_size = os.path.getsize(output_pdf) / (1024 * 1024)
    
    print("\n" + "=" * 50)
    print("✅ TARGET COMPRESSION COMPLETE!")
    print(f"Original Size:   {orig_size:.2f} MB")
    print(f"Compressed Size: {comp_size:.2f} MB")
    print(f"Reduction:       {((orig_size - comp_size) / orig_size) * 100:.1f}%")
    print("=" * 50)


if __name__ == "__main__":
    INPUT_FILE = "POLITY_20MB.pdf"  # Update with your file path
    OUTPUT_FILE = "POLITY_2.pdf"

    # Adjust params to hit ~20MB
    compress_pdf_to_target(
        input_pdf=INPUT_FILE,
        output_pdf=OUTPUT_FILE,
        target_dpi=70,        # Drops resolution slightly
        jpeg_quality=35,       # High compression quality for black/white text
        max_dimension=1200
    )