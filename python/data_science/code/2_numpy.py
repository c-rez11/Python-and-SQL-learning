import numpy as np

my_list = [1,2,3]
print(np.array(my_list))

print(np.arange(0,10))
print(np.arange(0,11,2)) # count from 0 to 10 by twos

print(np.zeros(3)) # an array of three zeroes
print(np.zeros((5,4))) # prints a 5x4 matrix of zeroes

print(np.ones(3)) # same idea with ones

print(np.linspace(0,10,3)) #creates array of 3 evenly-spaced numbers between 0 and 10

print(np.eye(4)) # creates a 4x4 identity matrix

#random 

#random.rand -- uniform distribution over [0,1]
print(np.random.rand(2)) 
print(np.random.rand(5,5))

#random.ran -- standard normal distribution with mean 0 and variance 1
print(np.random.randn(5,5))

#random.randint
print(np.random.randint(1,100)) # prints 1 random integer between 1 and 99
print(np.random.randint(1,200,10)) # prints 10 random integers between 1 and 199

#attributes of an array
arr = np.arange(25)
print(arr)
print(arr.reshape(5,5)) # returns the same arr data, but now in a 5x5 matrix

ranarr = np.random.randint(0,50,10)
print(ranarr)
print(ranarr.max()) # returns the max value of the array
print(ranarr.argmax()) # returns the INDEXED POSITION of the array

#shape
print(arr.shape)
print(arr.reshape(25,1))

#data type
print(arr.dtype)

#condition statements -- example
arr_10 = np.arange(1,11)
print(arr_10)
bool_arr = arr_10 > 5 # returns true/false booleans
print(bool_arr) 
print(arr_10[bool_arr]) # returns the values 6-10 which were "true" in bool_arr

