build:
	docker build -t cparsnipson/gt-poc .

# --init recommended to avoid zombie process issues with PID=1
# --ipc=host recommended for chromium to allow docker container access to the
#   host pc's resources
run:
	docker run -it -p 5900:5900 --rm --init --ipc=host cparsnipson/gt-poc /bin/bash

# run this on host computer
run-local:
	source src/.venv/bin/activate && \
	python src/main.py && \
	deactivate

shell:
	docker run -it -p 5900:5900 --rm --init --ipc=host --entrypoint=/bin/bash cparsnipson/gt-poc

root-shell:
	docker run -it -p 5900:5900 --rm --init --ipc=host --user=root --entrypoint=/bin/bash cparsnipson/gt-poc
