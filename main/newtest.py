array = [1,2,2,1,4,4,4]

result = {i: array.count(i) for i in array}

print (result)


l = {}
b = {}
for i in array:
	# b = {i: array.count(i)}
	l.update({i: array.count(i)})
	
print(l)