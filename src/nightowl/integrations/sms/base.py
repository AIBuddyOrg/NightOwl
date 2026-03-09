from abc import ABC, abstractmethod


class SMSAdapter(ABC):
    @abstractmethod
    def send(self, recipient: str, message: str) -> str:
        raise NotImplementedError
