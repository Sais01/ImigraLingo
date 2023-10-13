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
  
  url = f"https://viacep.com.br/ws/{cep}/json/"
  try:
    response = requests.get(url)
    data = response.json()
    response =f"{data['logradouro']}, {data['localidade']} - {data['uf']}, Brasil"
    return response
  except requests.exceptions.RequestException as e:
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
  geocoder = OpenCageGeocode(settings.API_KEY_OPENCAGE_GEOCODE)
  results = geocoder.geocode(address)

  if results and len(results) > 0:
    first_result = results[0]
    lat = first_result['geometry']['lat']
    lon = first_result['geometry']['lng']
    return lat, lon
  else:
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

  query = f'[out:json];node(around:5000,{lat},{lon})["amenity"="{place_type}"];out;'
  url = f"https://overpass-api.de/api/interpreter?data={query}"
  response = requests.get(url)
  data = response.json()

  if data and "elements" in data:
    results = data["elements"]
    places = []
    for i, place in enumerate(results[:5], start=1):
      nom = place.get("tags", {}).get("name", "Nom non disponible")
      adresse = place.get("tags", {}).get("addr:street", "Adresse non disponible")
      lat = place["lat"]
      lon = place["lon"]
      lien_maps = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=16/{lat}/{lon}"
      place_info = f"{i}. Nom: {nom}\n   Adresse: {adresse}\n   Lien sur Maps: {lien_maps}\n"
      places.append(place_info)
    return "\n".join(places)
  else:
    return "Aucun endroit trouvé à proximité."


if __name__ == "__main__":
  cep = input("Digite o CEP: ")
  address = cep_to_location(cep)

  if address:
    lat, lon = location_to_coordinates(address)
    places_by_coordinates(lat, lon)