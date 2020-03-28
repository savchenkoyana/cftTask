import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from pathlib import Path
import time

UPLOAD_FOLDER = 'static/audios'
SAVE_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = set(['mp3'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SAVE_FOLDER'] = SAVE_FOLDER

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
            return render_template('result_template.html', mp3_title=filename, image_name= ( plot_from_mp3(filename)+'?%d'%(time.time()) ) )
        else:
            flash('Invalid type')
    return render_template('upload_template.html')
    
from flask import send_from_directory

def plot_from_mp3(filename):
    my_filename = UPLOAD_FOLDER + '/' + filename
    y, sr = librosa.load(my_filename)
    os.remove(my_filename)
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    librosa.display.specshow(librosa.amplitude_to_db(D,ref=np.max), y_axis='log', x_axis='time')
    plt.title('Power spectrogram')
    plt.colorbar(format='%+2.0f dB')
    plt.tight_layout()
    path_to_png = SAVE_FOLDER + '/result.png'
    if os.path.isfile(path_to_png):
        os.remove(path_to_png)   
    plt.savefig(path_to_png)
    plt.clf()
    return path_to_png

if __name__ == '__main__':
    app.run(debug=False)
