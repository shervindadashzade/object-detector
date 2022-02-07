from fileinput import filename
from flask import Flask, render_template, request
import os
import random
import string
from yolov5.detect import run
from flask_cors import CORS
import urllib
import validators

app = Flask(__name__)
cors = CORS(app)

app.config['UPLOAD_FOLDER'] = os.path.join('static','uploads')
app.config['RESULT_FOLDER'] = os.path.join('static','results')

extensions_list= ['JPG','jpg','png','PNG']

@app.route("/")

def hello_world():
    return "<p>Hello, World! This is a test</p>"

@app.route('/upload')
def upload_file():
    return render_template('./upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def uploader_file():
    if request.method == 'POST':
        f = request.files['file']
        random_string = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(10))
        extension = f.filename.split('.')[-1]
        print(extension)
        if extension not in extensions_list:
            return 'Invalid file extension.'
        file_name = random_string +'.'+ extension
        print(file_name)
        uploaded_path_file = os.path.join(app.config['UPLOAD_FOLDER'],file_name)
        f.save(uploaded_path_file)
        run(weights='best.pt',project='static/results',name=random_string,source=uploaded_path_file)
        return render_template('result.html', result_img=os.path.join(app.config['RESULT_FOLDER'],random_string,file_name))
        return 'saved'


@app.post('/api/detect')
def detect_file():
        if 'file' not in request.files:
            return 'No file part.'
        f = request.files['file']
        random_string = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(10))
        extension = f.filename.split('.')[-1]
        print(extension)
        if extension not in extensions_list:
            return 'Invalid Image.'
        file_name = random_string +'.'+ extension
        print(file_name)
        uploaded_path_file = os.path.join(app.config['UPLOAD_FOLDER'],file_name)
        f.save(uploaded_path_file)
        run(weights='yolov5s.pt',project='static/results',name=random_string,source=uploaded_path_file)
        result_url = 'http://192.99.230.250:5000/' + os.path.join(app.config['RESULT_FOLDER'],random_string,file_name)
        return result_url

@app.put('/api/detect')
def detect_url():
        if 'url' not in request.form:
            return 'Missing url field.'
        url = request.form['url']
        random_string = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(10))
        print(random_string)
        if not validators.url(url):
            return 'Invalid url.'
        extension = url.split('.')[-1]
        file_name = random_string+'.'+extension
        if extension not in extensions_list:
            return 'Invalid Image.'
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url,'static/uploads/'+file_name)
        run(weights='yolov5s.pt',project='static/results',name=random_string,source='static/uploads/'+file_name)
        return 'http://192.99.230.250:5000/' + os.path.join(app.config['RESULT_FOLDER'],random_string,file_name)


if __name__ == '__main__':
    app.run(debug=True)