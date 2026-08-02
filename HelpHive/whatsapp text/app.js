// Sample matched volunteers data (will be replaced with API call)
let matchedVolunteers = [
    {
        id: 1,
        name: "Priya Sharma",
        skills: ["Tutoring", "Mentoring"],
        availability: "Weekends",
        location: "Mumbai",
        rating: 4.8
    },
    {
        id: 2,
        name: "Rahul Patel",
        skills: ["Counseling", "Career Advice"],
        availability: "Evenings",
        location: "Delhi",
        rating: 4.6
    },
    {
        id: 3,
        name: "Ananya Gupta",
        skills: ["Technical Help", "Web Development"],
        availability: "Flexible",
        location: "Bangalore",
        rating: 4.9
    },
    {
        id: 4,
        name: "Vikram Singh",
        skills: ["Elder Care", "Medical Assistance"],
        availability: "Mornings",
        location: "Chennai",
        rating: 4.7
    },
    {
        id: 5,
        name: "Deepa Iyer",
        skills: ["Mental Health Support", "Yoga Instruction"],
        availability: "Afternoons",
        location: "Hyderabad",
        rating: 4.5
    }
];

// Initialize selected volunteers array
let selectedVolunteers = [];

// DOM elements
const volunteersContainer = document.getElementById('volunteers-container');
const selectedContainer = document.getElementById('selected-container');
const sendRequestsBtn = document.getElementById('send-requests-btn');
const confirmationModal = document.getElementById('confirmation-modal');
const closeModalBtn = document.getElementById('close-modal-btn');

// Fetch matched volunteers from API
async function fetchMatchedVolunteers() {
    try {
        // Uncomment this when your API is ready
        /* 
        const response = await fetch('/api/matched-volunteers');
        const data = await response.json();
        return data;
        */
        
        // For now, return the sample data after a short delay to simulate API call
        return new Promise(resolve => {
            setTimeout(() => {
                resolve(matchedVolunteers);
            }, 500);
        });
    } catch (error) {
        console.error('Error fetching volunteers:', error);
        return []; // Return empty array if error
    }
}

// Display all matched volunteers
async function displayVolunteers() {
    volunteersContainer.innerHTML = '<p class="loading">Loading volunteers...</p>';
    
    const volunteers = await fetchMatchedVolunteers();
    
    if (volunteers.length === 0) {
        volunteersContainer.innerHTML = '<p class="no-results">No matching volunteers found.</p>';
        return;
    }
    
    volunteersContainer.innerHTML = '';
    
    volunteers.forEach(volunteer => {
        const card = document.createElement('div');
        card.className = 'volunteer-card';
        
        // Create skills HTML
        const skillsHTML = volunteer.skills.map(skill => 
            `<span class="skill-tag">${skill}</span>`
        ).join('');
        
        card.innerHTML = `
            <h3>${volunteer.name}</h3>
            <p>Location: ${volunteer.location}</p>
            <p>Availability: ${volunteer.availability}</p>
            <p>Rating: ${volunteer.rating} / 5</p>
            <div class="skills">${skillsHTML}</div>
            <button class="request-btn" data-id="${volunteer.id}">Request Help</button>
        `;
        
        volunteersContainer.appendChild(card);
        
        // Add event listener to the request button
        const requestBtn = card.querySelector('.request-btn');
        requestBtn.addEventListener('click', () => toggleVolunteerSelection(volunteer, requestBtn));
    });
}

// Toggle volunteer selection
function toggleVolunteerSelection(volunteer, button) {
    const index = selectedVolunteers.findIndex(v => v.id === volunteer.id);
    
    if (index === -1) {
        // Add to selected
        selectedVolunteers.push(volunteer);
        button.classList.add('selected');
        button.textContent = 'Selected';
    } else {
        // Remove from selected
        selectedVolunteers.splice(index, 1);
        button.classList.remove('selected');
        button.textContent = 'Request Help';
    }
    
    updateSelectedVolunteersUI();
}

// Update the selected volunteers UI
function updateSelectedVolunteersUI() {
    selectedContainer.innerHTML = '';
    
    if (selectedVolunteers.length === 0) {
        selectedContainer.innerHTML = '<p>No volunteers selected yet.</p>';
        return;
    }
    
    selectedVolunteers.forEach(volunteer => {
        const item = document.createElement('div');
        item.className = 'selected-volunteer';
        item.innerHTML = `
            <span>${volunteer.name} (${volunteer.skills.join(', ')})</span>
            <button class="remove-btn" data-id="${volunteer.id}">✕</button>
        `;
        selectedContainer.appendChild(item);
        
        // Add event listener to the remove button
        const removeBtn = item.querySelector('.remove-btn');
        removeBtn.addEventListener('click', () => removeSelectedVolunteer(volunteer.id));
    });
}

// Remove a volunteer from the selected list
function removeSelectedVolunteer(id) {
    selectedVolunteers = selectedVolunteers.filter(v => v.id !== id);
    
    // Update the request button in the volunteers list
    const requestBtn = document.querySelector(`.request-btn[data-id="${id}"]`);
    if (requestBtn) {
        requestBtn.classList.remove('selected');
        requestBtn.textContent = 'Request Help';
    }
    
    updateSelectedVolunteersUI();
}

// Send help requests
async function sendHelpRequests() {
    if (selectedVolunteers.length === 0) {
        alert('Please select at least one volunteer to request help from.');
        return;
    }
    
    // Show loading state
    sendRequestsBtn.disabled = true;
    sendRequestsBtn.textContent = 'Sending...';
    
    try {
        // Prepare data to send
        const requestData = {
            volunteers: selectedVolunteers.map(v => v.id),
            seekerId: 'current-user-id', // Replace with actual seeker ID
            timestamp: new Date().toISOString()
        };
        
        // Uncomment this when your API is ready
        /*
        const response = await fetch('/api/send-help-requests', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData),
        });
        
        const result = await response.json();
        
        if (!result.success) {
            throw new Error(result.message || 'Failed to send requests');
        }
        */
        
        // For now, simulate API call with a delay
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Show success modal
        confirmationModal.style.display = 'flex';
        
        // Reset selections
        selectedVolunteers.forEach(volunteer => {
            const requestBtn = document.querySelector(`.request-btn[data-id="${volunteer.id}"]`);
            if (requestBtn) {
                requestBtn.classList.remove('selected');
                requestBtn.textContent = 'Request Help';
            }
        });
        
        selectedVolunteers = [];
        updateSelectedVolunteersUI();
        
    } catch (error) {
        console.error('Error sending requests:', error);
        alert('An error occurred. Please try again later.');
    } finally {
        // Reset button state
        sendRequestsBtn.disabled = false;
        sendRequestsBtn.textContent = 'Send Help Requests';
    }
}

// Close the confirmation modal
function closeModal() {
    confirmationModal.style.display = 'none';
}

// Event listeners
sendRequestsBtn.addEventListener('click', sendHelpRequests);
closeModalBtn.addEventListener('click', closeModal);

// Initialize the app
document.addEventListener('DOMContentLoaded', () => {
    displayVolunteers();
    updateSelectedVolunteersUI();
});