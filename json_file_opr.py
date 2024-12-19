import os
import re
import json

# assign file location
f_path = "C:/Users/durgasurya.pesala/Downloads/test.json"


# func for reading file
def rd():
    with open(f_path,'r') as fr:
        l = json.load(fr)
        fr.close()
    return l

# func for creating new file
def crf(p,a,m):
    with open(p,m) as fw:
        json.dump(a,fw,indent=4)
        fw.close()
    return f"{p} successfully wirtten"

# Func to delete the file
def delt(a):
    os.remove(a)
    return f"file successfully deleted"

def main():
    try:
        d={}
        if os.path.exists(f_path):
            if os.path.isfile(f_path):
                print(f"Specified file exist")
                t = input("do you want to r,a or d")
                if t=='r':
                    print(f"{rd()}\n successfully read")
                elif t=='d':
                    print(delt(f_path))
                else:
                    d = rd()
                    h = int(input("enter no of keys to add in dict"))
                    for i in range(h):
                        k = input("enter a key")
                        d[k] = input("enter a value")
                    crf(f_path,d,'w')
                    
            elif os.path.isdir(f_path):
                print("creating a new json file")
                p = f_path+"/"+input("enter file name to be created")+ ".json"
                h = int(input("enter no of keys to create dict"))
                for i in range(h):
                    k = input("enter a key")
                    d[k] = input("enter a value")

                print(crf(p,d,'w'))
        elif re.search('.*(json)$',f_path):
            print("creating a json file that is not existed")
            h = int(input("enter no of keys to create dict"))
            for i in range(h):
                k = input("enter a key")
                d[k] = input("enter a value")
            m = input("which mode do you want to create file w or x")
            while m not in ('w','x'):
                print(f"please enter only w or x")
                m = input("enter x or w only")
            crf(f_path,d,m)
        else:
            print("the given path does not exist")
    except ValueError:
        print("error\n-----------------------------------")
        print("please enter numeric values")

if __name__ == '__main__':
    main()
else:
    print("Execution of main code in json_file_opr is not allowed in-directly")