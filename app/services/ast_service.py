import json
from typing import List, Dict, Any, Union, Optional


class Node:
    """
    Represents a node in an abstract syntax tree (AST).

    Each node can be an operator (AND, OR) or an operand, and can have left and right child nodes.
    """

    def __init__(self, type: str, value: str, left: Optional['Node'] = None, right: Optional['Node'] = None):
        """
        Initializes a new instance of the Node class.

        Args:
            type (str): The type of the node ('operator' or 'operand').
            value (str): The value of the node (operator symbol or operand expression).
            left (Optional[Node]): The left child node.
            right (Optional[Node]): The right child node.
        """
        self.type = type
        self.value = value
        self.left = left
        self.right = right

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the node and its children into a dictionary representation.

        Returns:
            Dict[str, Any]: A dictionary representing the node and its children.
        """
        return {
            'type': self.type,
            'value': self.value,
            'left': self.left.to_dict() if self.left else None,
            'right': self.right.to_dict() if self.right else None
        }

    @classmethod
    def from_dict(cls, data: Optional[Dict[str, Any]]) -> Optional['Node']:
        """
        Creates a Node instance from a dictionary representation.

        Args:
            data (Optional[Dict[str, Any]]): The dictionary representation of a node.

        Returns:
            Optional[Node]: A Node instance or None if the input data is None.
        """
        if data is None:
            return None
        return cls(
            type=data['type'],
            value=data['value'],
            left=cls.from_dict(data['left']),
            right=cls.from_dict(data['right'])
        )


class ASTService:
    """
    Provides services for parsing rule strings into ASTs, combining ASTs, and evaluating ASTs against data.
    """

    def parse_rule_string(self, rule_string: str) -> str:
        """
        Parses a rule string into an AST and returns its JSON representation.

        Args:
            rule_string (str): The rule string to be parsed.

        Returns:
            str: The JSON representation of the parsed AST.
        """
        tokens = rule_string.replace('(', ' ( ').replace(')', ' ) ').split()

        def parse_expression():
            stack = [[]]
            for token in tokens:
                if token == '(':
                    stack.append([])
                elif token == ')':
                    expr = stack.pop()
                    stack[-1].append(expr)
                elif token in ['AND', 'OR']:
                    stack[-1].append(token)
                else:
                    stack[-1].append(token)

            def build_tree(expr):
                if isinstance(expr, List):
                    if len(expr) == 1:
                        return build_tree(expr[0])
                    elif 'OR' in expr:
                        idx = expr.index('OR')
                        return Node('operator', 'OR', build_tree(expr[:idx]), build_tree(expr[idx + 1:]))
                    elif 'AND' in expr:
                        idx = expr.index('AND')
                        return Node('operator', 'AND', build_tree(expr[:idx]), build_tree(expr[idx + 1:]))
                return Node('operand', ' '.join(expr))

            return build_tree(stack[0])

        ast = parse_expression()
        return json.dumps(ast.to_dict())

    def combine_asts(self, asts: List[str]) -> str:
        """
        Combines multiple ASTs into a single AST with AND operator.

        Args:
            asts (List[str]): A list of JSON representations of ASTs to be combined.

        Returns:
            str: The JSON representation of the combined AST.
        """
        parsed_asts = [Node.from_dict(json.loads(ast)) for ast in asts]
        combined_ast = parsed_asts[0]
        for ast in parsed_asts[1:]:
            combined_ast = Node('operator', 'AND', combined_ast, ast)
        return json.dumps(combined_ast.to_dict())

    def evaluate_ast(self, ast: str, data: Dict[str, Any]) -> bool:
        """
        Evaluates an AST against provided data.

        Args:
            ast (str): The JSON representation of the AST.
            data (Dict[str, Any]): The data against which the AST is to be evaluated.

        Returns:
            bool: The result of the AST evaluation.
        """

        def evaluate_node(node: Node) -> bool:
            if node.type == 'operator':
                if node.value == 'AND':
                    return evaluate_node(node.left) and evaluate_node(node.right)
                elif node.value == 'OR':
                    return evaluate_node(node.left) or evaluate_node(node.right)
            elif node.type == 'operand':
                left, op, right = node.value.split()
                left_value = data.get(left)
                right_value = int(right) if right.isdigit() else right.strip("'")
                if op == '>':
                    return left_value > right_value
                elif op == '<':
                    return left_value < right_value
                elif op == '=':
                    return left_value == right_value
            return False

        parsed_ast = Node.from_dict(json.loads(ast))
        return evaluate_node(parsed_ast)
