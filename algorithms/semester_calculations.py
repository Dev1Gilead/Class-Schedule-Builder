def calculate_available_semesters(expected_graduation):
    try:
        # Process the expected graduation input to determine the graduation term and year
        if "-" in expected_graduation and len(expected_graduation) == 7:
            graduation_year = int(expected_graduation.split("-")[0])
            graduation_month = int(expected_graduation.split("-")[1])
            
            if graduation_month in [1, 2, 3, 4]:
                graduation_term = "Spring"
            elif graduation_month in [5, 6, 7, 8]:
                graduation_term = "Summer"
            elif graduation_month in [9, 10, 11, 12]:
                graduation_term = "Fall"
            else:
                raise ValueError("Invalid month in expected graduation date.")
        else:
            graduation_semester = expected_graduation.split()
            if len(graduation_semester) != 2:
                raise ValueError("Expected graduation date format should be 'Term Year' (e.g., 'Fall 2025').")
            
            graduation_term = graduation_semester[0]
            graduation_year = int(graduation_semester[1])

        # List of all terms in order (assuming standard U.S. academic terms)
        terms = ["Spring", "Summer", "Fall"]
        current_year = 2024  # You might want to calculate this dynamically
        current_term = "Fall"  # Assume starting from Fall 2024; adjust as needed
    except Exception as e:
        raise ValueError(f"Invalid expected graduation format: {expected_graduation}") from e

    semesters = []
    # Ensure we include at least the graduation term
    while True:
        semesters.append(f"{current_term} {current_year}")
        
        if (current_year, current_term) == (graduation_year, graduation_term):
            break

        if current_term == "Fall":
            current_term = "Spring"
            current_year += 1
        elif current_term == "Spring":
            current_term = "Summer"
        elif current_term == "Summer":
            current_term = "Fall"

    return semesters
