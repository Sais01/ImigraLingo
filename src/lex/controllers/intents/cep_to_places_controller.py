from services.geo_service      import cep_to_location, location_to_coordinates, places_by_coordinates
from utils.response_formatters import prepare_response_text

def handle_cep_to_places(event, context):
  """
  Given an event and context, extracts the user's inputted CEP (postal code) and desired point of interest type,
  retrieves the corresponding latitude and longitude coordinates, and returns a response text containing nearby places
  of the specified type. If the CEP is invalid or the address cannot be found, returns an error message.

  Args:
    event (dict): The event data passed by AWS Lex.
    context (dict): The context data passed by AWS Lex.

  Returns:
    str: A response text containing nearby places of the specified type, or an error message if the CEP is invalid
    or the address cannot be found.
  """
def handle_cep_to_places(event, context):
  try:
    slots      = event['interpretations'][0]['intent']['slots']
    cep        = slots['cepFromUser']['value']['originalValue']
    place_type = slots['pointsOfInterest']['value']['originalValue']

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