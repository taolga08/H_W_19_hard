from flask import request
from flask_restx import Resource, Namespace

from dao.model.genre import GenreSchema
from helpers import auth_required, admin_required
from implemented import genre_service

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):
    @auth_required
    def get(self):
        all_genre = genre_service.get_all()
        res = GenreSchema(many=True).dump(all_genre)
        return res, 200

    @admin_required
    def post(self):
        req_json = request.json
        genre = genre_service.create(req_json)
        return "", 201, {"location": f"/genres/{genre.id}"}


@genre_ns.route('/<int:gid>')
class GenreView(Resource):
    @auth_required
    def get(self, gid):
        genre = genre_service.get_one(gid)
        genre_data = GenreSchema().dump(genre)
        return genre_data, 200

    @admin_required
    def put(self, gid):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = gid
        genre_service.update(req_json)
        return "", 204

    @admin_required
    def delete(self, gid):
        genre_service.delete(gid)
        return "", 204
