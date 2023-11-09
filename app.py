from flask import Flask, render_template, request, redirect, send_file
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)

INPUT_FOLDER = 'input'
RESULT_FOLDER = 'joined'
OUTPUT_FOLDER = "output"
ALLOWED_EXTENSIONS = {'mp3'}
app.config['INPUT_FOLDER'] = INPUT_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['INPUT_FOLDER'], filename)
        file.save(file_path)

        # todo: process file

        return render_template('result.html', filename=filename )

    return 'Invalid file format.'

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['INPUT_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)