from flask import Blueprint, render_template
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

    @objects.route('/')
    def objects_page():
        objects = repository.get_all_objects()
        return render_template('objects.html', objects=objects)
    
    @objects.route('/<int:objectid>')
    def object_page(objectid):
        object = repository.get_object_by_objectid(objectid)
        objectLocation = repository.get_location_by_locationid(object.locationid)
        return render_template('object.html', object=object, objectLocation=objectLocation)
    return objects