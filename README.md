
# Social Networking API

## Installation

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd social_network
    ```
3. Activate virtual env
   cd projectdirectory
   source env/bin/activate

2. Build and run Docker containers:
    ```bash
    docker-compose up --build
    ```

3. Apply migrations:
   python3 manage.py makemigrations
   python3 manage.py migrate

4. API endpoints:
   signup - To sign up user, using email as a unique identifier and authentication
            POST http://127.0.0.1:8000/api/signup/
   login - Using email and password and Toekns for authentication
            POST http://127.0.0.1:8000/api/login/
   search - To search a user based on the keyword provided 
            GET http://127.0.0.1:8000/api/search/?q=<keyword>
   friend-request - To send a friend request to a user
            POST http://127.0.0.1:8000/api/friend-request/
   manage-friend-request - To accept or reject a friend request
            POST http://127.0.0.1:8000/api/friend-request/<int:id>/<str:action>/
   list-friends - To list all the friends 
            GET http://127.0.0.1:8000/api/friends
   pending-requests - To check the pending friend requests the user have to accept or reject
            GET http://127.0.0.1:8000/api/pending-requests/
5. Contains postman collection for all the API END points 
