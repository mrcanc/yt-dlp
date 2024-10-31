import re

from .common import InfoExtractor
from ..utils import (
    ExtractorError,
    RegexNotFoundError,
)


class SunoIE(InfoExtractor):
    IE_NAME = 'suno'
    _VALID_URL = r'https?://(?:www\.)?(?:app\.)?suno\.(?:com|ai)/(?:song|embed)/(?P<id>[0-9a-fA-F-]{36})'
    _TESTS = [{
        'url': 'https://suno.com/song/b540d8ca-ea46-4e63-8f3f-ab526e20eae9',
        'info_dict': {
            'id': 'b540d8ca-ea46-4e63-8f3f-ab526e20eae9',
            'ext': 'mp3',
            'title': 'You took my truck (ft. Foggy X) by @eviltyromancer | Suno',
            'description': 'sad trucker country, singer songwriter, anguished male trucker vocals song. Listen and make your own with Suno.',
            'duration': 143,
            'thumbnail': 'https://cdn2.suno.ai/b540d8ca-ea46-4e63-8f3f-ab526e20eae9_b4fe467a.jpeg',
        },
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        try:
            if self._html_search_regex(r'\\"is_video_pending\\":\s*(\w+)', webpage, 'is_video_pending') == 'true':
                raise ExtractorError('Video is pending and not yet available', expected=True)
        except RegexNotFoundError:
            pass

        return {
            'id': video_id,
            'title': self._og_search_title(webpage),
            'description': self._og_search_description(webpage),
            'thumbnail': self._og_search_thumbnail(webpage),
            'duration': int(self._html_search_regex(r'\\"duration\\":\s*(\d+)', webpage, 'duration')),
            'formats': [{'url': self._html_search_meta('og:audio', webpage)}, {'url': self._html_search_meta('og:video:url', webpage)}],
        }


class SunoPlaylistIE(InfoExtractor):
    IE_NAME = 'suno:playlist'
    _VALID_URL = r'https?://(?:www\.)?suno\.com/playlist/(?P<id>[0-9a-fA-F-]{36})'
    _TESTS = [{
        'url': 'https://suno.com/playlist/43b18060-512e-4c9d-9813-d9bd8ff5c61f',
        'info_dict': {
            'id': '43b18060-512e-4c9d-9813-d9bd8ff5c61f',
            'title': 'Good song by @inimitablebluegrass722 | Suno',
        },
        'playlist_count': 34,
    }]

    def _real_extract(self, url):
        playlist_id = self._match_id(url)
        webpage = self._download_webpage(url, playlist_id)

        entries = [
            self.url_result(
                f'https://suno.com/song/{video_id}',
                ie=SunoIE,
                video_id=video_id)
            for video_id in re.findall(r'data\-clip\-id="([0-9a-fA-F-]{36})"', webpage)
        ]

        return self.playlist_result(
            entries=entries,
            playlist_id=playlist_id,
            playlist_title=self._og_search_title(webpage),
        )
