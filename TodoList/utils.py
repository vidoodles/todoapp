"""
Utility Functions for Todo Apps
"""

def check_user_auth(user):
    """Checks if the user is authenticated

    Args:
        user (object): User Object

    Returns:
        object: returns User else return as False
    """
    return user if user.is_authenticated else False