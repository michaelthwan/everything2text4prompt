import os

# Define the chunk size in bytes (20MB)
chunk_size = 20 * 1024 * 1024

# Open the input file in binary mode
file_path = "temp.mp3"
with open(file_path, "rb") as f:
    # Read the file as binary data
    data = f.read()

    # Calculate the number of chunks needed
    file_size = os.path.getsize(file_path)
    num_chunks = file_size // chunk_size + (1 if file_size % chunk_size != 0 else 0)

    # Split the data into chunks
    for i in range(num_chunks):
        start = i * chunk_size
        end = min((i + 1) * chunk_size, file_size)
        chunk_data = data[start:end]

        # Write the chunk to a new file
        with open(f"file-part{i}.mp3", "wb") as chunk_file:
            chunk_file.write(chunk_data)
