from flask import Flask
import json
from sentence_transformers import SentenceTransformer
from flask import  jsonify, request
import os 
import torch
import flask
import uuid
from read_data_from_pdf import read_pfd_folder
from data_to_vec import convert_to_vector,search
from compare_resume import get_result
import shutil


app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload():

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2', device=device)

    
    directory = str(uuid.uuid4())
    parent_dir = "./data_cach/"
    path = os.path.join(parent_dir, directory)
    os.mkdir(path)
    if flask.request.method == "POST":
        files = flask.request.files.getlist("file")
        for file in files:
            file.save(os.path.join(path, file.filename))
    data_from_pdf =  read_pfd_folder(path)

 
    if (flask.request.values['name'] == ''):
        error = {
                "code": 400,
                "message": "REQUIRE FIELD 'Question'"
            }
        return jsonify(error), 400
    else:  
        jd = flask.request.values['name']
        k = int(flask.request.values['k'])
        print(k)
        index,data_pick = convert_to_vector(data_from_pdf,model)
        result = search(jd,index,5,model)
        Compare_Resume = get_result(jd,data_pick,result,directory)
        dir = './data_cach'
        for files in os.listdir(dir):
            path = os.path.join(dir, files)
            try:
                shutil.rmtree(path)
            except OSError:
                os.remove(path)
        print(Compare_Resume)

    response ={
        "status": True,
        "code": 200,
        "message": "Success",
        "results": Compare_Resume,
        "reference": ""
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8400)