// Volunteer dashboard script
// This would be on the volunteer's side of the application

// Sample data structure for volunteer matches/requests
const volunteerRequests = [
    {
        id: 101,
        seekerId: 5001,
        seekerName: "Amit Kumar",
        seekerPhone: "9876543210", // Added seeker phone
        volunteerPhone: "9123456789", // Added volunteer phone
        requestDate: "2025-03-09T14:30:00",
        needType: "Technical Help",
        status: "pending" // pending, accepted, declined
    },
    {
        id: 102,
        seekerId: 5002,
        seekerName: "Neha Reddy",
        seekerPhone: "9876543211", // Added seeker phone
        volunteerPhone: "9123456789", // Added volunteer phone
        requestDate: "2025-03-10T09:15:00",
        needType: "Career Advice",
        status: "pending"
    }
];

// DOM elements
const requestsContainer = document.getElementById('requests-container');
const notificationBadge = document.getElementById('notification-badge');

// Function to generate a WhatsApp link with a premade message
function generateWhatsAppLink(volunteerPhone, seekerPhone, seekerName, needType) {
    // Format phone numbers (remove any non-digit characters)
    const formattedVolunteerPhone = volunteerPhone.replace(/\D/g, '');
    const formattedSeekerPhone = seekerPhone.replace(/\D/g, '');
    
    // Create a customized greeting message (URL encoded)
    const message = encodeURIComponent(
        `Hello ${seekerName}! I'm a volunteer responding to your request for help with "${needType}". How can I assist you?`
    );
    
    // Generate the WhatsApp URL
    return `https://wa.me/${formattedSeekerPhone}?text=${message}`;
}

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
        requestCard.setAttribute('data-id', request.id);
        
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
                    <a href="${generateWhatsAppLink(
                        request.volunteerPhone,
                        request.seekerPhone,
                        request.seekerName,
                        request.needType
                    )}" class="whatsapp-btn" target="_blank">
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
        
        // If accepted, update UI with WhatsApp button immediately
        if (status === 'accepted') {
            const request = volunteerRequests[requestIndex];
            const requestCard = document.querySelector(`.request-card[data-id="${requestId}"]`);
            
            if (requestCard) {
                const actionsDiv = requestCard.querySelector('.request-actions');
                
                // Generate WhatsApp link
                const whatsappLink = generateWhatsAppLink(
                    request.volunteerPhone,
                    request.seekerPhone,
                    request.seekerName,
                    request.needType
                );
                
                // Update the actions div with WhatsApp button
                actionsDiv.innerHTML = `
                    <a href="${whatsappLink}" class="whatsapp-btn" target="_blank">
                        <img src="whatsapp-icon.png" alt="WhatsApp"> Connect on WhatsApp
                    </a>
                `;
                
                // Update the card class
                requestCard.className = `request-card accepted`;
                
                // Optional: Track the WhatsApp redirection (in a real app)
                // logWhatsAppRedirection(requestId);
            }
        } else {
            // For declined, just refresh the UI
            displayRequests();
        }
        
        // Update notification badge
        updateNotificationBadge();
    }
}

// Function to log WhatsApp redirection (would connect to backend)
function logWhatsAppRedirection(requestId) {
    // In a real app, this would make an API call to log the redirection
    console.log(`Logging WhatsApp redirection for request ${requestId}`);
    
    // Example API call:
    /*
    fetch('/api/log-whatsapp-redirection', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            requestId: requestId,
            timestamp: new Date().toISOString()
        }),
    });
    */
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
            seekerPhone: "9876543212", // Added seeker phone
            volunteerPhone: "9123456789", // Added volunteer phone
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

