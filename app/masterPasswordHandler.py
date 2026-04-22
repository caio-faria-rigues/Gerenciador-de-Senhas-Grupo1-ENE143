from app.Json_Manipulador import Json_Manipulador
from app.security.Json_seguranca import Json_seguranca

class MasterPasswordHandler:
    """
    Classe responsável por gerenciar a senha mestra e suas operações relacionadas.
    """
    def __init__(self):
        self.initializer = Json_seguranca()

        if not self.initializer.seg.esta_configurado():
            self.initializer.inicializar_sistema("123456")
        self.master_password = None
        self.master_password_usages = 1
        self.IS_MASTER_PASSWORD_VALID = False

    def _get_handler(self, master_password):
        """Instancia o manipulador com a senha fornecida no momento do uso."""
        return Json_Manipulador(master_password)

    def new_login(self, site, user, password, master_password):
        _, ref = self._get_handler(master_password).adicionar_site(site, user, password, master_password)
        self.decrement_master_password_usages()
        return ref

    def list_sites(self):
        return Json_Manipulador("").  _ler_cofre()

    def decrypt_password(self, indice, master_password):
        return self._get_handler(master_password).descriptografar_umso(indice, master_password)

    def delete_password(self, indice):
        Json_Manipulador("")._ler_cofre()
        self._get_handler("").deletar_site(indice)

    def set_master_password(self, master_password, new_master_password):
        sucesso, msg = self.initializer.trocar_senha_mestra(master_password, new_master_password)
        return sucesso, msg

    def set_master_password_usages(self, num):
        self.master_password_usages = num

    def decrement_master_password_usages(self):
        if self.master_password_usages > 0:
            self.master_password_usages -= 1
        if self.master_password_usages == 0:
            self.IS_MASTER_PASSWORD_VALID = False