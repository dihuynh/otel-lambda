variable "github_token" {
}

resource "aws_ssm_parameter" "github_token" {
  name        = "/github_token"
  description = "GitHub token"
  type        = "SecureString"
  value       = var.github_token
}