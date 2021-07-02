from flask_restful import Resource

from inforadar.models import CategorySchema, Category


class Metadata(Resource):
    def get(self):
        # Create the list of categories from our data
        category = Category.query.order_by(Category.id).all()

        # Serialize the data for the response
        category_schema = CategorySchema(many=True)
        data = category_schema.dump(category)
        return data
