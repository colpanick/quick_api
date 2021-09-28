from abc import ABC, abstractmethod


class Base(ABC):
    @abstractmethod
    def datasets(self):
        pass

    @abstractmethod
    def get_all(self, dataset, sort=None, order=None):
        pass

    @abstractmethod
    def get_record(self, dataset, record_id):
        pass

    @abstractmethod
    def post(self, dataset, data):
        pass

    @abstractmethod
    def put(self, dataset, record_id, data):
        pass

    @abstractmethod
    def patch(self, dataset, record_id, data):
        pass

    @abstractmethod
    def delete(self, dataset, record_id):
        pass
