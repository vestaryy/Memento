import requests

class YandexDisk:
    def __init__(self, token):
        self.token = token
        self.headers = {'Authorization': f'OAuth {self.token}'}
        self.base_url = 'https://cloud-api.yandex.net/v1/disk/resources'

    def create_folder(self, path):
        params = {'path': path}
        res = requests.put(self.base_url, headers=self.headers, params=params)
        return res.status_code in (201, 409)

    def upload_bytes(self, disk_path, file_bytes):
        
        upload_endpoint = f"{self.base_url}/upload"
        params = {'path': disk_path, 'overwrite': 'true'}
        
        res = requests.get(upload_endpoint, headers=self.headers, params=params)
        if res.status_code != 200:
            print(f"Ошибка получения ссылки: {res.json().get('message')}")
            return False
            
        href = res.json().get('href')
        
        upload_res = requests.put(href, data=file_bytes)
        
        return upload_res.status_code == 201

    def get_download_link(self, disk_path):
        download_endpoint = f"{self.base_url}/download"
        params = {'path': disk_path}
        
        res = requests.get(download_endpoint, headers=self.headers, params=params)
        if res.status_code == 200:
            return res.json().get('href')
        return None