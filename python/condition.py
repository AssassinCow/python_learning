mood_index=int(input("对象今天的心情指数是："))
is_at_home=bool(input("对象今天在不在家："))
if mood_index>=60:
    print("你今晚可以打游戏")
elif is_at_home:
    print("你不能打游戏")
else:  print("你可以打游戏")

## and or not

number=int(input("请你输入1~10之间的一个数字："))
if number<=3:
    print("你渴望成功")
elif number>7 and number<10:
    print("你放弃自己了")
elif number==10:
    print("你生无可恋")
else: print("不错")