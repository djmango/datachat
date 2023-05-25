from app.models import cnn, amazon, ebay, medium, reddit, yelp
from enum import Enum

class PydanticModelName(str, Enum):
    cnn = "cnn"
    amazon = "amazon"
    ebay = "ebay"
    medium = "medium"
    reddit = "reddit"
    yelp = "yelp"

pydantic_models = {
    PydanticModelName.cnn: cnn.CnnBase,
    PydanticModelName.amazon: amazon.AmazonBase,
    PydanticModelName.ebay: ebay.EbayBase,
    PydanticModelName.medium: medium.MediumBase,
    PydanticModelName.reddit: reddit.RedditBase,
    PydanticModelName.yelp: yelp.YelpBase,
}
