let menu = document.querySelector('#menu-bar');
let nav = document.querySelector('.nav');

menu.onclick = () => {
    menu.classList.toggle('fa-times');
    nav.classList.toggle('active');
}

const realFileBtn = document.getElementById("real-file");
const customBtn = document.getElementById("custom-button");
const customTxt = document.getElementById("custom-text");
const imagePreview = document.getElementById("image-preview");
const imageForm = document.getElementById("image-form");

// Open file dialog when custom button is clicked
customBtn.addEventListener("click", function() {
    realFileBtn.click();
});

// Preview selected image
realFileBtn.addEventListener("change", function() {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.addEventListener("load", function() {
            const image = new Image();
            image.src = this.result;
            image.classList.add("img-fluid");
            imagePreview.innerHTML = "";
            imagePreview.appendChild(image);
        });
        reader.readAsDataURL(file);
        customTxt.innerHTML = file.name;
    } else {
        customTxt.innerHTML = "No file chosen, yet.";
        imagePreview.innerHTML = "";
    }
});

// Handle form submission
imageForm.addEventListener("submit", function(event) {
    event.preventDefault();
    const formData = new FormData();
    formData.append("file", realFileBtn.files[0]);
    formData.append("prompt", document.getElementById("prompt").value);

    const loadingText = document.createElement("p");
    loadingText.textContent = "Uploading and processing your image...";
    imagePreview.innerHTML = "";
    imagePreview.appendChild(loadingText);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
    })
    .then(data => {
        if (data.success) {
            const editedImage = new Image();
            editedImage.src = `static/edited/${data.edited_image}`;
            editedImage.classList.add("img-fluid");
            imagePreview.innerHTML = "";
            imagePreview.appendChild(editedImage);
        } else {
            alert(data.error || "Error uploading the image.");
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred while uploading the image.");
    });
});
