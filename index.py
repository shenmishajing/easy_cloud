from flask import Flask
from flask import render_template, make_response, send_from_directory, send_file
from flask import request, redirect, url_for
from werkzeug.utils import secure_filename

import config
from config import config as cfg
from utils import *
from verify import verify, login, verify_already_login

from urllib import parse

app = Flask(__name__)


def verify_wrapper(f):
    def wrapper(*args, **kwargs):
        if verify_already_login(request.cookies):
            return f(*args, **kwargs)
        else:
            return redirect(url_for('HTML_verify'))

    wrapper.__name__ = f.__name__
    return wrapper


@app.route('/', methods = ['GET', 'POST'])
def HTML_verify():
    ''' verify target user'''

    try:
        if request.method == 'GET':
            if verify_already_login(request.cookies):
                return redirect(url_for('HTML_entry'))
            else:
                return render_template('verify.html', config = cfg)
        elif request.method == 'POST':
            _user = request.form['user']
            _password = request.form['password']
            if verify(_user, _password):
                response = make_response('success')
                login(response, _user)
                return response
            else:
                return 'failed'
    except Exception as e:
        print(e)
        return '404'


@app.route('/entry')
@verify_wrapper
def HTML_entry():
    return render_template('index.html', config = cfg)


@app.route('/hello')
@verify_wrapper
def HTML_hello():
    return render_template('hello.html', config = cfg)


@app.route('/filelist/<path:pathname>')
@verify_wrapper
def HTML_files(pathname):
    _pathname = config.project_path + pathname + '/'
    files = scan_folder_first(_pathname)
    return render_template('filelist.html', config = cfg, files = files, current_path = pathname)


@app.route('/download/<path:path_name>')
@verify_wrapper
def download(path_name):
    directory = os.path.dirname(config.project_path + path_name)
    filename = path_name.split('/')[-1]
    print(directory, filename)
    res = make_response(send_from_directory(directory, filename, as_attachment = True))
    return res


@app.route('/downloadex/<path:path_name>')
@verify_wrapper
def downloadex(path_name):
    response = make_response(send_file(config.project_path + path_name))
    basename = os.path.basename(path_name)
    response.headers['Content-Disposition'] = \
        'attachment;' \
        'filename*=UTF-8''{utf_filename}'.format(
            utf_filename = parse.quote(basename.encode('utf-8'))
        )
    return response


@app.route('/upload/<path:path_name>', methods = ['POST'])
@verify_wrapper
def upload_file(path_name):
    '''upload a new file in current floder'''
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            if os.path.exists(config.project_path + path_name):
                return 'upload failed'
            else:
                file.save(config.project_path + path_name)
                return 'upload success'


@app.route('/remove', methods = ['POST'])
@verify_wrapper
def remove_files():
    '''remove target file in current floder'''
    if request.method == 'POST':
        files = eval(request.form.get('files_json_value'))
        try:
            for file in files:
                if os.path.isfile(config.project_path + file):
                    os.remove(config.project_path + file)
                else:
                    delete_folder(config.project_path + file)

            if not os.path.exists(config.project_path + 'Files'):
                os.mkdir(config.project_path + 'Files')
            return 'delete success'
        except FileNotFoundError as e:
            print(e)
            return 'delete failed'


@app.route('/folder/<path:path_name>', methods = ['POST'])
@verify_wrapper
def create_folder(path_name):
    ''' create a new folder in current folder'''
    if request.method == 'POST':
        _folder_name = request.form.get('folder_name')
        if _folder_name:
            os.mkdir(os.path.join(config.project_path + path_name, _folder_name))
            return 'create success'


if __name__ == '__main__':
    app.run('127.0.0.1', threaded = True, debug = False, port = 4433, ssl_context = (config.pem_path, config.key_path))
