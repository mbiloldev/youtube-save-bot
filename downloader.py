import yt_dlp
import os


def download_instagram_video(url: str, output_dir: str) -> str | None:
    output_template = os.path.join(output_dir, "%(title).50s.%(ext)s")

    ydl_opts = {
        "outtmpl": output_template,
        "format": "mp4/best[ext=mp4]/best",
        "quiet": True,
        "no_warnings": True,
        # Instagram login talab qilsa, cookies.txt faylini bot papkasiga qo'ying
        # "cookiefile": "cookies.txt",
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

            if os.path.exists(file_path):
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
