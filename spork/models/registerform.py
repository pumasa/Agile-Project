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
        not_alowed_symbol = string.punctuation.replace('.','')
        not_alowed_symbol += " "
        # 1. if @ is in the string and only 1
        if not self.email.count('@') == 1 :
            return False

        # 2. if 1 char or more is before the @
        # 3. if 1 char or more is after the @
        try:    
            email_breakdown = self.email.split("@")
            left_half = email_breakdown[0]
            right_half = email_breakdown[1]
            if len(left_half) == 0 or len(right_half)<=3:
                return False
            for char in left_half:
                if char in not_alowed_symbol:
                    return False
        except:
            return False
        
        # 4. if . is after @
        if right_half.count('.') ==0 :
            return False
        # 5. if 2 char or more after .
        try:
            not_alowed_symbol = string.punctuation.replace('-','')
            not_alowed_symbol += " "   
            right_half_breakdown = right_half.split(".")
            for i in right_half_breakdown[1:]:
                if len(i)<2:
                    return False
                for char in i:
                    if char in not_alowed_symbol:
                        return False

            for char in right_half_breakdown[0]:
                if char in not_alowed_symbol:
                    return False
        except:
            return False
        
        return True
    
    
    def check_password_strength(self):
        symbol = string.punctuation

        upper_count = 0
        lower_count = 0
        special_count = 0
        number_count = 0
        
        if not len(self.password) >= 8:
            return False

        for char in self.password:
            if char.isupper():
                upper_count +=1
            if char.islower():
                lower_count +=1
            if char.isdigit():
                number_count +=1
            if char in symbol:
                special_count +=1

        if upper_count>0 and lower_count>0 and special_count>0 and number_count>0:
            return True
        else:
            return False

    def check_error(self):
        return {
            "confirm_password_error": not self.check_confirm_password(),
            "email_error": not self.check_email(),
            "password_strength_error": not self.check_password_strength()
        }
