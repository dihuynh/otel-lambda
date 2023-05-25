resource aws_sns_topic "recently_updated_repos" {
  name = "recently_updated_repos"
  tracing_config = "Active"
}

resource aws_sqs_queue "calculate_action_stats" {
  name = "calculate_action_stats"
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.deadletter.arn
    maxReceiveCount     = 4
  })
}

resource "aws_sns_topic_subscription" "subscription" {
  topic_arn = aws_sns_topic.recently_updated_repos.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.calculate_action_stats.arn
}

resource "aws_sqs_queue" "deadletter" {
  name = "calculate_action_stats_dlq"
}

data "aws_iam_policy_document" "this" {
  version   = "2012-10-17"
  policy_id = "default"
  statement {
    sid = "AllowSubscribedSnsTopics"

    effect  = "Allow"
    actions = ["sqs:SendMessage"]
    principals {
      identifiers = ["*"]
      type        = "AWS"
    }
    resources = [aws_sqs_queue.calculate_action_stats.arn]
    condition {
      test     = "ArnEquals"
      values   = [aws_sns_topic.recently_updated_repos.arn]
      variable = "aws:SourceArn"
    }
  }
}

resource "aws_sqs_queue_policy" "this" {
  policy    = data.aws_iam_policy_document.this.json
  queue_url = aws_sqs_queue.calculate_action_stats.url
}

output "upside_trifecta" {
  value = {
    "calculate_action_stats": aws_sqs_queue.calculate_action_stats.arn,
    "recently_updated_repos": aws_sns_topic.recently_updated_repos.arn
  }
}