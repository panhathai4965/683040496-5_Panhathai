"""
Panhathai Supporn
683040496-5
P2
"""
from datetime import datetime
class Person:
    running_number = 0

    def __init__(self, name, age, birthdate, bloodgroup, is_married):
        self.name = name 
        self.age  = age
        self._id = self.__generate_id()
        self._birthdate = birthdate
        self.__bloodgroup = bloodgroup
        self.__is_married = is_married
        
    
    def display_info(self):
        return f"Name: {self.name} \nAge: {self.age}"
    
    def display_all_info(self):
        return f"Name: {self.name} \nAge: {self.age} \nID: {self._id} \nBirthdate: {self._birthdate} \nBloodgroup: {self.__bloodgroup} \nMarried: {self.__is_married}"
    
    def __generate_id(self):
        Person.running_number += 1
        self._id = (f"{datetime.now().year}{Person.running_number:03d}")

    def get_bloodgroup(self):
        return self.__bloodgroup
    
    def get_married_status(self):
        return self.__is_married
#level 2
class Staff(Person):
    def __init__(self, name, age, birthdate, bloodgroup, is_marrired,  department, start_year):
        super().__init__(name, age, birthdate, bloodgroup, is_marrired)
        self.department = department
        self.start_year = start_year
        self.tenure_year = self.calculate_tenure_years()
        self.__salary = 0
        

    def calculate_tenure_years(self):
        current_year = datetime.now().year
        self.tenure_year = current_year - self.start_year
        return self.tenure_year
    
    def get_salary(self):
        return self.__salary
    
    def set_salary(self, new_salary):
        self.__salary = new_salary

    def display_info(self):
        return f"Name: {self.name} \nAge: {self.age} \nDepartment: {self.department} \nStart year: {self.start_year} \nTenure year: {self.tenure_year} \nSalary: {self.__salary}" 
    
    def display_all_info(self):
        return f"Name: {self.name} \nAge: {self.age} \nID: {self._id} \nBirthdate: {self._birthdate} \nBloodgroup: {self.get_bloodgroup()} \nMarried: {self.get_married_status()} \nDepartment: {self.department} \nStart year: {self.start_year} \nTenure year: {self.tenure_year} \nSalary: {self.get_salary()}"
class Student(Person):
    def __init__(self, name, age, birthdate, bloodgroup, is_marrired, start_year, major, level, grade_list = []):
        super().__init__(name, age, birthdate, bloodgroup, is_marrired)
        self.start_year = start_year
        self.major = major  
        self.level = level
        self.grade_list = grade_list
        self.gpa = self.calculate_gpa()
        self.__graduation_date = self.__calculate_graduation_date()


    def calculate_gpa_static(credits  = [], grades = []):
        grades_dict = {
            'A' : 4.0,
            'B+' : 3.5,
            'B' : 3.0,
            'C+' : 2.5,
            'C' : 2.0,
            'D+' : 1.5,
            'D' : 1.0,
            'F' : 0.0
        }
        total_credits = sum(credits)
        total_point = 0

        if total_credits == 0:
            return 0.0

        for i in range (len(credits)):
            total_point += credits[i] * grades_dict.get(grades[i].upper())
        return total_point / total_credits

    def calculate_gpa(self):
        total = sum(self.grade_list)
        self.gpa = total / len(self.grade_list)
        return self.gpa
    
    def __calculate_graduation_date(self):
        if self.level.lower() == "undergraduate":
            self.__graduation_date = self.start_year + 4
        elif self.level.lower() == "graduate":
            self.__graduation_date = self.start_year + 2
        return self.__graduation_date
    
    def get_graduation_date(self):
        return self.__graduation_date
    
    def display_all_info(self):
        return f"Name: {self.name} \nAge: {self.age} \nID: {self._id} \nBirthdate: {self._birthdate} \nBloodgroup: {self.get_bloodgroup()} \nMarried: {self.get_married_status()} \nStart year: {self.start_year} \nMajor: {self.major} \nLevel: {self.level} \nGPA: {self.gpa:.2f} \nGraduation date: {self.__graduation_date}"

#level 3
class Professor(Staff):
    dict_professorship = {
        0 : "lecturer",
        1 : "assistant professor",
        2 : "associate professor", 
        3 : "full professor",
        4 : "highest full professor",
        "lecturer": 0,
        "assistant professor": 1,
        "associate professor": 2,
        "full professor": 3,
        "highest full professor": 4
    }

    def __init__(self, name, age, birthdate, bloodgroup, is_marrired, department, start_year, professorship, admin_position = 0):
        super().__init__(name, age, birthdate, bloodgroup, is_marrired, department, start_year)
        self.professorship = professorship
        self.admin_position = admin_position
    
    def set_salary(self):
        if isinstance(self.professorship, str):
            self.professorship = Professor.dict_professorship.get(self.professorship.lower())
        self.__salary = 30000 + (self.tenure_year * 1000 )+ (self.professorship * 10000) + (self.admin_position * 10000)
        return self.__salary

    def display_all_info(self):
        return f"Name: {self.name} \nAge: {self.age} \nID: {self._id} \nBirthdate: {self._birthdate} \nBloodgroup: {self.get_bloodgroup()} \nMarried: {self.get_married_status()} \nDepartment: {self.department} \nStart year: {self.start_year} \nTenure year: {self.tenure_year} \nSalary: {self.get_salary()} \nProfessorship: {self.professorship} \nAdmin position: {self.admin_position}"
    
class Administrator(Staff):
    admin_positions_dict = {
        0 : "entry",
        1 : "professional",
        2 : "expert",
        3 : "manager",
        4 : "director",
        "entry": 0,
        "professional": 1,
        "expert": 2,
        "manager": 3,
        "director": 4
    }

    def __init__(self, name, age, birthdate, bloodgroup, is_marrired, department, start_year, admin_position):
        super().__init__(name, age, birthdate, bloodgroup, is_marrired, department, start_year)
        self.admin_position = admin_position
    
    def set_salary(self):
        if isinstance(self.admin_position, str):
            self.admin_position = Administrator.admin_positions_dict.get(self.admin_position.lower())
        self.__salary = 15000 + (self.tenure_year * 800 ) + (self.admin_position * 5000)
        return self.__salary
    
    def display_all_info(self):
        return f"Name: {self.name} \nAge: {self.age} \nID: {self._id} \nBirthdate: {self._birthdate} \nBloodgroup: {self.get_bloodgroup()} \nMarried: {self.get_married_status()} \nDepartment: {self.department} \nStart year: {self.start_year} \nTenure year: {self.tenure_year} \nSalary: {self.get_salary()} \nAdmin position: {self.admin_position}"
#level 4
class UndergraduateStudent(Student):
    def __init__(self, name, age, birthdate, bloodgroup, is_marrired, start_year, major, level, grade_list = [], club = None):
        super().__init__(name, age, birthdate, bloodgroup, is_marrired, start_year, major, level, grade_list)
        self.club = club
        self.coures_list = []
    
    def register_course(self, *courses):
        for course in courses:
            self.coures_list.append(course)
        return self.coures_list
    
    def display_all_info(self):
        return f"Name: {self.name} \nAge: {self.age} \nID: {self._id} \nBirthdate: {self._birthdate} \nBloodgroup: {self.get_bloodgroup()} \nMarried: {self.get_married_status()} \nStart year: {self.start_year} \nMajor: {self.major} \nLevel: {self.level} \nGPA: {self.gpa:.2f} \nGraduation date: {self.get_graduation_date()} \nClub: {self.club} \nCourses: {', '.join(self.coures_list)}"
    
class GraduateStudent(Student):
    def __init__(self, name, age, birthdate, bloodgroup, is_marrired, start_year, major, level, grade_list = [], advisor_name = ""):
        super().__init__(name, age, birthdate, bloodgroup, is_marrired, start_year, major, level, grade_list)
        self.advisor_name = advisor_name
        self.thesis_name = None
        self.__proposal_date = None
        self.__graduation_date = self.__calculate_graduation_date()

    def set_thesis_name(self, thesis_name):
        self.thesis_name = thesis_name

    def __calculate_graduation_date(self):
        if self.__proposal_date != None:
            self.__graduation_date = self.__proposal_date + 1
        else:
            self.__graduation_date = (datetime.now().date().year) + 2
        return self.__graduation_date

    def set_proposal_date(self, proposal_date):
        self.__proposal_date = proposal_date
        self.__graduation_date = self.__proposal_date + 1

    def return_proposal_date(self):
        return self.__proposal_date
    
    def return_graduation_date(self):
        return self.__graduation_date

    def display_all_info(self):
        return f"Name: {self.name} \nAge: {self.age} \nID: {self._id} \nBirthdate: {self._birthdate} \nBloodgroup: {self.get_bloodgroup()} \nMarried: {self.get_married_status()} \nStart year: {self.start_year} \nMajor: {self.major} \nLevel: {self.level} \nGPA: {self.gpa:.2f} \nGraduation date: {self.__graduation_date} \nThesis title: {self.thesis_name} \nAdvisor: {self.advisor_name}" 
    

print("----- Person -----")
person1 = Person("Poom", 25, "20-05-2006", "A", "no")
print(person1.display_all_info())

print("\n----- Staff -----")
staff1 = Staff("Phumin", 30, "02-05-2000", "B", "yes", "IT", 2007)
staff1.set_salary(30000)
print(staff1.display_all_info())

print("\n----- Student -----")
student1 = Student("moon", 30, "22-02-1999", "O", "no", 2000, "com", "undergraduate", [3.5, 4.0, 2.5])
print(student1.display_all_info())
print("\n----- Student_static -----")
student_static = Student.calculate_gpa_static([3,3,4,1,3], ['A', 'B+', 'C', 'A', 'F'])
print(f"Calculated GPA (static method): {student_static:.2f}")

print("\n----- Professor1 -----")
professor1 = Professor("Dr.Tin", 60, "09-10-1988", "AB", "yes", "Com", 1000, "full professor", 1)
professor1.set_salary()
print(professor1.display_all_info())
print("\n----- Professor2 -----")
professor2 = Professor("Dr.poom", 55, "16-09-1970", "A", "yes", "com", 1990, 2, 0)
professor2.set_salary()
print(professor2.display_all_info())

print("\n----- Administrator1 -----")
admin1 = Administrator("boss", 42, "06-07-1880", "B", "no", "com", 1890, "manager")
admin1.set_salary()
print(admin1.display_all_info())
print("\n----- Administrator2 -----")
admin2 = Administrator("fifa", 36, "25-03-1811", "O", "yes", "com", 1999, 3)
admin2.set_salary()
print(admin2.display_all_info())

print("\n----- UndergraduateStudent -----")
under1 = UndergraduateStudent("Poommm", 31, "22-07-2001", "AB", "no", 200, "com", "undergraduate", [3.0, 3.5, 4.0], "chess club")
under1.register_course("compo", "interaction", "data structure")
print(under1.display_all_info())

print("\n----- GraduateStudent -----")
grad1 = GraduateStudent("pim", 22, "04-04-2100", "A", "no", 2016, "com", "graduate", [3.5, 4.0, 3.0], "Dr.Klao")
grad1.set_thesis_name("AI in modern world")
grad1.set_proposal_date(2563)
print(f"Proposal date: {grad1.return_proposal_date()}")
print(grad1.display_all_info())  