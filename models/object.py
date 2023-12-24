class ObjectDTO:
    def __init__(self, data=None):
        if data is None:
            self.objectid = None
            self.accessioned = None
            self.accessionnum = None
            self.locationid = None
            self.title = None
            self.displayDate = None
            self.beginYear = None
            self.endYear = None
            self.visualBrowserTimeSpan = None
            self.medium = None
            self.dimensions = None
            self.inscription = None
            self.markings = None
            self.attributionInverted = None
            self.attribution = None
            self.provenanceText = None
            self.creditLine = None
            self.classification = None
            self.subClassification = None
            self.visualBrowserClassification = None
            self.parentid = None
            self.isVirtual = None
            self.departmentabbr = None
            self.portfolio = None
            self.series = None
            self.volume = None
            self.watermarks = None
            self.lastDetectedModification = None
            self.wikidataid = None
            self.customPrintURL = None
        else:
            self.objectid, self.accessioned, self.accessionnum, self.locationid, self.title, self.displayDate, self.beginYear, \
            self.endYear, self.visualBrowserTimeSpan, self.medium, self.dimensions, self.inscription, self.markings, \
            self.attributionInverted, self.attribution, self.provenanceText, self.creditLine, self.classification, \
            self.subClassification, self.visualBrowserClassification, self.parentid, self.isVirtual, self.departmentabbr, \
            self.portfolio, self.series, self.volume, self.watermarks, self.lastDetectedModification, self.wikidataid, \
            self.customPrintURL = self._handle_none_values(data)

    def _handle_none_values(self, data):
        return tuple(None if value is None or str(value).lower() == "none" else value for value in data)

    classification_elements = ["Painting", "Print", "Sculpture", "Drawing","Volume", "Portfolio","Photograph","New Media","Decorative Art","Technical Material"]
