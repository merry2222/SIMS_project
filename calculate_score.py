def calculate_score(employee_scores, all_scores):
    must  = 1
    should = 1
    merit = 1
    emp_must = 1
    emp_should = 1
    emp_merit = 1
    for score in all_scores:
        if score[1] == '3':
            must+=1
        if score[1] == '2':
            should+=1
        if score[1] == '1':
            merit+=1
    
    for score in employee_scores:
        if score == '3':
            emp_must+=1
        if score == '2':
            emp_should+=1
        if score == '1':
            emp_merit+=1
    
    score = emp_must/must*(75*emp_should/should + 25*emp_merit/merit)
    return f"{round(score)}%"