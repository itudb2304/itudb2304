from flask import Blueprint, render_template, request, redirect, url_for, flash
from repository.constituent_repository import ConstituentRepository
from repository.objects_repository import ObjectsRepository
from flask_paginate import Pagination, get_page_args

def constituents_bp(connection):
    constituents = Blueprint(
        "constituents",
        __name__,
        template_folder="../templates/constituents",
        static_folder="static/",
        url_prefix="/constituents",
    )

    repository = ConstituentRepository(connection=connection)
    objects_repository = ObjectsRepository(connection=connection)

    constituent_attributes = [
        "ulanid",
        "preferred-display-name",
        "forward-display-name",
        "lastname",
        "display-date",
        "artist-of-nga-object",
        "birthyear",
        "deathyear",
        "visualbrowsertimespan",
        "nationality",
        "constituent-type",
        "wikidataid",
    ]

    constituent_objects_attributes = [
        "objectid",
        "constituentid",
        "roletype",
        "role",
        "displaydate",
        "displayorder",
        "country",
    ]

    @constituents.route("/", methods=["GET", "POST"])
    def constituents_page():
        if request.method == "POST":
            if "constituent-search" in request.form:
                req = request.form["constituent-search"]
                return redirect(url_for(".constituent_by_name", name=req))
            elif "add-constituent" in request.form:
                req = request.form["add-constituent"]
                return redirect(url_for(".add_constituent"))
        else:
            page, per_page, offset = get_page_args(
                page_parameter="page", per_page_parameter="per_page"
            )
            per_page = 50
            total = repository.get_number_of_constituents()
            pagination_constituents = repository.get_all_constituents(
                offset=offset, limit=per_page
            )
            pagination = Pagination(
                page=page, per_page=per_page, total=total, css_framework='bootstrap4'
            )
            constituent_id = request.args.get("constituent_id")
            return render_template(
                "constituents.html",
                constituents_list=pagination_constituents,
                page=page,
                per_page=per_page,
                pagination=pagination
            )

    @constituents.route("/<string:name>", methods=["GET", "POST"])
    def constituent_by_name(name: str):
        if request.method == "POST":
            if "constituent-search" in request.form:
                req = request.form["constituent-search"]
                return redirect(url_for(".constituent_by_name", name=req))
            elif "add-constituent" in request.form:
                req = request.form["add-constituent"]
                return redirect(url_for(".add_constituent"))
        else:
            page, per_page, offset = get_page_args(
                page_parameter="page", per_page_parameter="per_page"
            )
            per_page = 50
            total = repository.get_number_of_constituents_by_name(name=name)
            pagination_constituents = repository.get_constituents_by_name(name=name, offset=offset, limit=per_page)
            pagination = Pagination(
                page=page, per_page=per_page, total=total, css_framework='bootstrap4'
            )
            return render_template(
                "constituents.html",
                constituents_list=pagination_constituents,
                page=page,
                per_page=per_page,
                pagination=pagination
            )

    @constituents.route("/add", methods=["GET", "POST"])
    def add_constituent():
        if request.method == "GET":
            return render_template("constituents_add.html")
        else:
            attributes = []
            for key in constituent_attributes:
                if key in request.form and len(request.form[key]):
                    attributes.append(request.form[key])
                else:
                    attributes.append(None)
            repository.add_constituent(attributes=attributes)
            flash("Constituent has been added successfully.", "success")
            return render_template("constituents_add.html")

    @constituents.route("/<int:id>", methods=["GET", "POST"])
    def constituent_objects(id: int):
        if request.method == "GET":
            page, per_page, offset = get_page_args(
                page_parameter="page", per_page_parameter="per_page"
            )
            per_page = 48
            total = repository.get_number_of_constituent_objects(id)
            pagination_constituent_objects = repository.constituent_objects(constituentid=id, offset=offset, limit=per_page)
            pagination = Pagination(
                page=page, per_page=per_page, total=total, css_framework='bootstrap4'
            )
            return render_template(
                "constituent_objects.html",
                constituent_objects=pagination_constituent_objects,
                constituentID=id,
                page=page,
                per_page=per_page,
                pagination=pagination
            )
        else:
            if 'add-constituent' in request.form:
                return redirect(url_for(".add_constituent_object", id=id))
            else:
                return redirect(url_for('.constituent_objects_by_name', constituentid=id, name=request.form['constituent-search']))
        
    @constituents.route('/<int:constituentid>/<string:name>', methods=['GET', 'POST'])
    def constituent_objects_by_name(constituentid: int, name: str):
        if request.method == 'GET':
            page, per_page, offset = get_page_args(
                page_parameter="page", per_page_parameter="per_page"
            )
            per_page = 48
            total = repository.number_of_constituent_objects_by_name(constituentid=constituentid, name=name)
            pagination_constituent_objects_by_name = repository.get_constituent_objects_by_name(constituentid=constituentid, name=name,limit=per_page, offset=offset)
            pagination = Pagination(
                page=page, per_page=per_page, total=total, css_framework='bootstrap4'
            )
            return render_template(
                "constituent_objects.html",
                constituent_objects=pagination_constituent_objects_by_name,
                constituentID=constituentid,
                page=page,
                per_page=per_page,
                pagination=pagination
            )
        else:
            return redirect(url_for('.constituent_objects_by_name', constituentid=constituentid, name=name))

    @constituents.route("/<int:id>/add-object", methods=["GET", "POST"])
    def add_constituent_object(id: int):
        if request.method == "GET":
            return render_template(
                "add_constituent_object.html",
                object_ids=repository.get_object_ids(),
                constituent_ids=repository.get_constituent_ids(),
                current_constituent=repository.get_constituent_by_id(id=id),
            )
        else:
            # OBJECT ID VALIDATION
            if "objectid" not in request.form:
                flash("Object ID field cannot be empty.", 'warning')
                return render_template(
                    "add_constituent_object.html",
                    object_ids=repository.get_object_ids(),
                    constituent_ids=repository.get_constituent_ids(),
                    current_constituent=repository.get_constituent_by_id(id=id),
                )
            elif repository.validate_object_id(request.form["objectid"])[0][0] > 0:
                attributes = []
                for att in constituent_objects_attributes:
                    if att in request.form:
                        attributes.append(request.form[att])
                    else:
                        attributes.append(None)
                attributes.append(
                    objects_repository.get_object_by_objectid(attributes[0]).title
                )
                attributes.append(
                    repository.get_constituent_by_id(attributes[1]).forwarddisplayname
                )
                repository.add_constituent_object(attributes=attributes)
                flash("Constituent object has been added successfully.", 'success')
                return render_template(
                    "add_constituent_object.html",
                    object_ids=repository.get_object_ids(),
                    constituent_ids=repository.get_constituent_ids(),
                    current_constituent=repository.get_constituent_by_id(id=id),
                )
            else:
                flash("Object ID invalid.", 'warning')
                return render_template(
                    "add_constituent_object.html",
                    object_ids=repository.get_object_ids(),
                    constituent_ids=repository.get_constituent_ids(),
                    current_constituent=repository.get_constituent_by_id(id=id),
                )

    @constituents.route(
        "/<int:constituent_id>/<int:relation_id>/", methods=["GET", "POST"]
    )
    def update_constituent_object(constituent_id: int, relation_id: int):
        if request.method == "GET":
            constituent_object = repository.get_constituent_object_by_id(relation_id)
            return render_template(
                "edit_constituent_object.html", constituent_object=constituent_object
            )
        else:
            attributes = []
            for att in constituent_objects_attributes:
                if att in request.form:
                    attributes.append(request.form[att])
                else:
                    attributes.append(None)
            repository.update_constituent_object(
                attributes=attributes, relationid=relation_id
            )
            flash("Constituent has been updated successfully.", "success")
            constituent_object = repository.get_constituent_object_by_id(relation_id)
            return render_template(
                "edit_constituent_object.html", constituent_object=constituent_object
            )

    @constituents.route(
        "/<int:constituentid>/<int:relationid>/delete", methods=["GET", "POST"]
    )
    def delete_constituent_object(constituentid: int, relationid: int):
        repository.delete_constituent_object(relationid=relationid)
        return redirect(url_for(".constituent_objects", id=constituentid))

    return constituents
