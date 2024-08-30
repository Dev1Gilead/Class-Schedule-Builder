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


import matplotlib.pyplot as plt
import pandas as pd

def plot_course_schedule(courses: dict[str, str]) -> None:
    # Initializing dictionary for DataFrame
    semester_structure = {
        "Fall 2024": {"A": [], "B": [], "Full": []},
        "Spring 2025": {"A": [], "B": [], "Full": []},
        "Summer 2025": {"A": [], "B": [], "Full": []},
        "Fall 2025": {"A": [], "B": [], "Full": []},
        "Spring 2026": {"A": [], "B": [], "Full": []},
        "Summer 2026": {"A": [], "B": [], "Full": []},
        "Fall 2026": {"A": [], "B": [], "Full": []},
    }

    # Populate the semester structure
    for course, period in courses.items():
        semester, half = period.rsplit(' ', 1)
        if half in semester_structure[semester]:
            semester_structure[semester][half].append(course)

    # Convert data to a DataFrame
    df = pd.DataFrame({
        semester: {
            "A": '\n'.join(semester_structure[semester]["A"]),
            "B": '\n'.join(semester_structure[semester]["B"]),
            "Full": '\n'.join(semester_structure[semester]["Full"])
        } for semester in semester_structure
    }).T

    # Plotting the calendar view
    fig, ax = plt.subplots(figsize=(12, 8))

    ax.set_axis_off()
    table = ax.table(
        cellText=df.values,
        rowLabels=df.index,
        colLabels=df.columns,
        cellLoc='center',
        loc='center'
    )

    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 4)

    # Highlighting full semester courses with a different color
    for (i, j), cell in table.get_celld().items():
        if i == 0 or j == -1:
            cell.set_text_props(weight='bold', color='white')
            cell.set_facecolor('#40466e')
        elif df.iloc[i-1, j-1] != '':
            if j == 2:  # Full semester
                cell.set_facecolor('#d6e0f5')
            else:
                cell.set_facecolor('#b3cde0')

    ax.set_title('Course Schedule Calendar', fontweight="bold", size=16)
    plt.show()
