class MasterPasswordHandler:
    def __init__(self):
        self.master_password = None
        self.master_password_usages = 1

        self.IS_MASTER_PASSWORD_VALID = False

    def set_master_password(self, password):
        self.master_password = password

    def verify_master_password(self, password):
        self.IS_MASTER_PASSWORD_VALID = True
        return self.master_password == password
    
    def set_master_password_usages(self, num):
        self.master_password_usages = num
    
    def decrement_master_password_usages(self):
        if self.master_password_usages > 0:
            self.master_password_usages -= 1
        if self.master_password_usages == 0:
            self.IS_MASTER_PASSWORD_VALID = False
    