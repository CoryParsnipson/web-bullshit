# botbrowser-test

Test botbrowser automation tool.

Repo [here](https://github.com/botswin/BotBrowser/tree/main).

## setup

1. Download a demo profile (or copy your own into place). Make a `./data/profiles`
   inside this repository. This is where the makefile will mount the container's
   volumes by default. Put the profile `.enc` files in here.

1. Rename the `--bot-profile` line to match the profile you just obtained.

1. `make build`

1. `make run`

1. Using vncviewer or some vnc software, log into `localhost:5900` to see any
   GUI activity going on inside the container.
