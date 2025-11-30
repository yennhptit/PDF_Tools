from flask import Flask, request, send_file
import os
from compress_script import smallpdf_style_compress

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return "PDF Compression API is running!"

@app.route("/compress", methods=["POST"])
def compress_pdf():
    if "file" not in request.files:
        return {"error": "No file uploaded"}, 400
    file = request.files["file"]
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    output_path = os.path.join(OUTPUT_FOLDER, f"compressed_{file.filename}")
    file.save(input_path)

    smallpdf_style_compress(input_path, output_path, quality=50, use_ghostscript=True, gs_quality="ebook")

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
