import os
import subprocess
from cartesia import Cartesia
from app.core.config import settings

client = Cartesia(
    api_key=settings.cartesia_api_key,
)

host_id = "694f9389-aac1-45b6-b726-9d9369183238"
guest_id = "a0e99841-438c-4a64-b679-ae501e7d6091"


def generate_audio_from_script(script: dict, output_dir: str) -> list:
    """Generate audio files from the script in response.json"""

    os.makedirs(output_dir, exist_ok=True)

    full_script = script["script"]
    audio_files = []

    for i, line_item in enumerate(full_script):
        speaker = line_item["speaker"]
        text = line_item["text"]

        # Choose voice based on speaker
        voice_id = host_id if speaker == "Host (Jane)" else guest_id

        # Generate audio
        audio_data = client.tts.bytes(
            model_id="sonic-2",
            transcript=text,
            voice={
                "mode": "id",
                "id": voice_id,
            },
            output_format={
                "container": "wav",
                "encoding": "pcm_f32le",
                "sample_rate": 44100,
            },
        )

        # Convert generator to bytes
        audio_data = b"".join(audio_data)

        # Save audio file
        filename = f"{i + 1:02d}_{speaker.replace(' ', '_').replace('(', '').replace(')', '')}.wav"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "wb") as f:
            f.write(audio_data)

        audio_files.append(filepath)
        print(f"Generated: {filename}")

    return audio_files


def concatenate_audio_files(audio_files, output_file: str) -> None:
    """Concatenate all audio files into one"""
    # Create a text file listing all audio files
    with open("file_list.txt", "w") as f:
        for audio_file in audio_files:
            f.write(f"file '{audio_file}'\n")

    # Use ffmpeg to concatenate
    subprocess.run(
        [
            "ffmpeg",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            "file_list.txt",
            "-c",
            "copy",
            output_file,
            "-y",
        ]
    )

    # Clean up
    os.remove("file_list.txt")
    print(f"Full podcast saved as: {output_file}")
