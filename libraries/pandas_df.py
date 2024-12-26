import numpy_arr as npa
import pandas as pd
import os

# creating an array from numpy_arr module
def np_arr():
    print(f"creating array from numpy_arr module")
    arr = npa.crt_arr()
    print(f"the array created with shape {arr.shape} :\n{arr}")
    return arr

# creating desired index for DataFrame
def arr_indx(arr):
    q = input(f"do you want to give desired indexes for df (yes | no) : ")

    while q.lower() not in ('yes','no'):
        print(f'please enter only yes or no')
        q = input(f"do you want to give desired  indexes for df (yes | no) : ")

    if q.lower() == 'yes':
        indx = []
        for i in range(arr.shape[0]):
            indx.append(input(f"enter {i+1} index : "))
        print(f"Desired Indexes are : \n{indx}")
    else:
        return "choosen not to have desired indexes"
    return indx

# Change the Col names
def arr_col(arr):
    q = input(f"do you want to give desired column names for df (yes | no) : ")

    while q.lower() not in ('yes','no'):
        print(f'please enter only yes or no')
        q = input(f"do you want to give desired  column names for df (yes | no) : ")

    if q.lower() == 'yes':
        col=[]
        for i in range(arr.shape[1]):
            col.append(input(f"enter {i+1} col name for df arr"))
        print(col)
    else:
        return "choosen not to have desired col names"
    return col

# creating datafram from arr created
def crt_df(arr,indx,col):
    q = input("do you have changed indexes and col names for df (yes | no)")
    while q.lower() not in ('yes','no'):
        q = input("do you have changed indexes and col names for df (yes | no)")
    
    if q.lower() == 'yes':
        df = pd.DataFrame(arr,index=indx,columns=col)
        print(f"Datafram created is :\n{df}")
    else:
        df = pd.DataFrame(arr)
        print(f"Datafram created is :\n{df}")
    return df

def add_col(df):
    
    q = input(f"do you want to add new col to DataFrame (yes | no): \n {df}")
    while q.lower() not in ('yes','no'):
        q = input("please enter yes or no only")
    
    if q.lower() == 'yes':
        cl=[]
        n = int(input(f"enter how many columns you want to add to df :\n{df}"))
        for i in range(n):
            c= input(f"enter new col{i+1} to be added")
            df[c] = input(f"enter value/list/tuple for col{i+1} adding")
            df[c] = df[c].astype(input(f'enter data type of col{i+1}'))
            cl.append(c)
        return print(f"{n} col : {cl} are added")

def check_dtypes(df):
    
    q = input("do you want to change any col dype (yes | no)")
    while q.lower() not in ('yes','no'):
        q = input("do you want to change any col dype (yes } no)")
    
    if q.lower() == 'yes':
        n = int(input('how many cols dtypes you want to change'))
        for i in range(n):
            col = input("enter col name")

            while col not in df.columns:
                col = input("enter col name as given in df")
            dt = input(f"enter data type of {col} you wanted to change")
            df[col] = df[col].astype(dt)
        return print(f"the dataframe with updated dtypes is : \n{df.dtypes}")

def manip(df):
    m = int(input("do you want to perform any basic opr in df (1 | 0)"))
    while m not in (1,0):
        m = int(input("do you want to perform any absic opr in df (1 | 0)"))
    
    if m==1:
        i=1
        while i:
            print("Choose which opr do you want to perform: ")
            q = int(input(f"\t1 - Addition\n\t2 - Subraction\n\t3 - division\n\t4 - Multiplication"))
            while q not in (1,2,3,4):
                q = int(input(f"1 - Addition\n2 - Subraction\n3 - division\n4 - Multiplication"))
            
            if q == 1:
                a = input("enter the addition stmt")
                print(f"Performing addition as per given expr: \n{exec(a)}")
            elif q == 2:
                a = input("enter the subraction stmt")
                print(f"Performing subraction as per given expr: \n{exec(a)}")
            elif q == 3:
                a = input("enter the Division stmt")
                print(f"Performing Division as per given expr: \n{exec(a)}")
            else:
                a = input("enter the Multiplication stmt")
                print(f"Performing Multiplication as per given expr: \n{exec(a)}")

        i = int(input("do you want to perform 1,2,3,4 again (1 | 0)"))
    else:
        print(f"choosen not to perform any opr")

    return df

def drop_col(df):
    q = int(input(f"do you want to drop any column in the df (1 | 0):\n{df}"))
    while q not in (1,0):
        q = int(input(f"do you want to drop any column in the df (1 | 0):\n\t{df}"))
    if q == 1:
        cols = []
        n = int(input("enter no of cols you want to drop from above df"))
        for i in range(n):
            d = input("enter col name you want to drop in the df")
            cols.append(d)
        df = df.drop(columns = cols)
    else:
        return "choosen not to drop any col from df"

    return df
        
def export_df(df):
    q = int(input("do you want to export df (1 | 0)"))
    while q not in (1,0):
        q = input("do you want to export df (1 | 0)")
    
    if q==1:
        f_path  = input("enter a directory path to export the df")
        if os.path.exists(f_path):
            print(f"exporting the df to file path \n{f_path}")
            format = int(input("in which format of file do you wnat to export the df :\n\t1 - Excel\n\t2 - csv\n\t3 - txt"))
            while format not in (1,2,3):
                format = int(input("in which format of file do you wnat to export the df :\n\t1 - Excel\n\t2 - csv\n\t3 - txt"))

            file_name = input("enter file name you want to create to laod the df")
            if format == 1:
                df.to_excel(f_path+'/'+file_name+'.xlsx')
            elif format == 2:
                df.to_csv(f_path+'/'+file_name+'.csv')
            else:
                df.to_csv(f_path+'/'+file_name+'.txt')
        else:
            print("directory does not exist")
    else:
        return "choosen not to export the df"

    return print(f"{df} exported successfully")

def crt_df_load():
    q = int(input("do you want to create df from file path (1 } 0)"))
    while q not in (1,0):
        q = int(input("do you want to create df from file path (1 } 0)"))
    
    if q==1:
        print(f"creating df from the file path specified in npa modue:\n{npa.f_path}")
        d = npa.crt_arr_gen()
        df_load = pd.DataFrame(d)
    else:
        return f"choosen not to create df from npa file path"

    return df_load


def main():
    arr = np_arr()
    indx = arr_indx(arr)
    col = arr_col(arr)
    df = crt_df(arr,indx,col)
    add_col(df)
    print(f"{df}\n\ncheck the cols data types : \n{df.dtypes}")
    check_dtypes(df)
    print(manip(df))
    print(drop_col(df))
    export_df(df)
    print(crt_df_load())

try:
    if __name__ == '__main__':
        main()
    else:
        print(f"execution  of main block in-directly no allowed")
except ValueError:
    print(f"enter correct data type value")
except:
    print("something went wrong")
