"""
Lang Ada AST 节点实现
"""

from dataclasses import dataclass
from typing import Union, List, Optional, Any
from abc import ABC, abstractmethod


class Node(ABC):
    """AST 节点基类"""
    def __init__(self, line: int, column: int):
        self.line = line      # 行号
        self.column = column  # 列号
    
    @abstractmethod
    def accept(self, visitor):
        """访问者模式支持"""
        pass


# 表达式类型的前向声明
class Expression(Node):
    """表达式基类"""
    pass


class Statement(Node):
    """语句基类"""
    pass


# ===== 字面量节点 =====

@dataclass
class NumberLiteral(Expression):
    """数字字面量"""
    value: Union[int, float]
    line: int = 0
    column: int = 0
    
    def accept(self, visitor):
        return visitor.visit_number_literal(self)


@dataclass
class StringLiteral(Expression):
    """字符串字面量"""
    value: str
    line: int = 0
    column: int = 0
    
    def accept(self, visitor):
        return visitor.visit_string_literal(self)


@dataclass
class BooleanLiteral(Expression):
    """布尔字面量"""
    value: bool
    line: int = 0
    column: int = 0
    
    def accept(self, visitor):
        return visitor.visit_boolean_literal(self)


# ===== 表达式节点 =====

@dataclass
class BinaryExpression(Expression):
    """二元表达式"""
    left: Expression
    operator: str  # '+', '-', '*', '/', '==', '!=', '<', '>', '<=', '>='
    right: Expression
    line: int = 0
    column: int = 0
    
    def accept(self, visitor):
        return visitor.visit_binary_expression(self)


@dataclass
class UnaryExpression(Expression):
    """一元表达式"""
    operator: str  # '+', '-', '!', 'not'
    operand: Expression
    line: int = 0
    column: int = 0
    
    def accept(self, visitor):
        return visitor.visit_unary_expression(self)


@dataclass
class VariableReference(Expression):
    """变量引用"""
    name: str
    line: int = 0
    column: int = 0
    
    def accept(self, visitor):
        return visitor.visit_variable_reference(self)


@dataclass
class CallExpression(Expression):
    """函数调用表达式"""
    function: Expression  # 通常是 VariableReference
    arguments: List[Expression]
    line: int = 0
    column: int = 0
    
    def accept(self, visitor):
        return visitor.visit_call_expression(self)


# ===== 声明节点 =====

@dataclass
class VariableDeclaration(Statement):
    """变量声明"""
    name: str
    type_annotation: Optional[str] = None  # 'int', 'float', 'string', 'bool'
    initializer: Optional[Expression] = None
    line: int = 0
    column: int = 0
    
    def accept(self, visitor):
        return visitor.visit_variable_declaration(self)


@dataclass
class Parameter:
    """函数参数"""
    name: str
    type_annotation: Optional[str] = None


@dataclass
class FunctionDeclaration(Statement):
    """函数声明"""
    name: str
    parameters: List[Parameter]
    return_type: Optional[str]
    body: 'BlockStatement'
    line: int = 0
    column: int = 0
    
    def accept(self, visitor):
        return visitor.visit_function_declaration(self)


# ===== 语句节点 =====

@dataclass
class ExpressionStatement(Statement):
    """表达式语句"""
    expression: Expression
    line: int = 0
    column: int = 0
    
    def accept(self, visitor):
        return visitor.visit_expression_statement(self)


@dataclass
class AssignmentStatement(Statement):
    """赋值语句"""
    target: VariableReference
    value: Expression
    line: int = 0
    column: int = 0
    
    def accept(self, visitor):
        return visitor.visit_assignment_statement(self)


@dataclass
class IfStatement(Statement):
    """条件语句"""
    condition: Expression
    then_branch: 'BlockStatement'
    else_branch: Optional['BlockStatement'] = None
    line: int = 0
    column: int = 0
    
    def accept(self, visitor):
        return visitor.visit_if_statement(self)


@dataclass
class WhileStatement(Statement):
    """while 循环语句"""
    condition: Expression
    body: 'BlockStatement'
    line: int = 0
    column: int = 0
    
    def accept(self, visitor):
        return visitor.visit_while_statement(self)


@dataclass
class ForStatement(Statement):
    """for 循环语句"""
    variable: str
    iterable: Expression
    body: 'BlockStatement'
    line: int = 0
    column: int = 0
    
    def accept(self, visitor):
        return visitor.visit_for_statement(self)


@dataclass
class ReturnStatement(Statement):
    """return 语句"""
    value: Optional[Expression] = None
    line: int = 0
    column: int = 0
    
    def accept(self, visitor):
        return visitor.visit_return_statement(self)


@dataclass
class BlockStatement(Statement):
    """代码块"""
    statements: List[Statement]
    line: int = 0
    column: int = 0
    
    def accept(self, visitor):
        return visitor.visit_block_statement(self)


# ===== 程序节点 =====

@dataclass
class Program(Node):
    """程序根节点"""
    statements: List[Statement]
    line: int = 0
    column: int = 0
    
    def accept(self, visitor):
        return visitor.visit_program(self)


# ===== 访问者模式 =====

class AstVisitor:
    """AST 访问者基类"""
    
    # 字面量
    def visit_number_literal(self, node: NumberLiteral): pass
    def visit_string_literal(self, node: StringLiteral): pass
    def visit_boolean_literal(self, node: BooleanLiteral): pass
    
    # 表达式
    def visit_binary_expression(self, node: BinaryExpression): pass
    def visit_unary_expression(self, node: UnaryExpression): pass
    def visit_variable_reference(self, node: VariableReference): pass
    def visit_call_expression(self, node: CallExpression): pass
    
    # 声明
    def visit_variable_declaration(self, node: VariableDeclaration): pass
    def visit_function_declaration(self, node: FunctionDeclaration): pass
    
    # 语句
    def visit_expression_statement(self, node: ExpressionStatement): pass
    def visit_assignment_statement(self, node: AssignmentStatement): pass
    def visit_if_statement(self, node: IfStatement): pass
    def visit_while_statement(self, node: WhileStatement): pass
    def visit_for_statement(self, node: ForStatement): pass
    def visit_return_statement(self, node: ReturnStatement): pass
    def visit_block_statement(self, node: BlockStatement): pass
    
    # 程序
    def visit_program(self, node: Program): pass


# ===== 打印访问者（用于调试） =====

class PrintVisitor(AstVisitor):
    """打印 AST 的访问者"""
    
    def __init__(self, indent: str = "  "):
        self.indent = indent
        self.level = 0
    
    def _print(self, *args):
        print(self.indent * self.level + " ".join(str(arg) for arg in args))
    
    def _visit(self, node, name: str):
        self._print(f"{name}(")
        self.level += 1
        result = node.accept(self)
        self.level -= 1
        self._print(f")")
        return result
    
    # 字面量
    def visit_number_literal(self, node: NumberLiteral):
        self._print(f"NumberLiteral(value={node.value})")
    
    def visit_string_literal(self, node: StringLiteral):
        self._print(f"StringLiteral(value='{node.value}')")
    
    def visit_boolean_literal(self, node: BooleanLiteral):
        self._print(f"BooleanLiteral(value={node.value})")
    
    # 表达式
    def visit_binary_expression(self, node: BinaryExpression):
        self._print(f"BinaryExpression(operator='{node.operator}')")
        self._visit(node.left, "left")
        self._visit(node.right, "right")
    
    def visit_unary_expression(self, node: UnaryExpression):
        self._print(f"UnaryExpression(operator='{node.operator}')")
        self._visit(node.operand, "operand")
    
    def visit_variable_reference(self, node: VariableReference):
        self._print(f"VariableReference(name='{node.name}')")
    
    def visit_call_expression(self, node: CallExpression):
        self._print(f"CallExpression(arguments={len(node.arguments)})")
        self._visit(node.function, "function")
        for i, arg in enumerate(node.arguments):
            self._visit(arg, f"arg{i}")
    
    # 声明
    def visit_variable_declaration(self, node: VariableDeclaration):
        self._print(f"VariableDeclaration(name='{node.name}', type={node.type_annotation})")
        if node.initializer:
            self._visit(node.initializer, "initializer")
    
    def visit_function_declaration(self, node: FunctionDeclaration):
        self._print(f"FunctionDeclaration(name='{node.name}', params={len(node.parameters)})")
        for i, param in enumerate(node.parameters):
            self._print(f"{self.indent * self.level}  param{i}: {param.name}: {param.type_annotation}")
        self._visit(node.body, "body")
    
    # 语句
    def visit_expression_statement(self, node: ExpressionStatement):
        self._print("ExpressionStatement")
        self._visit(node.expression, "expression")
    
    def visit_assignment_statement(self, node: AssignmentStatement):
        self._print("AssignmentStatement")
        self._visit(node.target, "target")
        self._visit(node.value, "value")
    
    def visit_if_statement(self, node: IfStatement):
        self._print("IfStatement")
        self._visit(node.condition, "condition")
        self._visit(node.then_branch, "then_branch")
        if node.else_branch:
            self._visit(node.else_branch, "else_branch")
    
    def visit_while_statement(self, node: WhileStatement):
        self._print("WhileStatement")
        self._visit(node.condition, "condition")
        self._visit(node.body, "body")
    
    def visit_for_statement(self, node: ForStatement):
        self._print(f"ForStatement(variable='{node.variable}')")
        self._visit(node.iterable, "iterable")
        self._visit(node.body, "body")
    
    def visit_return_statement(self, node: ReturnStatement):
        self._print("ReturnStatement")
        if node.value:
            self._visit(node.value, "value")
    
    def visit_block_statement(self, node: BlockStatement):
        self._print(f"BlockStatement(statements={len(node.statements)})")
        for i, stmt in enumerate(node.statements):
            self._visit(stmt, f"stmt{i}")
    
    # 程序
    def visit_program(self, node: Program):
        self._print(f"Program(statements={len(node.statements)})")
        for i, stmt in enumerate(node.statements):
            self._visit(stmt, f"stmt{i}")


# ===== 测试代码 =====

def test_ast_nodes():
    """测试 AST 节点的基本功能"""
    print("=== 测试 AST 节点 ===")
    
    # 创建一些测试节点
    number = NumberLiteral(value=42, line=1, column=1)
    string = StringLiteral(value="hello", line=1, column=6)
    binary = BinaryExpression(
        left=number,
        operator="+",
        right=StringLiteral(value=" world", line=1, column=10),
        line=1,
        column=8
    )
    
    # 使用打印访问者
    printer = PrintVisitor()
    binary.accept(printer)
    
    print("\n=== 测试完成 ===")


if __name__ == "__main__":
    test_ast_nodes()