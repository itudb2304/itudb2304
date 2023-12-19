from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from repository.objects_repository import ObjectDTO, ObjectsRepository
from flask import redirect, url_for, render_template, request, jsonify
from repository.media_repository import MediaRepository

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
            objects = repository.get_all_objects(selected_classifications)
            return render_template("objects.html", objects=objects)
 
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
            print(object.locationid)
            objectLocation = repository.get_location_by_locationid(object.locationid) if object.locationid else None
            media = None # fill later
            if media is None:
                media = "https://via.placeholder.com/150"
            return render_template('object.html', object=object, objectLocation=objectLocation, media=media)
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