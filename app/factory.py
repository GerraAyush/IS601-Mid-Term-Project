from typing import Type, Dict, Any


class FactoryBase:
    _item_dict: Dict[str, Dict[str, Any]] = {}
    _base_class: Type = object

    @classmethod
    def is_registered(cls, name: str) -> bool:
        return name.lower() in cls._item_dict

    @classmethod
    def register(
        cls, 
        name: str, 
        item_class: Type, 
        description: str
    ) -> None:
        if not issubclass(item_class, cls._base_class):
            raise TypeError(f"Item class must inherit from {cls._base_class.__name__}")
        cls._item_dict[name.lower()] = {"_cls": item_class, "desc": description}

    @classmethod
    def create(cls, name: str, **kwargs) -> Any:
        info = cls._item_dict.get(name.lower())
        if not info:
            raise ValueError(f"Unregistered item: {name}")
        return info["_cls"](**kwargs)

    @classmethod
    def list_items(cls) -> str:
        display_string = ""
        for name, info in cls._item_dict.items():
            display_string += f"  {name} - {info['desc']}\n"
        return display_string.rstrip()
