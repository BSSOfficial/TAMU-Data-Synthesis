import random

dictTest = {}
setTest = set()

names = ['zed','shs','asdf','name','eman','man','hhhh','your','zip','zag','fizz','buzz','tttt']

for x in range(1,100):
	setTest.add(random.randint(0,4000))
setTest = sorted(setTest)
for x in setTest:
	dictTest[x]=names[random.randint(0,12)]

print(dictTest)