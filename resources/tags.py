from flask import request, jsonify
from flask_restful import Resource, reqparse
from models.tags import (
    TagsModel
)
from models.schemas import (
    TagsSchema
)

class AddTag(Resource):
    def post(self):
        data = request.get_json(force=True)

        for _data in data:
            print(_data)
            if TagsModel.find_by_tag(_data['tag']):
                return {"message": "Tag already exists"}, 400
            data_to_input = TagsModel(
                tag = _data['tag']
            )
            data_to_input.save_to_db()

        return {
            "message": "Success!",
        }, 200

class GetAllTagsAPI(Resource):
    @classmethod
    def get(cls):
        tags_schema = TagsSchema(many=True)
        tags = TagsModel.query.all()
        output = tags_schema.dump(tags)
        return output