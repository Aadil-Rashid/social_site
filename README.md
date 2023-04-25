## Social Site
This is a project that implements social networking APIs. The project allows users to register, login, and send friend requests to other users. This README file provides a guide on how to use the project functionalities.

### Workflow Steps
After activating virtual_env and installing requirements

First, migrate the database by running the following command:

```
python manage.py migrate
```

Next, register a user by sending a **POST** request to the following endpoint:

```
http://127.0.0.1:8000/api/register/

with the following JSON data in the request body:
{
    "email": "user@google.com",
    "password": "test",
    "name": "user"
}
```

Alternatively, you can use the following command to create some dummy data in the database:

```
python manage.py create_users
```


To login and obtain an access token, send a **POST** request to the following endpoint:

```
http://127.0.0.1:8000/api/login/
with the following JSON data in the request body:

{
    "email": "aadil@gmail.com",
    "password": "test"
}
```

Copy the access token from the response, as it will be required for all subsequent requests. Note that the token will be valid for only 20 minutes.

Once you have the access token, you can start using the system. To view all users with all functionalities, send a **GET** request to the following endpoint:

```
http://127.0.0.1:8000/api/users/?limit=3&offset=0&search=far
where limit and offset are used for pagination, and 
search is used to search for users by name/or/email.
```

To view the friend list of the logged in user, send a **GET** request to the following endpoint:

```
http://127.0.0.1:8000/api/friend/list/
```


To view pending friend requests of the logged in user, send a **GET** request to the following endpoint:
```
http://127.0.0.1:8000/api/pending/list/
```

To send a friend request to another user, send a **POST** request to the following endpoint:

##### here user can't send more than 3 friend requests in a min

```
http://127.0.0.1:8000/api/send/request/<int:user_id>/
where user_id is the ID of the user to whome the friend request is being sent. 
Use the access token of the some other user for this request.
```

To accept a friend request, send a **PUT** request to the following endpoint:
```
http://127.0.0.1:8000/api/accept/<int:friend_id>/
where friend_id is the ID of the friend who sent the request.
```

To delete a friend request, send a **DELETE** request to the following endpoint:
```
http://127.0.0.1:8000/api/delete/<int:friend_id>/
where friend_id is the ID of the friend who sent the request.
```

### Conclusion
This project provides a basic implementation of social networking APIs that allows users to register, login, and send friend requests to each other. Please feel free to use and modify this project as per your needs.
