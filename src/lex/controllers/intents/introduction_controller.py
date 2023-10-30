from utils.response_formatters import prepare_response_text

def handle_introduction(event, context):
  """
  Handles the introduction intent, which welcomes the user to the ImigraLingo bot and provides instructions on how to use it.

  Args:
      event: The event data passed by Amazon Lex.
      context: The context data passed by Amazon Lex.

  Returns:
      A response object containing the welcome message and instructions.
  """
  response = f"Boas vindas ao ImigraLingo, bot de ajuda ao imigrante! O que deseja fazer? Caso não conheça meus comandos, digite 'ajuda'!\nBienvenue sur ImigraLingo, le bot d'aide pour les immigrants ! Que souhaitez-vous faire ? Si vous ne connaissez pas mes commandes, tapez 'aide' !"
  
  return prepare_response_text(event, response)