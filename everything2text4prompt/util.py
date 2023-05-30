import os


class BaseData:
    def __init__(self, full_content):
        self.full_content = full_content

    def shorten_text(self, text: str) -> str:
        if text is None or len(text) < 120:
            return text
        return text[:50] + " ... " + text[-50:]


class YoutubeData(BaseData):
    def __init__(self, transcript, title, description, ts_transcript_list):
        super().__init__(transcript)
        self.title = title
        self.description = description
        self.shorten_transcript = self.shorten_text(transcript)
        self.ts_transcript_list = ts_transcript_list


class PodcastData(BaseData):
    def __init__(self, transcript, title, description, ts_transcript_list):
        super().__init__(transcript)
        self.title = title
        self.description = description
        self.shorten_transcript = self.shorten_text(transcript)
        self.ts_transcript_list = ts_transcript_list


def chunk_mp3(file_path: str) -> list:
    chunk_size = 20 * 1024 * 1024  # 20MB

    with open(file_path, "rb") as f:
        data = f.read()  # Read the file as binary data

        # Calculate the number of chunks needed
        file_size = os.path.getsize(file_path)
        num_chunks = file_size // chunk_size + (1 if file_size % chunk_size != 0 else 0)

        # Split the data into chunks
        file_part_list = []
        for i in range(0, num_chunks):
            print(f"Splitting chunk {i + 1} of {num_chunks}")
            start = i * chunk_size
            end = min((i + 1) * chunk_size, file_size)
            chunk_data = data[start:end]

            # Write the chunk to a new file
            file_part = f"temp-part_{i + 1}_{num_chunks}_en.mp3"
            with open(file_part, "wb") as chunk_file:
                chunk_file.write(chunk_data)

            if os.path.getsize(file_part) < 2000:  # reject ~0 mp3 files
                continue
            file_part_list.append(file_part)
        print(f"chunk_mp3 summary: total_size = {file_size}, num_chunks = {num_chunks}")
    return file_part_list


if __name__ == '__main__':
    file_part_list = chunk_mp3("temp_short_en.mp3")
    print(file_part_list)
