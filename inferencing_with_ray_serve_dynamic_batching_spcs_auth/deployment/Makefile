# The make file

# load the various configurations from config file
cnf ?=config.env
include $(cnf)
export $(shell sed 's/=.*//' $(cnf))

# HELP
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

logout_docker:
	docker logout https://${IMAGE_REGISTRY}

login_docker: ## Build the customized osrm backend container
	snow spcs image-registry token --format=JSON --connection kipi_ltr | docker login https://${IMAGE_REGISTRY} -u 0sessiontoken --password-stdin

build_docker: ## Build the customized osrm backend container
	docker build --platform linux/amd64 -t $(SS_SERVICE_NAME) -f Dockerfile .

tag_docker: 
	docker tag $(SS_SERVICE_NAME) $(IMAGE_REGISTRY)/$(SS_SERVICE_NAME)
	
push_docker: ## tag and push the containers to the repo $(IMAGE_REGISTRY)
	docker push $(IMAGE_REGISTRY)/$(SS_SERVICE_NAME)

upload_yaml: ## upload yaml to stage $(SS_STAGE)
	snow stage copy --connection kipi_ltr --overwrite --no-auto-compress ./ltr_spcsauth.yaml @$(SS_DB).$(SS_SCHEMA).$(SS_STAGE)
	snow stage list --connection kipi_ltr --like "$(SS_STAGE)%"

######################## COMPOSITE TARGETS ######################

build_and_push_docker: logout_docker login_docker build_docker tag_docker push_docker logout_docker
all: build_and_push_docker upload_yaml