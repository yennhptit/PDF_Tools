# PDF Tools

A modern web application for PDF splitting. Split your PDF files into smaller PDFs based on page ranges.

## Features

### Split PDF
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
3. Click "Split PDF"

#### Split PDF
1. Upload your PDF file (file name will be displayed)
2. Enter page ranges (e.g., `1,2-3,4-10`)
3. Choose file naming option:
   - No prefix
   - Custom prefix (enter your prefix)
   - Original filename
4. Click "Split PDF"
5. Download ZIP file or individual PDF files

## Technologies Used

- **Python 3.7+** - Backend server
- **Flask** - Python web framework
- **PyMuPDF (fitz)** - PDF manipulation library
- **HTML5** - Structure and semantic markup
- **CSS3** - Modern styling
- **JavaScript** - UI interactions

## File Structure

```
PDF_Toos/
├── app.py              # Main Flask application
├── index.html          # Home page
├── split.html          # Split PDF page
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

