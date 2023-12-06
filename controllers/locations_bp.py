from flask import Blueprint, render_template, request
from repository.locations_repository import LocationsRepository
from repository.locations_repository import Location

def locations_bp(connection):
    locations = Blueprint(
        'locations',
        __name__,
        template_folder='templates/',
        static_folder='static/',
        url_prefix="/locations"
    )

    repository = LocationsRepository(connection=connection)

    @locations.route('/')
    def locations_page():
        locations = repository.get_buildings()
        return render_template("locations.html", locations=locations)
            

    @locations.route('/<floor_id>')
    def floor_page(floor_id):
        rooms = repository.get_rooms(floor_id)
        return render_template("location.html", rooms=rooms)
    
    @locations.route('/<location_id>')
    def location_page(location_id):
        locationkey = repository.get_locationkey(location_id)        
        rooms = repository.get_rooms(locationkey)
        return render_template("location.html", rooms=rooms)

    return locations
