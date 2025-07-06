def calculate_BMI(weight,height):
    BMI=weight/height**2
    if BMI<=18.5:
        category="偏瘦"
    elif 18.5<BMI<=25:
        category="正常"
    elif 25<BMI<=30:
        category="偏胖"
    else: category="肥胖"
    print(f"你的BMI分类为：{category}")
    return BMI

try:
    user_weight=float(input("请输入您的体重（单位：kg）："))
    user_height=float(input("请输入您的身高（单位：m）："))
    BMI=calculate_BMI(user_weight,user_height)
except ValueError:
    print("输入不合法，请重新输入")
except ZeroDivisionError:
    print("身高不能为0，请重新输入")
except:
    print("发生未知错误，请重新运行")
else:
    print("你的BMI值为："+str(BMI))
finally:
    print("程序结束运行") 
