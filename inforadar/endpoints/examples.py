from flask_restful import Resource

from inforadar.models import CrowdsourcedArticleSchema, CrowdsourcedArticle, CrowdsourcedIndicatorScore


class Examples(Resource):
    def get(self):
        # Create the list of csarticles from our data
        csarticle = CrowdsourcedArticle .query \
                                        .join(CrowdsourcedIndicatorScore, CrowdsourcedIndicatorScore.crowdsourced_article_id == CrowdsourcedArticle.id) \
                                        .group_by(CrowdsourcedArticle.id) \
                                        .filter(CrowdsourcedArticle.erc_registered == True) \
                                        .order_by(CrowdsourcedArticle.id.desc()).limit(3).all()

        # Serialize the data for the response
        csarticle_schema = CrowdsourcedArticleSchema(many=True)
        csarticle_data = csarticle_schema.dump(csarticle)

        return csarticle_data
