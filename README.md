# To do list - ggonzalez

## Cómo correr la app

0. Cambiar el nombre del archivo `.example-env` a `.env` e ingresar variables propias
```
$ mv .example-env .env
```

1. Instalar `virtualenv`:
```
$ pip install virtualenv
```

2. Abrir la terminal en la dirección del proyecto y ejecutar: 
```
$ virtualenv env
```

3. Después ejecutar el comando:
```
$ .\env\Scripts\activate
```

4. Luego instalar las dependencias:
```
$ (env) pip install -r requirements.txt
```

5. Finalmente, iniciar el servidor web:
```
$ (env) python app.py
```

La app se encontrará en `http://127.0.0.1:5000/`

