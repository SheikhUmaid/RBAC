# Testing

In the pwd (present working directory) Postman collection are provided for testing all the endpoints. For endpoint urls refer to [readme.me](../readme.me)

**while firing the server if you find any DB issues:**

delete db.sqlite file and apply migrations


```
python manage.py makemigrations
python manage.py migrate
```

api_server = '127.0.0.1:8000/api'
