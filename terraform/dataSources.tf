data "aws_lambda_function" "existingLambda" {
  function_name = "final-lex-bot-v1-dev-lexIntentVerifier"
}

data "external" "getBotId" {
  program = ["python", "utils/getBotId.py"]
  depends_on = [ aws_cloudformation_stack.finalSprintBotStackv1 ]
}