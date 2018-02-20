class InputFileReader:
    d3_index = 0
    user_id_index = 1
    d2_index = 2
    date_index = 3
    d1_index = 4
    
    parts_count = 5
            
    def handle_data_row(self, user_id, day, d1_category, d2_category, d3_category):
        raise "Method handle_data_row must be overriden!"
        
    @staticmethod        
    def format_line(user_id, day, d1_category, d2_category, d3_category):
        parts = [0] * InputFileReader.parts_count
        parts[InputFileReader.user_id_index] = user_id
        parts[InputFileReader.date_index] = day
        parts[InputFileReader.d1_index] = d1_category
        parts[InputFileReader.d2_index] = d2_category
        parts[InputFileReader.d3_index] = d3_category
        return ",".join(parts) + "\n"
        
    def read_input_file(self, input_file):
        with open(input_file, 'r') as input_data:
            # read and save the header
            self.header = input_data.next()
            for line in input_data:
                view = line.strip().split(',')
                if len(view) < InputFileReader.parts_count:
                    print ("malformed or empty line: ", line)
                    continue
                user_id = view[InputFileReader.user_id_index]
                day = view[InputFileReader.date_index]
                d1_category = view[InputFileReader.d1_index]
                d2_category = view[InputFileReader.d2_index]
                d3_category = view[InputFileReader.d3_index]
            
                self.handle_data_row(user_id, day, d1_category, d2_category, d3_category)
           