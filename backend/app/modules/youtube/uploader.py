import asyncio
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional
import pytz
from backend.app.config import settings
from backend.app.modules.youtube.upload_ledger import UploadLedger

YOUTUBE_SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl",
]

class YouTubeUploader:
    """
    Module O: Official YouTube Data API v3 Uploader & Scheduler.
    Handles resumable uploads, metadata injection, thumbnail & Hindi SRT caption upload,
    RFC 3339 publishAt timestamps, and strict fail-closed live upload enforcement.
    """

    def __init__(self):
        self.client_id = settings.YOUTUBE_CLIENT_ID
        self.client_secret = settings.YOUTUBE_CLIENT_SECRET
        self.refresh_token = settings.YOUTUBE_REFRESH_TOKEN

    def is_live_configured(self) -> bool:
        return (
            bool(self.client_id)
            and self.client_id != "mock_client_id"
            and bool(self.client_secret)
            and self.client_secret != "mock_client_secret"
            and bool(self.refresh_token)
            and self.refresh_token != "mock_refresh_token"
            and len(self.refresh_token) > 20
        )

    def convert_ist_to_utc_rfc3339(self, publish_time_ist_str: str, target_date_ist: datetime = None) -> str:
        """
        Converts IST (Asia/Kolkata) time to RFC 3339 UTC string required by YouTube API.
        e.g. 19:00 IST -> 13:30:00Z
        """
        ist = pytz.timezone(settings.PUBLISH_TIMEZONE)
        now_ist = datetime.now(ist) if target_date_ist is None else target_date_ist
        
        hrs, mins = map(int, publish_time_ist_str.split(":"))
        scheduled_ist = ist.localize(datetime(
            year=now_ist.year,
            month=now_ist.month,
            day=now_ist.day,
            hour=hrs,
            minute=mins,
            second=0
        ))
        
        utc_dt = scheduled_ist.astimezone(pytz.utc)
        return utc_dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    def _execute_live_upload_sync(
        self,
        video_path: Path,
        thumbnail_path: Optional[Path],
        subtitles_path: Optional[Path],
        body: Dict[str, Any]
    ) -> Dict[str, Any]:
        import socket
        import ssl
        import time
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload

        socket.setdefaulttimeout(120.0)

        creds = Credentials(
            token=None,
            refresh_token=self.refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=self.client_id,
            client_secret=self.client_secret,
            scopes=YOUTUBE_SCOPES,
        )
        creds.refresh(Request())

        youtube = build("youtube", "v3", credentials=creds)

        # 1. Resumable 1MB chunk video upload with automatic retry on write timeouts/SSL glitches
        media = MediaFileUpload(
            str(video_path),
            chunksize=1024 * 1024,
            resumable=True,
            mimetype="video/mp4",
        )
        request = youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media,
        )
        response = None
        retry_count = 0
        max_retries = 10
        while response is None:
            try:
                status, response = request.next_chunk()
                if status:
                    print(f"YouTube upload progress: {int(status.progress() * 100)}%")
                retry_count = 0
            except (TimeoutError, ssl.SSLError, socket.timeout, Exception) as e:
                retry_count += 1
                if retry_count > max_retries:
                    raise e
                wait_time = min(30, retry_count * 5)
                print(f"⚠️ YouTube upload chunk retry {retry_count}/{max_retries} in {wait_time}s: {e}")
                time.sleep(wait_time)

        video_id = response.get("id")
        if not video_id:
            raise RuntimeError(f"YouTube API did not return a video ID: {response}")

        # 2. Upload custom thumbnail if provided
        thumbnail_uploaded = False
        thumbnail_error = None
        if thumbnail_path and thumbnail_path.exists():
            try:
                youtube.thumbnails().set(
                    videoId=video_id,
                    media_body=MediaFileUpload(str(thumbnail_path), mimetype="image/jpeg"),
                ).execute()
                thumbnail_uploaded = True
            except Exception as e:
                thumbnail_error = str(e)

        # 3. Upload Hindi SRT caption track if provided
        subtitles_uploaded = False
        subtitles_error = None
        if subtitles_path and subtitles_path.exists() and subtitles_path.stat().st_size > 0:
            try:
                youtube.captions().insert(
                    part="snippet",
                    body={
                        "snippet": {
                            "videoId": video_id,
                            "language": "hi",
                            "name": "Hindi",
                            "isDraft": False,
                        }
                    },
                    media_body=MediaFileUpload(str(subtitles_path), mimetype="application/x-subrip"),
                ).execute()
                subtitles_uploaded = True
            except Exception as e:
                subtitles_error = str(e)

        return {
            "video_id": video_id,
            "thumbnail_uploaded": thumbnail_uploaded,
            "thumbnail_error": thumbnail_error,
            "subtitles_uploaded": subtitles_uploaded,
            "subtitles_error": subtitles_error,
        }

    async def upload_and_schedule_video(
        self,
        video_path: Path,
        thumbnail_path: Optional[Path],
        metadata: Dict[str, Any],
        scheduled_publish_time_ist: str = "19:00",
        target_date: Optional[datetime] = None,
        subtitles_path: Optional[Path] = None,
        simulate_upload: bool = True
    ) -> Dict[str, Any]:
        if not video_path.exists():
            raise FileNotFoundError(f"Video file {video_path} not found.")

        file_hash = UploadLedger.compute_sha256(video_path)
        ist = pytz.timezone(settings.PUBLISH_TIMEZONE)
        now_ist = datetime.now(ist)
        hrs, mins = map(int, scheduled_publish_time_ist.split(":"))
        base_dt = target_date or now_ist
        scheduled_ist = ist.localize(datetime(
            year=base_dt.year, month=base_dt.month, day=base_dt.day, hour=hrs, minute=mins, second=0
        ))
        # Use scheduled publishAt ONLY if it is safely (>15 min) in the future; otherwise publish public immediately
        # so delayed wakeups or close-to-slot daemon runs never fail with YouTube 400 invalidPublishAt.
        use_scheduled_publish = simulate_upload or (scheduled_ist > now_ist + timedelta(minutes=15))
        rfc3339_publish_at = scheduled_ist.astimezone(pytz.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        has_thumb = bool(thumbnail_path and thumbnail_path.exists())
        has_subs = bool(subtitles_path and subtitles_path.exists() and subtitles_path.stat().st_size > 0)

        status_block: Dict[str, Any] = {
            "privacyStatus": "private" if use_scheduled_publish else "public",
            "selfDeclaredMadeForKids": False,
        }
        if use_scheduled_publish:
            status_block["publishAt"] = rfc3339_publish_at

        # Standard YouTube API v3 request body
        body = {
            "snippet": {
                "title": metadata["title_hindi"],
                "description": metadata["description_hindi"],
                "tags": metadata["tags"],
                "categoryId": metadata.get("category_id", "27")
            },
            "status": status_block,
        }

        if simulate_upload:
            simulated_yt_id = f"yt_sim_{uuid.uuid4().hex[:8]}"
            return {
                "success": True,
                "simulated": True,
                "youtube_video_id": simulated_yt_id,
                "youtube_url": f"https://www.youtube.com/watch?v={simulated_yt_id}",
                "file_sha256": file_hash,
                "privacy_status": "private",
                "scheduled_publish_at_utc": rfc3339_publish_at,
                "scheduled_publish_at_ist": f"{scheduled_publish_time_ist} IST",
                "uploaded_at": datetime.utcnow().isoformat(),
                "has_thumbnail": has_thumb,
                "has_subtitles": has_subs,
                "subtitles_uploaded": False
            }

        # Live upload requested: fail closed if credentials are missing or API fails
        if not self.is_live_configured():
            return {
                "success": False,
                "simulated": False,
                "error": "Live YouTube upload requested, but valid OAuth credentials (YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_REFRESH_TOKEN) are not configured.",
                "file_sha256": file_hash,
                "has_thumbnail": has_thumb,
                "has_subtitles": has_subs,
                "subtitles_uploaded": False
            }

        try:
            live_res = await asyncio.to_thread(
                self._execute_live_upload_sync,
                video_path,
                thumbnail_path,
                subtitles_path,
                body,
            )
            video_id = live_res["video_id"]
            privacy_final = "private" if use_scheduled_publish else "public"
            return {
                "success": True,
                "simulated": False,
                "youtube_video_id": video_id,
                "youtube_url": f"https://youtube.com/shorts/{video_id}" if privacy_final == "public" else f"https://www.youtube.com/watch?v={video_id}",
                "file_sha256": file_hash,
                "privacy_status": privacy_final,
                "scheduled_publish_at_utc": rfc3339_publish_at if use_scheduled_publish else None,
                "scheduled_publish_at_ist": f"{scheduled_publish_time_ist} IST" if use_scheduled_publish else "Immediate Public",
                "uploaded_at": datetime.utcnow().isoformat(),
                "has_thumbnail": has_thumb,
                "thumbnail_uploaded": live_res["thumbnail_uploaded"],
                "thumbnail_error": live_res["thumbnail_error"],
                "has_subtitles": has_subs,
                "subtitles_uploaded": live_res["subtitles_uploaded"],
                "subtitles_error": live_res["subtitles_error"],
            }
        except Exception as e:
            return {
                "success": False,
                "simulated": False,
                "error": f"YouTube live upload failed: {str(e)}",
                "file_sha256": file_hash,
                "has_thumbnail": has_thumb,
                "has_subtitles": has_subs,
                "subtitles_uploaded": False
            }
