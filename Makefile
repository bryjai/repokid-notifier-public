HASH_GIT	:= $(shell git rev-parse --short HEAD) # Used to version artifacts
ARTIFACT_NAME := repokid-notifier
APP_BUCKET_NAME := bucket_name_to_store_code_build_artifacts
PROTON_TEMPLATE_BUCKET_NAME := bucket_name_to_store_proton_templates_artifacts

.PHONY: pack
pack:
	@echo "==== Generating function.zip file ===="
	zip function.zip requirements.txt __init__.py notifier/*

.PHONY: build-environment-template
build-environment-template:
	@echo "==== Generating tar.gz file ===="
	cd proton/environment && tar -zcvf ${ARTIFACT_NAME}-env-template.tar.gz *

.PHONY: build-service-template
build-service-template:
	@echo "==== Generating tar.gz file ===="
	cd proton/service && tar -zcvf ${ARTIFACT_NAME}-service-template.tar.gz *

.PHONY: proton-artifacts
proton-artifacts: build-environment-template build-service-template
	@echo "==== Copying Repokid Notifier proton Environment Template artifact to S3 ===="
	docker run -v $(shell pwd):/workspace/app -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
				-e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
				-e AWS_SESSION_TOKEN=${AWS_SESSION_TOKEN} \
				amazon/aws-cli \
				s3 cp /workspace/app/proton/environment/${ARTIFACT_NAME}-env-template.tar.gz s3://${PROTON_TEMPLATE_BUCKET_NAME}/repokid-notifier/environment/${HASH_GIT}/${ARTIFACT_NAME}-env-template.tar.gz

	@echo "==== Copying Repokid Notifier proton Service Template artifact to S3 ===="
	docker run -v $(shell pwd):/workspace/app -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
				-e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
				-e AWS_SESSION_TOKEN=${AWS_SESSION_TOKEN} \
				amazon/aws-cli \
				s3 cp /workspace/app/proton/service/${ARTIFACT_NAME}-service-template.tar.gz s3://${PROTON_TEMPLATE_BUCKET_NAME}/repokid-notifier/service/${HASH_GIT}/${ARTIFACT_NAME}-service-template.tar.gz

.PHONY: send-artifact-to-s3
send-artifact-to-s3: pack
	@echo "==== Copying Repokid Notifier proton Environment Template artifact to S3 ===="
	aws s3 cp function.zip s3://${APP_BUCKET_NAME}/function.zip

.PHONY: clean
clean:
	@echo "==== Clean up ===="
	rm -f kubeconfig
	rm -f ./secrets.*.yaml
	rm -f ./*.tgz


.PHONY: help
help:
	@grep -E '^[a -zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

