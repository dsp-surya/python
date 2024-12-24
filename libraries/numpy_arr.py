import numpy as np

# no of dimensions
dim = int(input(f"enter dim of array to be created"))

# file path from which arr wil be created
f_path = "C:/Users/durgasurya.pesala/Downloads/test.txt"

def crt_arr():

# creating array for given shape (n,m)
    arr_shape = []
    for i in range(dim):
        arr_shape.append(int(input(f"enter {i+1}th number in the {dim}-D arr.shape() to be created")))

    arr = np.array(arr_shape)
    dtyp = input(f"enter data type of elements to be in {dim}-D arr")
    d_arr = np.zeros(arr,dtype = dtyp)

# setting elements in array
    a= ''
    c='d_arr['
    for i in range(dim):
        if i<dim-1:
            c+= f'j{i},'
            a+= f'for j{i} in range({arr_shape[i]}):\n' + f'\t'*(i+1)
        else:
            c+= f'j{i}]'
            a+= f'for j{i} in range({arr_shape[i]}):\n' + f'\t'*(i+2) + c + f' = input("enter column value")'
    exec(a)
    return d_arr


# accessing elements in arr
def acs_arr(arr):

    q = input(f"do you want to access the elements in the {dim}-D arr: yes | no")

    while q.lower() not in ('yes','no'):
        q = input("please enter only yes or no")

    if q.lower() == 'yes':
        print(f"Accessing elements in the arr")
        e = "print(" + input(f"enter the accessibale arr notation in arr eg arr[1,2]:\n{arr} ") + ")"
        print(f"the value as per the givne input is")
        return exec(e)
    else:
        return f'Opted to not to access any element in the array'
    
def arr_cond(arr):
# display elements which statisfy the condition
    q = input(f"do you want to want to apply condition on the {dim}-D arr: yes | no")


    while q.lower() not in ('yes','no'):
        q = input("please enter only yes or no")

    if q.lower() == 'yes':
        cnd = input(f"enter the condition to display satisfied values in d_arr\n{arr}")
        print("displaying elements as per condition")
        e = "print(f'" + "{arr[arr" + cnd + "]}')"
        
        return exec(e)
    else:
        return "Opted not to check any conditon"

# creating array from a text file using genfromtxt func
def crt_arr_gen():
    print(f"creating array from the file {f_path} using genfromtxt()")
    gen_arr = np.genfromtxt(f_path,delimiter= ',',dtype = 'int32')
    return gen_arr

# creating array from a text file using loadtxt func
def crt_arr_load():
    print(f"creating array from the file {f_path} using loadtxt()")
    load_arr = np.loadtxt(f_path,dtype='int32',delimiter=',')
    return load_arr

def main():
    arr = crt_arr()
    print(arr)
    acs_arr(arr)
    arr_cond(arr)
    print(crt_arr_gen())
    print(crt_arr_load())

try:
    if __name__ == '__main__':
        main()
    else:
        print(f"execution of main code in-directly not allowed")
except ValueError:
    print(f"please enter the specified value")
except:
    print("something went wrong")

