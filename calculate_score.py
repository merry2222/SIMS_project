def calculate_score(employee_scores, all_scores):
    base = 0  # Using Axel calculation method change the value on base to 1 and vice versa if are using Johannes method

    must_req = base # N amount of must-have skills
    should_req = base
    merit_req = base

    matched_must = base # N amount of must-have skills matched
    matched_should = base
    matched_merit = base

    for score in all_scores:
        if score[1] == '3':
            must_req += 1
        if score[1] == '2':
            should_req += 1
        if score[1] == '1':
            merit_req += 1

    for score in employee_scores:
        if score == '3':
            matched_must += 1
        if score == '2':
            matched_should = 1
        if score == '1':
            matched_merit += 1

    if must_req == 0: # Avoid division by zero
        must_req = 1
    if should_req == 0:
        should_req = 1
    if merit_req == 0:
        merit_req = 1

    # score = must*(75*emp_should/should + 25*emp_merit/merit)  # Axel calculation method
    score = matched_must / must_req * 60 + matched_should / should_req * 30 + matched_merit / merit_req * 10  # Johannes calculation method
    return f"{round(score)}%"