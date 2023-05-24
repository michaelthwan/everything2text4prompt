import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi

from util import YoutubeData


def get_youtube_data(target_source: str) -> (str, bool, str):
    transcript = title = description = None
    try:
        title, description = get_video_info(target_source)
        transcript = convert_youtube_transcript(target_source)
    except Exception as e:
        return YoutubeData(transcript, title, description), False, str(e)
    return YoutubeData(transcript, title, description), True, ""


def get_video_info(target_source):
    url = f"https://www.youtube.com/watch?v={target_source}"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.content, "html.parser")

    title = soup.find("meta", itemprop="name")["content"]
    description = soup.find("meta", itemprop="description")["content"]

    return title, description


def convert_youtube_transcript(target_source) -> YoutubeData:
    def extract_video_id_from_url(url):
        return url.split("v=")[1]

    def is_url(url):
        return "youtube.com" in url

    if is_url(target_source):
        video_id = extract_video_id_from_url(target_source)
    else:
        video_id = target_source

    preferred_lang = ['en', 'zh', 'zh-Hans', 'zh-Hant', 'ja', 'it', 'de', 'fr']
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, preferred_lang)
    except Exception as e:
        import youtube_transcript_api
        if isinstance(e, youtube_transcript_api._errors.TranscriptsDisabled):
            return "", False, "Transcripts are disabled for this video"
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_generated_transcript(preferred_lang)
    text = " ".join([entry['text'] for entry in transcript])

    return text


if __name__ == '__main__':
    target_source = 'lSTEhG021Jc'
    youtube_data, is_success, error_msg = get_youtube_data(target_source)
    youtube_data: YoutubeData
    print(youtube_data.title)
    print(youtube_data.description)
    print(youtube_data.shorten_transcript)
