let map;
let marker;
let searchBox;

// Initialize the map
function initMap() {
    let defaultLocation = { lat: 37.7749, lng: -122.4194 }; // Default to San Francisco

    map = new google.maps.Map(document.getElementById("map"), {
        center: defaultLocation,
        zoom: 13,
    });

    marker = new google.maps.Marker({
        position: defaultLocation,
        map: map,
        draggable: true
    });

    // Load preferred location if saved
    loadPreferredLocation();

    // Add a search box
    let input = document.getElementById("search-box");
    let autocomplete = new google.maps.places.Autocomplete(input);
    autocomplete.bindTo("bounds", map);

    autocomplete.addListener("place_changed", function () {
        let place = autocomplete.getPlace();
        if (!place.geometry) return;

        let location = place.geometry.location;
        map.setCenter(location);
        marker.setPosition(location);
    });

    // Allow the user to manually set a marker by clicking on the map
    map.addListener("click", function (event) {
        marker.setPosition(event.latLng);
    });
}

// Save the preferred location
function savePreferredLocation() {
    let location = marker.getPosition();
    let preferredLocation = {
        lat: location.lat(),
        lng: location.lng()
    };

    localStorage.setItem("preferredLocation", JSON.stringify(preferredLocation));
    document.getElementById("preferred-location").innerText = 
        `Saved Location: Latitude ${preferredLocation.lat}, Longitude ${preferredLocation.lng}`;

    alert("Preferred location saved successfully!");
}

// Load the preferred location if available
function loadPreferredLocation() {
    let storedLocation = localStorage.getItem("preferredLocation");

    if (storedLocation) {
        let locationData = JSON.parse(storedLocation);
        let savedLatLng = new google.maps.LatLng(locationData.lat, locationData.lng);

        marker.setPosition(savedLatLng);
        map.setCenter(savedLatLng);

        document.getElementById("preferred-location").innerText = 
            `Saved Location: Latitude ${locationData.lat}, Longitude ${locationData.lng}`;
    }
}

// Clear the saved preferred location
function clearPreferredLocation() {
    localStorage.removeItem("preferredLocation");
    document.getElementById("preferred-location").innerText = "No preferred location saved.";
    alert("Preferred location cleared.");
}