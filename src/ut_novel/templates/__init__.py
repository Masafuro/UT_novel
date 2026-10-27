"""Template module for UT_novel."""
from ut_novel.templates.base import BaseTemplate
from ut_novel.templates.registry import TemplateRegistry

# Import built-in templates so they register themselves
from ut_novel.templates.undertale_16_9 import Undertale16x9Template
from ut_novel.templates.undertale_9_16 import Undertale9x16Template
from ut_novel.templates.r4_16_9 import R4_16x9_Template
from ut_novel.templates.r4_9_16 import R4_9x16_Template

__all__ = [
    "BaseTemplate",
    "TemplateRegistry",
    "Undertale16x9Template",
    "Undertale9x16Template",
    "R4_16x9_Template",
    "R4_9x16_Template",
]
