class SuperAdminCreds:
    __USERNAME = 'api1@gmail.com'
    __PASSWORD = 'asdqwe123Q'

    @classmethod
    def get_creds(cls):
        return cls.__USERNAME, cls.__PASSWORD #возвращает кортеж

    @classmethod
    def get_name(cls):
        return cls.__USERNAME

    @classmethod
    def get_password(cls):
        return cls.__PASSWORD
