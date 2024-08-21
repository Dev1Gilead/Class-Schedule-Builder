def is_time_slot_compatible(time_slot, preferences):
    """
    Check if the given time_slot is compatible with the student's preferred days and times.
    
    Parameters:
    - time_slot: A string representing the time slot (e.g., "MWF 10:00-11:00").
    - preferences: A dictionary containing the student's preferred days and times.
    
    Returns:
    - True if the time slot is compatible with the preferences, False otherwise.
    """
    # Extract the days and times from the time_slot string (e.g., "MWF 10:00-11:00")
    days, times = time_slot.split(' ')

    # Check if preferred_days is empty or not provided; if so, assume all days are acceptable
    days_match = any(preferred_day in days for preferred_day in preferences.get('preferred_days', [])) \
                 if preferences.get('preferred_days') else True

    # If the days match and there are no preferred times, assume all times are acceptable
    if days_match:
        if not preferences.get('preferred_times'):
            return True

        # If preferred_times is provided, check compatibility with the times
        start_time, end_time = map(int, times.replace(':', '').split('-'))

        for preferred_time in preferences['preferred_times']:
            pref_start, pref_end = map(int, preferred_time.replace(':', '').split('-'))

            # Check if the preferred times overlap with the time slot
            if pref_start <= end_time and pref_end >= start_time:
                return True

    return False



def is_course_offered_in_semester(semester, course_offered_terms):
    """
    Checks if a course is offered in a given semester.

    Parameters:
        semester (str): The semester to check (e.g., "Fall 2024").
        course_offered_terms (str): The terms during which the course is offered (e.g., "Fall A, Summer B").

    Returns:
        tuple: (True, section) if the course is offered in the semester, where `section` is "A", "B", or "full".
               (False, None) if the course is not offered in the semester.
    """
    term, year = semester.split()
    offered_terms = [t.strip() for t in course_offered_terms.split(',')]

    for offered_term in offered_terms:
        offered_term_parts = offered_term.split()
        if offered_term_parts[0] == term:
            if len(offered_term_parts) == 1:
                return True, "full"
            elif len(offered_term_parts) == 2 and offered_term_parts[1] in ["A", "B"]:
                return True, offered_term_parts[1]

    return False, None


def parse_prerequisites(prereq_string):
    """
    Parses the prerequisite string into a structured format.
    
    Parameters:
        prereq_string (str): The prerequisites string (e.g., "Course A; Course B|Course C").
    
    Returns:
        list: A list of prerequisite groups, with OR conditions within a group.
    """
    if not isinstance(prereq_string, str) or not prereq_string.strip():
        return []

    # Split by ';' to handle AND conditions
    and_conditions = [item.strip() for item in prereq_string.split(';')]
    
    # For each AND condition, further split by '|' to handle OR conditions
    parsed_prereqs = []
    for condition in and_conditions:
        or_conditions = [course.strip() for course in condition.split('|')]
        parsed_prereqs.append(or_conditions)
    
    return parsed_prereqs
