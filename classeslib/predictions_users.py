if __name__ == '__main__': 
    from input_file_reader import InputFileReader
else:
    from classeslib.input_file_reader import InputFileReader

class PredictionUser:
    def __init__(self):
        self.views = 0
        self.silent_weeks_d3_categories = set()
        self.target_categories = set() 
        
class SilentWeeksReader(InputFileReader):
    def __init__(self, users={}):
        self.users = users
        
    def handle_data_row(self, user_id, day, d1_category, d2_category, d3_category):
        if not self.users.has_key(user_id):
            self.users[user_id] = PredictionUser()
        self.users[user_id].views += 1
        self.users[user_id].silent_weeks_d3_categories.add(d3_category)
        if d3_category in self.users[user_id].target_categories:
            self.users[user_id].target_categories.remove(d3_category)
        
class FutureWeekReader(InputFileReader):
    def __init__(self, users={}):
        self.users = users
    
    def handle_data_row(self, user_id, day, d1_category, d2_category, d3_category):
        if not self.users.has_key(user_id):
            self.users[user_id] = PredictionUser()
        self.users[user_id].views += 1
        if not d3_category in self.users[user_id].silent_weeks_d3_categories:
            self.users[user_id].target_categories.add(d3_category)