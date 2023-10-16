import requests
from opencage.geocoder import OpenCageGeocode
from core.config import settings

def cep_to_location(cep):
  """
  Converts a Brazilian zip code (CEP) to a location object.

  Args:
    cep (str): The Brazilian zip code (CEP) to be converted.

  Returns:
    dict: A dictionary containing the location information for the given zip code.
        Returns None if the request to ViaCEP fails.
  """
  VIA_CEP_BASE_URL = settings.VIA_CEP_BASE_URL
  url = f"{VIA_CEP_BASE_URL}/ws/{cep}/json/"

  try:
    response = requests.get(url)
    data = response.json()
    response =f"{data['logradouro']}, {data['localidade']} - {data['uf']}, Brasil"
    return response
  
  except Exception as e:
    print(f"Error in ViaCEP request: {e}")
    return None


def location_to_coordinates(address):
  """
  Converts an address to its latitude and longitude coordinates.

  Args:
    address (str): The address to be converted.

  Returns:
    tuple: A tuple containing the latitude and longitude coordinates for the given address.
        Returns (None, None) if the request to OpenCage Geocode fails.
  """
  API_KEY_OPENCAGE_GEOCODE = settings.API_KEY_OPENCAGE_GEOCODE

  try:
    geocoder = OpenCageGeocode(API_KEY_OPENCAGE_GEOCODE)
    results = geocoder.geocode(address)

    if results and len(results) > 0:
      first_result = results[0]
      lat = first_result['geometry']['lat']
      lon = first_result['geometry']['lng']
      return lat, lon
    else:
      return None, None

  except Exception as e:
    print(f"Error in OpenCage Geocode request: {e}")
    return None, None


def places_by_coordinates(lat, lon, place_type):
  """
  Finds places of a given type within a certain radius of a given latitude and longitude.

  Args:
    lat (float): The latitude of the center point.
    lon (float): The longitude of the center point.
    place_type (str): The type of place to search for (e.g. "restaurant", "hospital", etc.).

  Returns:
    str: A string containing information about the places found.
      Returns "Aucun endroit trouvé à proximité." if no places are found.
  """
  OVERPASS_API_BASE_URL = settings.OVERPASS_API_BASE_URL
  OPENSTREETMAP_BASE_URL = settings.OPENSTREETMAP_BASE_URL
  AROUND_SEARCH_PLACES = settings.AROUND_SEARCH_PLACES
  NUMBER_OF_PLACES  = int(settings.NUMBER_OF_PLACES)
  
  query = f'[out:json];node(around:{AROUND_SEARCH_PLACES},{lat},{lon})["amenity"="{place_type}"];out;'
  url = f"{OVERPASS_API_BASE_URL}/api/interpreter?data={query}"

  try:
    response = requests.get(url)
    data = response.json()

    if data and "elements" in data:
      results = data["elements"]
      places = []
      for i, place in enumerate(results[:NUMBER_OF_PLACES], start=1):
        place_infos = place.get("tags", {})
        place_name = place_infos.get("name", "Nom non disponible")
        place_city = place_infos.get("addr:city", "Ville non disponible")
        place_number = place_infos.get("addr:housenumber", "Numéro non disponible")
        place_street = place_infos.get("addr:street", "Rue non disponible")
        place_address = f"{place_number}, rue {place_street}, {place_city}"

        lat = place["lat"]
        lon = place["lon"]
        maps_link = f"{OPENSTREETMAP_BASE_URL}/?mlat={lat}&mlon={lon}#map=16/{lat}/{lon}"
        place_info = f"{i}. Nom: {place_name}\n   Adresse: {place_address}\n   Lien sur Maps: {maps_link}\n"
        places.append(place_info)
      return "\n".join(places)
    else:
      return "Aucun endroit trouvé à proximité."
  
  except Exception as e:
    print(f"Error in Overpass API request: {e}")
    return None


