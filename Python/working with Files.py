def calculate_total(marks):
    """
    accepts a list of marks and returns their sum.
    """
    return sum(marks)

def calculate_average(marks):
    """
    accepts a list of marks and returns their Average.
    """
    return calculate_total(marks)/len(marks)

def get_grade(average):
    """
    that returns "A" if average > 90, "B" if average > 75, and "C" otherwise.
    """
    return "A" if average > 90 else "B" if average > 75 else "C"

def display_report(marks):
    """
    function display_report(marks) that calls all three functions above and prints:

    Total: <value>
    Average: <value>
    Grade: <value>
    """
    print(f"Total: {calculate_total(marks)} \nAverage: {calculate_average(marks)} \nGrade: {get_grade(calculate_average(marks))}")


marks = [88, 76, 95, 60, 82]

display_report(marks)