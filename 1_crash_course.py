print(1+1)
print(2+3*5)
num = 12
name = 'Sam'
print('My number is: {one}, and my name is: {two}'.format(one=num,two=name))
print('My number is: {}, and my name is: {}'.format(num,name))

#lists
list1 = [1,2,3]
print(list1)
list1.append('d')
print(list1)

#nested list
list2 = [1,2,[3,4]]
print(list2[2][1])

#dictionary
d = {'key1':'cat','key2':'dog',}
print(d['key1'])

#tuple
t = (1,2,3)
print(t[0])

"""important difference between tuples and dictionary: tuples are IMMUTABLE,
meaning you can't change the items inside the list"""

#sets -- a collection of unique elements
set1 = {1,1,1,2,2,2,3,3,3}
print(set1) #only returns {1,2,3}
set1.add(4)
print(set1)

#comparisons --remember equal is ==
print(1==2) # returns False

# if/else example
if 1 == 2:
    print('first')
elif 3 == 3:
    print('middle')
else:
    print('Last')

# for loops
seq = [1,2,3,4,5]
for item in seq:
    print(item)

# while loops
i = 1
while i < 5:
    print('i is: {}'.format(i))
    i = i+1

# range
range(5)
for i in range(5):
    print(i)

list(range(5))

# list comprehension
x = [1,2,3,4]
out = []
for item in x:
    out.append(item**2)
print(out) # use the 'x' list to create the 'out' list, which is each 'x' value squared

out2 = [item**2 for item in x] # the much quicker way to create a new list. This is list comprehension
print(out2) 

# functions
def my_function(name):
    print('Hello ' +name)
my_function('Carl')

def square(num):
    """This is a function that squares the input.
    Important to put this here within the function so future
    users can easily know what it does"""
    return num**2
square(2)

def times2(var):
    return var*2
print(times2(5))

# map and filter
seq = [1,2,3,4,5]
print(list(map(times2, seq)))

# lambda - return the map and filter from above much simpler
print(list(map(lambda var:var*2,seq)))

# methods
st = 'hello my name is Carl. #cool'
print(st.split())
print(st.split('#'))

print(d.keys())
print(d.items())
print(d.values())