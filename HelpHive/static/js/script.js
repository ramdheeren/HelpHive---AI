const API_BASE_URL = ""; // Ensure backend URL consistency

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(sendLocation, showError);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

async function sendLocation(position) {
    let lat = position.coords.latitude;
    let lon = position.coords.longitude;

    try {
        const response = await fetch('/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ latitude: lat, longitude: lon })
        });

        if (!response.ok) {
            throw new Error(`Location request failed: ${response.status}`);
        }

        await response.json();
        document.getElementById("preferred-location").innerText = "Location saved successfully.";
    } catch (error) {
        document.getElementById("preferred-location").innerText = "Unable to save your location.";
        console.error("Error saving location:", error);
    }
}

function showError(error) {
    const messages = {
        1: "Location permission was denied.",
        2: "Your location is currently unavailable.",
        3: "Location request timed out."
    };
    document.getElementById("preferred-location").innerText = messages[error.code] || "Unable to get your location.";
}

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("requestForm");
    const requestsList = document.getElementById("requestsList");
    const notificationsList = document.getElementById("notifications");
    const matchesByRequestId = new Map();

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

            const responseData = await response.json();
            displayMatches(responseData.request.id, responseData.matches || []);
            console.log("Request submitted successfully.");
            fetchRequests();
            form.reset();
            addNotification("✅ Request submitted successfully.");
        } catch (error) {
            console.error("Error submitting request:", error);
            addNotification("❌ Error connecting to the server.");
        }
    });

    function displayMatches(requestId, matches) {
        matchesByRequestId.set(requestId, matches);
    }

    function appendMatches(requestCard, requestId) {
        if (!matchesByRequestId.has(requestId)) return;

        const matches = matchesByRequestId.get(requestId);
        const matchSection = document.createElement("div");
        matchSection.classList.add("notification");

        if (!matches.length) {
            matchSection.textContent = "No matching volunteers found.";
            requestCard.appendChild(matchSection);
            return;
        }

        const heading = document.createElement("p");
        heading.textContent = "Matching volunteers:";
        matchSection.appendChild(heading);

        matches.forEach(match => {
            const volunteer = document.createElement("p");
            volunteer.textContent = `${match.first_name || ""} ${match.last_name || ""} | Skills: ${match.skills || "Not specified"} | Radius: ${match.radius || "Not specified"} | Days: ${match.days || "Not specified"}`;
            matchSection.appendChild(volunteer);
        });

        requestCard.appendChild(matchSection);
    }

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
            appendMatches(requestCard, req.id);
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
