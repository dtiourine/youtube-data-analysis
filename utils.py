import pandas as pd

def get_channel_id_by_name(youtube, channel_name):
    """
    Retrieves the YouTube channel ID and title for a given channel name using the YouTube Data API.

    Args:
        youtube (Resource): The YouTube API client instance.
        channel_name (str): The name of the YouTube channel to search for.

     Returns:
        tuple: A tuple containing the channel ID and the channel title if the channel is found.
        Returns (None, None) if the channel is not found or if an error occurs.

    Raises:
        HttpError: An error from the YouTube Data API with response details if the HTTP request failed.
        Exception: A general exception if an unexpected error occurs during the API request.
    """
    try:
        search_response = youtube.search().list(
            q=channel_name,
            part='id,snippet',
            maxResults=1,
            type='channel'
        ).execute()

        for search_result in search_response.get('items', []):
            if search_result['id']['kind'] == 'youtube#channel':
                return search_result['id']['channelId'], search_result['snippet']['title']
    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None, None

def get_channel_stats(youtube, channel_ids):
    """
    Fetches statistics for a list of YouTube channel IDs using the YouTube Data API.

    Args:
        youtube (Resource): An authorized Google API client instance for YouTube Data API v3.
        channel_ids (list of str): A list of YouTube channel IDs.

    Returns:
        pandas.DataFrame: A DataFrame containing the channel name, subscribers count, total views,
                          total number of videos, and uploads playlist ID for each channel.
                          Each row represents one channel.

    Raises:
        HttpError: If an error response is returned from the API call.
        ValueError: If 'channel_ids' is an empty list.

    """

    all_data = []

    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=','.join(channel_ids)
    )
    response = request.execute()

    # loop through items
    for item in response['items']:
        data = {'channelName': item['snippet']['title'],
                'subscribers': item['statistics']['subscriberCount'],
                'views': item['statistics']['viewCount'],
                'totalVideos': item['statistics']['videoCount'],
                'playlistId': item['contentDetails']['relatedPlaylists']['uploads']
                }

        all_data.append(data)

    return pd.DataFrame(all_data)

def get_video_ids(youtube, playlist_id):
    """
    Retrieves all video IDs from a YouTube playlist.

    This function iterates over all pages of a playlist's items, collecting video IDs
    until there are no more pages left to fetch.

    Args:
        youtube (Resource): An authorized Google API client instance for YouTube Data API v3.
        playlist_id (str): The unique identifier for the YouTube playlist.

    Returns:
        list of str: A list containing all video IDs from the specified playlist.

    Raises:
        HttpError: An error response from the API call if it fails.
    """
    video_ids = []

    request = youtube.playlistItems().list(
        part="snippet, contentDetails",
        playlistId=playlist_id,
        maxResults=50
    )
    response = request.execute()

    for item in response["items"]:
        video_ids.append(item['contentDetails']['videoId'])

    next_page_token = response.get('nextPageToken')
    while next_page_token is not None:
        request = youtube.playlistItems().list(
            part="snippet, contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response["items"]:
            video_ids.append(item['contentDetails']['videoId'])

        next_page_token = response.get('nextPageToken')

    return video_ids

def get_video_details(youtube, video_ids):
    """
    Fetches detailed information for a list of video IDs using the YouTube Data API.

    This function aggregates detailed statistics and metadata for each video ID provided in the list.
    The information fetched includes channel title, video title, description, tags, publication date,
    view count, like count, favorite count, comment count, duration, definition quality, and caption availability.
    Data is fetched in batches of 50 video IDs per API request due to API limitations.

    Args:
        youtube (Resource): An authorized Google API client instance for YouTube Data API v3.
        video_ids (list of str): A list of video IDs for which details are to be fetched.

    Returns:
        pandas.DataFrame: A DataFrame containing detailed statistics and metadata for each video.
                          Columns are video_id, channelTitle, title, description, tags, publishedAt,
                          viewCount, likeCount, favoriteCount, commentCount, duration, definition, and caption.

    Raises:
        HttpError: An error response from the API call if it fails.
    """
    all_video_info = []

    # Splitting the list of video IDs into chunks of 50 for batch processing
    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=','.join(video_ids[i: i + 50])
        )
        response = request.execute()

        # Loop through each video and extract required details
        for video in response['items']:
            stats_to_keep = {
                'snippet': ['channelTitle', 'title', 'description', 'tags', 'publishedAt'],
                'statistics': ['viewCount', 'likeCount', 'favoriteCount', 'commentCount'],
                'contentDetails': ['duration', 'definition', 'caption']
            }

            video_info = {'video_id': video['id']}

            # Nested loops to traverse the data structure and retrieve required fields
            for k in stats_to_keep:
                for v in stats_to_keep[k]:
                    try:
                        video_info[v] = video[k][v]
                    except KeyError:
                        video_info[v] = None  # Handling missing data by assigning None

            all_video_info.append(video_info)

    return pd.DataFrame(all_video_info)

