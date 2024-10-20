from components.instagram import BASE_URL_FRIENDSHIPS, XIGAPPID, instagram_request


def getUserFollowing(id: str, csrftoken) -> list:
    """
    Retrieves a list of users that the specified Instagram user ID is following.

    Args:
        id (str): The Instagram user ID to retrieve the following list for.

    Returns:
        list: A list of dictionaries containing following user information.
    """
    # Construct the URL for fetching users that the specified ID is following.
    url = BASE_URL_FRIENDSHIPS + id + f"/following/?count=25"
    # Set the necessary headers, including the csrf token and user ID.
    headers = {
        "cookie": f"csrftoken={csrftoken}; ds_user_id={id}; sessionid={id}%3A8o8K5zLqGYCyet%3A1%3AAYdPySdgKgpc33bh1Xn3Q5oatRSyiKl131JhQuPZLw;",
        "x-ig-app-id": XIGAPPID,
    }

    all_following = []
    while url:
        # Make the API request to fetch the list of following users.
        data = instagram_request(url, headers)
        if data is None:
            # Return the following list if there's an error.
            return all_following

        # Extract the list of following users from the response.
        users = data.get("users", [])
        all_following.extend(users)

        # Get the next page ID for pagination.
        next_max_id = data.get("next_max_id")
        # Update the URL for the next page of following users.
        url = (
            BASE_URL_FRIENDSHIPS + id + f"/following/?count=25&max_id={next_max_id}"
            if next_max_id
            else None
        )

        # Print progress to the console.
        print(f"Loading...{len(all_following)}", end="\r", flush=True)

    # Return the full list of following users.
    return all_following
