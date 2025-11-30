from flask import Flask, request, send_file, jsonify, send_from_directory
from flask_cors import CORS
import fitz  # PyMuPDF
import os
import tempfile
import zipfile
import shutil
import uuid
import time

app = Flask(__name__)
CORS(app)

# Store temporary split results
split_sessions = {}

# Parse page ranges from input string
def parse_page_ranges(input_str, total_pages):
    """Parse page ranges like '1,2-3,4-10' into list of page indices"""
    ranges = []
    parts = [p.strip() for p in input_str.split(',')]
    
    for part in parts:
        if not part:
            continue
        if '-' in part:
            try:
                start, end = part.split('-')
                start = int(start.strip())
                end = int(end.strip())
                
                if start < 1 or end > total_pages or start > end:
                    raise ValueError(f"Invalid range: {start}-{end}")
                
                pages = list(range(start - 1, end))
                ranges.append({'start': start, 'end': end, 'pages': pages})
            except ValueError as e:
                raise ValueError(f"Invalid range format: {part}")
        else:
            try:
                page = int(part.strip())
                if page < 1 or page > total_pages:
                    raise ValueError(f"Invalid page: {page}")
                ranges.append({'start': page, 'end': page, 'pages': [page - 1]})
            except ValueError as e:
                raise ValueError(f"Invalid page number: {part}")
    
    return ranges

# API Routes
@app.route('/split-pdf', methods=['POST'])
def split_pdf():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        page_ranges_str = request.form.get('pageRanges', '').strip()
        naming_option = request.form.get('namingOption', 'none')
        custom_prefix = request.form.get('customPrefix', '').strip()
        
        if not page_ranges_str:
            return jsonify({'error': 'Please enter page ranges'}), 400
        
        original_filename = os.path.splitext(file.filename)[0]
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_input:
            input_path = temp_input.name
            file.save(input_path)
        
        try:
            doc = fitz.open(input_path)
            total_pages = len(doc)
            ranges = parse_page_ranges(page_ranges_str, total_pages)
            
            if naming_option == 'custom':
                if not custom_prefix:
                    return jsonify({'error': 'Please enter a custom prefix'}), 400
                base_filename = custom_prefix
            elif naming_option == 'original':
                base_filename = original_filename
            else:
                base_filename = ''
            
            temp_dir = tempfile.mkdtemp()
            output_files = []
            
            for i, range_info in enumerate(ranges):
                new_doc = fitz.open()
                
                for page_num in range_info['pages']:
                    new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
                
                if range_info['start'] == range_info['end']:
                    range_str = str(range_info['start'])
                else:
                    range_str = f"{range_info['start']}-{range_info['end']}"
                
                if base_filename:
                    filename = f"{base_filename}_{range_str}.pdf"
                else:
                    filename = f"{range_str}.pdf"
                
                output_path = os.path.join(temp_dir, filename)
                new_doc.save(output_path)
                new_doc.close()
                
                output_files.append({
                    'path': output_path,
                    'filename': filename
                })
            
            doc.close()
            
            zip_path = os.path.join(temp_dir, 'split_pdfs.zip')
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_info in output_files:
                    zipf.write(file_info['path'], file_info['filename'])
            
            session_id = str(uuid.uuid4())
            split_sessions[session_id] = {
                'temp_dir': temp_dir,
                'files': output_files,
                'zip_path': zip_path,
                'created_at': time.time()
            }
            
            try:
                if os.path.exists(input_path):
                    os.unlink(input_path)
            except:
                pass
            
            file_list = [{'filename': f['filename'], 'range': f['filename'].replace('.pdf', '')} for f in output_files]
            return jsonify({
                'success': True,
                'session_id': session_id,
                'files': file_list,
                'zip_filename': 'split_pdfs.zip'
            })
            
        except Exception as e:
            try:
                if os.path.exists(input_path):
                    os.unlink(input_path)
                if 'temp_dir' in locals() and os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir, ignore_errors=True)
            except:
                pass
            raise
                
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Download routes
@app.route('/download-split-file/<session_id>/<filename>', methods=['GET'])
def download_split_file(session_id, filename):
    if session_id not in split_sessions:
        return jsonify({'error': 'Session not found or expired'}), 404
    
    session = split_sessions[session_id]
    file_info = next((f for f in session['files'] if f['filename'] == filename), None)
    
    if not file_info or not os.path.exists(file_info['path']):
        return jsonify({'error': 'File not found'}), 404
    
    return send_file(
        file_info['path'],
        mimetype='application/pdf',
        as_attachment=True,
        download_name=filename
    )

@app.route('/download-split-zip/<session_id>', methods=['GET'])
def download_split_zip(session_id):
    if session_id not in split_sessions:
        return jsonify({'error': 'Session not found or expired'}), 404
    
    session = split_sessions[session_id]
    
    if not os.path.exists(session['zip_path']):
        return jsonify({'error': 'ZIP file not found'}), 404
    
    return send_file(
        session['zip_path'],
        mimetype='application/zip',
        as_attachment=True,
        download_name='split_pdfs.zip'
    )

# Static file routes
@app.route('/', methods=['GET'])
def index():
    return send_from_directory('.', 'index.html')

@app.route('/split.html', methods=['GET'])
def split_page():
    return send_from_directory('.', 'split.html')

@app.route('/styles.css', methods=['GET'])
def styles():
    return send_from_directory('.', 'styles.css')

# Clean up old sessions
def cleanup_old_sessions():
    current_time = time.time()
    expired_sessions = []
    for session_id, session_data in split_sessions.items():
        if current_time - session_data['created_at'] > 3600:
            expired_sessions.append(session_id)
    
    for session_id in expired_sessions:
        try:
            session = split_sessions[session_id]
            if os.path.exists(session['temp_dir']):
                shutil.rmtree(session['temp_dir'], ignore_errors=True)
            del split_sessions[session_id]
        except:
            pass

@app.route('/health', methods=['GET'])
def health():
    cleanup_old_sessions()
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')

