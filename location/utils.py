from math import radians, sin, cos, sqrt, atan2

# Haversine formula to calculate distance
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of Earth in kilometers
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# Function to find the nearest recipient
def find_nearest_recipient(donor_location, recipient_locations):
    nearest_recipient = None
    shortest_distance = float('inf')
    
    for recipient in recipient_locations:
        distance = haversine_distance(
            donor_location.latitude,
            donor_location.longitude,
            recipient.latitude,
            recipient.longitude
        )
        if distance < shortest_distance:
            shortest_distance = distance
            nearest_recipient = recipient
    
    return nearest_recipient, shortest_distance
