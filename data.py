from params import *
#处理类间表数据
par = total_params()
f=open(par.fashion_catogory,'r')
lines=f.readlines()
category_dict=dict()
for line in lines:
    line=line.split()
    print(line)
    for id in line:
        temp=list(line)
        print(temp)
        temp.remove(id)
        print(temp)
        if id in category_dict:
            for i in temp:
                if i not in category_dict[id]:
                    category_dict[id].append(i)
        else:
            category_dict[id] =temp

f2=open(par.new_fashion_catogory,'w')
for i in category_dict:
    f2.write("%s\t"%i)
    for j in category_dict[i]:
        f2.write("%s\t"%j)
    f2.write('\n')




