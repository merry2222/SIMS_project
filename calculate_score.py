def calculate_score(employee_scores, all_scores):
    base = 1 # Needs to be base 1 to avoid division by 0 in case of empty requirements
    must  = base
    should = base
    merit = base
    emp_must = base
    emp_should = base
    emp_merit = base
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
    
    #score = emp_must/must*(75*emp_should/should + 25*emp_merit/merit)      # Axel calculation method
    score = emp_must/must*60 + emp_should/should*30 + emp_merit/merit*10    # Johannes calculation method
    return f"{round(score)}%"
