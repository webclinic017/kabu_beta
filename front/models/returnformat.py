'''
Created on 2019/12/14

@author: rubyuser
'''


class ReturnFormtat:
    status  =0
    message ='fail'
    
#     成功
    @classmethod
    def successinonfo(cls):
        
        obj =ReturnFormtat()
        obj.message ='success'
        obj.status  =1
        return obj
#     失敗    
    @classmethod
    def failinfo(cls):
        obj =ReturnFormtat()
        return obj
    