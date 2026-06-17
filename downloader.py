import yt_dlp
import os


def download_instagram_video(url: str, output_dir: str) -> str | None:


                return file_path

            # Fayl boshqa kengaytmada saqlangan bo'lishi mumkin
            base = os.path.splitext(file_path)[0]
            for ext in [".mp4", ".webm", ".mkv", ".mov"]:
                candidate = base + ext
                if os.path.exists(candidate):
                    return candidate

            return None

    except yt_dlp.utils.DownloadError as e:
        print(f"yt-dlp yuklab olish xatoligi: {e}")
        return None
    except Exception as e:
        print(f"Kutilmagan xatolik: {e}")
        return None
