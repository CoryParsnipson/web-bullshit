# botbrowser-test

Test botbrowser automation tool.

> [!CAUTION]
> This tool is paid subscription software disguised as free software. For free,
> you can only use the demo profiles and that limits you to bot-script javascript
> usage, and not any of the other automation interfaces. See
> [this page](https://github.com/botswin/BotBrowser/tree/main/examples/bot-script) 
> for more information about doing that.
>
> 30 profiles per month is $299 a month, and 100 profiles is $499 a month. You
> can do a one time purchase of profiles of $599 for 30 or $999 for 100 profiles
> locked to one version. Of course, payment is limited to only USDT (a crypto
> currency).

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
