# grocery-tracker-poc

Pull pricing and availability data (where available) about certain food items to see which store has the best price and if there are any sales. The proof of concept is as basic as possible, missing lots of features, but just trying to see how well this would work.

## Getting Starting

This app was developed with python 3.13.7 on Fedora 42 Linux.

### Setup

#### Docker

1. Install Docker

1. Run `make build`

1. Run `make run`. (This will run `python main.py` to start the app)

1. The docker container will open port 5900 for VNC, so open a VNC viewer program on the host machine to view. Point it to `localhost:5900`.

1. Further development cycles on docker involve making code changes, then running `make build`, and `make run` and then watching the progress on VNC viewer.

#### Local environment

1. Install python3 and pip.

1. Create virtual environment in this directory.

   ```
   python -m venv .venv
   ```

1. Enter the virtual environment.

    ```
    source .venv/bin/activate
    deactivate # use this to exit the virtualenv
    ```

1. Install required python packages.

    ```
    pip install -r requirements.txt
    ```

1. The rest TBD.

## Basic Use Case

To check the price of strawberries, scrap the websites of the following stores:

* Costco (sameday)
* Safeway (safeway website)
* Smart and Final (smart and final website, but instacart includes availability)
* Trader Joes (tj website, but no availability info)
* Whole Foods (Amazon website)

* excluding Target (but consider if working on non-poc?)
* excluding Walmart (but consider if working on non-poc?)

Repeat gathering this information on a daily/weekly(?) basis and store it in a database. Eventually, it may be useful to track the moving average of price per unit so you can show to users and appraise whether value is good or expensive.

List results in order of price per unit, ascending, with the front runner being the recommended store to buy from.

In the real app, we would want to let the user create item groups, that compare between stores, and then organize those item groups into a shopping list. This will show the user the best place to buy any given item on their list.

## Prior Art

### InStok / OctoShop

This was an app to "fix the disparity between in-store and online shopping prices and inventory". This eventually evolved into a browser plugin called OctoShop that let you track when certain items were re-stocked and price drops.

This appears to be almost exactly the same as what this app is trying to do.

OctoShop was eventually acquired by a company called Ibotta and their functionality was integrated into their app. Not sure if it is still available in its current form.

Octoshop was free for users and generated revenue from affiliate links by bringing traffic to websites. This seemed to be a challenge to the company to secure enough funding to be profitable?

### Every Grocery Store Website

It looks like most stores do not stock up to date availability and pricing information for their entire inventory, especially the fresh fruit and produce sections. Probably because it is too much effort and grocery stores don't have the most up-to-date electronic systems to track this closely. But certain companies, like Hmart and Whole Food show that this is possible given the right expertise and desire. From this it can be inferred that the common sentiment in the industry is that a properly functioning website may dampen in-store traffic, and thus they do not incentivize shopping online.

### Instacart

This is a big player in the space and has a large infrastructure that would be quite useful for the purposes of this app. Their system just happens to be like 90% of what this app needs, after which, the thin layer of business logic for shopping list management would be needed.

Why hasn't Instacart implemented this already?

1. Probably conflicts with their business model. You can't make one order to multiple stores, and you get other people to shop for you, not you trying to find the best price for everything.

1. Maybe they also don't want to upset grocery stores by making arbitration across grocery store items more efficient? This app would be dead if the market was completely efficient, but on the other hand, if the market was inefficient, then certain stores would be losing a lot of money.

## Investigation on Website Scrapability

### Instacart

Instacart has an insanely built up database of food pricing and availability information since they are an established player in the grocery delivery market. Their database isn't perfect, but they sometimes have information you can't find on some store's own websites.

The prices usually include some hidden percentage mark-up over in-store prices as a hidden fee.

For future reference:

* Costco -> blanket 17% markup, very accurate and consistent
* Safeway -> approx 17% markup, seems to vary
* Smart and Final -> 10% ish markup, varies a lot

Using instacart via automated methods appears to be difficult (but not impossible). Will need to be able to store sessions and log in via email code. Using python api access to a gmail account may be the way to go here. Lots of up front work to establish this infrastructure, unfortunately. I also suspect, given their engineering department expertise, that you would need to be very sophisticated in rotating vpns and request rate/timing, and playwright behavior to avoid detection.

**I feel like Instacart almost entirely obviates the need for this app. Ideally, maybe you could just build this app as a tiny plugin on top of instacart, such that you can search for an item, and then sort by price per unit in the search results across stores in your location, and then add to shopping list. I still feel like there is a lot of value (for the consumer) to be able to plan shopping lists with real time data**

### Costco

Website is not great and doesn't keep much information about fresh produce or warehouse info online. You can use the sameday website though (costco's gig economy delivery option which is powered by instacart anyway) to get some produce information.

### Safeway

Website is pretty good, though the product database is sprawling and large. No issues here. Holy fucking shit, they are loaded to the gills with anti-bot protection.

### Smart and Final

Website is not great. Item information does not seem too reliable.

### Trader Joe's

Website is also not great. No item availability, and missing a lot of their inventory. Some entries are there, and those that are, are good.

### Whole Foods

Great website. I guess, what do you expect from Amazon.

### Target

Website is good

### Walmart

Website is good
