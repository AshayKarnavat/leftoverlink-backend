// script.js
const BACKEND_URL = "https://leftoverlink-backend.onrender.com";


console.log("script.js loaded");

window.onload = function() {
    const currentSection = localStorage.getItem("currentSection");
    if(currentSection){
        showSection(currentSection);
    } else {
        showSection("home"); // only default if nothing is stored
    }

    const donateForm = document.getElementById("donate-form");
        donateForm.addEventListener("submit", (e) => {
            e.preventDefault();

            const food = document.getElementById("foodname").value;
            const quantity = document.getElementById("foodquantity").value;
            const location = document.getElementById("foodlocation").value;
            const user_id = localStorage.getItem("user_id"); // optional

            fetch(`${BACKEND_URL}/donations`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ food, quantity, location, user_id })
            })
            .then(res => res.json())
            .then(data => {
                console.log("Donation response:", data);
                alert(data.message);
                donateForm.reset();

                // Step 2: render the new donation card
                renderHomeDonations([data.donation]); // we’ll update the function next
            })
            .catch(err => console.error(err));
        });


    fetch(`${BACKEND_URL}/donations`, {
        method: "GET",
    })
    .then(response => response.json())
    .then(data => {
        console.log("All donations from server:", data);
        renderHomeDonations(data); // render all existing donations
    })
    .catch(error => {
        console.error("Something went wrong:", error);
    });




    // Update Profile username
    const username = localStorage.getItem("username");
    if(username){
        const profileUsernameEl = document.getElementById("profile-username");
        if(profileUsernameEl) profileUsernameEl.textContent = username;
    }

    // Handle logout inside Profile section
    const logoutBtn = document.getElementById("logout-btn");
    if(logoutBtn){
        logoutBtn.addEventListener("click", () => {
            localStorage.clear();
            window.location.href = "index.html"; // redirect to login page
        });
    }
}

function showSection(id) {
    console.log("showSection called for:", id); 
    ["home","donate","search","profile"].forEach(section => {
        const el = document.getElementById(section);
        if(el) el.style.display = "none";
    });

    const target = document.getElementById(id);
    if(target){
        if(id === "home") target.style.display = "flex";
        else target.style.display = "block";
    }
    // store last section
    localStorage.setItem("currentSection", id);
}

const logoutLink = document.getElementById("logout-link");
logoutLink.addEventListener("click", (e) => {
    e.preventDefault();
    localStorage.clear();
    window.location.href = "index.html"; // redirect to login page
});

//rendering cards from database in home-food-grid-id {index.html home section}
function renderHomeDonations(donations){
    const container = document.getElementById("home-food-grid");

    donations.forEach(donation => {
        const card = document.createElement("div");
        card.className = "card";

        card.innerHTML = `
            <img src="./images/${donation.food.toLowerCase()}.jpg" alt="${donation.food}">
            <h3>${donation.food}</h3>
            <p>Quantity: ${donation.quantity}, Location: ${donation.location}</p>
        `;

        container.append(card);
    });
}

//fetching from donations route
fetch(`${BACKEND_URL}/donations`,{
    method:"GET",
})
    .then(response => response.json())
    .then(data =>{
        console.log("daan kra hua from the server:",data);
        renderHomeDonations(data)
    })    
    .catch(error => {
        console.log("Something went wrong:",error);
    })

    