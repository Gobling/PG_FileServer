import os
import pathlib
import urllib.parse
from PIL import Image

project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, './')

from flask import Flask, render_template, request, redirect, jsonify, make_response
from flask import send_from_directory
#from flask import Response
#from flask import stream_with_context
#import requests

from flask_cors import CORS
from werkzeug.utils import secure_filename

#SLIDE_DIR = '/home/andreas/data/openslideimages'

#app = Flask(__name__, template_folder=template_path)
app = Flask(__name__)

CORS(app) # Added for cross-site access!!
#cors = CORS(app, resources={"/*": {"origins": "*"}})

@app.route("/")
def index():
    return "hello index"

@app.route("/upload-file", methods=["GET", "POST","OPTIONS"])
def upload_image ():

    print("starting upload-file")
#    if request.method == "OPTIONS":
#        print("requesting options")
#        resp = jsonify(success=True)
#        return resp

    if request.method == "POST":
        print("requesting post")
        if request.files:

            file = request.files["file"]
            fileName = request.form["fileName"]
            tmpPath = request.form["filePath"]
            if tmpPath[0] != "/":
                tmpPath = "/" + tmpPath
            filePath = "/data" + tmpPath

            #get file extension looking for last .  in fileName
            rev_fileName = fileName[::-1]
            tmpExtIndex = len(fileName) - rev_fileName.index(".")
            # split fileName to get extension
            shortFileName = fileName[0:tmpExtIndex]
            fileExtension = fileName[tmpExtIndex:len(fileName)].lower()

            print("fileName: " + fileName)
            print("filePath: " + filePath)
            print("fileExtension: " + fileExtension)

            if fileName != "":

                #filenameSec = secure_filename(urllib.parse.unquote(fileName))
                filenameSec = urllib.parse.unquote(fileName)
                #basedir = os.path.abspath(os.path.dirname(__file__))
                #print("Basedir : " + basedir)
                #file.save(os.path.join(filePath, filenameSec))
                try:
                    #pathlib.Path(os.path.join("/data", filePath)).mkdir(parents=True, exist_ok=True)
                    os.makedirs(filePath, exist_ok = True)
                    print("Directory '%s' created successfully" %filePath)
                except OSError as error:
                    print("Directory '%s' could not be created" %filePath)

                file.save(os.path.join(filePath, filenameSec))

                # if file is image and extension is tif or tiff, convert image to jpg after saving
                if fileExtension=="tif":
#                if filePath.index("/images") > -1 and (fileExtension=="tif" or fileExtension=="tiff"):
                    image_object = Image.open(os.path.join(filePath, filenameSec))
                    newFileName = shortFileName + "jpg"
                    if image_object.mode != "RGB":
                        print("Converting to rgb")
                        image_object = image_object.convert("RGB")
                    image_object.save(os.path.join(filePath, newFileName))
                    print("converted and saved file as: " + newFileName)
                    # need code to delete old file or better to keep it?

                print("Document saved: " + filenameSec)

                resp = jsonify(success=True)
                return resp
                # return "document uploaded"

    #return "No document uploaded"
    resp = jsonify(success=True)
    return resp


# Download from provided URL.
#@app.route('/<path:url>')
#def download(url):
    #req = requests.get(url, stream=True)
    #return Response(stream_with_context(req.iter_content()), content_type=req.headers['content-type'])

@app.route('/getdocument/<path:path>')
def send_document(path):
    print("Path: " + path)
    #get last / in path
    rev_path = path[::-1]
    tmpIndex = len(path) - rev_path.index("/")
    # split path to directory and filename
    tmpDirectory =  "/data/" + path[0:tmpIndex]
    tmpFileName = path[tmpIndex:len(path)]
    tmpFileName = tmpFileName.replace("&23","#")
    #fileNameSec = secure_filename(urllib.parse.unquote(tmpFileName))
    fileNameSec = urllib.parse.unquote(tmpFileName)
    print("Dir + Name: " + tmpDirectory + " " + fileNameSec)
    return send_from_directory(tmpDirectory, fileNameSec)


@app.route('/getimage/<path:path>')
def send_image(path):
    print("Path: " + path)
    #get last / in path
    rev_path = path[::-1]
    tmpIndex = len(path) - rev_path.index("/")
    # split path to directory and filename
    tmpDirectory =  "/data/" + path[0:tmpIndex]
    tmpFileName = path[tmpIndex:len(path)]
    tmpFileName = tmpFileName.replace("&23","#")
    #fileNameSec = secure_filename(urllib.parse.unquote(tmpFileName))
    fileNameSec = urllib.parse.unquote(tmpFileName)
    print("Dir + Name: " + tmpDirectory + " " + fileNameSec)
    return send_from_directory(tmpDirectory, fileNameSec)


if __name__== "__main__":
    app.run(host='0.0.0.0', port=8000)
    print("server is running")
