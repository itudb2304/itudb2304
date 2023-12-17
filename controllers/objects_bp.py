from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from repository.objects_repository import ObjectsRepository

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
            objects = repository.get_all_objects()
            return render_template("objects.html", objects=objects)
        
    
    @objects.route('/<int:objectid>', methods=["GET", "POST"])
    def object_page(objectid):
        if request.method == "GET":
            object = repository.get_object_by_objectid(objectid)
            objectLocation = repository.get_location_by_locationid(object.locationid)
            return render_template('object.html', object=object, objectLocation=objectLocation)
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

            print(objectDTO)
            print("Form data:", request.form)
            
            # update the object in the database
            repository.update_object(objectDTO)
            return redirect(url_for('objects.object_page', objectid=objectid))

    return objects