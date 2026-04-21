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
    
    def list_sites(self):
        return self.json_handler._ler_cofre()
    
    def decrypt_password(self, indice, master_password):
        return self.json_handler.descriptografar_umso(indice, master_password)
    
    def delete_password(self, indice):
        self.json_handler.deletar_site(indice)

    def set_master_password(self, master_password, new_master_password):
        self.initializer.trocar_senha_mestra(master_password, new_master_password)
        print("Senha mestra alterada com sucesso!")
    
    def set_master_password_usages(self, num):
        self.master_password_usages = num
    
    def decrement_master_password_usages(self):
        if self.master_password_usages > 0:
            self.master_password_usages -= 1
        if self.master_password_usages == 0:
            self.IS_MASTER_PASSWORD_VALID = False
    