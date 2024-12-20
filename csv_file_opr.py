import re
import os
import csv

f_path = "C:/Users/durgasurya.pesala/Downloads/test.csv"

def rd():
    with open(f_path,'r',newline = '') as fr:
        cnt = csv.reader(fr)
        l=[]
        for i in cnt:
            l.append(i)
        fr.close()
    return l

def crf(p,a,m):
    with open(p,m,newline='') as fw:
        cnt = csv.writer(fw)
        for i in a:
            cnt.writerow(i)
        fw.close()
    return f"successfully written"

def delt(a):
    os.remove(a)
    return f"{a} successfully deleted"

try:
    def main():
        if os.path.exists(f_path):
            print(f"{f_path} exists")
            if(os.path.isfile(f_path)):
                t=input("do you want to r,a or d")
                while t not in ('a','d','r'):
                    print("please enter only r ,a or d only")
                    t=input("do you want to r,a or d")

                if t=='r':
                    print(f"file {f_path} sucessfully read \n{rd()}")
                elif t=='d':
                    print(delt(f_path))
                else:
                    ll = rd()
                    cl = len(ll[0])
                    rw = int(input("enter neow of rows want to append"))
                    for i in range(rw):
                        l = [x for x in range(cl)]
                        for j in range(cl):
                            l[j] = input(f"enter value for the column {ll[0][j]}")
                    ll.append(l)
                    print(crf(f_path,ll,'w'))

            else:
                print(f'create new test file in the given dir {f_path}')
                p = f_path+"/"+input("enter file name to be created")+ ".csv"
                cn = int(input("enter no of cols"))
                rn = int(input("enter no of rows"))
                ll=[]
                for i in range(rn+1):
                    l=[x for x in range(cn)]
                    for j in range(cn):
                        if i==0:
                            l[j] = input(f"enter col name_{j+1}")
                        else:
                            l[j] = input(f"enter the values for column {ll[0][j]}")
                    ll.append(l)              
                print(crf(p,ll,'w'))
        elif re.search('.*(csv)$',f_path):
            print(f"creating file {f_path} which is not exist")
            cn = int(input("enter no of cols"))
            rn = int(input("enter no of rows"))
            ll=[]
            for i in range(rn+1):
                l=[x for x in range(cn)]
                for j in range(cn):
                    if i==0:
                        l[j] = input(f"enter col name_{j+1}")
                    else:
                        l[j] = input(f"enter the values for column {ll[0][j]}")
                ll.append(l)              
            print(crf(f_path,ll,'w'))
        else:
            print(f"{f_path} file doesnt exist")
except ValueError:
    print(f"please enter int values")
except:
    print("something went wrong")

if __name__ == '__main__':
    main()
else:
    print("main code cant be executed in-directly")