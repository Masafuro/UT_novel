"""Template Registry for discovering and instantiating dialogue templates."""
from typing import Dict, Type, List, Optional
from ut_novel.templates.base import BaseTemplate

class TemplateRegistry:
    """Registry managing available dialogue templates."""
    _registry: Dict[str, Type[BaseTemplate]] = {}
    _instances: Dict[str, BaseTemplate] = {}

    @classmethod
    def register(cls, template_cls: Type[BaseTemplate]):
        """Register a new template class."""
        # Instantiate temporarily to read the name, or require class attribute
        instance = template_cls()
        name = instance.name
        cls._registry[name] = template_cls
        cls._instances[name] = instance
        return template_cls

    @classmethod
    def get(cls, name: str) -> BaseTemplate:
        """
        Retrieve a registered template instance by name.
        Raises KeyError if not found.
        """
        if name not in cls._instances:
            if name in cls._registry:
                cls._instances[name] = cls._registry[name]()
            else:
                available = ", ".join(cls._registry.keys())
                raise KeyError(f"Template '{name}' not found. Available templates: [{available}]")
        return cls._instances[name]

    @classmethod
    def list_templates(cls) -> List[str]:
        """List names of all registered templates."""
        return list(cls._registry.keys())

    @classmethod
    def has(cls, name: str) -> bool:
        """Check if a template exists."""
        return name in cls._registry

