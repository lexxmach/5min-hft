### Main backend

To run the service, do the following:

1. Generate Secret key for JWT:
    ```bash
    openssl rand -hex 32
    ```
2. Add the Secret key to the file .env to core/src with the following information:
    ```bash
    SECRET_KEY=<Your secret key>
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=180
    ```
3. Run the following (in core/src):
    ```
    docker build -t core-5min .
    docker run -p 8000:8000 core-5min
    ```
4. The Swagger UI is avaiable here: http://0.0.0.0:8000/docs

Endpoints:

- register/ - register a user with the new username and password
- login/ - log in the user, return the auth token. Впоследствии для получения вопросов или отправки ответов надо будет прикладывать этот токен.
    - В Swagger UI это можно сделать просто нажав Authorize в правом верхнем углу, ввести логин и пароль и после этого все операции будут доступны
- questions/ - returns a new question based on the logged-in user