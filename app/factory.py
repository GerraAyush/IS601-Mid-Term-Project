# Datatypes
from typing import Type, Dict, Any


class FactoryBase:
    """
    Base factory class for registering, creating, and listing items dynamically.

    This class allows subclasses to register item classes with a string key
    and a description, then create instances dynamically using the key.
    
    Attributes:
        _item_dict (Dict[str, Dict[str, Any]]): Stores registered items with their
            class reference and description.
        _base_class (Type): Ensures all registered classes inherit from this base class.
    """

    _item_dict: Dict[str, Dict[str, Any]] = {}
    _base_class: Type = object

    @classmethod
    def is_registered(cls, name: str) -> bool:
        """
        Check if a given name is registered in the factory.
        
        Args:
            name (str): The name of the item to check.
        
        Returns:
            bool: True if registered, False otherwise.
        """
        return name.lower() in cls._item_dict

    @classmethod
    def register(
        cls, 
        name: str, 
        item_class: Type, 
        description: str
    ) -> None:
        """
        Register a new class in the factory.
        
        Args:
            name (str): Key to register the class under.
            item_class (Type): Class to register.
            description (str): Human-readable description of the class.
        
        Raises:
            TypeError: If `item_class` does not inherit from `_base_class`.
        """
        if not issubclass(item_class, cls._base_class):
            raise TypeError(f"Item class must inherit from {cls._base_class.__name__}")
        cls._item_dict[name.lower()] = {"_cls": item_class, "desc": description}

    @classmethod
    def create(cls, name: str, **kwargs) -> Any:
        """
        Create an instance of a registered class using its name.
        
        Args:
            name (str): Name of the registered item.
            **kwargs: Any keyword arguments to pass to the class constructor.
        
        Returns:
            Any: An instance of the registered class.
        
        Raises:
            ValueError: If the name is not registered.
        """
        info = cls._item_dict.get(name.lower())
        if not info:
            raise ValueError(f"Unregistered item: {name}")
        return info["_cls"](**kwargs)

    @classmethod
    def list_items(cls) -> str:
        """
        Return a formatted string listing all registered items and their descriptions.
        
        Returns:
            str: List of registered items.
        """
        display_string = ""
        for name, info in cls._item_dict.items():
            display_string += f"  {name} - {info['desc']}\n"
        return display_string.rstrip()
