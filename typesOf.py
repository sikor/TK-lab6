'''                
__/\\\\\\\\\\\\\\\_________________________________________________________        
 _\///////\\\/////__________________________________________________________       
  _______\/\\\__________/\\\__/\\\___/\\\\\\\\\______________________________      
   _______\/\\\_________\//\\\/\\\___/\\\/////\\\_____/\\\\\\\\___/\\\\\\\\\\_     
    _______\/\\\__________\//\\\\\___\/\\\\\\\\\\____/\\\/////\\\_\/\\\//////__    
     _______\/\\\___________\//\\\____\/\\\//////____/\\\\\\\\\\\__\/\\\\\\\\\\_   
      _______\/\\\________/\\_/\\\_____\/\\\_________\//\\///////___\////////\\\_  
       _______\/\\\_______\//\\\\/______\/\\\__________\//\\\\\\\\\\__/\\\\\\\\\\_ 
        _______\///_________\////________\///____________\//////////__\//////////__
      '''

class Types():
    def __init__(self):
        ops = ['+', '-', '*', '/']
        relOps = ['<', '>', '==','!=','<=','>=']
        
        typesList = ['int', 'str', 'float']
        types = {}
        
        for op in ops + relOps:
            types[op] = {}
            for t in typesList:
                types[op][t] = {}
                for t2 in typesList:
                    types[op][t][t2] = "types_error"
        
        # trzeba pouzupelniac
        for op in ops:
            types[op]['int']['int'] = 'int'
            types[op]['float']['float'] = 'float'
            types[op]['int']['float'] = 'float'
            types[op]['float']['int'] = 'float'
            
            
        for op in relOps:
            types[op]['int']['int'] = 'int'
            types[op]['float']['float'] = 'int'
            types[op]['int']['float'] = 'int'
            types[op]['float']['int'] = 'int'
            types[op]['str']['str'] = 'int'
            
            
        types['+']['str']['str'] = 'str'
        types['*']['str']['int'] = 'str'
            
            
        types['+']['int']['int'] = 'int'
        types['-']['int']['int'] = 'int'
        types['*']['int']['int'] = 'int'
        types['/']['int']['int'] = 'int'
        
        
        types['+']['int']['float'] = 'float'
        types['*']['str']['int'] = 'str'
        types['>']['str']['str'] = 'int'
        
        self.types = types
        
    def checkType(self, op, arg1, arg2):
        return self.types[op][arg1][arg2]
        
    def error(self):
        return "types_error"
