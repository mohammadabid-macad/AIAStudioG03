document.addEventListener('DOMContentLoaded', function() {
    var map = L.map('map').setView([51.505, -0.09], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap'
    }).addTo(map);

    var marker;

    map.on('click', function(e) {
        document.getElementById('coordinates').value = e.latlng.lat + ", " + e.latlng.lng;
        if (marker) {
            map.removeLayer(marker);
        }
        marker = new L.Marker(e.latlng).addTo(map);
    });

    L.Control.geocoder().addTo(map);

    function displayImage(file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const img = document.createElement('img');
            img.src = e.target.result;
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = ''; // Clear previous images
            resultsDiv.appendChild(img);
        };
        reader.readAsDataURL(file);
    }

    document.getElementById('imageInput').addEventListener('change', function() {
        const imageFile = this.files[0];
        displayImage(imageFile);
    });

    function submitData() {
        const imageFile = document.getElementById('imageInput').files[0];
        const formData = new FormData();
        formData.append('file', imageFile);

        fetch('/upload_image', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            const segmentedImg = document.createElement('img');
            segmentedImg.src = data.segmented_image_path;
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = ''; // Clear previous images
            resultsDiv.appendChild(segmentedImg);

            const coordinates = document.getElementById('coordinates').value.split(", ");
            const lat = parseFloat(coordinates[0]);
            const lon = parseFloat(coordinates[1]);

            fetch('/analyze_location', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    lat: lat,
                    lon: lon,
                    segmentation_results: data.segmentation_results
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log(data); // Display or use the analysis results as needed
            })
            .catch(error => console.error('Error:', error));
        })
        .catch(error => console.error('Error:', error));
    }

    document.querySelector('button').addEventListener('click', submitData);
});
