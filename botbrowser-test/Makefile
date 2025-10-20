build:
	docker build -t cparsnipson/botbrowser-test .

run:
	docker run -it --rm --init --ipc=host \
	-p 9222:9222 \
	-p 5900:5900 \
	--name botbrowser-test \
	-v ./data/profiles:/botbrowser/profiles \
	cparsnipson/botbrowser-test \
	"--bot-profile=/botbrowser/profiles/chrome141_win10_x64.enc" \
	"--remote-debugging-port=9222"

shell:
	docker run -it --rm --init --ipc=host -p 5900:5900 -p 9222:9222 --entrypoint=/bin/bash \
	-v ./data/profiles:/botbrowser/profiles \
	cparsnipson/botbrowser-test
