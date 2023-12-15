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
            return redirect(url_for('objects.objects_page'))
        
    return objects