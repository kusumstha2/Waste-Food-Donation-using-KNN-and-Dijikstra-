from django.shortcuts import render
from location.models import DonorLocation, RecipientLocation
from math import radians, sin, cos, sqrt, atan2
import heapq  # For priority queue implementation in Dijkstra's algorithm

# Haversine formula to calculate distance
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the Earth in km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c

# Dijkstra's algorithm to calculate shortest paths
# Dijkstra's algorithm to calculate shortest paths
# Dijkstra's algorithm to calculate shortest paths
# Dijkstra's algorithm to calculate shortest paths
# Dijkstra's algorithm to calculate shortest paths
def dijkstra(donor_location, recipient_locations):
    graph = {}
    distances = {}

    # Build the graph with distance calculations
    for recipient_location in recipient_locations:
        distance = haversine_distance(
            donor_location.latitude, donor_location.longitude,
            recipient_location.latitude, recipient_location.longitude
        )
        # Store recipient's coordinates and distance in graph
        graph[(recipient_location.latitude, recipient_location.longitude)] = (recipient_location, distance)
        distances[(recipient_location.latitude, recipient_location.longitude)] = distance

    # Priority queue for finding shortest path
    priority_queue = [(0, (donor_location.latitude, donor_location.longitude))]
    visited = set()

    while priority_queue:
        current_distance, current_location = heapq.heappop(priority_queue)

        if current_location in visited:
            continue

        visited.add(current_location)

        # Check neighbors and update distances
        for neighbor, (recipient_location, weight) in graph.items():
            if neighbor not in visited:
                new_distance = current_distance + weight
                if new_distance < distances.get(neighbor, float('inf')):
                    distances[neighbor] = new_distance
                    heapq.heappush(priority_queue, (new_distance, neighbor))

    return distances




# View to find nearest recipients using Dijkstra's algorithm
# View to find nearest recipients using Dijkstra's algorithm
def search_recipients(request):
    donor = request.user.donor  # Assuming `request.user` is linked to a donor model
    donor_location = DonorLocation.objects.get(donor=donor)

    # Fetch all recipient locations
    recipient_locations = RecipientLocation.objects.all()

    # Apply Dijkstra's algorithm to calculate distances
    distances = dijkstra(donor_location, recipient_locations)

    # Prepare recipient data with calculated distances
    recipient_distances = [
        {
            'name': recipient_location.recipient.user.username,
            'latitude': recipient_location.latitude,
            'longitude': recipient_location.longitude,
            'distance': round(distances[(recipient_location.latitude, recipient_location.longitude)], 2),  # Corrected access
        }
        for recipient_location in recipient_locations
    ]

    # Sort recipients by distance
    sorted_recipients = sorted(recipient_distances, key=lambda x: x['distance'])

    # Pass top 5 nearest recipients to the context
    context = {
        'donor_location': {
            'latitude': donor_location.latitude,
            'longitude': donor_location.longitude,
        },
        'recipients': sorted_recipients[:5],  # Top 5 nearest recipients
    }

    return render(request, 'recipient_search_results.html', context)
