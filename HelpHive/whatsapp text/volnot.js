// Volunteer dashboard script
// This would be on the volunteer's side of the application

// Sample data structure for volunteer matches/requests
const volunteerRequests = [
    {
        id: 101,
        seekerId: 5001,
        seekerName: "Amit Kumar",
        requestDate: "2025-03-09T14:30:00",
        needType: "Technical Help",
        status: "pending" // pending, accepted, declined
    },
    {
        id: 102,
        seekerId: 5002,
        seekerName: "Neha Reddy",
        requestDate: "2025-03-10T09:15:00",
        needType: "Career Advice",
        status: "pending"
    }
];

// DOM elements
const requestsContainer = document.getElementById('requests-container');
const notificationBadge = document.getElementById('notification-badge');

// Update notification badge
function updateNotificationBadge() {
    const pendingRequests = volunteerRequests.filter(req => req.status === 'pending').length;
    
    if (pendingRequests > 0) {
        notificationBadge.textContent = pendingRequests;
        notificationBadge.style.display = 'flex';
    } else {
        notificationBadge.style.display = 'none';
    }
}

// Display help requests
function displayRequests() {
    requestsContainer.innerHTML = '';
    
    if (volunteerRequests.length === 0) {
        requestsContainer.innerHTML = '<p class="no-requests">You have no pending help requests.</p>';
        return;
    }
    
    volunteerRequests.forEach(request => {
        const requestCard = document.createElement('div');
        requestCard.className = `request-card ${request.status}`;
        
        // Format date
        const requestDate = new Date(request.requestDate);
        const formattedDate = requestDate.toLocaleDateString('en-IN', {
            day: 'numeric',
            month: 'short',
            year: 'numeric'
        });
        
        const formattedTime = requestDate.toLocaleTimeString('en-IN', {
            hour: '2-digit',
            minute: '2-digit'
        });
        
        // Create request card HTML
        requestCard.innerHTML = `
            <div class="request-header">
                <h3>Request from ${request.seekerName}</h3>
                <span class="request-date">${formattedDate} at ${formattedTime}</span>
            </div>
            <p>Help needed: ${request.needType}</p>
            <div class="request-actions">
                ${request.status === 'pending' ? `
                    <button class="accept-btn" data-id="${request.id}">Accept</button>
                    <button class="decline-btn" data-id="${request.id}">Decline</button>
                ` : request.status === 'accepted' ? `
                    <a href="https://wa.me/+91XXXXXXXXXX?text=Hello%20${encodeURIComponent(request.seekerName)},%20I%20am%20responding%20to%20your%20help%20request." class="whatsapp-btn" target="_blank">
                        <img src="whatsapp-icon.png" alt="WhatsApp"> Connect on WhatsApp
                    </a>
                ` : `
                    <span class="declined-message">You declined this request</span>
                `}
            </div>
        `;
        
        requestsContainer.appendChild(requestCard);
        
        // Add event listeners if pending
        if (request.status === 'pending') {
            const acceptBtn = requestCard.querySelector('.accept-btn');
            const declineBtn = requestCard.querySelector('.decline-btn');
            
            acceptBtn.addEventListener('click', () => handleRequestResponse(request.id, 'accepted'));
            declineBtn.addEventListener('click', () => handleRequestResponse(request.id, 'declined'));
        }
    });
}

// Handle accept/decline response
function handleRequestResponse(requestId, status) {
    // Find the request in our data
    const requestIndex = volunteerRequests.findIndex(req => req.id === requestId);
    
    if (requestIndex !== -1) {
        // Update status
        volunteerRequests[requestIndex].status = status;
        
        // In a real app, you would send this update to your backend
        console.log(`Request ${requestId} ${status}`);
        
        // Refresh the UI
        displayRequests();
        updateNotificationBadge();
    }
}

// Initialize notification system
function initializeNotifications() {
    // This would normally connect to a real-time notification system
    // For example, using WebSockets or Firebase
    console.log('Notification system initialized');
    
    // Simulate receiving a new request (in a real app this would come from your backend)
    setTimeout(() => {
        const newRequest = {
            id: 103,
            seekerId: 5003,
            seekerName: "Sunita Verma",
            requestDate: new Date().toISOString(),
            needType: "Mentoring",
            status: "pending"
        };
        
        volunteerRequests.push(newRequest);
        
        // Show notification
        showNewRequestNotification(newRequest);
        
        // Update UI
        displayRequests();
        updateNotificationBadge();
    }, 10000); // Simulate after 10 seconds
}

// Show browser notification for new request
function showNewRequestNotification(request) {
    // Check if browser supports notifications
    if (!("Notification" in window)) {
        console.log("This browser does not support desktop notifications");
        return;
    }
    
    // Check if permission is already granted
    if (Notification.permission === "granted") {
        createNotification(request);
    }
    // Otherwise, ask for permission
    else if (Notification.permission !== "denied") {
        Notification.requestPermission().then(permission => {
            if (permission === "granted") {
                createNotification(request);
            }
        });
    }
}

// Create the notification
function createNotification(request) {
    const notification = new Notification("New Help Request", {
        body: `${request.seekerName} needs help with ${request.needType}`,
        icon: "notification-icon.png" // Add your icon
    });
    
    notification.onclick = function() {
        window.focus();
        notification.close();
    };
}

// Initialize the app
document.addEventListener('DOMContentLoaded', () => {
    displayRequests();
    updateNotificationBadge();
    initializeNotifications();
});