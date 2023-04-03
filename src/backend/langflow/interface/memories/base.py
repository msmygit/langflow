from typing import Dict, List

from langflow.interface.base import LangChainTypeCreator
from langflow.interface.custom_lists import memory_type_to_cls_dict
from langflow.settings import settings
from langflow.utils.util import build_template_from_class


class MemoryCreator(LangChainTypeCreator):
    type_name: str = "memories"

    @property
    def type_to_loader_dict(self) -> Dict:
        if self.type_dict is None:
            self.type_dict = memory_type_to_cls_dict
        return self.type_dict

    def get_signature(self, name: str) -> Dict | None:
        """Get the signature of a memory."""
        try:
            return build_template_from_class(name, memory_type_to_cls_dict)
        except ValueError as exc:
            raise ValueError("Memory not found") from exc

    def to_list(self) -> List[str]:
        return [
            memory.__name__
            for memory in self.type_to_loader_dict.values()
            if memory.__name__ in settings.memories or settings.dev
        ]


memory_creator = MemoryCreator()