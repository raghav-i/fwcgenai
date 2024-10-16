from flask import Flask, request, Response, render_template
from werkzeug.utils import secure_filename
import os
import subprocess
import cv2
import matplotlib.pyplot as plt
import torch
from pyngrok import ngrok

# Flask app setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_PATH'] = 'static/uploads'  # Upload directory
app.config['EDITED_PATH'] = 'static/edited'  # Directory for edited images

# Ensure the upload and edited directories exist
os.makedirs(app.config['UPLOAD_PATH'], exist_ok=True)
os.makedirs(app.config['EDITED_PATH'], exist_ok=True)

# Set the port for the Flask app
port_no = 5000

# Set ngrok authentication token (replace with your own token)
ngrok.set_auth_token("2dDIoLlPFXbh3Mynt1AS6xejBaR_5QNdrAv2uRqReqS1WJQ4o")
public_url = ngrok.connect(port_no).public_url
print(f"To access the global link, please click {public_url}")

# Visualization code
def plot_single_image(img_file_path, title):
    img_bgr = cv2.imread(img_file_path)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    plt.imshow(img_rgb)
    plt.axis('off')
    plt.title(title)
    plt.show()

def visualize_output(input_img_file, edited_img_file):
    # Plot and save images
    plot_single_image(input_img_file, title='Input Image')
    plot_single_image(edited_img_file, title='Edited Image')

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Save uploaded file
        file = request.files['file']
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_PATH'], filename)
        file.save(file_path)

        # Retrieve the user-provided prompt from the form
        editing_prompt = request.form['prompt']  # Get the prompt input

        # Call the training script (you may want to adjust parameters as needed)
        subprocess.run(['torchrun', '--nnodes=1', '--nproc_per_node=1', 'train.py',
                        '--image_file_path', file_path,
                        '--image_caption', 'trees',  # You can customize this as needed
                        '--editing_prompt', editing_prompt,  # Use the user-provided prompt here
                        '--diffusion_model_path', 'stabilityai/stable-diffusion-2-inpainting',
                        '--output_dir', app.config['EDITED_PATH'],  # Use the same path for output
                        '--draw_box', '--lr', '5e-3',
                        '--max_window_size', '15', '--per_image_iteration', '7',
                        '--epochs', '1', '--num_workers', '8',
                        '--seed', '42', '--pin_mem',
                        '--point_number', '6', '--batch_size', '1'])

        # Define the path for the edited image (assumes a single output)
        edited_image_path = os.path.join(app.config['EDITED_PATH'], 'edited_image.png')  # Adjust based on your training script

        # Visualize output
        visualize_output(file_path, edited_image_path)

    return render_template("index.html")

if __name__ == '__main__':
    app.run(port=port_no)
