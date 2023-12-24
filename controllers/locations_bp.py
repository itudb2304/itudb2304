from flask import Blueprint, render_template, request, redirect, url_for, abort
from repository.locations_repository import LocationsRepository
from repository.locations_repository import Location

def locations_bp(connection):
    locations = Blueprint(
        'locations',
        __name__,
        template_folder='../templates/locations',
        static_folder='static/',
        url_prefix="/locations"
    )

    repository = LocationsRepository(connection=connection)

    @locations.route('/', methods=['GET', 'POST'])
    def locations_page():      
        if request.method == "POST":    
            building_key = request.form["building_key"] 
            if "delete" in request.form:
                building = repository.get_location(building_key)
                repository.delete_location(building)
                return redirect(url_for("locations.locations_page"))
            if "edit" in request.form:
                return redirect(url_for('locations.building_edit_page', building_id=building_key))
        else:
            filter = request.args.get("locations-search")
            locations = repository.get_locations(filter)
            buildings = repository.get_buildings()
            return render_template("locations.html", locations=locations, buildings=buildings)
    
    @locations.route('building/<building_id>', methods=['GET', 'POST'])
    def building_page(building_id): 
        if request.method == "POST":           
            if "delete" in request.form:
                building = repository.get_location(building_id)
                repository.delete_location(building)
                return redirect(url_for("locations.locations_page"))
            if "edit" in request.form:
                return redirect(url_for('locations.building_edit_page', building_id=building_id))
        else:
            building = repository.get_location(building_id)
            floors = repository.get_floors(building_id)
            return render_template("building.html", building = building, floors = floors)
    
    @locations.route('/new_building', methods=['GET', 'POST'])
    def building_add_page():
        if request.method == "GET":
            values = {"name": "", "isPublic": "", "floors": ""}
            return render_template("building_edit.html", values = values)
        if 'save' in request.form:
            building_name = request.form["name"]
            building_isPublic = 1 if request.form["isPublic"] == 'Yes' else 0
            building_floors = request.form.getlist('floors[]')
            building = Location(building_name, "building", building_isPublic)
            building_key = repository.add_location(building)
            for floor_name in building_floors:
                new_floor = Location(floor_name, "floor", 0, building_key)
                repository.add_location(new_floor)          
            return redirect(url_for("locations.locations_page"))
        else:
            return redirect(url_for("locations.locations_page"))
    
    @locations.route('/<building_id>/edit', methods=['GET', 'POST'])
    def building_edit_page(building_id):
        if request.method == "GET":
            building = repository.get_location(building_id)
            building_isPublic = 'Yes' if building.isPublic == 1  else 'No'
            building_floors = repository.get_floors(building_id)
            values = {"name": building.name, "isPublic": building_isPublic, "floors": building_floors}
            return render_template("building_edit.html", values = values)
        if 'save' in request.form:
            building_name = request.form["name"]
            building_isPublic = 1 if request.form["isPublic"] == 'Yes' else 0
            building_floors = request.form.getlist('floors[]')
            building = Location(building_name, "building", building_isPublic, key = building_id)
            repository.update_location(building)
            for floor_name in building_floors:
                new_floor = Location(floor_name, "floor", 0, building_id)
                repository.add_location(new_floor)
                
            return redirect(url_for("locations.building_page", building_id=building_id))
        else:
            return redirect(url_for("locations.building_page", building_id=building_id  ))

    @locations.route('floor/<floor_id>', methods=['GET', 'POST'])
    def floor_page(floor_id): 
        if request.method == "POST":           
            if "delete" in request.form:
                floor = repository.get_location(floor_id)
                repository.delete_location(floor)
                return redirect(url_for("locations.locations_page"))
            if "edit" in request.form:
                return redirect(url_for('locations.floor_edit_page', floor_id=floor_id))
        else:
            rooms = repository.get_rooms(floor_id)
            floor = repository.get_location(floor_id)
            return render_template("floor.html", rooms=rooms, floor=floor)
    
    @locations.route('floor/<floor_id>/edit', methods=['GET', 'POST'])
    def floor_edit_page(floor_id):
        floor = repository.get_location(floor_id)
        if request.method == "GET":
            if floor is None:
                abort(404)
            floor_isPublic = 'Yes' if floor.isPublic == 1  else 'No'
            floor_rooms = repository.get_rooms(floor_id)
            values = {"name": floor.name, "isPublic": floor_isPublic, "rooms": floor_rooms}
            return render_template("floor_edit.html", values = values)
        if 'save' in request.form:
            floor_name = request.form["name"]
            floor_isPublic = 1 if request.form["isPublic"] == 'Yes' else 0
            floor_rooms = request.form.getlist('rooms[]')
            updated_floor = Location(floor_name, "floor", floor_isPublic, floor.partof, floor_id)
            repository.update_location(updated_floor)
            for room_name in floor_rooms:
                building = repository.get_location(floor.partof)
                room = Location(room_name, "room", 0, floor_id, building=building.name)
                room_key = repository.add_location(room)
                room.key = room_key
                repository.add_locationid(room)
            return redirect(url_for("locations.floor_page", floor_id=floor_id))
        else:
            return redirect(url_for("locations.floor_page", floor_id=floor_id))
    
    @locations.route('room/<room_id>', methods=['GET', 'POST'])
    def room_page(room_id):  
        room = repository.get_location(room_id)     
        if request.method == "POST":       
            if "delete" in request.form:
                repository.delete_location(room)       
                return redirect(url_for("locations.floor_page", floor_id=room.partof))
            if "edit" in request.form:
                return redirect(url_for('locations.room_edit_page', room_id=room_id))
        else:
            objects = repository.get_objects(room_id)
            return render_template("room.html", objects=objects, room=room)
    
    @locations.route('room/<room_id>/edit', methods=['GET', 'POST'])
    def room_edit_page(room_id):
        room = repository.get_location(room_id)
        if request.method == "GET":
            room_isPublic = 'Yes' if room.isPublic == 1  else 'No'
            room_objects = repository.get_objects(room_id)
            values = {"name": room.name, "isPublic": room_isPublic, "objects": room_objects}
            return render_template("room_edit.html", values = values)
        if 'save' in request.form:
            room_name = request.form["name"]
            room_isPublic = 1 if request.form["isPublic"] == 'Yes' else 0
            room_objects = request.form.getlist('objects[]')
            removed_objects = request.form.getlist('removed_objects[]')
            for object_id in removed_objects:
                repository.remove_object(object_id, room_id)
            updated_room = Location(room_name, "room", room_isPublic, room.partof, room_id)
            repository.update_location(updated_room)
            repository.update_locationid(updated_room)
            for object_id in room_objects:
                repository.add_object(object_id, room_id)
            return redirect(url_for("locations.room_page", room_id=room_id))
        else:
            return redirect(url_for("locations.room_page", room_id=room_id))
    
    return locations
