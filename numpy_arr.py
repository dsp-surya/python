import numpy as np

try:
# no of dimensions
    dim = int(input(f"enter dim of array to be created"))

# creating array for given shape (n,m)
    arr_shape = []
    for i in range(dim):
        arr_shape.append(int(input(f"enter axis-{i} of {dim}-D arr to be created")))

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
            a+= f'for j{i} in range({arr_shape[i]}):\n' + f'\t'*(i+2) + c + f' = {dtyp}(input("enter column value"))'

    exec(a)
    print(d_arr)

# accessing elements in arr

    q = input(f"do you want to access the elements in the {dim}-D arr: yes | no")

    while q.lower() not in ('yes','no'):
        q = input("please enter only yes or no")

    if q.lower() == 'yes':
        print(f"Accessing elements in the arr")
        e = "print(" + input(f"enter the accessibale arr notation in d_arr eg d_arr[1,2]: \n{d_arr}") + ")"
        exec(e)

# display elements whicha statisfy the condition
    q = input(f"do you want to want to apply condition on the {dim}-D arr: yes | no")


    while q.lower() not in ('yes','no'):
        q = input("please enter only yes or no")

    if q.lower() == 'yes':
        cnd = input("enter the condition to display satisfied values in d_arr")
        print("displaying elements as per condition")
        e = "print(f'" + "{d_arr[d_arr" + cnd + "]}')"
        exec(e)

# creating array from a text file
    f_path = "C:/Users/durgasurya.pesala/Downloads/test.txt"
    print(f"creating array from the file {f_path}")
    gen_arr = np.genfromtxt(f_path,delimiter= ',')
    print(gen_arr)



except ValueError:
    print("please enter the specified value")
except:
    print("something went wrong")