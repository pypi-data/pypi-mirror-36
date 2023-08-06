# -*- coding: utf-8 -*-

"""
These rules checks ``import`` statements to be defined correctly.

Note:

    Explicit is better than implicit.
    Flat is better than nested.
    Sparse is better than dense.
    Readability counts.

"""

from wemake_python_styleguide.errors.base import ASTStyleViolation


class LocalFolderImportViolation(ASTStyleViolation):
    """
    Forbids to have imports relative to the current folder.

    Reasoning:
        We should pick one style and stick to it.
        We have decided to use the explicit one.

    Example::

        # Correct:
        from my_package.version import get_version

        # Wrong:
        from .version import get_version
        from ..drivers import MySQLDriver

    Note:
        Returns Z100 as error code

    """

    #: Error message shown to the user.
    error_template = 'Found local folder import "{0}"'
    code = 100


class NestedImportViolation(ASTStyleViolation):
    """
    Forbids to have nested imports in functions.

    Reasoning:
        Usually nested imports are used to fix the import cycle.
        So, nested imports show that there's an issue with you design.

    Solution:
        You don't need nested imports, you need to refactor your code.
        Introduce a new module, a find another way to do what you want to do.
        Rething how your layered architecture should look like.

    Example::

        # Correct:
        from my_module import some_function

        def some(): ...

        # Wrong:
        def some():
            from my_module import some_function

    See also:
        https://github.com/seddonym/layer_linter

    Note:
        Returns Z101 as error code

    """

    #: Error message shown to the user.
    error_template = 'Found nested import "{0}"'
    code = 101


class FutureImportViolation(ASTStyleViolation):
    """
    Forbids to use ``__future__`` imports.

    Reasoning:
        Almost all ``__future__`` imports are legacy ``python2`` compatibility
        tools that are no longer required.

    Solution:
        Remove them. Drop ``python2`` support.

    Except, there are some new ones for ``python4`` support.
    See
    :py:data:`~wemake_python_styleguide.constants.FUTURE_IMPORTS_WHITELIST`
    for the full list of allowed future imports.

    Example::

        # Correct:
        from __future__ import annotations

        # Wrong:
        from __future__ import print_function

    Note:
        Returns Z102 as error code

    """

    #: Error message shown to the user.
    error_template = 'Found future import "{0}"'
    code = 102


class DottedRawImportViolation(ASTStyleViolation):
    """
    Forbids to use imports like ``import os.path``.

    Reasoning:
        We should pick one style and stick to it.
        We have decided to use the readable one.

    Example::

        # Correct:
        from os import path

        # Wrong:
        import os.path

    Note:
        Returns Z103 as error code

    """

    #: Error message shown to the user.
    error_template = 'Found dotted raw import "{0}"'
    code = 103


class SameAliasImportViolation(ASTStyleViolation):
    """
    Forbids to use the same alias as the original name in imports.

    Reasoning:
        Why would you even do this in the first place?

    Example::

        # Correct:
        from os import path

        # Wrong:
        from os import path as path

    Note:
        Returns Z104 as error code

    """

    #: Error message shown to the user.
    error_template = 'Found same alias import "{0}"'
    code = 104
