import yt_dlp
import os


def download_instagram_video(url: str, output_dir: str) -> str | None:


                return file_path

       

    except yt_dlp.utils.DownloadError as e:
        print(f"yt-dlp yuklab olish xatoligi: {e}")
        return None
    except Exception as e:
        print(f"Kutilmagan xatolik: {e}")
        return None
