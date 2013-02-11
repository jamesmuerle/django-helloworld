class Errors:
	SUCCESS = 1 # a success
	ERR_BAD_CREDENTIALS = -1 # (for login) cannot find the user/password pair in the database
	ERR_USER_EXISTS = -2 # (for add) trying to add a user that already exists
	ERR_BAD_USERNAME = -3 # (for add) invalid user name (user name should be non-empty and at most 128 ascii characters long)
	ERR_BAD_PASSWORD = -4 # (for add) invalid password (password should be at most 128 ascii characters)