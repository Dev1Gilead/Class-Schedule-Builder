from models.schedule import Schedule
from models.student import fetch_student_data, fetch_required_courses
from algorithms.utils import is_time_slot_compatible
from algorithms.semester_calculations import calculate_available_semesters
from algorithms.course_sorting import sort_courses_by_num_prerequisites_fulfilled, reorder_courses_by_prerequisites
from algorithms.schedule_helpers import is_course_offered_in_semester, calculate_total_credits, plot_course_schedule

def generate_schedule(student_id, preferences):
    try:
        # Fetch student data and courses from the database
        student = fetch_student_data(student_id)
        if not student:
            raise ValueError(f"No student found with ID: {student_id}")
        print(f"Student found: {student.student_id}")

        # Fetch required courses for the student
        remaining_courses = fetch_required_courses(student)
        #print(f"Remaining courses: {remaining_courses}")

        # Calculate the number of available semesters until graduation
        semesters = calculate_available_semesters(preferences['expected_graduation'])
        print(f"Available semesters: {semesters}")

        # Initialize the schedule and semester load
        schedule = Schedule()
        max_credits_per_semester = 18

        # Sort courses by their prerequisite fulfillment impact
        sorted_courses = sort_courses_by_num_prerequisites_fulfilled(remaining_courses)
        new_sorted = reorder_courses_by_prerequisites(sorted_courses, student.completed_courses)

        print(f"\033[33mSorted courses by prerequisites fulfillment: {sorted_courses}")
        print(f"New Sorted courses: {new_sorted}{"\033[0m"}")

        # Calculate average credits per semester
        total_credits = calculate_total_credits(sorted_courses)
        avg_credits_per_semester = -(-total_credits // len(semesters))  # Round up to the nearest whole number
        if avg_credits_per_semester > 18:
            avg_credits_per_semester = 18  # Ensure the average credits does not exceed 18
        print(f"Total credits: {total_credits}")
        print(f"Initial average starting credits per semester: {avg_credits_per_semester}")

        # Function to attempt scheduling with a given average credits cap
        def attempt_scheduling(avg_credits_cap):
            schedule.clear()
            semester_load = {semester: 0 for semester in semesters}
            unscheduled_courses = []

            # Traverse semesters and attempt to add courses to the schedule
            for semester in semesters:
                for course in sorted_courses:
                    course_code = course['course_code']
                    course_credits = int(course['credits'])

                    if semester_load[semester] + course_credits > max_credits_per_semester:
                        continue  # Skip if adding this course would exceed the max credits for this semester

                    if semester_load[semester] + course_credits > avg_credits_cap:
                        print(f"{"\033[32m"}Exceed average credtis, and avrage is: {avg_credits_cap}{"\033[32m"}")
                        continue  # Skip if adding this course would exceed the average credits cap

                    if course_code in schedule.get_scheduled_courses():
                        continue  # Skip if the course is already scheduled
                    
                    is_course_offered, term = is_course_offered_in_semester(semester, course)
                    if is_course_offered:
                        if not is_time_slot_compatible(semester, preferences):
                            continue  # Skip if the course's time slot is not compatible with preferences

                        print(f"Scheduling course {course_code} in term {semester}")
                        
                        schedule.add_course(course_code, (semester + " " + term))
                        semester_load[semester] += course_credits
                        # Stop looking at other courses once this course is scheduled in the semester

            # Handle unscheduled courses
            for course in sorted_courses:
                if course['course_code'] not in schedule.get_scheduled_courses():
                    print(f"Could not schedule course {course['course_code']}")
                    unscheduled_courses.append(course['course_code'])

            final_schedule, _ = schedule.get_final_schedule()
            print(f"temp unscedul;ed courses: {unscheduled_courses}")
            return final_schedule, unscheduled_courses

        # Try scheduling with the initial average credits cap
        final_schedule, unscheduled_courses = attempt_scheduling(avg_credits_per_semester)

        # If there are unscheduled courses, increase the average credits cap and try again
        while unscheduled_courses and avg_credits_per_semester < 18:
            avg_credits_per_semester = min(avg_credits_per_semester + 3, 18)
            print(f"Increasing average credits per semester to {avg_credits_per_semester}")
            final_schedule, unscheduled_courses = attempt_scheduling(avg_credits_per_semester)

        print(f"\033[32mFinal schedule: {final_schedule}\033[0m")
        print(f"Unscheduled courses: {unscheduled_courses}")
        plot_course_schedule(final_schedule)
        return final_schedule, unscheduled_courses

    except Exception as e:
        # Log the error or handle it appropriately
        print(f"An error occurred while generating the schedule: {e}")
        return {}, []  # Return empty schedule and unscheduled courses lists in case of failure
