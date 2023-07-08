def ifelse(conditions, yes, no):
    if conditions:
        return yes
    else:
        return no

# class CheckVars:
#     def __init__(self):
#         self.args = ['RGB', 'R', 'G', 'B', 'RE', 'NIR']

#     def check(self):
#         print(self.args)
#         return [arg for arg in self.args if arg in globals()]
    
def check_bands(bands = ['RGB', 'R', 'G', 'B', 'RE', 'NIR']):
    return [i for i in bands if i in globals()]