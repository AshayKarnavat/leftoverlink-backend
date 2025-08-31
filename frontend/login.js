//login.js
const BACKEND_URL = "https://leftoverlink-backend.onrender.com";

// loginForm.js

const loginForm = document.getElementById("login-form");
const registerForm = document.getElementById("register-form");
const message = document.getElementById("message");

const showRegisterLink = document.getElementById("show-register");
const showLoginLink = document.getElementById("show-login");

// Toggle to Register
showRegisterLink.addEventListener("click", () => {
    loginForm.style.display = "none";
    registerForm.style.display = "block";
    message.textContent = "";
});

// Toggle to Login
showLoginLink.addEventListener("click", () => {
    registerForm.style.display = "none";
    loginForm.style.display = "block";
    message.textContent = "";
});

// Handle login submit
loginForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;

    fetch(`${BACKEND_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
    })
    .then(res => res.json())
    .then(data => {
        if(data.error){
            message.textContent = data.error;
            message.style.color = "red";
        } 
        else {
            message.textContent = data.message;
            message.style.color = "green";
            
            localStorage.setItem("user_id", data.user_id);
            localStorage.setItem("username", data.username); 
            setTimeout(() => {
                window.location.href = "home.html";
            }, 1000);
        }
    })
    .catch(err => console.error(err));
});

// Handle register submit
registerForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const username = document.getElementById("register-username").value;
    const email = document.getElementById("register-email").value;
    const password = document.getElementById("register-password").value;

    fetch(`${BACKEND_URL}/users`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, password }),
    })
    .then(res => res.json())
    .then(data => {
        if(data.error){
            message.textContent = data.error;
            message.style.color = "red";
        } 
        else {
            message.textContent = data.message + " Please login.";
            message.style.color = "green";
            registerForm.style.display = "none";
            loginForm.style.display = "block";
        }
    })
    .catch(err => console.error(err));
});
