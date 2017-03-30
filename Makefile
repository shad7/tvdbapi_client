MAKEFLAGS += --warn-undefined-variables
SHELL := /bin/bash
.SHELLFLAGS := -o pipefail -euc
.DEFAULT_GOAL := all

export PROJECT = tvdbapi_client

# Windows environment?
CYG_CHECK := $(shell hash cygpath 2>/dev/null && echo 1)
ifeq ($(CYG_CHECK),1)
	VBOX_CHECK := $(shell hash VBoxManage 2>/dev/null && echo 1)

	# Docker Toolbox (pre-Windows 10)
	ifeq ($(VBOX_CHECK),1)
		ROOT := /${PROJECT}
	else
		# Docker Windows
		ROOT := $(shell cygpath -m -a "$(shell pwd)")
	endif
else
	# all non-windows environments
	ROOT := $(shell pwd)
endif

DEV_IMAGE := ${PROJECT}_dev

TEST_API_KEY ?=
TEST_API_USER ?=
TEST_API_PASSWORD ?=
NOSE_NOCAPTURE ?=

ALL_PY := py27 py34 py35
PYVER ?= py27

DOCKERRUN := docker run --rm \
	-e PROJECT="${PROJECT}" \
	-e PY_VERSION="${PYVER}" \
	-e NOSE_NOCAPTURE=${NOSE_NOCAPTURE} \
	-e TEST_API_KEY="${TEST_API_KEY}" \
    -e TEST_API_USER="${TEST_API_USER}" \
    -e TEST_API_PASSWORD="${TEST_API_PASSWORD}" \
    -v ${ROOT}:/${PROJECT} \
    -w /${PROJECT} \
    ${DEV_IMAGE}:${PYVER}


all: all-lint all-cover

.PHONY: clean
clean: prepare
	${DOCKERRUN} invoke clean --all
	@rm -rf .tvdb_cache cover doc/build

## Same as clean but also removes cached dependencies.
veryclean: clean
	@rm -rf .tmp

## builds the dev container
prepare: .tmp/dev_image_id-${PYVER}
.tmp/dev_image_id-%: requirements.txt test-requirements.txt
	@mkdir -p .tmp
	@docker rmi -f ${DEV_IMAGE}:${PYVER} > /dev/null 2>&1 || true
	@echo "Building dev container ${PYVER}"
	@docker build -t ${DEV_IMAGE}:${PYVER} -f Dockerfile.dev-${PYVER} .
	@docker inspect -f "{{ .ID }}" ${DEV_IMAGE}:${PYVER} > .tmp/dev_image_id-${PYVER}

prepare-%:
	@$(MAKE) --no-print-directory PYVER=$* prepare

.PHONY: all-prepare
all-prepare: $(addprefix prepare-, $(ALL_PY))

test-%:
	@$(MAKE) --no-print-directory PYVER=$* test

.PHONY: all-test
all-test: $(addprefix test-, $(ALL_PY))

cover-%:
	@$(MAKE) --no-print-directory PYVER=$* cover

.PHONY: all-cover
all-cover: $(addprefix cover-, $(ALL_PY))
	${DOCKERRUN} bash ./scripts/test.sh --merge

lint-%:
	@$(MAKE) --no-print-directory PYVER=$* lint

.PHONY: all-lint
all-lint: $(addprefix lint-, $(ALL_PY))

.PHONY: test
test: prepare
	${DOCKERRUN} bash ./scripts/test.sh

.PHONY: cover
cover: prepare
	${DOCKERRUN} bash ./scripts/test.sh --cover

.PHONY: lint
lint: prepare
	${DOCKERRUN} flake8 --show-source ${PROJECT}

.PHONY: docs
docs: prepare
	${DOCKERRUN} python setup.py build_sphinx

.PHONY: changelog
changelog: prepare
	${DOCKERRUN} invoke write_changelog

# ------ Docker Helpers
.PHONY: drma
drma:
	@docker rm $(shell docker ps -a -q) 2>/dev/null || :

.PHONY: drmia
drmia:
	@docker rmi $(shell docker images -q --filter "dangling=true") 2>/dev/null || :

.PHONY: drmvu
drmvu:
	@docker volume rm $(shell docker volume ls -qf dangling=true) 2>/dev/null || :
