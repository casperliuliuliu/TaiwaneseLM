from pytube import Playlist

def get_playlist_urls(playlist_url):
    try:
        playlist = Playlist(playlist_url)
        # This fixes the empty playlist.videos list
        playlist._video_regex = r"\"url\":\"(/watch\?v=[\w-]*)"
        
        return [video.watch_url for video in playlist.videos]
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Example usage
playlist_url = 'https://www.youtube.com/playlist?list=PLoROMvodv4rNiJRchCzutFw5ItR_Z27CM'
video_urls = get_playlist_urls(playlist_url)
for url in video_urls:
    print(url)
