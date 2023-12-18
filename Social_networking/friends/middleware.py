from django.core.cache import cache
from django.http import HttpResponseForbidden

class FriendRequestRateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request is for sending a friend request
        if request.method == 'POST' and request.path == '/ap/send_friend_request/':
            user_id = request.POST.get('sender') or request.user.id

            # Define a cache key based on the user's ID
            cache_key = f"friend_request_count:{user_id}"

            # Get the current count or set it to 0 if it doesn't exist
            request_count = cache.get(cache_key, 0)

            # Check if the user has exceeded the limit of 3 friend requests within a minute
            if request_count >= 3:
                return HttpResponseForbidden("You cannot send more than 3 friend requests within a minute.\n Please wait for minute and then try again")

            # If the limit is not exceeded, increment the count in the cache
            request_count += 1
            cache.set(cache_key, request_count, 60)  # Store the count for 60 seconds (1 minute)

        return self.get_response(request)
