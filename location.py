class Location:
    def __init__(self, building, location_key, description = "") -> None:
        self.building = building
        self.location_key = location_key
        self.location_id = None
        self.description = description
