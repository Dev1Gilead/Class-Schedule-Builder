def is_course_offered_in_semester(course, semester):
    """
    Checks if a course is offered in the specified semester.
    Assumes that 'terms_offered' in the course dictionary contains terms like "Fall A, Spring B, Summer"
    and 'recurrence' specifies how often the course is repeated (every year, every two years, etc.)
    """
    # Get the main term (Fall, Spring, Summer) and sub-term (A, B, Full) from the semester
    main_term, term_year = semester.split()
    sub_term = term_year[-1] if term_year[-1].isalpha() else "Full"
    term_year = int(term_year[:-1]) if term_year[-1].isalpha() else int(term_year)

    # Check the recurrence of the course
    course_recurrence = int(course.get('recurrence', 1))
    if (term_year - 2024) % course_recurrence != 0:
        return False

    # Check if the course is offered in the given term and sub-term
    offered_terms = course['terms_offered'].split(',')
    for term in offered_terms:
        term = term.strip()
        if main_term in term and (sub_term in term or "Full" in term):
            return True
    return False

def calculate_total_credits(courses):
    return sum(int(course['credits']) for course in courses)

def is_course_offered_in_semester(semester, course):
    #print(f"semester: {semester}")
    #print(f"course: {course}")
    """
    Checks if a course is offered in a given semester.

    Parameters:
        semester (str): The semester to check (e.g., "Fall 2024").
        course_offered_terms (str): The terms during which the course is offered (e.g., "Fall A, Summer B").

    Returns:
        tuple: (True, section) if the course is offered in the semester, where `section` is "A", "B", or "full".
               (False, None) if the course is not offered in the semester.
    """
    # Extract the main term (e.g., "Fall") and the year (e.g., "2024") from the semester string
    term, year = semester.split()
    #print(f"term: {term}")

    # Split the course offered terms into a list of terms (e.g., ["Fall A", "Summer B"])
    offered_terms = [t.strip() for t in course['terms_offered'].split(',')]
    recurrence = course['recurrence'] #will be implemented later

    #print(f"offered terms: {offered_terms}")

    # Iterate over the offered terms to see if any match the current semester
    for offered_term in offered_terms:
        offered_term_parts = offered_term.split()

        if offered_term_parts[0] == term:
            if len(offered_term_parts) == 1:
                # The course is offered for the full term (e.g., "Fall")
                return True, "full"
            elif len(offered_term_parts) == 2 and offered_term_parts[1] in ["A", "B"]:
                # The course is offered for a sub-term (e.g., "Fall A" or "Fall B")
                return True, offered_term_parts[1]

    # If no matches were found, return False
    return False, None


def initialize_semester_load(semesters, sub_terms=["", " A", " B"]):
    """
    Initialize the semester load dictionary with all semesters and sub-terms.

    Args:
        semesters (list): A list of semesters (e.g., ['Fall 2024', 'Spring 2025']).
        sub_terms (list): A list of sub-terms (e.g., ['', ' A', ' B']). Defaults to ['', ' A', ' B'].

    Returns:
        dict: A dictionary with keys for each semester and sub-term, initialized to 0.
    """
    semester_load = {}
    for semester in semesters:
        for sub_term in sub_terms:
            semester_load[f"{semester}{sub_term}"] = 0

    #print(f"Semester Load: {semester_load}")
    #print(f"Semester load initialized with keys: {list(semester_load.keys())}")
    return semester_load
