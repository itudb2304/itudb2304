class objectTextEntryDTO:
    texttypes = [ "bibliography", "exhibition_history", "lifetime_exhibition", "other_collections", "exhibition_history_footnote", "documentary_labels_inscriptions", "inscription_footnote"]
    def __init__(self, data):
        text_entries = {text_type: [] for text_type in self.texttypes}

        for row in data:
            text_type = row[2]
            if text_type in self.texttypes:
                text_entries[text_type].append([row[1], row[3]]) #text, year
        self.text_entries = text_entries
