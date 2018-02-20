class UserCategory:
    def __init__(self):
        self.views = 0
        self.from_silent_weeks = False

class UserInterests:       
    def __init__(self, user_id):
        self.user_id = user_id
        self.total_views = 0
        self.d1_categories = {}
        self.d2_categories = {}
        self.d3_categories = {}
        
    def update_category_statistics(self, categories_dict, category, update_count, silent_week):
        if not categories_dict.has_key(category):
            categories_dict[category] = UserCategory()
        categories_dict[category].views += update_count
        categories_dict[category].from_silent_weeks |= silent_week
    
    def increment_views(self, d1_category, d2_category, d3_category, silent_week):
        self.total_views += 1
        self.update_category_statistics(self.d1_categories, d1_category, 1, silent_week)
        self.update_category_statistics(self.d2_categories, d2_category, 1, silent_week)
        self.update_category_statistics(self.d3_categories, d3_category, 1, silent_week)                       
    
    def update_statistics(self, partial_statistic):
        self.total_views += partial_statistic.total_views  
        
        for category in partial_statistic.d1_categories.keys():
            d1_category = partial_statistic.d1_categories[category]
            self.update_category_statistics(
                self.d1_categories,
                category,
                d1_category.views,
                d1_category.from_silent_weeks)
        
        for category in partial_statistic.d2_categories.keys():
            d2_category = partial_statistic.d2_categories[category]
            self.update_category_statistics(
                self.d2_categories,
                category,
                d2_category.views,
                d2_category.from_silent_weeks)
            
        for category in partial_statistic.d3_categories.keys():
            d3_category = partial_statistic.d3_categories[category]
            self.update_category_statistics(
                self.d3_categories,
                category,
                d3_category.views,
                d3_category.from_silent_weeks)
    
    def reset(self):
        self.total_views = 0
        self.d1_categories = {}
        self.d2_categories = {}
        self.d3_categories = {}
        
# Tests
if __name__ == '__main__': 
    
    # Test viewed categories increment
    
    # arrange
    user_interests = UserInterests("user1")

    # act
    user_interests.increment_views("category_d1_1", "category_d2_11", "category_d3_111", False)
    user_interests.increment_views("category_d1_1", "category_d2_11", "category_d3_113", True)
    user_interests.increment_views("category_d1_1", "category_d2_12", "category_d3_124", False)

    user_interests.increment_views("category_d1_3", "category_d2_34", "category_d3_345", True)

    # assert
    assert user_interests.total_views == 4, "wrong total views count!"
    assert len(user_interests.d1_categories) == 2, "wrong d1 categories!"
    assert len(user_interests.d2_categories) == 3, "wrong d2 categories!"
    assert len(user_interests.d3_categories) == 4, "wrong d3 categories!"

    # category_d1_1
    category_d1_1_views = user_interests.d1_categories["category_d1_1"]
    category_d1_1_passed = category_d1_1_views.views == 3
    assert category_d1_1_passed, "wrong category_d1_1 views count"

    # category_d2_11
    category_d2_11_views = user_interests.d2_categories["category_d2_11"]
    category_d2_11_passed = category_d2_11_views.views == 2
    assert category_d2_11_passed, "wrong category_d2_11 views count"

    # category_d3_111
    category_d3_111_views = user_interests.d3_categories["category_d3_111"]
    category_d3_111_passed = (category_d3_111_views.views == 1 
                          and not category_d3_111_views.from_silent_weeks)
    assert category_d3_111_passed, "wrong category_d3_111 views state"

    # category_d3_113
    category_d3_113_views = user_interests.d3_categories["category_d3_113"]
    category_d3_113_passed = (category_d3_113_views.views == 1 
                          and category_d3_113_views.from_silent_weeks)
    assert category_d3_111_passed, "wrong category_d3_113 views state"

    # category_d2_12
    category_d2_12_views = user_interests.d2_categories["category_d2_12"]
    category_d2_12_passed = category_d2_12_views.views == 1
    assert category_d2_12_passed, "wrong category_d2_12 views count"

    # category_d3_124
    category_d3_124_views = user_interests.d3_categories["category_d3_124"]
    category_d3_124_passed = (category_d3_124_views.views == 1 
                          and not category_d3_124_views.from_silent_weeks)
    assert category_d3_124_passed, "wrong category_d3_124 views state"

    # category_d1_3
    category_d1_3_views = user_interests.d1_categories["category_d1_3"]
    category_d1_3_passed = category_d1_3_views.views == 1
    assert category_d1_3_passed, "wrong category_d1_3 views count"

    # category_d2_34
    category_d2_34_views = user_interests.d2_categories["category_d2_34"]
    category_d2_34_passed = category_d2_34_views.views == 1
    assert category_d2_34_passed, "wrong category_d2_34 views count"

    # category_d3_345
    category_d3_345_views = user_interests.d3_categories["category_d3_345"]
    category_d3_345_passed = (category_d3_345_views.views == 1 
                          and category_d3_345_views.from_silent_weeks)
    assert category_d3_111_passed, "wrong category_d3_345 views state"

    print ("Categories views increment - PASSED")
    
    
    # Test user interests partial update
    
    # arrange
    user_interests = UserInterests("user1")
    user_interests_partial = UserInterests("user1")

    # act
    user_interests.increment_views("category_d1_1", "category_d2_11", "category_d3_111", False)

    user_interests_partial.increment_views("category_d1_1", "category_d2_11", "category_d3_113", False)
    user_interests_partial.increment_views("category_d1_1", "category_d2_12", "category_d3_124", False)

    user_interests.update_statistics(user_interests_partial)
    user_interests_partial = UserInterests("user1")

    user_interests_partial.increment_views("category_d1_1", "category_d2_11", "category_d3_111", True)
    user_interests_partial.increment_views("category_d1_1", "category_d2_11", "category_d3_114", True)
    user_interests_partial.increment_views("category_d1_1", "category_d2_13", "category_d3_135", True)

    user_interests.update_statistics(user_interests_partial)

    # assert
    # category_d1_1 node
    category_d1_1_node = user_interests.d1_categories["category_d1_1"]
    category_d1_1_node_correct = (category_d1_1_node.views == 6)
    assert category_d1_1_node_correct, "wrong result in category_d1_1"

    # category_d2_11
    category_d2_11_node = user_interests.d2_categories["category_d2_11"]
    category_d2_11_node_correct = (category_d2_11_node.views == 4)
    assert category_d2_11_node_correct, "wrong result in category_d2_11"

    # category_d2_12
    category_d2_12_node = user_interests.d2_categories["category_d2_12"]
    category_d2_12_node_correct = (category_d2_12_node.views == 1)
    assert category_d2_12_node_correct, "wrong result in category_d1_1.category_d2_12"

    # category_d2_13
    category_d2_13_node = user_interests.d2_categories["category_d2_13"]
    category_d2_13_node_correct = (category_d2_13_node.views == 1)
    assert category_d2_12_node_correct, "wrong result in category_d2_13"

    # d3 category nodes
    d3_categories = (user_interests.d3_categories["category_d3_111"],
              user_interests.d3_categories["category_d3_113"],
              user_interests.d3_categories["category_d3_114"],
              user_interests.d3_categories["category_d3_124"],
              user_interests.d3_categories["category_d3_135"])

    if (d3_categories[0].views == 2):
        correct_d3_categories = [d3_categories[0]]
    else:
        correct_d3_categories =[]
    
    correct_d3_categories += [node for node in d3_categories[1:] if node.views == 1]
    assert len(correct_d3_categories) == len(d3_categories), "wrong view count in d3 categories!" 

    silent_weeks_flag_correct = (d3_categories[0].from_silent_weeks 
                             and d3_categories[3].from_silent_weeks
                             and d3_categories[4].from_silent_weeks)

    print ("Test user interests partial update - PASSED")