import ast
from typing import List, Dict

def sort_courses_by_num_prerequisites_fulfilled(courses_to_take):

    #sorts courses by the number of prerequisits thy fullfil. Nothing more. 
    
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
    print(f"Sotred courses: {sorted_courses}")

    #for temp in sorted_courses:
        #print(f"{"\033[31m"} Sorted courses 1st: {temp['course_code']}{"\033[0m"}")
    return sorted_courses


def reorder_courses_by_prerequisites(sorted_courses: List[Dict[str, str]], temp_taken_classes: str) -> List[Dict[str, str]]:
    taken_classes = temp_taken_classes.split(",")
    print(f"Taken classes: {taken_classes}")
    print(f"The type of taken_classes is: {type(taken_classes)}")

    new_list = []
    remaining_courses = sorted_courses[:]  # Create a copy of the input list to work with

    while remaining_courses:
        progress_made = False
        print(f"\nRemaining courses: {[course['course_code'] for course in remaining_courses]}")
        for course in remaining_courses:
            course_code = course['course_code']
            prerequisites = course['prerequisites']
            
            # Safely convert prerequisites from string to list of lists, if necessary
            if isinstance(prerequisites, str) and prerequisites != '[]':
                prerequisites = ast.literal_eval(prerequisites)
            elif prerequisites == '[]':
                prerequisites = []
            
            print(f"Checking course: {course_code}, Prerequisites: {prerequisites}")
            
            # Check if at least one prerequisite in each alternative group is in new_list or taken_classes
            if all(
                any(prereq in [c['course_code'] for c in new_list] or prereq in taken_classes for prereq in prereq_list) 
                for prereq_list in prerequisites
            ):
                print(f"Adding {course_code} to new list.")
                new_list.append(course)  # Add the course to the new list
                remaining_courses.remove(course)  # Remove the course from the remaining list
                progress_made = True
                break  # Start the loop again to recheck remaining courses
            else:
                print(f"Cannot add {course_code} yet, prerequisites not met.")

        if not progress_made:
            # Identify the unmet prerequisites for the remaining courses
            unmet_prereqs = {}
            for course in remaining_courses:
                course_code = course['course_code']
                prerequisites = course['prerequisites']
                if isinstance(prerequisites, str) and prerequisites != '[]':
                    prerequisites = ast.literal_eval(prerequisites)
                elif prerequisites == '[]':
                    prerequisites = []
                
                unmet = [
                    prereq for prereq_list in prerequisites 
                    for prereq in prereq_list 
                    if prereq not in [c['course_code'] for c in new_list] and prereq not in taken_classes
                ]
                if unmet:
                    unmet_prereqs[course_code] = unmet
            
            print(f"Unmet prerequisites: {unmet_prereqs}")
            raise ValueError(f"Cannot resolve course ordering due to unsatisfied prerequisites: {unmet_prereqs}")
    
    print(f"Final course order: {[course['course_code'] for course in new_list]}")
    return new_list
