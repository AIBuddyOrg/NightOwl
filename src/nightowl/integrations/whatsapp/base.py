from abc import ABC, abstractmethod


class WhatsAppAdapter(ABC):
    @abstractmethod
    def send_message(self, wa_id: str, message: str) -> str:
        raise NotImplementedError
