import os
import secrets
from main import main
from flask_assets import Environment, Bundle
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from waitress import serve


pwd = os.getcwd()
path = pwd + "/main.py"
UPLOAD_FOLDER = pwd + "/uploads"
ALLOWED_EXTENSIONS = {'zip'}

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
env = Environment(app)
js = Bundle('js/clarity-icons.min.js', 'js/clarity-icons-api.js',
            'js/clarity-icons-element.js', 'js/custom-elements.min.js')
env.register('js_all', js)
css = Bundle('css/clarity-ui.min.css', 'css/clarity-icons.min.css')
env.register('css_all', css)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    error = None
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            error = "No selected file"
            return render_template('index.html', error=error)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('index.html', name=filename), main(filename)
    return render_template('index.html', error=error)


if __name__ == '__main__':
    #app.run(host="0.0.0.0", port=5000, debug=True)
    serve(app, host="0.0.0.0", port=5000)
