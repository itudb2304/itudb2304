from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from repository.objects_repository import ObjectDTO, ObjectsRepository
from flask import redirect, url_for, render_template, request, jsonify
from flask_paginate import Pagination, get_page_args

def objects_bp(connection):
    objects = Blueprint(
        'objects',
        __name__,
        template_folder='../templates/objects',
        static_folder='static/',
        url_prefix="/objects",
    )

    repository = ObjectsRepository(connection=connection)

    @objects.route('/', methods=['GET', 'POST'])
    def objects_page():
        if request.method == "GET":
            selected_classifications = request.args.getlist('classification')
            title_filter = request.args.get('title')
            credit_line_filter = request.args.get('creditLine')

            if request.args.get('sort'):
                sort_by_title = request.args.get('sort')
            else:
                sort_by_title = "none"

            page, per_page, offset = get_page_args(
                page_parameter="page", per_page_parameter="per_page"
            )
            all_objects = repository.get_all_objects(selected_classifications, title_filter, credit_line_filter, sort_by_title)
            objects = repository.get_all_objects(selected_classifications, title_filter, credit_line_filter, sort_by_title, limit=per_page, offset=offset)
           
            per_page = 20
            totalLen = len(all_objects)
            pagination = Pagination(
                page=page, per_page=per_page, total=totalLen, css_framework='bootstrap4'
            )
            return render_template("objects.html", 
                                objects=objects,
                                page=page, 
                                per_page=per_page,
                                pagination=pagination, 
                                selected_classifications=selected_classifications, 
                                title_filter=title_filter, 
                                credit_line_filter=credit_line_filter,
                                sort=sort_by_title)

    @objects.route('/object_addition', methods=['GET', 'POST'])
    def object_addition_page():
        newObject = ObjectDTO()
        newObject.objectid = repository.get_max_objectid() + 1

        if request.method == "GET":
            return render_template("object_edit.html", objectDTO=newObject)
        else:
            photoUrl = request.form["textUrl"]
            assistiveText = request.form["assistiveText"]
            if(photoUrl != ""):
                repository.add_media_to_object(newObject.objectid, photoUrl, assistiveText)

            newObject.accessioned = request.form["accessioned"]
            newObject.accessionnum = request.form["accessionnum"]
            newObject.title = request.form["title"]
            newObject.beginYear = request.form["beginYear"]
            newObject.endYear = request.form["endYear"]
            newObject.medium = request.form["medium"]
            newObject.attribution = request.form["attribution"]
            newObject.creditLine = request.form["creditLine"]
            newObject.classification = request.form["classification"]
            newObject.isVirtual = request.form["isVirtual"]

            newObject.displayDate = newObject.beginYear if newObject.beginYear == newObject.endYear else newObject.beginYear + "," + newObject.endYear 
            newObject.visualBrowserTimeSpan = f"{(int(newObject.beginYear) // 25) * 25 + 1} to {(int(newObject.beginYear) // 25 + 1) * 25}"
            newObject.visualBrowserClassification = newObject.classification.lower()
            newObject.attributionInverted = " ".join(reversed(newObject.attribution.split(",")))

            repository.add_object(newObject)
            return redirect(url_for('objects.object_page', objectid=newObject.objectid))
        
    
    @objects.route('/<int:objectid>', methods=["GET", "POST"])
    def object_page(objectid):
        if request.method == "GET":
            object = repository.get_object_by_objectid(objectid)
            object_text_entries = repository.get_object_text_entries(objectid) 
            constituentslist = repository.get_object_constituents(objectid)
            objectLocation = repository.get_location_by_locationid(object.locationid) if object.locationid else None
            media = repository.get_media_by_objectid(objectid)
            return render_template('object.html', object=object,constituentslist=constituentslist, objectLocation=objectLocation, media=media, text_entry=object_text_entries.text_entries)
        else:
            repository.delete_object(objectid)
            return jsonify(success=True)

    @objects.route('/<int:objectid>/edit', methods=["GET", "POST"])
    def object_edit_page(objectid):
        if request.method == "GET":
            object = repository.get_object_by_objectid(objectid)
            media = repository.get_media_by_objectid(objectid)
            return render_template('object_edit.html',objectDTO=object, media=media)
        else:
            alteredAssistiveText = request.form["alteredAssistiveText"]
            repository.edit_media_of_object(objectid, alteredAssistiveText)

            objectDTO = repository.get_object_by_objectid(objectid)
            objectDTO.accessioned = request.form["accessioned"]
            objectDTO.accessionnum = request.form["accessionnum"]
            objectDTO.title = request.form["title"]
            objectDTO.beginYear = request.form["beginYear"]
            objectDTO.endYear = request.form["endYear"]
            objectDTO.medium = request.form["medium"]
            objectDTO.attribution = request.form["attribution"]
            objectDTO.creditLine = request.form["creditLine"]
            objectDTO.classification = request.form["classification"]
            objectDTO.isVirtual = request.form["isVirtual"]

            objectDTO.displayDate = objectDTO.beginYear if objectDTO.beginYear == objectDTO.endYear else objectDTO.beginYear + "," + objectDTO.endYear 
            objectDTO.visualBrowserTimeSpan = f"{(int(objectDTO.beginYear) // 25) * 25 + 1} to {(int(objectDTO.beginYear) // 25 + 1) * 25}"
            objectDTO.visualBrowserClassification = objectDTO.classification.lower()
            objectDTO.attributionInverted = " ".join(reversed(objectDTO.attribution.split(",")))
            
            repository.update_object(objectDTO)
            return redirect(url_for('objects.object_page', objectid=objectid))

    return objects