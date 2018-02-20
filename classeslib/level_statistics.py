''' Holds amount of views for each category of specified level  '''

class LevelStatistics:      
    def __init__(self, level):
        self.level = level
        self.categories_statistics = {}
    
    def increment_statistics(self, category):
        if not self.categories_statistics.has_key(category):
            self.categories_statistics[category] = 1
        else:
            self.categories_statistics[category] += 1
    
    def update_statistics(self, partial_statistics):
        for category in partial_statistics.categories_statistics.keys():
            partial_statistic = partial_statistics.categories_statistics[category]
            if not self.categories_statistics.has_key(category):
                self.categories_statistics[category] = partial_statistic
            else:
                self.categories_statistics[category] += partial_statistic                
    
    def reset(self):
        self.categories_statistics = {}

# Tests
if __name__ == '__main__': 
   
    # Test category statistics increment
    
    # arrange
    level_statistics = LevelStatistics("d1")

    # act
    level_statistics.increment_statistics("category1")
    level_statistics.increment_statistics("category2")
    level_statistics.increment_statistics("category3")
    level_statistics.increment_statistics("category1")
    level_statistics.increment_statistics("category1")

    # assert
    passed_category1 = (level_statistics.categories_statistics.has_key("category1")  
        and level_statistics.categories_statistics["category1"] == 3)
    assert passed_category1, "wrong category1 increment!"

    passed_category2 = (level_statistics.categories_statistics.has_key("category2")  
        and level_statistics.categories_statistics["category2"] == 1)
    assert passed_category2, "wrong category2 increment!"

    passed_category3 = (level_statistics.categories_statistics.has_key("category3")  
        and level_statistics.categories_statistics["category3"] == 1)
    assert passed_category3, "wrong category3 increment!"
    
    print ("Category statistics increment - PASSED")
    
    
    # Test categories update by partial statistics
    
    # arrange
    level_statistics = LevelStatistics("d1")
    partial_statistics = LevelStatistics("d1")

    # act
    level_statistics.increment_statistics("category1")
    level_statistics.increment_statistics("category2")
    level_statistics.increment_statistics("category3")
    level_statistics.increment_statistics("category1")
    level_statistics.increment_statistics("category1")

    partial_statistics.increment_statistics("category1")
    partial_statistics.increment_statistics("category3")
    partial_statistics.increment_statistics("category3")
    partial_statistics.increment_statistics("category4")

    level_statistics.update_statistics(partial_statistics)

    # assert
    passed_category1 = (level_statistics.categories_statistics.has_key("category1")  
        and level_statistics.categories_statistics["category1"] == 4)
    assert passed_category1, "wrong category1 update!"

    passed_category2 = (level_statistics.categories_statistics.has_key("category2")  
        and level_statistics.categories_statistics["category2"] == 1)
    assert passed_category2, "wrong category2 update!"

    passed_category3 = (level_statistics.categories_statistics.has_key("category3")  
        and level_statistics.categories_statistics["category3"] == 3)
    assert passed_category3, "wrong category3 update!"

    passed_category4 = (level_statistics.categories_statistics.has_key("category4")  
        and level_statistics.categories_statistics["category4"] == 1)
    assert passed_category3, "wrong category4 update!"
    
    print ("Categories update by partial statistics - PASSED")
    
