import requests
import io
from youtube_transcript_api import YouTubeTranscriptApi


class Everything2Text4Prompt:
    def __init__(self):
        pass

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
        # You will need to add the logic to fetch and convert podcast transcripts
        # based on a specific podcast URL, or consider using a Podcast Transcript API
        raise NotImplementedError("Podcast transcript conversion is not implemented yet")
        response = requests.get(podcast_url)
        transcript = response.text
        return transcript

    def convert_pdf_to_text(self, pdf_file):
        raise NotImplementedError("PDF to text conversion is not implemented yet")
    #     with open(pdf_file, 'wb') as file:
    #         file.write(pdf_file)
    #
    #     reader = PdfReader(pdf_file)
    #     text = []
    #
    #     for page in reader.pages:
    #         text.append(page.extract_text())
    #
    #     return "\n".join(text)


if __name__ == "__main__":
    converter = Everything2Text4Prompt()

    # medium = "youtube"
    # target_source = "8S0FDjFBj8o"  # Default English
    # target_source = "lSTEhG021Jc"  # Default auto-generated English
    # target_source = "https://www.youtube.com/watch?v=lSTEhG021Jc&ab_channel=EddieGM"  # Test the handling if people input URL
    # target_source = "https://www.youtube.com/watch?v=29WGNfuxIxc&ab_channel=PanSci%E6%B3%9B%E7%A7%91%E5%AD%B8"  # Default Chinese
    # target_source = "https://www.youtube.com/watch?v=K0SZ9mdygTw&t=757s&ab_channel=MuLi"  # Subtitle not available

    medium = "podcast"
    # 通用人工智能离我们多远，大模型专家访谈 ｜S7E11 硅谷徐老师 x OnBoard！
    target_source = "https://podcasts.google.com/feed/aHR0cHM6Ly9mZWVkcy5maXJlc2lkZS5mbS9ndWlndXphb3poaWRhby9yc3M/episode/YzIxOWI4ZjktNTZiZi00NGQ3LTg3NjctYWZiNTQzOWZjMTNk?sa=X&ved=0CAUQkfYCahcKEwjwp9icjv_-AhUAAAAAHQAAAAAQLA&hl=zh-TW"

    youtube_transcript, is_success, error_msg = converter.convert_youtube_transcript(target_source)
    print(youtube_transcript)
    print(is_success, error_msg)
