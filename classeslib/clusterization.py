class UsersClaster:
    def __init__(self, label, center):
        self.label = label
        self.center = center
        self.d3_categories_popularity = {}
        self.d3_categories_sorted = []
    
    def add_user_d3_categories(self, user):                    
        for d3_category in user.d3_categories.keys():
            if not self.d3_categories_popularity.has_key(d3_category):
                self.d3_categories_popularity[d3_category] = user.d3_categories[d3_category].views
            else:
                self.d3_categories_popularity[d3_category] += user.d3_categories[d3_category].views                 