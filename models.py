from fastai.vision import *
import os
from flask import Flask, flash, request, redirect, url_for,render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'my unobvious secret key'

def predict(img_name):
    path = Path()
    img = open_image(img_name)
    learn = load_learner(path)
    pred_class, pred_idx, outputs = learn.predict(img)
    return(pred_class)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    result='none'
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            #flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return redirect(url_for('uploaded_file',filename=filename))
            paths = 'uploads/'+filename
            result = predict(paths)
            print(result)
            #flash(result)
    return  render_template('index.html',result=result)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    path = 'uploads/'+filename
    result = predict(path)
    print(result)
    return render_template('results.html',result=result)

if __name__ == "__main__":
    app.run(debug=True)