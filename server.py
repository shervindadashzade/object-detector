from fileinput import filename
from flask import Flask, render_template, request
import os
import random
import string
from yolov5.detect import run

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = os.path.join('static','uploads')
app.config['RESULT_FOLDER'] = os.path.join('static','results')
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
        file_name = random_string +'.'+ extension
        print(file_name)
        uploaded_path_file = os.path.join(app.config['UPLOAD_FOLDER'],file_name)
        f.save(uploaded_path_file)
        run(weights='best.pt',project='static/results',name=random_string,source=uploaded_path_file)
        return render_template('result.html', result_img=os.path.join(app.config['RESULT_FOLDER'],random_string,file_name))
        return 'saved'

if __name__ == '__main__':
    app.run(debug=True)