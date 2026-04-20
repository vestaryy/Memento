import requests
import datetime
from datetime import timedelta

class YandexDiskManager:
    def __init__(self, token):
        self.token = token
        self.headers = {"Authorization": f"OAuth {self.token}"}
        self.base_url = "https://cloud-api.yandex.net/v1/disk/resources"

    def create_folder(self, path):
        params = {"path": path}
        response = requests.put(self.base_url, headers=self.headers, params=params)
        return response.status_code in [201, 409]

    def upload_file(self, path_on_disk, file_bytes):
        try:
            params = {"path": path_on_disk, "overwrite": "true"}
            res = requests.get(f"{self.base_url}/upload", headers=self.headers, params=params)
            
            if res.status_code != 200:
                return False
                
            upload_url = res.json().get("href")
            
            upload_res = requests.put(upload_url, data=file_bytes)
            return upload_res.status_code == 201
        except Exception as e:
            return False

    def sync_all(self, memories, db_sess):
        updated = False
        for item in memories:
            if not item.has_valid_cache():
                params = {"path": item.yandex_path}
                res = requests.get(f"{self.base_url}/download", headers=self.headers, params=params)
                if res.status_code == 200:
                    item.cached_url = res.json().get("href")
                    item.url_expires = datetime.datetime.now() + timedelta(minutes=30)
                    updated = True
        if updated:
            db_sess.commit()