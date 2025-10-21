build:
	docker build -t cparsnipson/camoufox-test .

# --init recommended to avoid zombie process issues with PID=1
# --ipc=host recommended for chromium to allow docker container access to the
#   host pc's resources
run:
	docker run -it -p 5900:5900 --rm --init --ipc=host cparsnipson/camoufox-test /bin/bash

shell:
	docker run -it -p 5900:5900 --rm --init --ipc=host --entrypoint=/bin/bash cparsnipson/camoufox-test

root-shell:
	docker run -it -p 5900:5900 --rm --init --ipc=host --user=root --entrypoint=/bin/bash cparsnipson/camoufox-test
