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
app.config['UPLOAD_PATH'] = 'static/uploads'

# Ensure the upload directory exists
os.makedirs(app.config['UPLOAD_PATH'], exist_ok=True)

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

def visualize_output(input_img_file, output_dir):
    item_dir = os.listdir(output_dir)[0]
    item_res_dir = os.path.join(output_dir, item_dir, 'results')

    final_output_file = os.path.join(item_res_dir, 'final_output.png')

    # Plot and save images
    plot_single_image(input_img_file, title='Input Image')
    plot_single_image(final_output_file, title='Edited Image')

    # Save the edited image
    output_image_path = 'edited/edited_image.png'
    cv2.imwrite(output_image_path, cv2.imread(final_output_file))
    print(f'Edited image saved at: {output_image_path}')

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Save uploaded file
        file = request.files['file']
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_PATH'], filename)
        file.save(file_path)

        # Call the training script (you may want to adjust parameters as needed)
        subprocess.run(['torchrun', '--nnodes=1', '--nproc_per_node=1', 'train.py',
                        '--image_file_path', file_path,
                        '--image_caption', 'trees',
                        '--editing_prompt', 'a big tree with many flowers in the center',
                        '--diffusion_model_path', 'stabilityai/stable-diffusion-2-inpainting',
                        '--output_dir', 'output/',
                        '--draw_box', '--lr', '5e-3',
                        '--max_window_size', '15', '--per_image_iteration', '7',
                        '--epochs', '1', '--num_workers', '8',
                        '--seed', '42', '--pin_mem',
                        '--point_number', '6', '--batch_size', '1'])

        # Visualize output
        visualize_output(file_path, 'output/')

    return render_template("index.html")

if __name__ == '__main__':
    app.run(port=port_no)
