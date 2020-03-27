import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

UPLOAD_FOLDER = '/home/yana/Documents/temp'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
               
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
        else:
            flash('Invalid type')
    return render_template('upload_template.html')
    
from flask import send_from_directory

def plot_from_mp3(D):
    librosa.display.specshow(librosa.amplitude_to_db(D,ref=np.max),y_axis='log', x_axis='time')
    plt.title('Power spectrogram')
    plt.colorbar(format='%+2.0f dB')
    plt.tight_layout()
    plt.show()
    plt.savefig(UPLOAD_FOLDER+"temp.png")
    plt = Image.open(UPLOAD_FOLDER+"temp.png")
    return plt

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    #MyFile = UPLOAD_FOLDER + filename
    y, sr = librosa.load(librosa.util.example_audio_file())
    D = np.abs(librosa.stft(y))
    return render_template('result_template.html', image_title="LOL", image_name=plot_from_mp3(D))
#send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=False)