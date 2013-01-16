operators = ['+', '-', '*', '/', '<', '>', '==','!=','<=','>=']
typesList = ['int', 'string', 'float', 'char']
types = {}
for op in operators:
	types[op] = {}
	for t in typesList:
		types[op][t] = {}
		for t2 in typesList:
			types[op][t][t2] = "type_error"

# trzeba pouzupelniac
types['+']['int']['int'] = 'int'
types['-']['int']['int'] = 'int'
types['*']['int']['int'] = 'int'
types['/']['int']['int'] = 'int'


types['+']['int']['float'] = 'float'
types['*']['string']['int'] = 'string'
types['>']['string']['string'] = 'int'


print types