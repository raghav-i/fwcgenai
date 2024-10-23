let menu = document.querySelector('#menu-bar');
let nav = document.querySelector('.nav');
let chatbotVisible = false;

menu.onclick = () => {
    menu.classList.toggle('fa-times');
    nav.classList.toggle('active');
}

let section = document.querySelectorAll('section');
let navLinks = document.querySelectorAll('header .nav a');

window.onscroll = () => {
    menu.classList.remove('fa-times');
    nav.classList.remove('active');

    section.forEach(sec => {
        let top = window.scrollY;
        let height = sec.offsetHeight;
        let offset = sec.offsetTop - 150;
        let id = sec.getAttribute('id');

        if (top >= offset && top < offset + height) {
            navLinks.forEach(links => {
                links.classList.remove('active');
                document.querySelector('header .nav a[href*=' + id + ']').classList.add('active');
            });
        };
    });
}

document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('send-message').onclick = function () {
      const userInput = document.getElementById('user-input');
      const message = userInput.value.trim();

      if (message) {
          addMessage(message);
          fetch('/chat', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify({ message: message })
          })
          .then(response => {
              if (!response.ok) {
                  throw new Error('Network response was not ok');
              }
              return response.json();
          })
          .then(data => {
              const botResponse = data.response;
              addMessage(botResponse, false);
          })
          .catch(error => {
              console.error('There has been a problem with your fetch operation:', error);
          });

          userInput.value = '';
      }
  };
});


const realFileBtn = document.getElementById("real-file");
const customBtn = document.getElementById("custom-button");
const customTxt = document.getElementById("custom-text");
const imagePreview = document.getElementById("image-preview");

document.getElementById('file-upload').addEventListener('change', function (event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            const previewImage = document.getElementById('imagePreview');
            previewImage.src = e.target.result;
            previewImage.style.display = 'block'; 
        };
        reader.readAsDataURL(file); 
    }
});

customBtn.addEventListener("click", function () {
    realFileBtn.click();
});

realFileBtn.addEventListener("change", function () {
    const file = this.files[0];

    if (file) {
        const reader = new FileReader();

        reader.addEventListener("load", function () {
            const image = new Image();
            image.src = this.result;
            image.classList.add("w-100"); 
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



function toggleChatbot() {
    const chatbot = document.getElementById('chatbot');
    chatbotVisible = !chatbotVisible;
    chatbot.style.display = chatbotVisible ? 'block' : 'none';
}


document.getElementById('close-chatbot').onclick = function () {
    toggleChatbot();
};

function addMessage(message, isUser = true) {
  const messageDiv = document.createElement('div');
  messageDiv.innerHTML = message; 
  messageDiv.className = isUser ? 'user-message' : 'bot-message'; 
  document.getElementById('chatbot-messages').appendChild(messageDiv);
}

