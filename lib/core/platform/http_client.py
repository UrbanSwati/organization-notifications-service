from dataclasses import  dataclass
from abc import ABC, abstractmethod
from typing import Dict, Optional, Union, List


@dataclass
class Response:
    status: int

    def json(self) -> Union[Dict, List]:
        pass


class HTTPClient(ABC):

    @abstractmethod
    async def get(self, url: str, headers: Optional[Dict] = None, timeout: int = 10) -> Response:
        pass
