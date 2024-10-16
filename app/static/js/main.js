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
            image.classList.add("img-fluid"); // Adjust image width as needed
            imagePreview.innerHTML = ""; // Clear previous image if any
            imagePreview.appendChild(image);
        });

        reader.readAsDataURL(file);
        customTxt.innerHTML = file.name; // Display file name
    } else {
        customTxt.innerHTML = "No file chosen, yet.";
        imagePreview.innerHTML = ""; // Clear image preview
    }
});

// Handle form submission
imageForm.addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent default form submission

    // Create FormData object to send files and prompt
    const formData = new FormData();
    formData.append("file", realFileBtn.files[0]); // Append file
    formData.append("prompt", document.getElementById("prompt").value); // Append prompt text

    // Indicate loading state (optional)
    const loadingText = document.createElement("p");
    loadingText.textContent = "Uploading and processing your image...";
    imagePreview.innerHTML = ""; // Clear previous previews
    imagePreview.appendChild(loadingText); // Show loading message

    // Use fetch to send form data to the Flask app
    fetch('/upload', { // Update this URL to match your Flask endpoint
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // Expecting a JSON response
    })
    .then(data => {
        // Handle the response data here
        if (data.success) {
            // If the response indicates success, you can show the edited image
            const editedImage = document.createElement("img");
            editedImage.src = `/static/edited/${data.edited_image}`; // Update this path if necessary
            editedImage.classList.add("img-fluid");
            imagePreview.innerHTML = ""; // Clear previous previews
            imagePreview.appendChild(editedImage); // Display edited image
        } else {
            // Handle errors if needed
            alert(data.error || "Error uploading the image."); // Display specific error message if available
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred while uploading the image.");
    });
});
