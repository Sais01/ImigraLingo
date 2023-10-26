def check_has_text(input_list):
  """
  Checks if the input list has any text.

  Args:
      input_list (list): A list of strings.

  Returns:
      bool: True if the input list has at least one string, False otherwise.
  """
  if len(input_list) > 0:
    return True
  else:
    return False