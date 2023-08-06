# -*- coding: utf-8 -*-

import ast

from wemake_python_styleguide.constants import BAD_MAGIC_METHODS
from wemake_python_styleguide.violations.best_practices import (
    BadMagicMethodViolation,
    StaticMethodViolation,
)
from wemake_python_styleguide.violations.consistency import (
    RequiredBaseClassViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


class WrongClassVisitor(BaseNodeVisitor):
    """
    This class is responsible for restricting some ``class`` antipatterns.

    Here we check for stylistic issues and design patterns.
    """

    def _check_decorators(self, node: ast.FunctionDef) -> None:
        for decorator in node.decorator_list:
            decorator_name = getattr(decorator, 'id', None)
            if decorator_name == 'staticmethod':
                self.add_violation(StaticMethodViolation(node))

    def _check_magic_methods(self, node: ast.FunctionDef) -> None:
        if node.name in BAD_MAGIC_METHODS:
            self.add_violation(BadMagicMethodViolation(node, text=node.name))

    def _check_base_class(self, node: ast.ClassDef) -> None:
        if len(node.bases) == 0:
            self.add_violation(RequiredBaseClassViolation(node, text=node.name))

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """
        Checking class definitions.

        Used to find:
        1. Base class violations

        Raises:
            RequiredBaseClassViolation

        """
        self._check_base_class(node)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """
        Checking class methods.

        Used to find:
        1. `@staticmethod` decorators
        2. Detect forbiden magic methods

        Raises:
            StaticMethodViolation
            BadMagicMethodViolation

        """
        self._check_decorators(node)
        self._check_magic_methods(node)
        self.generic_visit(node)
