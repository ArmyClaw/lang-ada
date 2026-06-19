# AST 节点类型设计

## 概述

为 LangAda 编程语言的语法分析器定义完整的抽象语法树（AST）节点类型。

## 基础结构

所有 AST 节点都继承自基类 `Node`，提供位置信息和通用的访问模式。

### 节点基类

```python
class Node:
    """AST 节点基类"""
    def __init__(self, line: int, column: int):
        self.line = line      # 行号
        self.column = column  # 列号
    
    def accept(self, visitor):
        """访问者模式支持"""
        raise NotImplementedError
```

## 字面量节点

### NumberLiteral
```python
@dataclass
class NumberLiteral(Node):
    """数字字面量"""
    value: Union[int, float]
    
    def accept(self, visitor):
        return visitor.visit_number_literal(self)
```

### StringLiteral  
```python
@dataclass
class StringLiteral(Node):
    """字符串字面量"""
    value: str
    
    def accept(self, visitor):
        return visitor.visit_string_literal(self)
```

### BooleanLiteral
```python
@dataclass  
class BooleanLiteral(Node):
    """布尔字面量"""
    value: bool
    
    def accept(self, visitor):
        return visitor.visit_boolean_literal(self)
```

## 表达式节点

### BinaryExpression
```python
@dataclass
class BinaryExpression(Node):
    """二元表达式"""
    left: 'Expression'
    operator: str  # '+', '-', '*', '/', '==', '!=', '<', '>', '<=', '>='
    right: 'Expression'
    
    def accept(self, visitor):
        return visitor.visit_binary_expression(self)
```

### UnaryExpression
```python
@dataclass
class UnaryExpression(Node):
    """一元表达式"""
    operator: str  # '+', '-', '!', 'not'
    operand: 'Expression'
    
    def accept(self, visitor):
        return visitor.visit_unary_expression(self)
```

### VariableReference
```python
@dataclass
class VariableReference(Node):
    """变量引用"""
    name: str
    
    def accept(self, visitor):
        return visitor.visit_variable_reference(self)
```

### CallExpression
```python
@dataclass
class CallExpression(Node):
    """函数调用表达式"""
    function: 'Expression'  # 通常是 VariableReference
    arguments: List['Expression']
    
    def accept(self, visitor):
        return visitor.visit_call_expression(self)
```

## 声明节点

### VariableDeclaration
```python
@dataclass
class VariableDeclaration(Node):
    """变量声明"""
    name: str
    type_annotation: Optional[str] = None  # 'int', 'float', 'string', 'bool'
    initializer: Optional['Expression'] = None
    
    def accept(self, visitor):
        return visitor.visit_variable_declaration(self)
```

### FunctionDeclaration
```python
@dataclass
class FunctionDeclaration(Node):
    """函数声明"""
    name: str
    parameters: List[Parameter]
    return_type: Optional[str]
    body: 'BlockStatement'
    
    def accept(self, visitor):
        return visitor.visit_function_declaration(self)
```

@dataclass
class Parameter:
    """函数参数"""
    name: str
    type_annotation: Optional[str] = None
```

## 语句节点

### ExpressionStatement
```python
@dataclass
class ExpressionStatement(Node):
    """表达式语句"""
    expression: Expression
    
    def accept(self, visitor):
        return visitor.visit_expression_statement(self)
```

### AssignmentStatement
```python
@dataclass
class AssignmentStatement(Node):
    """赋值语句"""
    target: VariableReference
    value: Expression
    
    def accept(self, visitor):
        return visitor.visit_assignment_statement(self)
```

### IfStatement
```python
@dataclass
class IfStatement(Node):
    """条件语句"""
    condition: Expression
    then_branch: 'BlockStatement'
    else_branch: Optional['BlockStatement'] = None
    
    def accept(self, visitor):
        return visitor.visit_if_statement(self)
```

### WhileStatement
```python
@dataclass
class WhileStatement(Node):
    """while 循环语句"""
    condition: Expression
    body: 'BlockStatement'
    
    def accept(self, visitor):
        return visitor.visit_while_statement(self)
```

### ForStatement
```python
@dataclass
class ForStatement(Node):
    """for 循环语句"""
    variable: str
    iterable: Expression
    body: 'BlockStatement'
    
    def accept(self, visitor):
        return visitor.visit_for_statement(self)
```

### ReturnStatement
```python
@dataclass
class ReturnStatement(Node):
    """return 语句"""
    value: Optional[Expression] = None
    
    def accept(self, visitor):
        return visitor.visit_return_statement(self)
```

### BlockStatement
```python
@dataclass
class BlockStatement(Node):
    """代码块"""
    statements: List[Statement]
    
    def accept(self, visitor):
        return visitor.visit_block_statement(self)
```

## 程序节点

### Program
```python
@dataclass
class Program(Node):
    """程序根节点"""
    statements: List[Statement]
    
    def accept(self, visitor):
        return visitor.visit_program(self)
```

## 类型定义

```python
# 表达式类型的联合
Expression = Union[
    NumberLiteral, StringLiteral, BooleanLiteral,
    BinaryExpression, UnaryExpression, VariableReference,
    CallExpression
]

# 语句类型的联合  
Statement = Union[
    ExpressionStatement, AssignmentStatement, IfStatement,
    WhileStatement, ForStatement, ReturnStatement,
    VariableDeclaration, FunctionDeclaration, BlockStatement
]
```

## 访问者模式

```python
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
```

## 设计要点

1. **类型安全**: 使用 Union 类型确保表达式和语句的类型安全
2. **位置信息**: 每个节点都记录源码位置，便于错误报告和调试
3. **可扩展性**: 访问者模式支持 AST 的遍历和转换
4. **完整的语言特性**: 覆盖 LangAda 的所有语法结构
5. **清晰分离**: 区分表达式（有值）和语句（执行操作）