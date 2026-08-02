const API_BASE_URL = "http://127.0.0.1:8000"; // Ensure backend URL consistency

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(sendLocation, showError);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

function sendLocation(position) {
    let lat = position.coords.latitude;
    let lon = position.coords.longitude;
    
    fetch('/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ latitude: lat, longitude: lon })
    })
    .then(response => response.json());
    // .then(data => {
    //     document.getElementById("location").innerText = `Location saved: ${lat}, ${lon}`;
    // });
}

function showError(error) {
    alert("Error getting location: " + error.message);
}

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("requestForm");
    const requestsList = document.getElementById("requestsList");
    const notificationsList = document.getElementById("notifications");

    // ✅ Fetch stored requests from backend
    async function fetchRequests() {
        try {
            console.log("Fetching requests from:", `${API_BASE_URL}/requests`);
            const response = await fetch(`${API_BASE_URL}/requests`);

            if (!response.ok) throw new Error(`Server Error: ${response.status}`);

            const requests = await response.json();
            console.log("Received requests:", requests);
            displayRequests(requests);
        } catch (error) {
            console.error("Error fetching requests:", error);
            addNotification("❌ Error fetching requests. Check console for details.");
        }
    }

    // ✅ Submit request to backend
    form.addEventListener("submit", async function (event) {
        event.preventDefault();
        
        const name = document.getElementById("name").value.trim();
        const requestDetails = document.getElementById("requestDetails").value.trim();
        requestStatus = "awaiting-response";

        if (!name || !requestDetails) {
            addNotification("⚠ Please fill out all fields.");
            return;
        }

        try {
            console.log("Submitting request:", { name, requestDetails });

            const response = await fetch(`${API_BASE_URL}/requests`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name, requestDetails, requestStatus })
            });

            if (!response.ok) throw new Error(`Failed to submit request: ${response.status}`);
            
            console.log("Request submitted successfully.");
            fetchRequests();
            form.reset();
            addNotification("✅ Request submitted successfully.");
        } catch (error) {
            console.error("Error submitting request:", error);
            addNotification("❌ Error connecting to the server.");
        }
    });

    // ✅ Display requests in UI with event delegation
    function displayRequests(requests) {
        requestsList.innerHTML = requests.length ? "" : "<p>No requests available.</p>";

        requests.forEach(req => {
            const requestCard = document.createElement("div");
            requestCard.classList.add("request-card");
            requestCard.innerHTML = `
                <p><strong>${req.name}</strong>: ${req.requestDetails}</p>
                <div class="btn-group">
                    <button class="accept" data-id="${req.id}">Accept</button>
                    <button class="reject" data-id="${req.id}">Reject</button>
                </div>
            `;
            requestsList.appendChild(requestCard);
        });

        console.log("Displayed requests:", requests);
    }

    // ✅ Event delegation for Accept/Reject buttons
    requestsList.addEventListener("click", async function (event) {
        const button = event.target;
        if (button.classList.contains("accept")) {
            await handleRequest(button.dataset.id, "accept");
        } else if (button.classList.contains("reject")) {
            await handleRequest(button.dataset.id, "reject");
        }
    });

    // ✅ Accept or Reject request and notify
    async function handleRequest(id, action) {
        try {
            console.log(`Attempting to ${action} request with ID: ${id}`);

            const response = await fetch(`${API_BASE_URL}/requests/${id}/${action}`, {
                method: "PATCH",
            });

            if (!response.ok) throw new Error(`Failed to ${action} request: ${response.status}`);
            
            console.log(`Request ${action}ed successfully.`);
            addNotification(action === "accept" ? "✔ Request accepted." : "❌ Request rejected.");
            fetchRequests();
        } catch (error) {
            console.error(`Error ${action}ing request:`, error);
            addNotification("❌ Error connecting to server.");
        }
    }

    // ✅ Show notification for actions with limit
    function addNotification(message) {
        if (notificationsList.children.length > 5) {
            notificationsList.removeChild(notificationsList.firstChild);
        }

        const notification = document.createElement("div");
        notification.classList.add("notification");
        notification.innerHTML = `<p>${message}</p>`;
        notificationsList.appendChild(notification);

        // Auto-remove after 5 seconds
        setTimeout(() => notification.remove(), 5000);
    }

    fetchRequests(); // Load requests on page load
});
