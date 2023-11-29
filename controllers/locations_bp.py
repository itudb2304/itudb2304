from flask import Blueprint, render_template
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
    
    @locations.route('/<location>')
    def location_page(location):  
        floors = repository.get_floors(location)
        return render_template("location.html", floors=floors)

    return locations
