## read readline readlines

f=open("data1.txt", "r", encoding="utf-8")
context=f.read()
print(context)
f.close()

print("\n")

with open("./data2.txt","r",encoding="utf-8") as f:##不用再写close
    lines=f.readlines()
    for line in lines:
        print(line)





