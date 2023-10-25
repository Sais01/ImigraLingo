from utils.response_formatters import prepare_response_text

def handle_how_to_make_docs(event, context):
    """
    Returns a response with a link to the necessary information for document issuance.

    Args:
    - event: The event data passed by the AWS service.
    - context: The context data passed by the AWS service.

    Returns:
    - A response with a link to the necessary information for document issuance.
    """
    link     = "https://encurtador.com.br/nqswz"
    response = f"Você pode encontrar todas as informações necessárias para a emissão de documentos no link: {link}"
    return prepare_response_text(event, response)