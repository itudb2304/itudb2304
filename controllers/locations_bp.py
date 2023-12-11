from flask import Blueprint, render_template, request, redirect, url_for, abort
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

    @locations.route('/', methods=['GET', 'POST'])
    def locations_page():
        if request.method == "GET":
            locations = repository.get_buildings()
            return render_template("locations.html", locations=locations)
        else:
            form_location_keys = request.form.getlist("location_keys")
            for form_location_key in form_location_keys:
                repository.delete_location(form_location_key)
            return redirect(url_for("locations.locations_page"))
    
    @locations.route('/new_building', methods=['GET', 'POST'])
    def building_add_page():
        if request.method == "GET":
            values = {"name": "", "isPublic": ""}
            return render_template("locations_edit.html", values = values)
        else:
            building_name = request.form["name"]
            building_isPublic = 1 if request.form["isPublic"] == 'Yes' else 0
            building = Location(building_name, "building", building_isPublic)
            repository.add_location(building)
            return redirect(url_for("locations.locations_page"))
    
    @locations.route('/<building_id>/edit', methods=['GET', 'POST'])
    def building_edit_page(building_id):
        if request.method == "GET":
            building = repository.get_location(building_id)
            if building is None:
                abort(404)
            building_isPublic = 'Yes' if building.isPublic == 1  else 'No'
            values = {"name": building.name, "isPublic": building_isPublic}
            return render_template("locations_edit.html", values = values)
        else:
            building_name = request.form["name"]
            building_isPublic = 1 if request.form["isPublic"] == 'Yes' else 0
            building = Location(building_name, "building", building_isPublic, key = building_id)
            print(building.key)
            repository.update_location(building)
            return redirect(url_for("locations.locations_page"))


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
