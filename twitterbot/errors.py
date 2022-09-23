# Delete errors

class TweetDoesNotExist(Exception):
    message = "The ID that you entered doesn't exist"
    error_code = 40901
    status_code = 409

  