# Tragicbyte

## Project Description
Tragicbyte is a text-based image editor powered by generative AI, enabling users to transform their images through descriptive prompts. This web application aims to provide a seamless editing experience, making it accessible to a diverse audience while showcasing the potential of AI-driven creativity. (Website building in progress)

## Tech Stack
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Backend:** Flask
- **AI Model:** Stable Diffusion Inpainting
- **Hosting:** ngrok
- **Version Control:** Git

## Tools and Trends Used
- Generative AI for image editing
- Text-to-image transformation technologies
- 3D modeling and augmented reality frameworks (future plans)

## Project Dependencies
- Flask
- torch
- albumentations
- other necessary libraries (list them as needed)

## Project Idea Roadmap
1. **Phase 1:** Implement text-based image editing while maintaining consistency.
2. **Phase 2:** Develop capabilities to convert edited images into 3D models.
3. **Phase 3:** Integrate 3D models into an AR experience.
4. **Phase 4:** Create a fully generative AR application.

## Innovation
Tragicbyte's roadmap lays out a clear and structured progression towards a fully generative AR experience. This innovation aims to merge traditional image editing with cutting-edge technologies, allowing users to engage with their images in entirely new dimensions.

## Technical Complexity
The application requires extensive generation time due to the complexities of the AI models used for inpainting and generating images. Optimizing performance while maintaining quality is a key challenge.

## Go-To-Market Strategy
- **Target Audience:** 
  - Individuals interested in skincare and beauty.
  - Professionals in dermatology and aesthetics.
  - Content creators and influencers.
  - Designers and artists looking for innovative editing tools.
  - General consumers wanting creative image editing experiences.
  
- **Marketing Channels:** 
  - Social media campaigns targeting beauty and skincare communities.
  - Collaborations with influencers and industry professionals.
  - Content marketing through blogs and tutorials demonstrating the application.

- **Launch Strategy:** 
  - A phased launch beginning with a closed beta to gather user feedback.
  - Gradually opening access to a wider audience while refining the application based on user insights.

## Societal and Market Impact
Tragicbyte aims to democratize advanced image editing, making it accessible to a wide range of users. By leveraging generative AI, the application not only enhances personal creativity but also has the potential to reshape industries like skincare, fashion, and marketing. As users gain access to sophisticated editing tools, the overall quality of visual content across platforms is expected to rise, benefiting both creators and consumers.

## Running
On colab:

```
!git clone https://github.com/raghav-i/fwcgenai
%cd fwcgenai
```
```
!wget https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Linux-x86_64.sh
!bash Mambaforge-Linux-x86_64.sh -b -f -p /usr/local
!export PATH=/usr/local/bin/:$PATH

!pip install opencv-python torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cu118
!pip install timm einops albumentations matplotlib tensorboard jax accelerate
!pip install diffusers ftfy madgrad openai-clip numpy transformers
!pip install flask pyngrok
```
```
# Visualization code
import matplotlib.pyplot as plt
import os
import cv2
def plot_single_image(img_file_path, title):
  # Load and display the image
  img_bgr = cv2.imread(img_file_path)
  img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
  plt.imshow(img_rgb)
  plt.axis('off')  # Hide axes
  plt.title(title)  # Set the title of the plot
  plt.show()

def visualize_output(input_img_file, output_dir):
  item_dir = os.listdir(output_dir)[0]
  item_res_dir = os.path.join(output_dir, item_dir, 'results')

  final_output_file = os.path.join(item_res_dir, 'final_output.png')
  plot_single_image(input_img_file, title='Input Image')
  plot_single_image(final_output_file, title='Edited Image')

plot_single_image('choose your image', title='Input Image')
```
```
# Set point_number as 6 and per_image_iteration as 7 for faster editing.
# Since runwayml has removed its impressive inpainting model 'runwayml/stable-diffusion-inpainting',
# so just set `--diffusion_model_path 'stabilityai/stable-diffusion-2-inpainting'`.

!torchrun --nnodes=1 --nproc_per_node=1 train.py \
  --image_file_path images/1.png \
  --image_caption 'trees' \
  --editing_prompt 'enter your prompt' \
  --diffusion_model_path 'stabilityai/stable-diffusion-2-inpainting' \
  --output_dir output/ \
  --draw_box \
  --lr 5e-3 \
  --max_window_size 15 \
  --per_image_iteration 7 \
  --epochs 1 \
  --num_workers 8 \
  --seed 42 \
  --pin_mem \
  --point_number 6 \
  --batch_size 1
  ```
  ```
  # Visualize the output
print('Editing prompt:', 'your prompt')
visualize_output('your image', 'output')
```