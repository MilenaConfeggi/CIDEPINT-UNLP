# CIDEPINT-UNLP
manage.py permite ejecutar los comandos de flask y que los distintos backends accedan a la bd 
## Para usar manage.py:
```bash
python manage.py (servicios/administracion) run
```
```bash
python manage.py (servicios/administracion) reset-db
```
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
PORT=3306
DB_NAME=cidepint
DB_USER=cidepint_admin
DB_PASSWORD= (Poner su contraseña)
DB_HOST=localhost

## Para los del grupo de servicios
En el frontend a la altura del index.html tienen que crear un .env en el que este la url de backend en development

```bash
VITE_API_URL=http://127.0.0.1:5000
```
tambien vamos a necesitar un .env.production donde va a estar la url de produccion pero todavia no tenemos servidor!!!