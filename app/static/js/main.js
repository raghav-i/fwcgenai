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

customBtn.addEventListener("click", function() {
    realFileBtn.click();
});

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
    event.preventDefault();
    // Add logic here to handle the form data submission to the server
    // You can use fetch or axios to send the image and prompt to your Flask app
});
