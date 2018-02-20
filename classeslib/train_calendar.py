last_public_day = 54
last_private_day = 61
    
test_week = range(last_public_day - 6, last_public_day + 1)
test_silent_weeks = range(test_week[0] - 21, test_week[0])
    
target_week = range(test_week[0] - 7, test_week[0])    
target_silent_weeks = range(target_week[0] - 21, target_week[0])

public_train_days = range(1, target_week[0])
private_train_days = range(1, last_public_day+1)

# Tests
if __name__ == '__main__': 
    assert len(test_week) == 7, "test week has not 7 days!"
    assert len(target_week) == 7, "target week has not 7 days!"
    assert len(test_silent_weeks) == 21, "test silent weeks have not 21 days!"
    assert len(target_silent_weeks) == 21, "target silent weeks have not 21 days!"
    assert len(public_train_days) == TrainCalendar.last_public_day - 7*2, "too few public train days!"
    assert len(private_train_days) == TrainCalendar.last_public_day, "too few private train days!"
    
    print ("Train calendar tests - PASSED")