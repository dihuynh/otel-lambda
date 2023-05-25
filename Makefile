plan:
	export TF_VAR_github_token=$(GITHUB_TOKEN) && terraform -chdir=infra/terraform plan

apply:
	export TF_VAR_github_token=$(GITHUB_TOKEN) && terraform -chdir=infra/terraform apply -auto-approve

deploy:
	npx sls deploy

invoke:
	aws lambda invoke --function-name otel-demos-dev-upside_trifecta_sender --payload {} result.out && cat result.out