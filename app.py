from werkzeug.utils import secure_filename
from natsort import natsorted
from file_splitter import FileSpliter
import os
import pydub
import tempfile
from flask import Flask
from flask import *
from file_splitter import *

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

        split_silence(app.config['OUTPUT_FOLDER'],app.config['INPUT_FOLDER'],[-45],[300])
        join_audio(app.config['OUTPUT_FOLDER'],app.config['RESULT_FOLDER'])

        return render_template('result.html', filename="joined.mp3")

    return 'Invalid file format.'

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['RESULT_FOLDER'], filename), as_attachment=True)

def join_audio(input, output):
    slices = [f for f in os.listdir(input) if f.endswith('.mp3')]
    slices = natsorted(slices)
    audio_segments = []  

    for s in slices:
        path = os.path.join(input, s)
        audio_segment = pydub.AudioSegment.from_file(path)
        audio_segments.append(audio_segment)

    joined_audio = pydub.AudioSegment.empty()
    for s in audio_segments:
        joined_audio = joined_audio + s

    joined_audio.export(os.path.join(output,"joined.mp3"), format="mp3")
    
    
def split_silence(destination, source, silence_threshs, min_silence_lens):
    fileSpliter = FileSpliter(source,destination)
    fileSpliter.split_silence(silence_threshs, min_silence_lens)


if __name__ == '__main__':
    app.run(debug=True)