from app.Json_Manipulador import Json_Manipulador
from app.security.Json_seguranca import Json_seguranca

class MasterPasswordHandler:
    def __init__(self):
        self.initializer = Json_seguranca()

        self.initializer.inicializar_sistema("caio")

        self.json_handler = Json_Manipulador('caio')  # Inicializa com uma senha mestra padrão (pode ser alterada posteriormente)
        self.master_password = None
        self.master_password_usages = 1

        self.IS_MASTER_PASSWORD_VALID = False
    
    def new_login(self, site, user, password, master_password):
        if self.IS_MASTER_PASSWORD_VALID:
            pass
        _, ref = self.json_handler.adicionar_site(site, user, password, master_password)
        self.decrement_master_password_usages()
        return ref

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
    