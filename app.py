from flask import Flask, render_template, request, url_for
import os
import fitz  # PyMuPDF
from gtts import gTTS

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
AUDIO_FOLDER = 'static/audio'
PDF_FOLDER = 'static/pdf'

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)
os.makedirs(PDF_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'pdf_file' not in request.files:
        return 'No file part'

    file = request.files['pdf_file']
    if file.filename == '':
        return 'No selected file'

    if file and file.filename.endswith('.pdf'):
        # Save PDF
        pdf_filename = file.filename
        pdf_path = os.path.join(PDF_FOLDER, pdf_filename)
        file.save(pdf_path)

        # Extract text
        doc = fitz.open(pdf_path)
        full_text = ''
        for page in doc:
            full_text += page.get_text()

        # Convert to speech using gTTS
        tts = gTTS(full_text)
        audio_filename = 'output.mp3'
        audio_path = os.path.join(AUDIO_FOLDER, audio_filename)
        tts.save(audio_path)

        return render_template(
            "reader.html",
            pdf_url=url_for('static', filename=f'pdf/{pdf_filename}'),
            audio_url=url_for('static', filename=f'audio/{audio_filename}')
        )

    return 'Invalid file format'

if __name__ == '__main__':
    app.run(debug=True)
