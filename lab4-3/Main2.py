"""
Panhathai Suporn
683040496-5
P2
"""

from datetime import datetime
from University import *

print("----Professor----")
prof = Professor(
    "Dr.Strange", 55, "1970-03-03", "B+", True,
    "Chemistry", 2005, professorship=3, admin_position=1
)
prof.display_info()

print("\n----Administrator----")
admin = Administrator(
    "Mei", 20, "2006-12-01", "AB", True,
    "Digital", 2025, admin_position=1
)
admin.display_info()

print("\n----Undergratuated Student----")
ug = UndergraduateStudent(
    "Namfah", 21, "2005-15-08", "O", False,
    2022, "Engineering",
    grade_list=[(3, 'A'), (3, 'B')], club = "ENPhoto"
)
ug.register_course("EN101")
ug.register_course("IC010")
ug.display_info()

print("\n----Graduate Student----")
gs = GraduateStudent(
    "Neo", 26, "1998-09-06", "O", False,
    2024, "Computer Data Science",
    grade_list=[(3, 'A'), (3, 'A')],
    advisor_name= "Dr.Melvin Sona Calixton"
)
gs.set_thesis_name("Student's perception recgonization of cannabis")
gs.set_proposal_date(datetime(2025, 6, 1))
gs.display_info()