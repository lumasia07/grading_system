"""Module to analyze student perfomance data from a CSV file"""
import csv
import sys

def get_data_list(csv_file_name):
    """
    Reads data contained in a CSV file & returns a list of lists containing student performance data.
    Args:
        csv_file_name: Name of the CSV file to be read on input
    Return: 
        List of lists containing student performance data
    """
    data_list = []
    try:
        with open(csv_file_name, 'r', newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)
            for row in csv_reader:
                num_row = [row[0], row[1]] + [float(x) for x in row[2:]]
                data_list.append(num_row)
        return data_list
    except FileNotFoundError:
        print(f"Error: File {csv_file_name} not found. Please try again!!\n")
        sys.exit(1)
    except ValueError:
        print(f"Error: Invalid data in {csv_file_name}\n.Please check row {row}.\n")
        sys.exit(1)

def calculate_student_averages(data_list):
    """
    Calculates average scores for each student in each term.
    Args:
        data_list: Main list of student performance data
    Return:
        List of student averages
    """
    student_averages_list = []
    
    """Group data by student and term"""
    students = {}
    for row in data_list:
        sid, term = row[0], row[1]
        scores = row[2:]
        
        if sid not in students:
            students[sid] = {}
        
        if term not in students[sid]:
            students[sid][term] = []
        
        students[sid][term] = scores
    
    """Calculates student averages"""
    for sid, student_terms_data in students.items():
        for term, scores in student_terms_data.items():
            if scores:
                average_score = sum(scores) / len(scores)
                student_averages_list.append([term, sid, average_score])
    
    return student_averages_list

def calculate_class_averages(data_list):
    """
    Calculates class averages for each subject in each term.
    Args:
        data_list: List of student performance data
    Return:
        List of class averages for each subject in each term
    """

    """Subjects (excluding SID and Term)"""
    subjects = ['Chi', 'Eng', 'Math', 'GS', 'CS', 'Music', 'VA', 'PE']
    class_averages_list = []
    
    for term in ['1', '2']:
        for subject_index, subject in enumerate(subjects):
            subject_scores = [row[subject_index+2] for row in data_list if row[1] == term]
            
            if subject_scores:
                class_average = sum(subject_scores) / len(subject_scores)
                class_averages_list.append([term, subject, class_average])
    
    return class_averages_list

def identify_highest_achieving_students(data_list):
    """
    Identifies highest-achieving student for each subject in each term.
    Args:
        data_list: List of student performance data
    Return:
        List of highest-achieving students for each subject in each term
    """

    """Subjects (excluding SID and Term)"""
    subjects = ['Chi', 'Eng', 'Math', 'GS', 'CS', 'Music', 'VA', 'PE']
    highest_achieving_students_list = []
    
    for term in ['1', '2']:
        for subject_index, subject in enumerate(subjects):
            term_subject_data = [
                row for row in data_list 
                if row[1] == term
            ]
            
            if term_subject_data:
                """Finds highest score and corresponding student"""
                highest_score_row = max(
                    term_subject_data, 
                    key=lambda x: x[subject_index+2]
                )
                highest_achieving_students_list.append([
                    term, 
                    subject, 
                    highest_score_row[0], 
                    highest_score_row[subject_index+2]
                ])
    
    return highest_achieving_students_list

def identify_lowest_achieving_students(data_list):
    """
    Identifies lowest-achieving student for each subject in each term.
    Args:
        data_list: List of student performance data
    Return:
        List of lowest-achieving students for each subject in each term
    """

    """Subjects (excluding SID and Term)"""
    subjects = ['Chi', 'Eng', 'Math', 'GS', 'CS', 'Music', 'VA', 'PE']
    lowest_achieving_students_list = []
    
    for term in ['1', '2']:
        for subject_index, subject in enumerate(subjects):
            term_subject_data = [
                row for row in data_list 
                if row[1] == term
            ]

            if term_subject_data:
                """Find lowest score and corresponding student"""
                lowest_score_row = min(
                    term_subject_data, 
                    key=lambda x: x[subject_index+2]
                )
                lowest_achieving_students_list.append([
                    term, 
                    subject, 
                    lowest_score_row[0], 
                    lowest_score_row[subject_index+2]
                ])
    
    return lowest_achieving_students_list

def analyze_performance_trends(data_list):
    """
    Analyzes class performance trends across the terms.
    Args:
        data_list: List of student performance data
    Return:
        List of performance trend percentages accross the terms
    """

    """Get class averages"""
    class_averages = calculate_class_averages(data_list)
    
    """Subjects in question"""
    subjects = ['Chi', 'Eng', 'Math', 'GS', 'CS', 'Music', 'VA', 'PE']
    performance_trend_list = []
    
    for subject in subjects:
        """Find Term One and Term Two averages for this subject"""
        term_one_average = next(
            (avg for avg in class_averages 
             if avg[0] == '1' and avg[1] == subject), 
            None
        )
        term_two_average = next(
            (avg for avg in class_averages 
             if avg[0] == '2' and avg[1] == subject), 
            None
        )
        
        if term_one_average and term_two_average:
            """Calculate percentage change using provided formula"""
            percentage_change = (
                (term_two_average[2] - term_one_average[2]) / term_one_average[2]
            ) * 100
            
            performance_trend_list.append([
                subject, 
                round(percentage_change, 2)
            ])
    
    return performance_trend_list

def get_most_improved_student(student_averages):
    """
    Find the student with the most significant improvement across all.
    Args:
        student_averages: List of student averages
    Return:
        SID of most improved student
    """

    """Group averages by student"""
    student_term_avg = {}
    for entry in student_averages:
        term, sid, avg = entry
        if sid not in student_term_avg:
            student_term_avg[sid] = {'1': None, '2': None}
        student_term_avg[sid][term] = avg
    
    """Calculates improvement"""
    improvements = []
    for sid, terms in student_term_avg.items():
        if terms['1'] is not None and terms['2'] is not None:
            improvement = terms['2'] - terms['1']
            improvements.append((sid, improvement))
    
    """Returns SID of most improved student"""
    return max(improvements, key=lambda x: x[1])[0] if improvements else None

"""Main function"""
def main():
    """Prompt user for CSV file name"""
    csv_file_name = input("Please input a CSV file name: ")
    
    """Read data from given CSV file"""
    data_list = get_data_list(csv_file_name)
    
    """"Performance analyses"""
    student_averages = calculate_student_averages(data_list)
    class_averages = calculate_class_averages(data_list)
    highest_students = identify_highest_achieving_students(data_list)
    lowest_students = identify_lowest_achieving_students(data_list)
    performance_trends = analyze_performance_trends(data_list)
    
    """Find most improved student"""
    most_improved_student = get_most_improved_student(student_averages)
    
    """Find subject with highest Term 1 average"""
    highest_term_one_subject = max(
        [avg for avg in class_averages if avg[0] == '1'], 
        key=lambda x: x[2],
        default=["N/A", "N/A", 0],
        )[1]
    
    """Find highest achieving Math student in Term 1"""
    highest_math_student_term_one = next(
        (student[2] for student in highest_students 
         if student[0] == '1' and student[1] == 'Math'), 
        "N/A"
    )
    
    """Find lowest achieving CS student in Term 2"""
    lowest_cs_student_term_two = next(
        (student[2] for student in lowest_students 
         if student[0] == '2' and student[1] == 'CS'), 
        "N/A"
    )
    
    """Find subject with highest positive percentage change in class average between terms"""
    highest_trend_subject= max(
        [trend for trend in performance_trends if trend[1] > 0], 
        key=lambda x: x[1],
        default=["N/A", "N/A", 0]
    )[0]
    
    """Write output to file"""
    with open('StudentScoresAnalysis.txt', 'w') as f:
        f.write(f"The SID is {most_improved_student}\n")
        f.write(f"The subject is {highest_term_one_subject}\n")
        f.write(f"The SID is {highest_math_student_term_one}\n")
        f.write(f"The SID is {lowest_cs_student_term_two}\n")
        f.write(f"The subject is {highest_trend_subject}\n")
    
    print("Analysis complete\n.Results written to StudentScoresAnalysis.txt\n")

if __name__ == "__main__":
    main()