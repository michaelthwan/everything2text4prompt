import re

import openai
import requests
from youtube_transcript_api import YouTubeTranscriptApi

from .util import chunk_mp3


class Everything2Text4Prompt:
    def __init__(self, openai_api_key, is_azure=False):
        self.openai_api_key = openai_api_key
        self.is_azure = is_azure
        openai.api_key = self.openai_api_key

    def convert_text(self, medium, target_source) -> (str, bool, str):
        if medium == "youtube":
            return self.convert_youtube_transcript(target_source)
        elif medium == "podcast":
            return self.convert_podcast_transcript(target_source)
        elif medium == "pdf":
            return self.convert_pdf_to_text(target_source)
        else:
            raise Exception("Unsupported medium")

    def convert_youtube_transcript(self, target_source) -> (str, bool, str):
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

        # TODO get also the title, description of video
        return text, True, "Success"

    def convert_podcast_transcript(self, podcast_url):
        def download_mp3(url: str, file_path: str):
            with open(file_path, "wb") as file:
                response = requests.get(url)
                file.write(response.content)

        content = requests.get(podcast_url)
        mp3_url = re.findall("(?P<url>\;https?://[^\s]+)", content.text)[0].split(';')[1]
        print(f"mp3_url: {mp3_url}")
        mp3_file_path = "temp.mp3"
        download_mp3(mp3_url, mp3_file_path)
        print(f"Downloaded mp3 file")
        file_part_list = chunk_mp3(mp3_file_path)
        transcript_list = []
        for file_part in file_part_list:
            file = open(file_part, "rb")
            print(f"Calling openai whisper-1 for {file_part}")
            transcript = openai.Audio.transcribe("whisper-1", file)
            transcript_list.append(transcript)
        print(transcript_list)
        return " ".join(transcript_list), True, "Success"

    def convert_pdf_to_text(self, target_source):
        raise NotImplementedError("PDF to text conversion is not implemented yet")
        # with open(pdf_file, 'wb') as file:
        #     file.write(pdf_file)
        #
        # reader = PdfReader(pdf_file)
        # text = []
        #
        # for page in reader.pages:
        #     text.append(page.extract_text())
        #
        # return "\n".join(text)


if __name__ == "__main__":
    openai_api_key = ""
    converter = Everything2Text4Prompt(openai_api_key)

    medium = "youtube"
    # target_source = "8S0FDjFBj8o"  # Default English
    target_source = "lSTEhG021Jc"  # Default auto-generated English
    # target_source = "https://www.youtube.com/watch?v=lSTEhG021Jc&ab_channel=EddieGM"  # Test the handling if people input URL
    # target_source = "https://www.youtube.com/watch?v=29WGNfuxIxc&ab_channel=PanSci%E6%B3%9B%E7%A7%91%E5%AD%B8"  # Default Chinese
    # target_source = "https://www.youtube.com/watch?v=K0SZ9mdygTw&t=757s&ab_channel=MuLi"  # Subtitle not available

    # medium = "podcast"
    # Short english
    # Moment 108 - This Powerful Tool Can Change Your Life: Africa Brooke
    # target_source = "https://podcasts.google.com/feed/aHR0cHM6Ly9mZWVkcy5idXp6c3Byb3V0LmNvbS8xNzE3MDMucnNz/episode/NWQzYmJlZDktNzA1Mi00NzU5LThjODctMzljMmIxNmJjZDM3?sa=X&ved=0CAUQkfYCahcKEwig_fW00YH_AhUAAAAAHQAAAAAQLA"

    # Long Chinese
    # TODO: Not sure why it is not working after chunking
    # 通用人工智能离我们多远，大模型专家访谈 ｜S7E11 硅谷徐老师 x OnBoard！
    # target_source = "https://podcasts.google.com/feed/aHR0cHM6Ly9mZWVkcy5maXJlc2lkZS5mbS9ndWlndXphb3poaWRhby9yc3M/episode/YzIxOWI4ZjktNTZiZi00NGQ3LTg3NjctYWZiNTQzOWZjMTNk?sa=X&ved=0CAUQkfYCahcKEwjwp9icjv_-AhUAAAAAHQAAAAAQLA&hl=zh-TW"

    transcript, is_success, error_msg = converter.convert_text(medium, target_source)
    print(transcript)
    print(is_success, error_msg)