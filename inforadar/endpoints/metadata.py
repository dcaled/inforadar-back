from flask_restful import Resource

from inforadar.models import CategorySchema, Category


class Metadata(Resource):
    def get(self):
        # Create the list of categories from our data
        category = Category.query.order_by(Category.id).all()

        # Serialize the data for the response
        category_schema = CategorySchema(many=True)
        category_data = category_schema.dump(category)

        # Order to be exhibit in the front-end.
        front_end_order = ["factual", "opinion", "entertainment", "satire", "conspiracy"]
        response = sorted(category_data, key=lambda k: front_end_order.index(k["name"]))

        return response
