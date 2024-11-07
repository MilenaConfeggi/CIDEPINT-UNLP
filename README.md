# CIDEPINT-UNLP
manage.py permite ejecutar los comandos de flask y que los distintos backends accedan a la bd 
## Para usar manage.py:
python manage.py (servicios/administracion) run
python manage.py (servicios/administracion) reset-db
## Configuración:
### Creamos la bd:
```bash
CREATE DATABASE cidepint;
```

### Creamos un usuario:
```bash
CREATE USER 'cidepint_admin'@'localhost' IDENTIFIED BY 'Unacontraseña!123';
```

### Por ultimo, le damos al usuario recien creado todos los permisos:
```bash
GRANT ALL PRIVILEGES ON cidepint.* TO 'cidepint_admin'@'localhost';
```
```bash
FLUSH PRIVILEGES;
```

## Creen un .env en la raiz que contenga lo siquiente
(Poner su contraseña)
PORT=3306
DB_NAME=cidepint
DB_USER=cidepint_admin
DB_PASSWORD= 
DB_HOST=localhost