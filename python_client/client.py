import requests


class Version:
    def __init__(self, major=1, minor=0, micro=0):
        """
        Tests:
            >>> Version(1, -2, 0)
            Traceback (most recent call last):
            ValueError: invalid number, must be positive
        """
        self.major = major
        self.minor = minor
        self.micro = micro
        if major < 0 or minor < 0 or micro < 0:
            raise ValueError('invalid number, must be positive')

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


class DownloadArtifactError(Exception):
    pass


class DeleteArtifactError(Exception):
    pass


class Client:
    # TODO credentials as argument, passed in Jenkins
    credentials = ('justyna.guzik11@gmail.com',
                   'cmVmdGtuOjAxOjE3MTMxMDMxMzA6V2ZMSHpYeVc1RExVUVJoZFFnVUJVTzZ5dVND')

    @staticmethod
    def download_specific(filename: str):
        url = 'https://jguzik.jfrog.io/artifactory/generic-local/' + filename
        r = requests.get(url, auth=Client.credentials)

        if not 199 < r.status_code < 300:
            raise DownloadArtifactError

        with open(filename, 'wb') as f:
            f.write(r.content)

    @staticmethod
    def download_latest():
        url = 'https://jguzik.jfrog.io/artifactory/api/storage/generic-local'
        r = requests.get(url, auth=Client.credentials)

        #  parse the response
        file_list = r.json()['children']
        current_latest = Version(0, 0, 0)
        for file in file_list:
            filename = file['uri'].lstrip('/file_').rstrip('.json')
            numbers = [int(num) for num in filename.split('.')]
            if current_latest < (current := Version(numbers[0], numbers[1], numbers[2])):
                current_latest = current
        latest_filename = 'file_' + str(current_latest) + '.json'
        Client.download_specific(latest_filename)

    @staticmethod
    def upload_new(filename: str):
        url = 'https://jguzik.jfrog.io/artifactory/generic-local/' + filename
        r = requests.put(url, data=open(filename, 'rb'), auth=Client.credentials)

    @staticmethod
    def delete_specific(filename: str):
        url = 'https://jguzik.jfrog.io/artifactory/generic-local/' + filename
        r = requests.delete(url, auth=Client.credentials)
        if not 199 < r.status_code < 300:
            raise DeleteArtifactError


python_client = Client()
# python_client.download_specific('file_1.0.1.json')
python_client.upload_new('file_1.0.2.json')
python_client.download_latest()
# python_client.delete_specific('file_1.0.2.json')
