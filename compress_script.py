# compress_script.py
import fitz  # PyMuPDF
from PIL import Image
from io import BytesIO
import pikepdf
import os
import subprocess
import shutil

def print_progress(prefix, current, total):
    percent = int(current / total * 100)
    bar_len = 30
    filled_len = int(bar_len * percent // 100)
    bar = "█" * filled_len + "-" * (bar_len - filled_len)
    print(f"\r{prefix}: |{bar}| {percent}% ", end="", flush=True)

def compress_images(input_file, temp_file, quality=50, max_dim=1500):
    doc = fitz.open(input_file)
    total_images = sum(len(doc[page].get_images(full=True)) for page in range(len(doc)))
    if total_images == 0:
        doc.save(temp_file)
        doc.close()
        return
    img_counter = 0
    for page_index in range(len(doc)):
        page = doc[page_index]
        images = page.get_images(full=True)
        for img in images:
            img_counter += 1
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            img_obj = Image.open(BytesIO(image_bytes))
            if img_obj.mode == "RGBA":
                background = Image.new("RGB", img_obj.size, (255, 255, 255))
                background.paste(img_obj, mask=img_obj.split()[3])
                img_obj = background
            elif img_obj.mode == "LA":
                background = Image.new("L", img_obj.size, 255)
                background.paste(img_obj, mask=img_obj.split()[1])
                img_obj = background
            elif img_obj.mode == "CMYK":
                img_obj = img_obj.convert("RGB")
            elif img_obj.mode != "RGB":
                img_obj = img_obj.convert("RGB")
            if img_obj.width > max_dim or img_obj.height > max_dim:
                img_obj.thumbnail((max_dim, max_dim), Image.LANCZOS)
            if base_image["ext"].lower() != "jpeg":
                buf = BytesIO()
                img_obj.save(buf, format="JPEG", quality=quality, optimize=True, progressive=True)
                doc.update_stream(xref, buf.getvalue())
            print_progress("Compressing images", img_counter, total_images)
    doc.save(temp_file, garbage=1, deflate=True)
    doc.close()

def optimize_pdf(temp_file, output_file):
    pdf = pikepdf.open(temp_file)
    pdf.save(output_file, compress_streams=True, linearize=True)
    pdf.close()

def compress_with_ghostscript(input_file, output_file, quality="ebook"):
    gs_path = shutil.which("gs") or shutil.which("gswin64c") or shutil.which("gswin32c")
    if not gs_path:
        return False
    try:
        gs_command = [
            gs_path,
            "-sDEVICE=pdfwrite",
            f"-dPDFSETTINGS=/{quality}",
            "-dCompatibilityLevel=1.4",
            "-dNOPAUSE",
            "-dQUIET",
            "-dBATCH",
            "-dDetectDuplicateImages=true",
            "-dCompressFonts=true",
            "-dSubsetFonts=true",
            "-dColorImageDownsampleType=/Bicubic",
            "-dColorImageResolution=150",
            "-dGrayImageDownsampleType=/Bicubic",
            "-dGrayImageResolution=150",
            "-dMonoImageDownsampleType=/Bicubic",
            "-dMonoImageResolution=150",
            f"-sOutputFile={output_file}",
            input_file
        ]
        subprocess.run(gs_command, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def smallpdf_style_compress(input_file, output_file, quality=50, use_ghostscript=True, gs_quality="ebook"):
    temp_file1 = "temp_compress1.pdf"
    temp_file2 = "temp_compress2.pdf"
    compress_images(input_file, temp_file1, quality)
    optimize_pdf(temp_file1, temp_file2)
    if use_ghostscript:
        if compress_with_ghostscript(temp_file2, output_file, gs_quality):
            if os.path.exists(temp_file1): os.remove(temp_file1)
            if os.path.exists(temp_file2): os.remove(temp_file2)
        else:
            if os.path.exists(temp_file2): os.rename(temp_file2, output_file)
            if os.path.exists(temp_file1): os.remove(temp_file1)
    else:
        if os.path.exists(temp_file2): os.rename(temp_file2, output_file)
        if os.path.exists(temp_file1): os.remove(temp_file1)
