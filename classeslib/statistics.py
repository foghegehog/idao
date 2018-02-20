import shelve
if __name__ == '__main__': 
    from users_interests import UserCategory, UserInterests
    from level_statistics import LevelStatistics
    from input_file_reader import InputFileReader
else:
    from classeslib.users_interests import UserCategory, UserInterests
    from classeslib.level_statistics import LevelStatistics
    from classeslib.input_file_reader import InputFileReader


class StatisticsDumper:
    
    d1_level_statistics_key = "d1_level_statistics"
    d2_level_statistics_key = "d2_level_statistics"
    d3_level_statistics_key = "d3_level_statistics"

    user_statistics_key_prefix = "user_id_"
    
    def __init__(self, dump_file_path):
        self.dump_file_path = dump_file_path
    
    def update_category_statistics(self, db, level_key, partial_statistics):
        if not db.has_key(level_key):
            db[level_key] = partial_statistics
        else:
            saved_statistics = db[level_key]
            saved_statistics.update_statistics(partial_statistics)
            db[level_key] = saved_statistics
            
    def save_statistics(self, d1_level_statistics, d2_level_statistics, d3_level_statistics, users_interests):
        db = shelve.open(self.dump_file_path)
    
        self.update_category_statistics(db, StatisticsDumper.d1_level_statistics_key, d1_level_statistics)
        self.update_category_statistics(db, StatisticsDumper.d2_level_statistics_key, d2_level_statistics)
        self.update_category_statistics(db, StatisticsDumper.d3_level_statistics_key, d3_level_statistics)
    
        for user_id in users_interests.keys():
            user_key = StatisticsDumper.user_statistics_key_prefix + user_id
            if not db.has_key(user_key):
                db[user_key] = users_interests[user_id]
            else:
                saved_user = db[user_key]
                saved_user.update_statistics(users_interests[user_id])
                db[user_key] = saved_user
         
        db.close()
    
    @staticmethod
    def restore_statistics(file_from):
        db = shelve.open(file_from)
        d1_level_statistics = db[StatisticsDumper.d1_level_statistics_key]
        d2_level_statistics = db[StatisticsDumper.d2_level_statistics_key]
        d3_level_statistics = db[StatisticsDumper.d3_level_statistics_key]
        
        db.close()
        
        return (d1_level_statistics, d2_level_statistics, d3_level_statistics)
    
    @staticmethod
    def get_all_users_ids(file_from):
        db = shelve.open(file_from)
        keys = db.keys()
        db.close()
        return [key.replace(StatisticsDumper.user_statistics_key_prefix, "") for key in keys
               if key.startswith(StatisticsDumper.user_statistics_key_prefix)]
    
    @staticmethod
    def get_users_interests(users_ids, file_from):        
        db = shelve.open(file_from)
        users_interests = {}
        for user_id in users_ids:
            user_key = StatisticsDumper.user_statistics_key_prefix + user_id
            if db.has_key(user_key):
                users_interests[user_id] = db[user_key]
            #else:
            #    print "user " + user_id + " unknown"
        db.close()
        return users_interests
        
    
class StatisticsCounter(InputFileReader):      
    def __init__(self, dump_lines_count, train_data_file, dumper):
        self.dump_lines_count = dump_lines_count
        self.train_data_file = train_data_file
        self.dumper = dumper
        self.d1_level_statistics = LevelStatistics("d1")
        self.d2_level_statistics = LevelStatistics("d2")
        self.d3_level_statistics = LevelStatistics("d3")
        self.users_interests = {}
        self.lines_count = 0
    
    def handle_data_row(self, user_id, day, d1_category, d2_category, d3_category):
        self.d1_level_statistics.increment_statistics(d1_category)
        self.d2_level_statistics.increment_statistics(d2_category)
        self.d3_level_statistics.increment_statistics(d3_category)   
            
        if not self.users_interests.has_key(user_id):
            self.users_interests[user_id] = UserInterests(user_id)
        self.users_interests[user_id].increment_views(d1_category, d2_category, d3_category, False)
        
        self.lines_count += 1
        if self.lines_count == self.dump_lines_count:
            self.dumper.save_statistics(
                self.d1_level_statistics,
                self.d2_level_statistics,
                self.d3_level_statistics,
                self.users_interests)
                
            self.d1_level_statistics.reset()
            self.d2_level_statistics.reset()
            self.d3_level_statistics.reset()
            self.users_interests = {}
                
            self.lines_count = 0
            
    def calculate_statistics(self):
        self.read_input_file(self.train_data_file)
        if self.lines_count > 0:
            self.flush_reminder()
    
    def flush_reminder(self):
        self.dumper.save_statistics(
            self.d1_level_statistics,
            self.d2_level_statistics,
            self.d3_level_statistics,
            self.users_interests)       
        

# Tests
if __name__ == '__main__': 
    
    import os

    # arrange
    test_db_file = "../tests_data/testdb.db"
    if (os.path.isfile(test_db_file)):
        os.remove(test_db_file)

    dumper = StatisticsDumper(test_db_file)
    counter = StatisticsCounter(5, "../tests_data/unittest.train.csv", dumper)

    # act
    counter.calculate_statistics()
    d1_level_statistics, d2_level_statistics, d3_level_statistics = StatisticsDumper.restore_statistics(test_db_file)

    users_ids = StatisticsDumper.get_all_users_ids(test_db_file)
    users_interests = StatisticsDumper.get_users_interests(users_ids, test_db_file)        

    # assert    
    d1_categories_correct = (len(d1_level_statistics.categories_statistics.keys()) == 3 
                         and d1_level_statistics.categories_statistics.has_key("1")
                         and d1_level_statistics.categories_statistics.has_key("2")
                         and d1_level_statistics.categories_statistics.has_key("3"))
    assert d1_categories_correct, "wrong d1 categories statistics!"

    d2_categories_correct = (len(d2_level_statistics.categories_statistics.keys()) == 6 
                         and d2_level_statistics.categories_statistics.has_key("11")
                         and d2_level_statistics.categories_statistics.has_key("12")
                         and d2_level_statistics.categories_statistics.has_key("21")
                         and d2_level_statistics.categories_statistics.has_key("22")
                         and d2_level_statistics.categories_statistics.has_key("31")
                         and d2_level_statistics.categories_statistics.has_key("32"))
    assert d2_categories_correct, "wrong d2 categories statistics!"

    d3_categories_correct = (len(d3_level_statistics.categories_statistics.keys()) == 12 
                         and d3_level_statistics.categories_statistics.has_key("111")
                         and d3_level_statistics.categories_statistics.has_key("112")
                         and d3_level_statistics.categories_statistics.has_key("121")
                         and d3_level_statistics.categories_statistics.has_key("122")
                         and d3_level_statistics.categories_statistics.has_key("211")
                         and d3_level_statistics.categories_statistics.has_key("212")
                         and d3_level_statistics.categories_statistics.has_key("221")
                         and d3_level_statistics.categories_statistics.has_key("222")
                         and d3_level_statistics.categories_statistics.has_key("311")
                         and d3_level_statistics.categories_statistics.has_key("312")
                         and d3_level_statistics.categories_statistics.has_key("321")
                         and d3_level_statistics.categories_statistics.has_key("322"))
    assert d3_categories_correct, "wrong d3 categories statistics!"

    # user ids 
    assert len(users_ids) == 4 and len(set(users_ids) - {"1", "2", "3", "4"}) == 0, "wrong user ids!"
    
    # user 1
    user1 = users_interests["1"]

    assert user1.total_views == 3, "wrong total views count for user 1"

    user1_d1_categories_correct = (len(user1.d1_categories.keys()) == 3
                              and user1.d1_categories.has_key("1")
                              and user1.d1_categories.has_key("2")
                              and user1.d1_categories.has_key("3"))
    assert user1_d1_categories_correct, "wrong d1 categories for user 1"

    user1_d2_categories_correct = (len(user1.d2_categories.keys()) == 3
                              and user1.d2_categories.has_key("11")
                              and user1.d2_categories.has_key("21")
                              and user1.d2_categories.has_key("31"))
    assert user1_d2_categories_correct, "wrong d2 categories for user 1"

    user1_d3_categories_correct = (len(user1.d3_categories.keys()) == 3
                              and user1.d3_categories.has_key("111")
                              and user1.d3_categories["111"].views == 1
                              and user1.d3_categories.has_key("211")
                              and user1.d3_categories["211"].views == 1
                              and user1.d3_categories.has_key("311")
                              and user1.d3_categories["311"].views == 1)
    assert user1_d3_categories_correct, "wrong d3 categories for user 1"


    # user 2
    user2 = users_interests["2"]

    assert user2.total_views == 3, "wrong total views count for user 2"

    user2_d1_categories_correct = (len(user2.d1_categories.keys()) == 3
                              and user2.d1_categories.has_key("1")
                              and user2.d1_categories.has_key("2")
                              and user2.d1_categories.has_key("3"))
    assert user2_d1_categories_correct, "wrong d1 categories for user 2"

    user2_d2_categories_correct = (len(user2.d2_categories.keys()) == 3
                              and user2.d2_categories.has_key("11")
                              and user2.d2_categories.has_key("21")
                              and user2.d2_categories.has_key("31"))
    assert user2_d2_categories_correct, "wrong d2 categories for user 2"

    user2_d3_categories_correct = (len(user2.d3_categories.keys()) == 3
                              and user2.d3_categories.has_key("112")
                              and user2.d3_categories["112"].views == 1
                              and user2.d3_categories.has_key("212")
                              and user2.d3_categories["212"].views == 1
                              and user2.d3_categories.has_key("312")
                              and user2.d3_categories["312"].views == 1)
    assert user2_d3_categories_correct, "wrong d3 categories for user 2"

    # user 3
    user3 = users_interests["3"]

    assert user3.total_views == 3, "wrong total views count for user 3"

    user3_d1_categories_correct = (len(user3.d1_categories.keys()) == 3
                              and user3.d1_categories.has_key("1")
                              and user3.d1_categories.has_key("2")
                              and user3.d1_categories.has_key("3"))
    assert user3_d1_categories_correct, "wrong d1 categories for user 3"

    user3_d2_categories_correct = (len(user3.d2_categories.keys()) == 3
                              and user3.d2_categories.has_key("12")
                              and user3.d2_categories.has_key("22")
                              and user3.d2_categories.has_key("32"))
    assert user3_d2_categories_correct, "wrong d2 categories for user 3"

    user3_d3_categories_correct = (len(user3.d3_categories.keys()) == 3
                              and user3.d3_categories.has_key("121")
                              and user3.d3_categories["121"].views == 1
                              and user3.d3_categories.has_key("221")
                              and user3.d3_categories["221"].views == 1
                              and user3.d3_categories.has_key("321")
                              and user3.d3_categories["321"].views == 1)
    assert user2_d3_categories_correct, "wrong d3 categories for user 3"

    # user 4
    user4 = users_interests["4"]

    assert user4.total_views == 3, "wrong total views count for user 4"

    user4_d1_categories_correct = (len(user4.d1_categories.keys()) == 3
                              and user4.d1_categories.has_key("1")
                              and user4.d1_categories.has_key("2")
                              and user4.d1_categories.has_key("3"))
    assert user4_d1_categories_correct, "wrong d1 categories for user 4"

    user4_d2_categories_correct = (len(user4.d2_categories.keys()) == 3
                              and user4.d2_categories.has_key("12")
                              and user4.d2_categories.has_key("22")
                              and user4.d2_categories.has_key("32"))
    assert user4_d2_categories_correct, "wrong d2 categories for user 4"

    user4_d3_categories_correct = (len(user4.d3_categories.keys()) == 3
                              and user4.d3_categories.has_key("122")
                              and user4.d3_categories["122"].views == 1
                              and user4.d3_categories.has_key("222")
                              and user4.d3_categories["222"].views == 1
                              and user4.d3_categories.has_key("322")
                              and user4.d3_categories["322"].views == 1)
    assert user4_d3_categories_correct, "wrong d3 categories for user 4"

    print ("Statistics calculation tests - PASSED")
    