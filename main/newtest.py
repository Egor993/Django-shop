from datetime import datetime

intcount = 30000

def timer(funk):
	def wrapper(*args, **kwargs):
		start = datetime.now()
		res = funk(*args, **kwargs)
		print(datetime.now() - start)
		return res
	return wrapper
@timer
def buh(var=64):
	# start = datetime.now()
	count = 0
	for i in range(var):
		count += 2**i
	# time = datetime.now() - start
	# print(time)
	return count/intcount

print(buh())

@timer
def buh2(var=64):
	# start = datetime.now()
	count = sum([2**i for i in range(64)])
	# time = datetime.now() - start
	# print(time)
	return count/intcount

print(buh2())


