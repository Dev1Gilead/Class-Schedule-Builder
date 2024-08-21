class Schedule:
    def __init__(self):
        self.courses = {}
        self.unscheduled_courses = []

    def add_course(self, course_code, term_time):
        """
        Add a course to the schedule with the specified term and time.
        The term_time parameter should include both the term and the time offered, 
        e.g., "Fall A (14:00-16:00)" or "Fall A (Pending)".
        """
        self.courses[course_code] = term_time

    def add_unscheduled_course(self, course_code):
        """Add a course to the list of unscheduled courses."""
        self.unscheduled_courses.append(course_code)

    def get_final_schedule(self):
        """Return the final schedule and list of unscheduled courses."""
        return self.courses, self.unscheduled_courses

    def get_scheduled_courses(self):
        """Return a list of all scheduled courses."""
        return list(self.courses.keys())
