#Toggle state
class Toggle_Condition():
    
    
    def __init__(self, state = 0):
        self.state = state
        return
    
    def process(self, BMI_input):
        if BMI_input and self.state == 0:
            Hardware_output = 1
            self.state = 1
        elif BMI_input and self.state == 1:
            Hardware_output = 0
            self.state = 0
        elif not BMI_input and self.state == 1:
            Hardware_output = 1
        else:
            Hardware_output = 0
        
        return Hardware_output