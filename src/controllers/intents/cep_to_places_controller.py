from services.geo_service import cep_to_location, location_to_coordinates, places_by_coordinates
from responseFormatters import prepare_response_text

def handle_cep_to_places(event, context):
  try:
    slots = event['interpretations'][0]['intent']['slots']
    cep = slots['cep']['value']['interpretedValue']
    place_type = slots['place_type']['value']['interpretedValue']
    address = cep_to_location(cep)
    if address:
      lat, lon = location_to_coordinates(address)
      response = places_by_coordinates(lat, lon, place_type)
      return prepare_response_text(event, response)
    else:
      return prepare_response_text(event, "Adresse non trouvée.")
    
  except Exception as e:
    print(f"Error in cep_to_places_controller: {e}")
    return prepare_response_text(event, f"Erreur lors du traitement de la demande d'achat: {str(e)}")
