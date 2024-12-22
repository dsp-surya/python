# file operation for plain test files

import os
import re

# assign file location
f_path = "C:/Users/durgasurya.pesala/Downloads/test.txt"

# func for appending file
def apnd(a):
    with open(f_path,'a') as f:
        f.write(f"\n{a}")
        f.close()
    return f"file appended succesfully"

# func for reading file
def rd():
    with open(f_path,'r') as fr:
        print(fr.read())
        fr.close()
    return f"file read successfully"

# func for creating new file
def crf(p,a,m):
    with open(p,m) as fw:
        fw.write(a)
        fw.close()
    return f"{p} successfully created"

# Func to delete the file
def delt(a):
    os.remove(a)
    return f"file successfully deleted"

def main():
    try:
        if os.path.exists(f_path):
            if os.path.isfile(f_path) :
                print(f"{f_path} is a file\n----------------------")
                t = input("do you want to read, delete or append the file r : read ,d : delete & a: append")

                while  t not in ('r','a','d') :
                    print("please enter values r ,d or a")
                    t = input("do you want to read the file or append the file r : read & a: append")

                if t=='r':
                    print(f"reading file {f_path} :")
                    print(rd())
                elif t=='d':
                    print(f"deleting the file {f_path}")
                    delt(f_path)
                else:
                    print(f"appending file {f_path} :")
                    a = input("enter lines to append it to the file")
                    print(apnd(a))

            elif os.path.isdir(f_path):
                print(f"this is a dir\ncreating file in dir {f_path}")
                p = f_path+"/"+input("enter file name to be created")+ ".txt"
                a = input("enter line to be added while creating file")
                print(crf(p,a,'w'))

        else:
            if re.search('.*(txt)$',f_path):
                print(f"creating txt file {f_path} which is not existed")
                a = input("enter line to be added while creating file")
                m = input("enter in which mode file has to be creted w or x") 
                while m not in ('w','x'):
                    print("please enter only m or x values")
                    m = input("enter in which mode file has to be creted w or x") 
                crf(f_path,a,m)
                
            else:
                print("given path is not a txt file or dir doesnt exist")

    except ValueError:
        print("error\n-----------------\nplease enter int values 1 or 0 only")
    except:
        print("something went wrong")

if __name__ == '__main__':
    main()
else:
    print("indirect execution of main code in file_opr module is not allowed")