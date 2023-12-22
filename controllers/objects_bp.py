from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from repository.objects_repository import ObjectDTO, ObjectsRepository
from flask import redirect, url_for, render_template, request, jsonify
from repository.media_repository import MediaRepository
from math import ceil

def objects_bp(connection):
    objects = Blueprint(
        'objects',
        __name__,
        template_folder='templates/',
        static_folder='static/',
        url_prefix="/objects",
    )

    repository = ObjectsRepository(connection=connection)

    @objects.route('/', methods=['GET', 'POST'])
    def objects_page():
        if request.method == "GET":
            selected_classifications = request.args.getlist('classification')
            print(selected_classifications)
            title_filter = request.args.get('title')
            credit_line_filter = request.args.get('creditLine')
            page = request.args.get('page', default=1, type=int)
            objects_per_page = 20

            objects = repository.get_all_objects(selected_classifications, title_filter, credit_line_filter)
            total_pages = ceil(len(objects) / objects_per_page)

            start_index = (page - 1) * objects_per_page
            end_index = start_index + objects_per_page
            paginated_objects = objects[start_index:end_index]

            return render_template("objects.html", objects=paginated_objects, total_pages=total_pages, current_page=page, selected_classifications=selected_classifications, title_filter=title_filter, credit_line_filter=credit_line_filter)

    @objects.route('/object_addition', methods=['GET', 'POST'])
    def object_addition_page():
        newObject = ObjectDTO()
        newObject.objectid = repository.get_max_objectid() + 1

        if request.method == "GET":
            return render_template("object_edit.html", objectDTO=newObject)
        else:
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
            print(constituentslist)
            objectLocation = repository.get_location_by_locationid(object.locationid) if object.locationid else None
            media = None # fill later
            if media is None:
                media = "https://via.placeholder.com/150"

            return render_template('object.html', object=object,constituentslist=constituentslist, objectLocation=objectLocation, media=media, text_entry=object_text_entries.text_entries)
        else:
            repository.delete_object(objectid)
            print("Deleted object with objectid successfuly", objectid)
            return jsonify(success=True)

    @objects.route('/<int:objectid>/edit', methods=["GET", "POST"])
    def object_edit_page(objectid):
        if request.method == "GET":
            object = repository.get_object_by_objectid(objectid)
            return render_template('object_edit.html',objectDTO=object)
        else:
            objectDTO = repository.get_object_by_objectid(objectid)
            # update the objectDTO with the form data
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
            
            # update the object in the database
            repository.update_object(objectDTO)
            return redirect(url_for('objects.object_page', objectid=objectid))

    return objects