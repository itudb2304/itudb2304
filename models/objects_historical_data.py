class ObjectsHistoricalData:
    def __init__(
        self,
        dataType: str,
        objectID: int,
        displayOrder: int,
        forwardText: str = None,
        invertedText: str = None,
        remarks: str = None,
        effectiveDate: str = None
    ):
        self.dataType = dataType
        self.objectID = objectID
        self.displayOrder = displayOrder
        self.forwardText = forwardText
        self.invertedText = invertedText
        self.remarks = remarks
        self.effectiveDate = effectiveDate
