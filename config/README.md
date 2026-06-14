Creacion de modulos dentro de app

```bash
  python manage.py startapp name_modulo apps/name_modulo                                                                                             
```

Configuracion del modulo

- entrar al modulo y abrir nombre_modulo/apps.py
- Modificar por esto
```python
class Mobre_moduloConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.nombre_modulo'                                                                             
```

Migraciones de modulos de acuerdo a su esquema
```bash
python manage.py migrate modulo --database=esquema                                                                                                    
```