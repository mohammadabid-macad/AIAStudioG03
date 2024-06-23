import osmnx as ox
import geopandas as gpd
from shapely.geometry import Point

def get_building_info(lat, lon):
    # Create a bounding box around the given coordinates
    distance = 1000  # distance in meters for the bounding box
    bbox = ox.utils_geo.bbox_from_point(point=(lat, lon), dist=distance)

    # Load the OSMnx graph for the bounding box
    G = ox.graph_from_bbox(bbox[0], bbox[1], bbox[2], bbox[3], network_type='all')
    buildings = ox.geometries_from_bbox(bbox[0], bbox[1], bbox[2], bbox[3], tags={'building': True})

    # Calculate the distance from the given point to all building centroids and find the closest building
    buildings['centroid'] = buildings.centroid
    given_point = Point(lon, lat)
    buildings['distance'] = buildings['centroid'].apply(lambda x: x.distance(given_point))
    closest_building = buildings.loc[buildings['distance'].idxmin()]

    # Retrieve the corresponding building polygon
    building_polygon = closest_building['geometry']

    # Get building info
    osm_id = str(closest_building.name)  # Ensure it's a standard string
    building_name = closest_building.get('name', 'N/A')  # Attempt to get the building name if available

    # Check for building levels
    building_levels = closest_building.get('building:levels', 'No Building levels information found on OSM')

    # Mapping dictionary for building categories
    building_type_mapping = {
        'house': 'residential',
        'apartments': 'residential',
        'residential': 'residential',
        'semidetached_house': 'residential',
        'terrace': 'residential',
        'dormitory': 'residential',
        'retail': 'retail',
        'commercial': 'commercial',
        'detached': 'residential',
        'garages': 'other',
        'office': 'office',
        'university': 'education',
        'school': 'education',
        'garage': 'other',
        'roof': 'other',
        'church': 'religious',
        'shed': 'other',
        'service': 'other',
        'industrial': 'industrial',
        'train_station': 'transport',
        'hotel': 'hospitality',
        'pub': 'hospitality',
        'air_shaft': 'other',
        'warehouse': 'industrial',
        'hospital': 'healthcare',
        'construction': 'other',
        'public': 'institution',
        'bridge': 'transport',
        'college': 'education',
        'kiosk': 'commercial',
        'civic': 'institution',
        'block': 'other',
        'no': 'other',
        'healthcare': 'healthcare',
        'bunker': 'other',
        'toilets': 'public',
        'hall_of_residence': 'education',
        'restaurant': 'hospitality',
        'kindergarten': 'education',
        'greenhouse': 'other',
        'conservatory': 'other',
        'tower': 'other',
        'hut': 'other',
        'museum': 'institution',
        'presbytery': 'religious',
        'outbuilding': 'other',
        'chapel': 'religious',
        'silo': 'industrial',
        'cafe': 'hospitality',
        'sports_centre': 'sports',
        'multiple': 'other',
        'air_vent': 'other',
        'commerical': 'commercial',
        'container': 'other',
        'student_residence': 'education',
        'shelter': 'public',
        'ruins': 'other',
        'substation': 'other',
        'transportation': 'transport',
        'balcony': 'other',
        'council_flats': 'residential',
        'disused_station': 'transport',
        'portacabins': 'other',
        'cinema': 'hospitality',
        'boathouse': 'other',
        'artists_studio': 'institution',
        'chimney': 'other',
        'vent_shaft': 'other',
        'library': 'institution',
        'gatehouse': 'institution',
        'sports_hall': 'sports',
        'convent': 'religious',
    }

    # Apply the mapping to categorize the closest building type
    closest_building_category = building_type_mapping.get(closest_building['building'], 'other')

    return {
        "osm_id": osm_id,
        "building_name": building_name,
        "building_category": closest_building_category,
        "building_levels": building_levels
    }
