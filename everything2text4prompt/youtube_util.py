import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi

from util import YoutubeData
from urllib.parse import parse_qs


class YoutubeUtil:
    @staticmethod
    def get_youtube_data(target_source: str) -> (str, bool, str):
        transcript = title = description = ts_transcript_list = None
        try:
            video_id = YoutubeUtil.parse_video_id(target_source)
            title, description = YoutubeUtil.get_video_info(video_id)
            transcript, ts_transcript_list = YoutubeUtil.convert_youtube_transcript(video_id)
        except Exception as e:
            return YoutubeData(transcript, title, description, ts_transcript_list), False, str(e)
        return YoutubeData(transcript, title, description, ts_transcript_list), True, ""

    @staticmethod
    def is_url(url):
        return "youtube.com" in url

    @staticmethod
    def parse_video_id(target_source):
        if YoutubeUtil.is_url(target_source):
            # e.g. https://www.youtube.com/watch?v=lSTEhG021Jc&ab_channel=EddieGM -> lSTEhG021Jc
            query = parse_qs(target_source.split('?', 1)[1])
            return query["v"][0]
        if len(target_source) == 11:
            return target_source
        raise Exception("Invalid youtube video id")

    @staticmethod
    def get_video_info(target_source):
        url = f"https://www.youtube.com/watch?v={target_source}"
        response = requests.get(url)

        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.content, "html.parser")

        title = soup.find("meta", itemprop="name")["content"]
        description = soup.find("meta", itemprop="description")["content"]

        return title, description

    @staticmethod
    def convert_youtube_transcript(video_id) -> (str, list):
        def merge_transcript(transcript):
            ts_transcript_list = []

            current_start = transcript[0]['start']
            current_text = transcript[0]['text']
            for i in range(1, len(transcript)):
                if transcript[i]['start'] - current_start >= 30:
                    ts_transcript_list.append({'text': current_text, 'start': current_start})
                    current_start = transcript[i]['start']
                    current_text = transcript[i]['text']
                else:
                    current_text += ' ' + transcript[i]['text']

            ts_transcript_list.append({'text': current_text, 'start': current_start})
            return ts_transcript_list

        preferred_lang = ['en', 'zh', 'zh-HK', 'zh-Hans', 'zh-Hant', 'ja', 'ko', 'it', 'de', 'fr',
                          'tr', 'tk', 'lg', 'da', 'eu', 'mi', 'jv', 'eo', 'gl', 'ca', 'nso', 'gu', 'sw', 'ne', 'ny', 'gn', 'be', 'lt', 'ig', 'is', 'hu', 'id', 'hi', 'ky', 'lo', 'ay', 'fy', 'es',
                          'kri', 'hr', 'kn', 'iw', 'el', 'hy', 'bn', 'la', 'lv', 'ln', 'fa', 'bs', 'pl', 'fi', 'ak', 'am', 'ar', 'az', 'sq', 'as', 'ru', 'bg', 'sd', 'af', 'kk', 'cy', 'co', 'xh', 'yo',
                          'hmn', 'dv', 'sn', 'ee', 'haw', 'ku', 'no', 'pa', 'ka', 'th', 'ta', 'te', 'ht', 'uk', 'uz', 'ur', 'ts', 'zu', 'so', 'mt', 'ms', 'mk', 'mg', 'mr', 'ml', 'km', 'ceb', 'cs',
                          'sa', 'nl', 'bho', 'su', 'ti', 'sl', 'sk', 'ps', 'fil', 'vi', 'tg', 'st', 'sr', 'or', 'om', 'yi', 'et', 'ga', 'sv', 'pt', 'si', 'ug', 'mn', 'qu', 'ha', 'my', 'rw', 'lb',
                          'sm', 'ro', 'gd', 'tt', ]
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, preferred_lang)
        except Exception as e:
            import youtube_transcript_api
            if isinstance(e, youtube_transcript_api._errors.TranscriptsDisabled):
                raise Exception(e)
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            transcript = transcript_list.find_generated_transcript(preferred_lang)
        text = " ".join([entry['text'] for entry in transcript])
        merged_transcript = merge_transcript(transcript)

        return text, merged_transcript


if __name__ == '__main__':
    target_source = 'lSTEhG021Jc'
    youtube_data, is_success, error_msg = YoutubeUtil.get_youtube_data(target_source)
    youtube_data: YoutubeData
    print(youtube_data.title)
    print(youtube_data.description)
    print(youtube_data.shorten_transcript)

    print("Transcript with timestamp:")
    # for entry in youtube_data.ts_transcript_list:
    #     print(f"{int(entry['start'] // 60)}:{int(entry['start'] % 60):02d} {entry['text'][:50]}")
    for entry in youtube_data.ts_transcript_list:
        print(f"{int(entry['start'] // 60)}:{int(entry['start'] % 60):02d} {entry['text']}")
