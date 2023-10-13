resource "aws_iam_role" "finalSprintBotIamRoleStackv1" {
  name = "finalSprintBotIamRoleStackv1"
  assume_role_policy = jsonencode(
    {
      "Version" : "2012-10-17",
      "Statement" : [
        {
          "Effect" : "Allow",
          "Principal" : {
            "Service" : "lexv2.amazonaws.com"
          },
          "Action" : "sts:AssumeRole"
        }
      ]
  })
}