import os
from flask import Flask, render_template

app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = os.path.abspath('./maps_overnight-viz/')
# Get a list of all image filenames from the 'static' folder
image_files = [f for f in os.listdir("static")]
@app.route('/')
def index():
    return render_template('index.html', image_files=image_files)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8000,debug=True)