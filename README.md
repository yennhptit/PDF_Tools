# PDF Tools

A modern web application for PDF manipulation with two powerful features: PDF splitting and PDF compression.

## Features

### 1. Split PDF
- Split PDF files into smaller PDFs based on page ranges
- Support for single pages and page ranges (e.g., `1,2-3,4-10,5-8`)
- Three naming options:
  - No prefix: `1.pdf`, `2-3.pdf`
  - Custom prefix: `IELTS_1.pdf`, `IELTS_2-3.pdf`
  - Original filename: `filename_1.pdf`, `filename_2-3.pdf`
- All split files are downloaded as a ZIP file
- Individual file download links available
- Loading states during file upload and processing
- Display selected file name in upload area

### 2. Compress PDF
- Reduce PDF file size while maintaining quality
- Compress images in PDF using JPEG compression
- Optimize PDF structure with pikepdf
- Display compression statistics
- Preview compressed PDF in browser
- Loading states with progress bar

## Installation

1. Install Python 3.7 or higher
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Starting the Server

**Windows:**
```bash
# Option 1: Double-click start_server.bat
# Option 2: Run in command prompt
python app.py
```

**Linux/Mac:**
```bash
python3 app.py
```

The server will run on `http://localhost:5000`

### Using the Application

1. **Start the Python server** (see above)
2. Open your browser and go to `http://localhost:5000`
3. Choose either "Split PDF" or "Compress PDF"

#### Split PDF
1. Click "Split PDF" from home page
2. Upload your PDF file (file name will be displayed)
3. Enter page ranges (e.g., `1,2-3,4-10`)
4. Choose file naming option
5. Click "Split PDF"
6. Download ZIP file or individual PDF files

#### Compress PDF
1. Click "Compress PDF" from home page
2. Upload your PDF file (file name will be displayed)
3. Click "Compress PDF"
4. View compressed PDF and download

## Technologies Used

- **Python 3.7+** - Backend server
- **Flask** - Python web framework
- **PyMuPDF (fitz)** - PDF manipulation library
- **Pillow (PIL)** - Image processing library
- **pikepdf** - PDF optimization library
- **HTML5** - Structure and semantic markup
- **CSS3** - Modern styling
- **JavaScript** - UI interactions

## File Structure

```
PDF_Toos/
├── app.py              # Main Flask application
├── index.html          # Home page
├── split.html          # Split PDF page
├── compress.html       # Compress PDF page
├── styles.css          # Shared stylesheet
├── requirements.txt    # Python dependencies
├── start_server.bat    # Windows startup script
└── README.md           # Documentation
```

## Notes

- All processing is done server-side using Python
- Files are processed on the server and returned to the browser
- Split PDF files are stored temporarily and cleaned up after 1 hour
- All comments in the code are in English

## License

This project is open source and available for personal and commercial use.

