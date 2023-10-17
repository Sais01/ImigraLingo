resource "aws_cloudformation_stack" "finalSprintAliasBotStackv1" {
    name = "finalSprintAliasBotStackv1"

    template_body = jsonencode({
        Resources = {
            schoolAssistantBotAlias = {
                Type = "AWS::Lex::BotAlias"
                Properties = {
                    BotId = data.external.getBotId.result["bot_id"]
                    BotAliasName = "finalSprintAliasBotv1"
                    Description = "Alias para o bot da sprint final."
                    BotVersion = "3"
                    BotAliasLocaleSettings = [{
                        LocaleId = "pt_BR"
                        BotAliasLocaleSetting = {
                            Enabled = true
                            CodeHookSpecification = {
                                LambdaCodeHook = {
                                    CodeHookInterfaceVersion = "1.0"
                                    LambdaArn = data.aws_lambda_function.existingLambda.arn
                                }
                            }
                        }
                    }]
                }
            }
        }
    })
    depends_on = [ aws_cloudformation_stack.finalSprintBotStackv1 ]
}