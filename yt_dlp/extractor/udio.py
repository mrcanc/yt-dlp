import re

from .common import InfoExtractor


class UdioIE(InfoExtractor):
    IE_NAME = 'udio'
    _VALID_URL = r'https?://(?:www\.)?udio\.com/(?:songs)/(?P<id>[0-9a-fA-F-]{36}|[0-9a-zA-Z]{22})'
    _TESTS = [{
        'url': 'https://www.udio.com/songs/0a39b334-ab82-48b7-9693-eafd55e70a9d',
        'info_dict': {
            'id': '0a39b334-ab82-48b7-9693-eafd55e70a9d',
            'ext': 'mp3',
            'title': 'MrTomMusic - I Let You Drown | Udio',
            'description': 'Listen to I Let You Drown by MrTomMusic on Udio. Discover, create, and share music with the world. Use the latest technology to create AI music in seconds.',
            'duration': 281,
            'thumbnail': 'https://imagedelivery.net/C9yUr1FL21Q6JwfYYh2ozQ/69996f61-a2f9-401e-15dd-059a5eea2f00/public',
        },
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        return {
            'id': video_id,
            'title': self._og_search_title(webpage),
            'description': self._og_search_description(webpage),
            'thumbnail': self._og_search_thumbnail(webpage),
            'duration': int(self._html_search_regex(r'\\"duration\\":\s*(\d+)', webpage, 'duration')),
            'formats': [
                {'url': self._html_search_meta('og:audio:url', webpage)},
                {'url': self._html_search_meta('og:video:url', webpage)},
            ],
        }


class UdioPlaylistIE(InfoExtractor):
    IE_NAME = 'udio:playlist'
    _VALID_URL = r'https?://(?:www\.)?udio\.com/playlists/(?P<id>[0-9a-zA-Z-]+)'
    _TESTS = [{
        'url': 'https://www.udio.com/playlists/dfHRrAzNtjroBg1Au5GTQ3',
        'info_dict': {
            'id': 'dfHRrAzNtjroBg1Au5GTQ3',
            'title': 'Reflections by DonTheMusic | Udio',
            'description': 'Listen to Reflections by DonTheMusic on Udio. Discover, create, and share music with the world. Use the latest technology to create AI music in seconds.',
        },
        'playlist_count': 16,
    }]

    def _real_extract(self, url):
        playlist_id = self._match_id(url)
        webpage = self._download_webpage(url, playlist_id)

        match_entries = self._search_regex(r'\\"song_list\\":\[(.*?)\]', webpage, 'match_entries')

        entries = [
            self.url_result(
                f'https://udio.com/songs/{video_id}',
                ie=UdioIE,
                video_id=video_id,
            )
            for video_id in re.findall(r'\\"(.*?)\\"', match_entries)
        ]

        return self.playlist_result(
            entries=entries,
            playlist_id=playlist_id,
            playlist_title=self._og_search_title(webpage),
            playlist_description=self._og_search_description(webpage),
        )
