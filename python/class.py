class Student:
    def __init__(self,name,student_id):
        self.name=name
        self.student_id=student_id
        self.grades={"语文":0,"数学":0,"英语":0}
    def set_grade(self,course,grade):
        if course in self.grades:
            self.grades[course]=grade

    def print_grades(self):
        print(f"学生{self.name}(学号:{self.student_id})的成绩为：")
        for course in self.grades:
            print(f"{course}: {self.grades[course]}")


chen=Student("小陈","100618")
chen.set_grade("语文",92)
chen.set_grade("数学",94)
chen.print_grades()




class Employee:
    def __init__(self,name,id):
        self.name=name
        self.id=id

    def print_info(self):
        print(f"员工名字:{self.name}，工号:{self.id}")

class FullTimeEmployee(Employee):
    def __init__(self,name,id,monthly_salary):
        super().__init__(name,id)
        self.monthly_salary=monthly_salary

    def calculate_monthly_pay(self):
        return self.monthly_salary

class PartTimeEmployee(Employee):
    def __init__(self,name,id,daily_salary,workdays):
        super().__init__(name,id)
        self.daily_salary=daily_salary
        self.workdays=workdays

    def calculate_monthly_pay(self):
        return self.daily_salary*self.workdays


zhangsan=FullTimeEmployee("张三","1001",6000)
lisi=PartTimeEmployee("李四","1002",230,15)

zhangsan.print_info()
lisi.print_info()

print(zhangsan.calculate_monthly_pay())
print(lisi.calculate_monthly_pay())









