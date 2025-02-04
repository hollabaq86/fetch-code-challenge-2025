.PHONY: console build

console: build
	docker run -it -v="$(PWD):/fetch-code-challenge-2025" --net="host" fetch-code-challenge-2025 /bin/bash -l -c "bundle install;bash -l"

build:
	docker build -t fetch-code-challenge-2025 .