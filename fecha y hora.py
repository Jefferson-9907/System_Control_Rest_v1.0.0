from datetime import datetime

fecha = datetime.now()
fecha_creacion = '{}/{}/{}'.format(fecha.day, fecha.month, fecha.year)
print(fecha_creacion)
