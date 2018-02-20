import numpy as np
import scipy.sparse

if __name__ == '__main__': 
    from users_interests import UserCategory, UserInterests
else:
    from classeslib.users_interests import UserCategory, UserInterests

def build_categories_features_matrix(d1_categories, d2_categories, d3_categories, users_interests):
    d2_categories_shift = len(d1_categories)
    d3_categories_shift = d2_categories_shift + len(d2_categories)
    
    user_categories_matrix = scipy.sparse.lil_matrix(
        (len(users_interests), d3_categories_shift + len(d3_categories)), dtype=np.int8)
    
    user_row = 0
    for user in users_interests.values():
        for d1_category in user.d1_categories.keys():
            category_index = d1_categories.index(d1_category)
            user_categories_matrix[user_row, category_index] += user.d1_categories[d1_category].views
            
        for d2_category in user.d2_categories.keys():
            category_index = d2_categories_shift + d2_categories.index(d2_category)
            user_categories_matrix[user_row, category_index] += user.d2_categories[d2_category].views
            
        for d3_category in user.d3_categories.keys():
            category_index = d3_categories_shift + d3_categories.index(d3_category)
            user_categories_matrix[user_row, category_index] += user.d3_categories[d3_category].views
        
        user_row += 1
    
    return user_categories_matrix

# Tests
if __name__ == '__main__': 
    
    # arrange
    test_d1_categories = ["1"]
    test_d2_categories = ["11", "12"]
    test_d3_categories = ["111", "121", "122"]

    user1 = UserInterests("user1")
    user2 = UserInterests("user2")
    test_user_interests = { "user1": user1, "user2": user2 }
    user1_index = test_user_interests.keys().index("user1")
    user2_index = test_user_interests.keys().index("user2")

    # act
    user1.increment_views("1", "11", "111", False)
    user1.increment_views("1", "11", "111", False)
    user1.increment_views("1", "12", "121", False)
    user1.increment_views("1", "12", "122", False)

    user2.increment_views("1", "12", "121", False)
    user2.increment_views("1", "12", "122", False)
    user2.increment_views("1", "12", "122", False)
    user2.increment_views("1", "12", "122", False)

    test_matrix = build_categories_features_matrix(
        test_d1_categories, test_d2_categories, test_d3_categories, test_user_interests)

    # assert
    user1_correct = (test_matrix[user1_index, 0] == 4 
                 and test_matrix[user1_index, 1] == 2
                 and test_matrix[user1_index, 2] == 2
                 and test_matrix[user1_index, 3] == 2
                 and test_matrix[user1_index, 4] == 1
                 and test_matrix[user1_index, 5] == 1)
    assert user1_correct, "user 1 features are wrong!"

    user2_correct = (test_matrix[user2_index, 0] == 4 
                 and test_matrix[user2_index, 1] == 0
                 and test_matrix[user2_index, 2] == 4
                 and test_matrix[user2_index, 3] == 0
                 and test_matrix[user2_index, 4] == 1
                 and test_matrix[user2_index, 5] == 3)
    assert user2_correct, "user 2 features are wrong!"

    print ("Feature matrix creation tests - PASSED")