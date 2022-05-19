import string

class RegisterForm:
    def __init__(self,email,password,confirm_password) -> None:
        self.email = email
        self.password = password
        self.confirm_password = confirm_password
        
    def check_confirm_password(self):
        if self.password == self.confirm_password:
            return True
        else:
            return False
    
    def check_email(self):
        # if not string       
        if isinstance(self.email,str) == False:
            return False
        
        # Five checking point
        # 1. if @ is in the string and only 1
        # 2. if 1 char or more is before the @
        # 3. if 1 char or more is after the @
        # 4. if . is after @
        # 5. if 2 char or more after .
        
        
        # 1. if @ is in the string and only 1
        if not self.email.count('@') == 1 :
            return False

        # 2. if 1 char or more is before the @
        # 3. if 1 char or more is after the @
        try:    
            email_breakdown = self.email.split("@")
            left_half = email_breakdown[0]
            right_half = email_breakdown[1]
        except:
            return False
        
        # 4. if . is after @
        if right_half.count('.') ==0 :
            return False
        
        # 5. if 2 char or more after .
        try:
            not_alowed_symbol = string.punctuation.replace('-','')    
            right_half_breakdown = self.email.split(".")
            for i in right_half_breakdown[1:]:
                if len(i)<2:
                    return False
                for char in i:
                    if char in not_alowed_symbol:
                        return False
        except:
            return False
        
        return True
    
    
        