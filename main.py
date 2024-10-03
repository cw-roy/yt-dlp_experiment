#!/usr/bin/env python3

import os
import sys
import re
import subprocess
import logging
from logging.handlers import TimedRotatingFileHandler

# Get the directory of the script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Configure logging with a rotating log file
log_file_path = os.path.join(script_directory, "download_log.log")
log_handler = TimedRotatingFileHandler(
    log_file_path, when="W0", interval=1, backupCount=2, encoding="utf-8"
)
log_handler.suffix = "%Y-%m-%d.log"  # Include the date in the log file name
log_handler.maxBytes = 2 * 1024 * 1024  # Set max log file size to 2 megabytes

logging.basicConfig(
    handlers=[log_handler],
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def check_ffmpeg():
    """
    Check if FFmpeg is installed on the machine.

    Returns:
        bool: True if FFmpeg is installed, False otherwise.
    """
    try:
        subprocess.run(
            ["ffmpeg", "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True,
        )
        return True
    except subprocess.CalledProcessError:
        return False


def create_output_directory(output_directory):
    """
    Create the output directory if it doesn't exist.

    Args:
        output_directory (str): The directory to save the downloaded video or audio.

    Returns:
        None
    """
    try:
        os.makedirs(output_directory, exist_ok=True)
    except OSError as e:
        print(f"Error creating output directory: {e}")
        sys.exit(1)


def strip_metadata(file_path):
    """
    Strip metadata from the final downloaded file using FFmpeg.

    Args:
        file_path (str): Path to the input file to strip metadata from.

    Returns:
        None
    """
    try:
        # Remove any existing metadata using FFmpeg on the final downloaded file
        stripped_file_path = file_path + "_stripped" + os.path.splitext(file_path)[1]

        # Construct FFmpeg command to remove all metadata
        cmd = [
            "ffmpeg",
            "-hide_banner",
            "-i",
            file_path,
            "-map_metadata",
            "-1",  # Remove all metadata
            "-c:v",
            "copy",  # Copy video codec without re-encoding
            "-c:a",
            "copy",  # Copy audio codec without re-encoding
            "-y",  # Overwrite existing file if needed
            stripped_file_path,
        ]

        # Run the FFmpeg command
        result = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        # Check for successful execution and handle any errors
        if result.returncode == 0:
            # Replace the original file with the stripped file
            os.replace(stripped_file_path, file_path)
            logging.info(f"Metadata successfully stripped for: {file_path}")
        else:
            # Log a warning if FFmpeg encountered an issue (e.g., no metadata found)
            logging.warning(
                f"FFmpeg encountered a non-critical issue while stripping metadata: {result.stderr}"
            )
            # Attempt to replace the file anyway (to maintain consistent behavior)
            if os.path.exists(stripped_file_path):
                os.replace(stripped_file_path, file_path)

    except FileNotFoundError:
        logging.error(f"File not found for metadata stripping: {file_path}")
    except Exception as e:
        logging.error(f"Error stripping metadata: {e}")

def download_youtube_media(url, base_output_directory, audio_only=False):
    """
    Download a YouTube video or audio given its URL using yt-dlp.

    Args:
        url (str): The URL of the YouTube video.
        base_output_directory (str): The base directory to save the downloaded video or audio.
        audio_only (bool): If True, only download the audio.

    Returns:
        None
    """
    try:
        # Determine the appropriate subdirectory based on whether it's audio or video
        output_directory = os.path.join(base_output_directory, "Audio" if audio_only else "Video")

        # Create the output directory if it doesn't exist
        create_output_directory(output_directory)

        logging.info(f"Downloading started for URL: {url} to {output_directory}")

        # Set format string based on user choice
        format_string = "bestaudio" if audio_only else "bestvideo+bestaudio/best"

        # Construct yt-dlp command
        cmd = [
            "yt-dlp",
            "-f",
            format_string,
            "--output",
            os.path.join(output_directory, "%(title)s.%(ext)s"),
            "--restrict-filenames",
            "--no-mtime",  # Don't use original upload time for file
            "--no-embed-metadata",  # Do not embed any metadata
            "--no-progress",  # Suppress download progress display
            url,
        ]

        # If audio only, use --extract-audio and specify the audio format as mp3
        if audio_only:
            cmd.append("--extract-audio")
            cmd.append("--audio-format")
            cmd.append("mp3")
        else:
            # Only include --merge-output-format for video downloads
            cmd.append("--merge-output-format")
            cmd.append("mp4")

        # Run the yt-dlp command
        result = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True
        )

        # Log command output for debugging
        logging.info(f"yt-dlp stdout: {result.stdout}")
        logging.info(f"yt-dlp stderr: {result.stderr}")

        # Determine the final file path by parsing the yt-dlp output
        filename_match = re.search(r"\[download\] Destination: (.+)", result.stdout)
        if filename_match:
            final_file_path = filename_match.group(1)
            logging.info(f"Download completed successfully: {final_file_path}")

            # Strip metadata from the final merged file
            strip_metadata(final_file_path)
            print(f"Media downloaded and metadata stripped successfully for URL: {url}")
        else:
            # If the final merged file is not found in output, log and display a warning
            print(
                f"Failed to locate the final file for URL: {url}. Check log for details."
            )
            logging.warning(
                f"Could not locate final file in yt-dlp output for URL: {url}"
            )

    except subprocess.CalledProcessError as e:
        logging.error(f"An error occurred while downloading: {e}")
        print(f"Error: Failed to download URL: {url}. Check the log for more details.")

def process_input(input_str):
    """
    Determine whether the input is a URL or a path to a .txt file.

    Args:
        input_str (str): User input.

    Returns:
        list: List of URLs to process.
    """
    if input_str.startswith("http"):
        # If input starts with "http", treat it as a single URL
        return [input_str]
    elif input_str.lower().endswith(".txt"):
        # If input ends with ".txt", treat it as a path to a text file
        with open(input_str, "r") as file:
            urls = [line.strip() for line in file if line.strip()]
            if not urls:
                print("Error: The .txt file does not contain valid URLs.")
                sys.exit(1)
            return urls
    else:
        # Otherwise, treat it as an unknown input
        print("Error: Unknown input format.")
        sys.exit(1)


if __name__ == "__main__":
    # Check if FFmpeg is installed
    if not check_ffmpeg():
        print("Error: FFmpeg not installed.")
        sys.exit(1)

    # Prompt for YouTube video URL or path to a .txt file
    print("YouTube Media Downloader using yt-dlp")
    print(
        "Provide a single URL, or a .txt file containing a list of URLs. Example: `url_list.txt`"
    )
    print("Enter the video URL or path to a .txt file:")
    user_input = sys.stdin.readline().strip()

    # Process the input to get a list of URLs
    urls_to_process = process_input(user_input)

    # Ask the user if they want to download video or audio only
    print("Do you want to download the full (V)ideo or (A)udio only? (V/A):")
    media_choice_input = sys.stdin.readline().strip().lower()

    if media_choice_input == "a":
        audio_only = True
    elif media_choice_input == "v":
        audio_only = False
    else:
        print("Invalid choice. Please enter 'V' for video or 'A' for audio.")
        sys.exit(1)

    # Set the output directory in the same directory as the script
    output_directory = os.path.join(script_directory, "YouTube_downloads")

    # Download the videos or audio using yt-dlp
    for url in urls_to_process:
        download_youtube_media(url, output_directory, audio_only=audio_only)
