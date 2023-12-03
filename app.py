from werkzeug.utils import secure_filename
from natsort import natsorted
from file_splitter import FileSpliter
import os
import pydub
from flask import Flask
from flask import *
from file_splitter import *
from datetime import datetime

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
        
        timestamp = datetime.now()

        split_silence(app.config['OUTPUT_FOLDER'],app.config['INPUT_FOLDER'],[-45],[300])
        join_audio(app.config['OUTPUT_FOLDER'],app.config['RESULT_FOLDER'],timestamp)
        
        remove_files_from_folder(app.config['INPUT_FOLDER'])
        remove_files_from_folder(app.config['OUTPUT_FOLDER'])
        
        try:
            file_path = os.path.join(app.config['RESULT_FOLDER'], f"joined_{timestamp}.mp3")

            if os.path.exists(file_path):
                return send_file(file_path, as_attachment=True)
            else:
                abort(404, "File not found")

        except Exception as e:
            return f"Error: {str(e)}"

    return 'Invalid file format.'

def join_audio(input, output,timestamp):
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

    joined_audio.export(os.path.join(output,f"joined_{timestamp}.mp3"), format="mp3")
    
    
def split_silence(destination, source, silence_threshs, min_silence_lens):
    fileSpliter = FileSpliter(source,destination)
    fileSpliter.split_silence(silence_threshs, min_silence_lens)

def remove_files_from_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Error: {e}")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)