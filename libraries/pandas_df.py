import numpy_arr as npa
import pandas as pd

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

    indx = []
    for i in range(arr.shape[0]):
        indx.append(input(f"enter {i+1} index : "))
    print(f"Desired Indexes are : \n{indx}")
    return indx

# Change the Col names
def arr_col(arr):
    q = input(f"do you want to give desired column names for df (yes | no) : ")

    while q.lower() not in ('yes','no'):
        print(f'please enter only yes or no')
        q = input(f"do you want to give desired  column names for df (yes | no) : ")

    col=[]
    for i in range(arr.shape[1]):
         col.append(input(f"enter {i+1} col name for df arr"))
    return col

# creating datafram from arr created
def crt_df(arr,indx,col):
    df = pd.DataFrame(arr,index=indx,columns=col)
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

def tm_avg(df):
    df['Total_Marks'] = df['English'] + df['Telugu'] + df['Hindi']
    df['Avg_Marks'] = df['Total_Marks']/3
    return f"Total Marks & Avg in DF are updated"


def main():
    arr = np_arr()
    indx = arr_indx(arr)
    col = arr_col(arr)
    df = crt_df(arr,indx,col)
    add_col(df)
    print(f"{df}\n\ncheck the cols data types : \n{df.dtypes}")
    check_dtypes(df)
    #tm_avg(df)

main()
"""try:
    if __name__ == '__main__':
        main()
    else:
        print(f"execution  of main block in-directly no allowed")
except ValueError:
    print(f"enter correct data type value")
except:
    print("something went wrong")

"""