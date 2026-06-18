# Lang Ada Lexer 接口规范

## 1. 概述

Lexer（词法分析器）负责将Lang Ada源代码文本转换为Token序列，为后续的语法分析和语义分析提供基础。

## 2. 接口定义

### 2.1 Lexer 类

```python
from typing import List, Optional
from src.lang_token import Token, TokenType

class Lexer:
    """
    Lang Ada 词法分析器
    
    职责：
    - 将源代码文本转换为Token序列
    - 识别关键字、标识符、字面量、运算符和标点符号
    - 处理空白字符和缩进
    - 提供Token的向前查看和消费功能
    - 报告词法错误和位置信息
    """
    
    def __init__(self, source: str):
        """
        初始化词法分析器
        
        Args:
            source (str): 要分析的源代码字符串
            
        初始化后的状态：
        - position: 0 (当前字符位置)
        - line: 1 (当前行号)
        - column: 1 (当前列号)
        - current_char: source[0] (当前字符)
        - tokens: [] (空Token列表)
        - peeked_token: None (向前查看的Token)
        """
        pass
    
    def tokenize(self) -> List[Token]:
        """
        将整个源代码转换为Token序列
        
        Returns:
            List[Token]: Token列表，按在源代码中出现的顺序排列
            
        处理流程：
        1. 重置内部状态
        2. 逐个字符读取源代码
        3. 识别并创建相应的Token
        4. 处理空白字符和换行符
        5. 处理缩进/反缩进
        6. 遇到文件结束符时停止
        
        异常：
        - LexError: 当遇到无法识别的词法结构时抛出
        """
        pass
    
    def peek(self) -> Token:
        """
        向前查看下一个Token，但不消费它
        
        Returns:
            Token: 下一个Token
            
        特性：
        - 返回相同的Token，每次调用结果不变
        - 不改变内部状态（position, line, column等）
        - 如果到达文件末尾，返回EOF Token
        
        使用场景：
        - 语法分析器需要预览下一个Token
        - 实现回溯功能
        """
        pass
    
    def advance(self) -> Token:
        """
        消费并返回下一个Token
        
        Returns:
            Token: 被消费的Token
            
        特性：
        - 移动当前位置到下一个Token的开始
        - 更新position、line、column等状态
        - 内部会自动调用peek()获取下一个Token
        - 如果到达文件末尾，返回EOF Token
        
        使用场景：
        - 语法分析器逐个消费Token
        - 实现自顶向下的语法分析
        """
        pass
    
    def skip_whitespace(self) -> None:
        """
        跳过连续的空白字符
        
        功能：
        - 跳过空格、制表符、换行符等空白字符
        - 更新位置信息（line、column）
        - 不创建任何Token
        - 保持当前位置在下一个非空白字符
        
        特性：
        - 处理不同类型的空白字符
        - 正确处理行号和列号的更新
        - 保留缩进信息用于INDENT/DEDENT Token
        """
        pass
```

### 2.2 辅助方法

```python
class Lexer(Lexer):
    # 基础方法已定义 above
    
    def _read_number(self) -> Token:
        """读取数字字面量，返回NUMBER Token"""
        pass
    
    def _read_string(self) -> Token:
        """读取字符串字面量，返回STRING Token"""
        pass
    
    def _read_identifier(self) -> Token:
        """读取标识符或关键字，返回IDENT或KEYWORD Token"""
        pass
    
    def _read_operator(self) -> Token:
        """读取运算符，返回相应的OP Token"""
        pass
    
    def _read_punctuation(self) -> Token:
        """读取标点符号，返回PUNCT Token"""
        pass
    
    def _handle_indent(self) -> Token:
        """处理缩进，返回INDENT或DEDENT Token"""
        pass
    
    def _current_char(self) -> Optional[str]:
        """获取当前字符，如果到达末尾返回None"""
        pass
    
    def _next_char(self) -> Optional[str]:
        """获取下一个字符，如果到达末尾返回None"""
        pass
    
    def _skip_single_line_comment(self) -> None:
        """跳过单行注释 (# 开头到行尾)"""
        pass
    
    def _skip_multi_line_comment(self) -> None:
        """跳过多行注释 (/* */ 包围)"""
        pass
```

### 2.3 异常类

```python
class LexError(Exception):
    """
    词法分析错误
    
    Attributes:
        message (str): 错误信息
        line (int): 错误所在的行号
        column (int): 错误所在的列号
        position (int): 错误在源代码中的位置
        
    Usage:
        raise LexError("Invalid character 'x'", line=5, column=10)
    """
    pass
```

## 3. 使用示例

### 3.1 基本使用

```python
# 创建词法分析器
source = """
fn main() {
    let x = 42;
    let y = "hello";
    return x + y;
}
"""
lexer = Lexer(source)

# 获取所有Token
tokens = lexer.tokenize()
for token in tokens:
    print(token)

# 前向查看和消费
next_token = lexer.peek()
print(f"Next token: {next_token}")

token = lexer.advance()
print(f"Consumed token: {token}")
```

### 3.2 高级用法

```python
# 逐个消费Token
lexer = Lexer(source)
while True:
    token = lexer.advance()
    if token.type == TokenType.EOF:
        break
    print(f"Line {token.line}: {token}")
```

### 3.3 错误处理

```python
try:
    lexer = Lexer("invalid source code $")
    tokens = lexer.tokenize()
except LexError as e:
    print(f"Lexical error at line {e.line}, column {e.column}: {e.message}")
```

## 4. Token 生成规则

### 4.1 关键字
- 保留字：fn, if, else, while, for, in, return, true, false, int, float, string, bool
- 大小写敏感：必须小写

### 4.2 标识符
- 字母开头，后跟字母、数字或下划线
- 不能是关键字
- 支持Unicode字符

### 4.3 字面量
- 数字：整数、浮点数
- 字符串：双引号或单引号包围
- 布尔值：true, false

### 4.4 运算符
- 算术：+, -, *, /, %
- 比较：==, !=, <, <=, >, >=
- 逻辑：&&, ||, !
- 赋值：=

### 4.5 标点符号
- 括号：(, ), {, }, [, ]
- 分隔符：,, ., ;, :, ..
- 特殊：缩进、反缩进

## 5. 错误处理

### 5.1 错误类型
1. **无效字符**：无法识别的字符
2. **未闭合字符串**：缺少结束引号
3. **未闭合注释**：缺少结束标记
4. **无效数字格式**：错误的数字格式
5. **语法错误**：不符合词法规则的序列

### 5.2 错误报告
每个错误都包含：
- 错误类型描述
- 行号和列号
- 错误位置信息

## 6. 性能要求

- 时间复杂度：O(n)，n为源代码长度
- 空间复杂度：O(n)，用于存储Token列表
- 支持大文件处理（>10MB）

## 7. 测试要求

### 7.1 单元测试
- 所有公共方法的测试
- 各种Token类型的识别测试
- 错误处理测试
- 边界条件测试

### 7.2 集成测试
- 完整源代码的词法分析
- 与语法分析器的集成
- 性能测试

## 8. 版本控制

- 当前版本：1.0.0
- 兼容性：与Lang Ada 1.0 规范兼容
- 向后兼容：新版本不应破坏现有API