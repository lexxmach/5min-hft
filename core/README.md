### Main backend
To run:

```
docker build -t core-5min .
docker run -p 9090:9090 core-5min
```

Swagger UI: http://0.0.0.0:9090/docs

Endpoints:

- /user/register/ - register a user with the new username and password
- /user/login/ - log in the user, return the auth token
- questions/ - returns a new question based on the logged-in user