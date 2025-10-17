import os

# NOTE: hard code these urls for now, but real product should either crawl or
# let the user search and bookmark items
PRODUCT_URLS = {
    "costco" : [
        "https://sameday.costco.com/store/costco/products/18876359-strawberries-2-lbs-2-lb",
        "https://sameday.costco.com/store/costco/products/18848254-organic-strawberries-2",
    ],
    "safeway": [
        "https://www.safeway.com/shop/product-details.184070124.html", # 1lb prepacked strawberries
        "https://www.safeway.com/shop/product-details.960012546.html", # 2lb prepacked strawberries
        "https://www.safeway.com/shop/product-details.184700156.html", # 1lb organic strawberries
    ],
    "smart-and-final": [
        "https://www.smartandfinal.com/sm/planning/rsid/327/product/strawberries-id-00853447003390",
        "https://www.smartandfinal.com/sm/planning/rsid/327/product/organic-strawberries-id-00853447003642"
    ],
    "trader-joes": [
        "https://www.traderjoes.com/home/products/pdp/strawberries-1-lb-035878",
        "https://www.traderjoes.com/home/products/pdp/strawberries-2-lb-078515",
        "https://www.traderjoes.com/home/products/pdp/organic-strawberries-1-lb-080331",
    ],
    "whole-foods": [
        "https://www.amazon.com/Produce-ambient-room-temperature-Strawberries/dp/B08911ZP3Y?almBrandId=VUZHIFdob2xlIEZvb2Rz&fpw=alm&s=wholefoods",
        "https://www.amazon.com/Fresh-Produce-Brands-Vary-040/dp/B002B8Z98W?almBrandId=VUZHIFdob2xlIEZvb2Rz&fpw=alm&s=wholefoods",
        "https://www.amazon.com/Fresh-Produce-Brands-May-Vary/dp/B07PQNBKCK?almBrandId=VUZHIFdob2xlIEZvb2Rz&fpw=alm&s=wholefoods"
    ],
}


def environment():
    """
    Returns which environment to run in. Defaults to prod.

    :return: str with environment ("dev"|"prod")
    """
    environment = os.environ["ENVIRONMENT"] if "ENVIRONMENT" in os.environ else "dev"
    return "dev" if environment != "prod" else "prod"


def in_docker():
    """
    Return bool to check if we are running in a docker or not. NOTE, this
    relies on proper Dockerfile setup, so check those files.

    :return: bool - True if in docker, False if not in docker
    """
    return os.environ["IN_DOCKER"] == "true" if "IN_DOCKER" in os.environ else False


def pause_at_beginning():
    """
    Set environment variable 'PAUSE_AT_BEGINNING' to make app pause playwright
    before doing anything else.

    :return: bool if set (true for pause), or None if not set (will pause or not depending on env)
    """
    if "PAUSE_AT_BEGINNING" not in os.environ:
        return None
    return bool(os.environ["PAUSE_AT_BEGINNING"])
