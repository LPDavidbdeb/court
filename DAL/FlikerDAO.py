# flickr_dao.py

import flickrapi
from datetime import datetime
import pickle
import os
from dateutil.parser import parse


class FlickrDAO:
    def __init__(self, account_name, config, cache_dir="DL/photos/Flickrs"):
        self.account_name = account_name
        self.api_key = config['api_key']
        self.api_secret = config['api_secret']
        self.user_id = config['user_id']
        self.token_cache_file = config['token_cache_file']
        self.flickr = flickrapi.FlickrAPI(self.api_key, self.api_secret, format='parsed-json', token_cache_location=self.token_cache_file)
        self._authenticate()
        self.cache_dir

    def _authenticate(self):
        if not self.flickr.token_valid():
            self.flickr.get_request_token(oauth_callback='oob')
            authorize_url = self.flickr.auth_url(perms='read')
            print(f"Visit this URL to authorize '{self.account_name}':\n{authorize_url}")
            verifier = input("Verifier code: ").strip()
            self.flickr.get_access_token(verifier)

    def list_albums(self):
        response = self.flickr.photosets.getList(user_id=self.user_id)
        return response['photosets']['photoset']

    def get_album_photos(self, album_title: str) -> list[dict]:
        albums = self.list_albums()
        album_id = next((a['id'] for a in albums if a['title']['_content'] == album_title), None)
        if not album_id:
            raise ValueError(f"Album '{album_title}' not found")

        photo_list = self.flickr.photosets.getPhotos(
            user_id=self.user_id,
            photoset_id=album_id
        )['photoset']['photo']

        photo_data_list = []

        for photo in photo_list:
            photo_id = photo['id']
            secret = photo['secret']

            sizes = self.flickr.photos.getSizes(photo_id=photo_id)
            info = self.flickr.photos.getInfo(photo_id=photo_id, secret=secret)

            photo_data_list.append({
                'photo_id': photo_id,
                'sizes': sizes,
                'info': info
            })

        return photo_data_list

    def save_data(self, data: dict):
        """Save data dictionary as a pickle file named by account and current date."""
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"{self.account_name}_{date_str}.pkl"
        file_path = os.path.join(self.cache_dir, filename)
        with open(file_path, "wb") as f:
            pickle.dump(data, f)
        print(f"Saved API data to cache file: {file_path}")
        return file_path