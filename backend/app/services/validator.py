import ast
from typing import List, Tuple
from app.domain.models import ValidationResult

class ValidationService:
    def validate_code(self, code: str) -> ValidationResult:
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return ValidationResult(
                is_valid=False,
                errors=[f"Syntax Error: {str(e)}"]
            )

        errors = []
        has_test_class = False
        has_test_method = False
        has_allure_decorator = False

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if "Test" in node.name or "Tests" in node.name:
                    has_test_class = True
                
                for decorator in node.decorator_list:
                    if self._is_allure_decorator(decorator):
                        has_allure_decorator = True

            if isinstance(node, ast.FunctionDef):
                if node.name.startswith("test_"):
                    has_test_method = True
                for decorator in node.decorator_list:
                    if self._is_allure_decorator(decorator):
                        has_allure_decorator = True

        if not has_test_class:
            errors.append("Missing Test Class (must contain 'Test' in name)")
        if not has_test_method:
            errors.append("Missing Test Method (must start with 'test_')")
        if not has_allure_decorator:
            errors.append("Missing @allure decorators")

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            fixed_code=None
        )

    def _is_allure_decorator(self, node: ast.AST) -> bool:
        if isinstance(node, ast.Call):
            return self._is_allure_decorator(node.func)
        
        if isinstance(node, ast.Attribute):
            if isinstance(node.value, ast.Name) and node.value.id == "allure":
                return True
        
        return False
