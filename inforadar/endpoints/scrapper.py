import sys

from cerberus import Validator
from flask import request
from flask_restful import Resource
from newspaper import Article
from newspaper import Config

import inforadar.config as config
from inforadar.models import CrowdsourcedArticle
from inforadar.util.check_erc_entries import is_registered_domain

class Scraper(Resource):
    def post(self):
        """
        Receives an url, extracts the data, stores the data into the db, and returns the data.
        Input: url
        Output: parsed content
        """

        # --------------------------
        # Request validation.
        # --------------------------
        if not request.data:
            return {'message': f"Missing a JSON body in the request."}, 422

        schema = {'url': {'type': 'string', 'required': True}, }

        validator = Validator(schema)
        validator.validate(request.get_json(force=True))
        if not validator.validate(request.get_json(force=True)):
            return {'message': f"Unsupported json object: " + str(validator.errors)}, 400

        data = request.get_json(force=True)

        # --------------------------
        # Check if article is in database and, if not, insert it on database.
        # --------------------------
        crowdsourced_article = CrowdsourcedArticle.query.filter_by(url=data["url"]).first()
        if not crowdsourced_article:
            try:
                user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
                n3k_config = Config()
                n3k_config.browser_user_agent = user_agent

                article = Article(data["url"], config=n3k_config)
                article.download()
                article.parse()

                if article.title == "" or article.text == "":
                    return {'message': f"Failed to scrape article (unable to retrieve headline or body text): " +\
                                       str(data["url"])}, 500
                else:
                    publish_date = None
                    if article.publish_date:
                        publish_date = article.publish_date.strftime('%Y-%m-%d %H:%M:%S')

                    erc_flag = True if is_registered_domain(data["url"]) else False
                    crowdsourced_article = CrowdsourcedArticle(
                        headline=article.title,
                        body_text=article.text,
                        url=data["url"],
                        top_image=article.top_image,
                        publish_date=publish_date,
                        erc_registered=erc_flag
                    )

                    # TODO:
                    # article.top_image > save blob

                    config.db.session.add(crowdsourced_article)
                    config.db.session.commit()

            except Exception as err:
                print(err)
                return {'message': f"Failed to scrape article: " + str(data["url"]) + "."}, 500

        article_data = {
            "id": crowdsourced_article.id,
            "url": crowdsourced_article.url,
            "headline": crowdsourced_article.headline,
            "body_text": crowdsourced_article.body_text,
            "top_image": crowdsourced_article.top_image,
            "publish_date": None
        }
        if crowdsourced_article.publish_date:
            article_data["publish_date"] = crowdsourced_article.publish_date.isoformat()
        return article_data, 200
