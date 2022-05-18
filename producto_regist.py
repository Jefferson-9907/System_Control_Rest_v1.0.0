class ProductoRegistration:
    """
        Esta clase es una clase modelo para obtener valores del formulario de registro del estudiante y
        establecer todos los datos en la tabla de la base de datos backend llamada estudiantes
    """

    def __init__(self, e_descripcion_1, e_valor_c_1, e_valor_v_1, e_estado_1):
        self.__e_descripcion_1 = e_descripcion_1
        self.__e_valor_c_1 = e_valor_c_1
        self.__e_valor_v_1 = e_valor_v_1
        self.__e_estado_1 = e_estado_1

    # ===========================set methods=======================

    def set_e_descripcion_1(self, e_descripcion_1):
        self.__e_descripcion_1 = e_descripcion_1

    def set__e_valor_c_1(self, e_valor_c_1):
        self.__e_valor_c_1 = e_valor_c_1

    def set__e_valor_v_1(self, e_valor_v_1):
        self.__e_valor_v_1 = e_valor_v_1

    def set_e_estado_1(self, e_estado_1):
        self.__e_estado_1 = e_estado_1

    # =====================get methods========================

    def get_e_descripcion_1(self):
        return self.__e_descripcion_1

    def get_e_valor_c_1(self):
        return self.__e_valor_c_1

    def get_e_valor_v_1(self):
        return self.__e_valor_v_1

    def get_e_estado_1(self):
        return self.__e_estado_1


class GetDatabase:
    def __init__(self, database):
        self.__database = database

    def get_database(self):
        return self.__database
