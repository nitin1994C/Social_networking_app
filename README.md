# Social_networking App


Brief description of your project.

## Installation

1. **Clone the Repository:**

git clone https://github.com/your-username/your-repository.git
   
2.Navigate to the Project Directory:
cd your-repository

3.Create a Virtual Environment:
  python -m venv venv
4.Activate the Virtual Environment:

On Windows:
venv\Scripts\activate

5.Install Dependencies:
pip install -r requirements.txt

6.Run Migrations:
python manage.py migrate

7.Run the Development Server:
python manage.py runserver

8.Access the API:
Open your web browser and go to http://localhost:8000 (or the specified port).

API Endpoints:

POST /api/send_friend_request/: Send a friend request.

POST /api/accept_friend_request/{request_id}/: Accept a friend request.

POST /api/reject_friend_request/{request_id}/: Reject a friend request.

GET /api/list_friends/: List friends.

GET /api/list_pending_requests/: List pending friend requests.

Add more endpoints as needed.
Authentication
The API uses Token Authentication.
