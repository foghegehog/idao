# get "candidates" categories for prediction from both popular user's cluster categories and most viewed user's categories
def get_candidate_categories(cluster, user_id, user, users_interests, common_d3_categories_sorted):
    
    candidates = set()
    
    for category in cluster.d3_categories_sorted:
        if category not in user.silent_weeks_d3_categories:
            candidates.add(category)
            if len (candidates) == 10:
                break
                        
    sorted_user_categories = sorted(
        users_interests[user_id].d3_categories.keys(),
        key = lambda key: users_interests[user_id].d3_categories[key],
        reverse = True)
    for category in sorted_user_categories:
        if category not in user.silent_weeks_d3_categories:
            candidates.add(category)
        if len(candidates) == 20:
            break
                    
    common_category_index = 0
    while len(candidates) < 5 and common_category_index < len (common_d3_categories_sorted):
        commom_category = common_d3_categories_sorted[common_category_index]
        common_category_index += 1
        if category not in user.silent_weeks_d3_categories:
            candidates.add(category)
            
    return candidates

def get_users_predicted_categories(in_file_path, out_file_path, common_d3_categories, predictions_count = 5):
    users_categories = {}
    with open(in_file_path, 'r') as in_data:
        with open(out_file_path, 'r') as ratings:
            for input_line in in_data:
                tag = input_line.split('|')[0].split(' ')[1]
                user_id, category = tag.split('-')
                rating = float(ratings.next())
                if not users_categories.has_key(user_id):
                    users_categories[user_id] = {}
                users_categories[user_id][category] = rating
    
    users_predictions = {}
    for user_id in users_categories.keys():
        categories = sorted(
            users_categories[user_id].keys(),
            key = lambda c: users_categories[user_id][c],
            reverse = True)
        users_predictions[user_id] = categories[:predictions_count]
        if len(users_predictions[user_id]) < predictions_count:
            rest = predictions_count - len(users_predictions[user_id])
            users_predictions[user_id] += common_d3_categories[:rest]
    return users_predictions