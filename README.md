# YouTube Media Downloader using `yt-dlp`

Code is mine, README written by ChatGPT because writing documentation is boring, and this is just a fun side project. 

Developed and tested on Linux; I might work on a Windows version later.

I use Ruff [ https://docs.astral.sh/ruff/ ] for my linter.

TIP: Use a venv (virtual environment) if you don't want yt-dlp installed globally. [ https://docs.python.org/3.10/library/venv.html ]

---

ChatGPT content begins: This Python script allows users to download videos or extract audio from YouTube using the powerful `yt-dlp` tool. The script supports downloading multiple URLs, either specified directly or via a text file, and offers users the option to choose between full video downloads or audio-only extraction.

## Features

- **Download Options**: Choose to download full videos or extract audio only.
- **Batch Downloads**: Provide a single URL or a `.txt` file containing multiple URLs for batch processing.
- **Automatic Output Directory Management**: Automatically creates and manages an output directory for saving media files.
- **Metadata Stripping**: Uses `FFmpeg` to remove unnecessary metadata from downloaded media files.
- **Logging**: Detailed logging of all download activities with support for rotating log files.

## Requirements

Make sure the following dependencies are installed on your system:

1. **Python 3.6+**
2. **yt-dlp**
3. **FFmpeg**

### Installing `yt-dlp`

You can install `yt-dlp` using the following command:

```bash
pip install yt-dlp
```

### Installing `FFmpeg`

You will also need `FFmpeg` for audio and video processing. Follow the [FFmpeg installation guide](https://ffmpeg.org/download.html) to install it on your system.

## Usage

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-repository/yt-media-downloader.git
   cd yt-media-downloader
   ```

2. **Run the Script:**

   Run the script and provide a YouTube URL or a path to a text file containing multiple URLs:

   ```bash
   python3 main.py
   ```

3. **Input Options:**

   - Enter a single YouTube URL (e.g., `https://www.youtube.com/watch?v=example`).
   - Or, enter the path to a `.txt` file containing multiple URLs (e.g., `url_list.txt`).

4. **Choose Media Type:**

   When prompted, choose whether you want to download full videos or audio-only:

   - Enter `V` for full video.
   - Enter `A` for audio only.

5. **Output:**

   The script saves all downloaded files in the `YouTube_downloads` directory located in the same folder as the script. The filenames will correspond to the video or song titles.

## Logging

The script logs its activities to a file named `download_log.log`, located in the script directory. Logs are rotated weekly and kept for up to 2 weeks. This can be useful for tracking downloads or diagnosing issues.

## Example

```
YouTube Media Downloader using yt-dlp
Provide a single URL, or a .txt file containing a list of URLs. Example: `url_list.txt`
Enter the video URL or path to a .txt file:
> https://www.youtube.com/watch?v=dQw4w9WgXcQ

Do you want to download the full (V)ideo or (A)udio only? (V/A):
> A

Media downloaded and metadata stripped successfully for URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

## Troubleshooting

- **Error: `FFmpeg not installed.`**

  Ensure that `FFmpeg` is installed and accessible from the command line.

- **Error: Failed to download URL. Check the log for more details.**

  If the download fails, refer to the `download_log.log` file for a detailed error report.

## Disclaimer

This script is intended for personal use only. Ensure you comply with YouTube’s Terms of Service and copyright laws when using it.