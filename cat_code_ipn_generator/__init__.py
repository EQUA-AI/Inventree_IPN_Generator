# -*- coding: utf-8 -*-
"""Category-Based IPN Generator Plugin for InvenTree

Automatically generates Internal Part Numbers (IPNs) based on
category metadata containing category codes and sequential numbering.
"""

from .core import CategoryIPNGeneratorPlugin

__version__ = "1.0.0"
__all__ = ['CategoryIPNGeneratorPlugin']
