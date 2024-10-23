from flask import Flask, request, render_template, jsonify  # Import jsonify
from werkzeug.utils import secure_filename
import os
import torch
from PIL import Image
import torchvision.transforms as T
import google.generativeai as genai
from dotenv import load_dotenv
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, TextAreaField
from wtforms.validators import InputRequired
import logging

load_dotenv()


# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_PATH'] = 'static/uploads'

# Set up the Gemini API key directly in the Flask app
app.config['GEMINI_API_KEY'] = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=app.config['GEMINI_API_KEY'])

# Define form for file upload
class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Submit")

def format_chat_response(response):

    while '**' in response:
        response = response.replace('**', '<strong>', 1)
        response = response.replace('**', '</strong>', 1)


    response = response.replace('.**', '.<br><br>')


    lines = response.splitlines()  
    formatted_lines = []
    for line in lines:
        if line.startswith('*'):
            line = line[1:].strip()  
            formatted_lines.append(f'<li>{line}</li>') 
        else:
            formatted_lines.append(line) 

    if formatted_lines:
        response = '<ul>' + ''.join(formatted_lines) + '</ul>'

    return response

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')  
    app.logger.info(f"Received message: {user_message}")  

    if user_message:
        response = get_gemini_response(user_message)  
        formatted_response = format_chat_response(response)  
        app.logger.info(f"Response from Gemini: {formatted_response}")  
        return jsonify({'response': formatted_response})  
    app.logger.warning("No message received")  
    return jsonify({'response': 'No message received'}), 400

def get_gemini_response(question):
    model = genai.GenerativeModel("gemini-pro")
    chat = model.start_chat(history=[])
    response = chat.send_message(question, stream=True)
    full_response = ""
    for chunk in response:
        full_response += chunk.text
    return full_response


def format_gemini_response(response):
    formatted_response = response
    while '**' in formatted_response:
        formatted_response = formatted_response.replace('**', '<strong>', 1)
        formatted_response = formatted_response.replace('**', '</strong>', 1)
    
  
    formatted_response = formatted_response.replace('\n', '<br>')
    return formatted_response




@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    res = None
    description = None
    form = UploadFileForm()
    chat_response = None  
    show_chat_form = False  

    if form.validate_on_submit():
        file = form.file.data  
        filename = secure_filename(file.filename)
        filepath = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_PATH'], filename)
        file.save(filepath)  

        # Perform image classification
        classes = ['acanthosis-nigricans', 'acne', 'acne-scars', 'alopecia-areata', 'dry', 'melasma', 'oily', 'vitiligo', 'warts']
        model = torch.load('./skin-model.pt', map_location=torch.device('cpu'))
        device = torch.device('cpu')
        model.to(device)
        img = Image.open(filepath).convert("RGB")
        tr = get_transforms()
        res = predict(model, img, tr, classes) 

        # Get description from Gemini based on the diagnosis
        diagnosis = f"The diagnosis is: {res}. Can you provide a simple explanation about this condition? Additionally, provide a simple remedy or treatment and other medical suggestions relevant."
        description = get_gemini_response(diagnosis)  # Fetch response from Gemini LLM
        description = format_gemini_response(description)

    return render_template("index2.html", form=form, res=res, description=description, chat_response=chat_response)





# Function to apply image transforms
def get_transforms():
    transform = []
    transform.append(T.Resize((512, 512)))
    transform.append(T.ToTensor())
    return T.Compose(transform)

def predict(model, img, tr, classes):
    img_tensor = tr(img)
    out = model(img_tensor.unsqueeze(0))
    pred, idx = torch.max(out, 1)
    return classes[idx]

if __name__ == '__main__':
    app.run(debug=True)
