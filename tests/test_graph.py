import pandas as pd

# Data provided
courses = {
    'BBST 103': 'Fall 2024 A', 'BBST 165': 'Fall 2024 A', 'BUSN 211': 'Fall 2024 B',
    'ENGL 112': 'Fall 2024 Full', 'MATH 210': 'Fall 2024 Full', 'BUSN 220': 'Fall 2024 A',
    'BBST 210': 'Spring 2025 B', 'BUSN 323': 'Spring 2025 B', 'BUSN 347': 'Spring 2025 A',
    'BUSN 376': 'Spring 2025 B', 'BBST 209': 'Spring 2025 A', 'BBST 260': 'Spring 2025 B',
    'BUSN 361': 'Summer 2025 B', 'BUSN 370': 'Summer 2025 A', 'ARTS 100': 'Summer 2025 A',
    'BIOS 100': 'Summer 2025 A', 'BIOS 121': 'Summer 2025 B', 'BUSN 212': 'Summer 2025 B',
    'BUSN 319': 'Fall 2025 A', 'BUSN 320': 'Fall 2025 A', 'BUSN 422': 'Fall 2025 B',
    'BBST 306': 'Fall 2025 A', 'COMM 200': 'Fall 2025 B', 'ENGL 313': 'Fall 2025 Full',
    'BUSN 328': 'Spring 2026 B', 'ENGL 220': 'Spring 2026 B', 'PSYC 200': 'Spring 2026 A',
    'BUSN 230': 'Summer 2026 B', 'BUSN 478': 'Summer 2026 B', 'MUSC 314': 'Summer 2026 A',
    'POSC 225': 'Summer 2026 A', 'SPAN 100': 'Summer 2026 A', 'SPAN 200': 'Summer 2026 B',
    'PHIL 210': 'Fall 2026 Full'
}

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

# Create DataFrame from the structured data
df = pd.DataFrame({
    semester: {
        "A": ', '.join(semester_structure[semester]["A"]),
        "B": ', '.join(semester_structure[semester]["B"]),
        "Full": ', '.join(semester_structure[semester]["Full"])
    } for semester in semester_structure
}).T

# Display the DataFrame
print(df)
