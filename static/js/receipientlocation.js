document.addEventListener('DOMContentLoaded', function () {
    // Create the OpenLayers map
    const map = new ol.Map({
      target: 'map', // ID of the div where the map will be rendered
      layers: [
        new ol.layer.Tile({
          source: new ol.source.OSM(), // OpenStreetMap tile source
        }),
      ],
      view: new ol.View({
        center: ol.proj.fromLonLat([85.3240, 27.7172]), // Center the map on Kathmandu (Longitude: 85.3240, Latitude: 27.7172)
        zoom: 12, // Zoom level (12 is ideal for a city-level view)
      }),
    });

    // Create a vector source to store the marker
    const vectorSource = new ol.source.Vector();

    // Create a vector layer to hold the marker
    const markerLayer = new ol.layer.Vector({
      source: vectorSource,
    });

    // Add the marker layer to the map
    map.addLayer(markerLayer);

    // Create a marker (initially placed at Kathmandu's coordinates)
    const marker = new ol.Feature({
      geometry: new ol.geom.Point(ol.proj.fromLonLat([85.3240, 27.7172])), // Initial marker position in Kathmandu
    });

    // Add the marker to the vector source
    vectorSource.addFeature(marker);

    // Add click event listener to move the marker when user clicks on the map
    map.on('click', function (event) {
      const coordinate = event.coordinate;
      
      // Update the marker's position
      marker.setGeometry(new ol.geom.Point(coordinate));

      // Convert coordinates to longitude and latitude
      const lonLat = ol.proj.toLonLat(coordinate);
      document.getElementById('status-message').innerText = `Location selected: Longitude ${lonLat[0]}, Latitude ${lonLat[1]}`;
    });

    // Handle the save location button click
    document.getElementById('save-location').addEventListener('click', function () {
      const coords = marker.getGeometry().getCoordinates();
      const lonLat = ol.proj.toLonLat(coords); // Convert coordinates to [longitude, latitude]

      function getCSRFToken() {
        // If CSRF token is set in a meta tag:
        let token = document.querySelector('meta[name="csrf-token"]');
        if (token) {
          return token.getAttribute('content');
        }
        return ''; // Return empty string if CSRF token is not found
      }

      // Fetch CSRF token
      const csrfToken = getCSRFToken();
      console.log(csrfToken); // For debugging

      // Send the latitude and longitude to the Django view via AJAX
      fetch('/saveuserlocation/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken, // Ensure CSRF token is included
        },
        body: JSON.stringify({
          latitude: lonLat[1], // latitude
          longitude: lonLat[0], // longitude
        }),
      })
      .then((response) => response.json())
      .then((data) => {
        document.getElementById('status-message').innerText = `Location saved: Latitude ${lonLat[1]}, Longitude ${lonLat[0]}`;
      })
      .catch((error) => console.error('Error:', error));
    });
  });