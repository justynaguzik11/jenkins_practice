import requests


class Version:
    def __init__(self, major=1, minor=0, micro=0):
        self.major = major
        self.minor = minor
        self.micro = micro

    def __str__(self):
        """
        Tests:
            >>> str(Version(1, 2, 0))
            '1.2.0'
        """
        return f'{self.major}.{self.minor}.{self.micro}'

    def __gt__(self, other):
        """
        Tests:
            >>> Version(1, 2, 0) > Version(1, 1, 0)
            True
            >>> Version(1, 1, 1) > Version(1, 1, 0)
            True
            >>> Version(2, 1, 1) > Version(1, 1, 10)
            True
            >>> Version(2, 1, 0) > Version(2, 1, 1)
            False
        """
        if isinstance(other, Version):
            if self.major != other.major:
                return self.major > other.major
            if self.minor != other.minor:
                return self.minor > other.minor
            return self.micro > other.micro
        else:
            raise TypeError('wrong type')


class Client:
    @staticmethod
    def download_specific(filename: str):
        url = 'https://jguzik.jfrog.io/artifactory/generic-local/' + filename
        credentials = ('justyna.guzik11@gmail.com',
                       'cmVmdGtuOjAxOjE3MTMxMDMxMzA6V2ZMSHpYeVc1RExVUVJoZFFnVUJVTzZ5dVND')
        r = requests.get(url, auth=credentials)
        print(r.json())

        with open(filename, 'wb') as f:
            f.write(r.content)

    @staticmethod
    def download_latest():
        url = 'https://jguzik.jfrog.io/artifactory/api/storage/generic-local'
        credentials = ('justyna.guzik11@gmail.com',
                       'cmVmdGtuOjAxOjE3MTMxMDMxMzA6V2ZMSHpYeVc1RExVUVJoZFFnVUJVTzZ5dVND')
        r = requests.get(url, auth=credentials)

        #  parse the response
        file_list = r.json()['children']
        current_latest = Version(0, 0, 0)
        for file in file_list:
            filename = file['uri']
            filename = filename.lstrip('/file_').rstrip('.json')
            numbers = [int(num) for num in filename.split('.')]
            current_latest = max(current_latest, Version(numbers[0], numbers[1], numbers[2]))
        print(current_latest)
        #  download_specific(latest)

    @staticmethod
    def upload_new(filename='file'):
        filename += '_1.0.2.json'
        url = 'https://jguzik.jfrog.io/artifactory/generic-local/' + filename
        credentials = ('justyna.guzik11@gmail.com',
                       'cmVmdGtuOjAxOjE3MTMxMDMxMzA6V2ZMSHpYeVc1RExVUVJoZFFnVUJVTzZ5dVND')
        r = requests.put(url, filename, auth=credentials)
        print(r.text)


python_client = Client()
# python_client.download_specific('file_1.0.0.json')
python_client.download_latest()
# python_client.upload_new('file')
