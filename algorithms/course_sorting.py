def sort_courses(courses_to_take):
    # Step 1: Create a dictionary to store the prerequisite fulfillment score
    fulfillment_scores = {course['course_code']: 0 for course in courses_to_take}
    
    # Step 2: Calculate the prerequisite fulfillment score for each course
    for course in courses_to_take:
        course_code = course['course_code']
        for other_course in courses_to_take:
            prerequisites = eval(other_course['prerequisites'])  # Convert the string list to an actual list
            # Check if the current course is a prerequisite for the other course
            if any([course_code in prereq_list for prereq_list in prerequisites]):
                fulfillment_scores[course_code] += 1
    print (f"fullfilment scores:{fulfillment_scores}\n\n")
    # Step 3: Sort the courses by fulfillment score and by course number for tiebreakers
    sorted_courses = sorted(courses_to_take, key=lambda x: (-fulfillment_scores[x['course_code']], x['course_code']))
    
    return sorted_courses
