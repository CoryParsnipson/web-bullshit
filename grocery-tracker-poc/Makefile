build:
	docker -t cparsnipson/gt-poc docker

# --init recommended to avoid zombie process issues with PID=1
# --ipc=host recommended for chromium to allow docker container access to the
#   host pc's resources
run:
	docker run -it --rm --init --ipc=host cparsnipson/gt-poc /bin/bash
