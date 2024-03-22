# https://youtu.be/ZS1ivzlymPQ
"""

Werkzeug provides a bunch of utilities for developing WSGI-compliant applications. 
These utilities do things like parsing headers, sending and receiving cookies, 
providing access to form data, generating redirects, generating error pages when 
there's an exception, even providing an interactive debugger that runs in the browser. 
Flask then builds upon this foundation to provide a complete web framework.
"""

from flask import Flask, render_template, request, redirect, flash, send_file, make_response
from werkzeug.utils import secure_filename
from models.Predict import Predictor
import os
from models.Predict import Predictor
from models.Velocity_assigner.assign_velocity import VelocityAssigner

predictor = Predictor()
# va = VelocityAssigner()

#Save images to the 'static' folder as Flask serves images from this directory
UPLOAD_FOLDER = 'static/midi/'

#Create an app object using the Flask class. 
app = Flask(__name__, static_folder="static")

#Add reference fingerprint. 
#Cookies travel with a signature that they claim to be legit. 
#Legitimacy here means that the signature was issued by the owner of the cookie.
#Others cannot change this cookie as it needs the secret key. 
#It's used as the key to encrypt the session - which can be stored in a cookie.
#Cookies should be encrypted if they contain potentially sensitive information.
app.secret_key = "secret key"

#Define the upload folder to save images uploaded by the user. 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Define the route to be home. 
#The decorator below links the relative route of the URL to the function it is decorating.
#Here, index function is with '/', our root directory. 
#Running the app sends us to index.html.
#Note that render_template means it looks for the file in the templates folder. 
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def submit_file():
    global res_path
    if request.method == 'POST':
        # Check if the file is present in the request
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        
        # Check if the file name is empty
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        
        # Check the file size
        if 'file' in request.files and request.files['file'].content_length > 5 * 1024 * 1024:  # 5 MB
            flash('File size exceeds 5 MB. Please upload a smaller file.')
            return redirect(request.url)
        
        if file:
            filename = secure_filename(file.filename)  # Use this werkzeug method to secure filename.
            save_path = os.path.join(app.config['UPLOAD_FOLDER'],'user_file.midi')
            file.save(save_path)
            res_path = predictor.generate_drum(save_path)

            checkbox_value = request.form.get('assing-velocity', None)

            if checkbox_value == 'on':
                # print('[+] calculating velocities')
                # va.assing_velocity2midi(res_path) #! overwrites the given drum midi file
                print('[+] velocity assigner disabled')


            label = "Drum successfully generated"
            flash(label)
            full_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            flash(full_filename)
            return redirect('/download')



@app.route('/download')
def download_file():
    global res_path
    # Generate or fetch the file content dynamically
    with open(res_path,'rb') as f:
        file_content = f.read()

    # Create a response with the file content as attachment
    response = make_response(file_content)

    # Set the appropriate content type and headers for file download
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = 'attachment; filename="'+os.path.basename(res_path)+'"'
    redirect('/')

    return response

if __name__ == "__main__":
    print("[+] RUNNING")
    # port = int(os.environ.get('PORT', 3009)) #Define port so we can map container port to localhost
    # app.run(host='0.0.0.0', port=port)  #Define 0.0.0.0 for Docker
    app.run()

