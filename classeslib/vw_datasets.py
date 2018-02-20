class VwDatasetWriter:
    row_format = '{} {}-{} |Data {} |Candidate {}\n'    
     
    def __init__(self, writable_file):
        self.file = writable_file
        
    def write(self, class_label, user_id, candidate, data):
        row = VwDatasetWriter.row_format.format(class_label, user_id, candidate, data, candidate)
        self.file.write(row)
        
        