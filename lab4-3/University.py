"""
Panhathai Suporn
683040496-5
P2
"""

from datetime import datetime

class Person:
    __running_number = 0

    def __init__(self, name, age, birthdate, bloodgroup, is_married):
        self.name = name
        self.age = age

        self._birthdate = birthdate
        self._id = self.__generate_id()

        self.__bloodgroup = bloodgroup
        self.__is_married = is_married


    def __generate_id(self):
        Person.__running_number += 1
        year = datetime.now().year
        return f"{year}{Person.__running_number:03d}"
    
    def display_info(self):
        print(f"NAME : {self.name}")
        print(f"AGE : {self.age}")
        print(f"ID : {self._id}")

class Staff(Person):
    def __init__(self, name, age, birthdate, bloodgroup, is_married, department, start_year):
        super().__init__(name, age, birthdate, bloodgroup, is_married)
        self.department = department
        self.start_year = start_year
        self.__salary = 0
        self.tenure_year = self.__calculate_tenure()


    def __calculate_tenure(self):
        return datetime.now().year - self.start_year
    
    def get_salary(self):
        return self.__salary
    
    def set_salary(self, salary):
        self.__salary = salary

    def display_info(self):
        super().display_info()
        print(f"DEPARTMENT : {self.department}")
        print(f"TRNURE YEAR : {self.tenure_year}")
        print(f"SALARY : {self.__salary}")

class Student(Person):
    def __init__(self, name, age, birthdate, bloodgroup, is_married, start_year, major, level, grade_list=None):
        super().__init__(name, age, birthdate, bloodgroup, is_married)
        self.start_year = start_year
        self.major = major
        self.level = level
        self.grade_list = grade_list if grade_list else []
        self.gpa = self.calculate_instance_gpa()
        self.__graduate_date = self.__calcualate_graduation_date()

    
    def calculate_gpa(grade_credit_list):
        grade_map = {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'F': 0}
        total_points = 0
        total_credits = 0

        for credit, grade in grade_credit_list:
            total_points += credit * grade_map[grade]
            total_credits += credit

    def calculate_instance_gpa(self):
        return Student.calculate_gpa(self.grade_list)
    
    def __calcualate_graduation_date(self):
        if self.level.lower() == "undergraduate":
            return self.start_year + 4
        elif self.level.lower() == "graduate":
            return self.start_year + 2
        
        return None
    
    def display_info(self):
        super().display_info()
        print(f"MAJOR : {self.major}")
        print(f"LEVEL : {self.level}")
        print(f"GPA : {self.gpa}")
        print(f"GRADUATION : {self.__graduate_date}")

class Professor(Staff):
    def __init__(self, name, age, birthdate, bloodgroup, is_married, department, start_year, professorship, admin_position=0):
        super().__init__(name, age, birthdate, bloodgroup, is_married, department, start_year)
        self.professorship = professorship
        self.admin_position = admin_position
        self.set_salary()
    
    def set_salary(self):
        salary =(
            30000
            + self.tenure_year * 1000
            + self.professorship * 10000
            + self.admin_position * 10000
        )
        super().set_salary(salary)

    def display_info(self):
        super().display_info()
        print(f"PROFESSORSHIP : {self.professorship}")
        print(f"ADMIN LEVEL : {self.admin_position}")

class Administrator(Staff):
    def __init__(self, name, age, birthdate, bloodgroup, is_married, department, start_year, admin_position):
        super().__init__(name, age, birthdate, bloodgroup, is_married, department, start_year)
        self.admin_position = admin_position
        self.set_salary()

    def set_salary(self):
        salary = (
            15000
            + self.tenure_year * 800
            + self.admin_position * 5000
        )
        super().set_salary(salary)

    def display_info(self):
        super().display_info()
        print(f"ADMIN LEVEL: {self.admin_position}")

class UndergraduateStudent(Student):
    def __init__(self, name, age, birthdate, bloodgroup, is_married, start_year, major, grade_list=None, club=None, course_list=None):
        super().__init__(name, age, birthdate, bloodgroup, is_married, start_year, major, "undergraduate",grade_list)
        self.club = club
        self.course_list = course_list if course_list else []

    def register_course(self, course):
        self.course_list.append(course)

    def display_info(self):
        super().display_info()
        print(f"CLUB : {self.club}")
        print(f"COURSES : {self.course_list}")

class GraduateStudent(Student):
    def __init__(self, name, age, birthdate, bloodgroup, is_married, start_year, major, grade_list=None, advisor_name=None):
        super().__init__(name, age, birthdate, bloodgroup, is_married, start_year, major, "graduate" ,grade_list)
        self.advisor_name = advisor_name
        self.thesis_name = None
        self.__proposal_date = None

    def _Student__calculate_graduation_date(self):
        if self.__proposal_date:
            return self.__proposal_date.year + 1
        return datetime.today().year + 2
    
    def set_proposal_date(self, proposal_date):
        self.__proposal_date = proposal_date
        self._Student__graduation_date = self._Student__calculate_graduation_date()

    def set_thesis_name(self, thesis_name):
        self.thesis_name = thesis_name

    def get_proposal_date(self):
        return self.__proposal_date
    

    def display_info(self):
        super().display_info()
        print(f"ADVISOR : {self.advisor_name}")
        print(f"THESIS : {self.thesis_name}")
        print(f"PROPOSAL DATE: {self.__proposal_date}")