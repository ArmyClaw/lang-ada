# Lang Ada Token 类型体系设计

## 1. Token 类型定义

### 基础 Token 类型枚举

```python
class TokenType(Enum):
    # 字面量
    NUMBER      = "NUMBER"      # 数字字面量 (123, 3.14)
    STRING      = "STRING"      # 字符串字面量 ("hello", 'world')
    IDENT       = "IDENT"       # 标识符 (变量名、函数名)
    BOOL        = "BOOL"        # 布尔值 (true, false)
    
    # 关键字 (保留字)
    KEYWORD     = "KEYWORD"     # 关键字基类
    
    # 具体关键字
    FN          = "FN"          # 函数定义关键字
    IF          = "IF"          # 条件语句
    ELSE        = "ELSE"        # 否则分支
    WHILE       = "WHILE"       # 循环
    FOR         = "FOR"         # for循环
    IN          = "IN"          # in操作符
    RETURN      = "RETURN"      # 返回语句
    TRUE        = "TRUE"        # 布尔真
    FALSE       = "FALSE"       # 布尔假
    INT         = "INT"         # int类型声明
    FLOAT       = "FLOAT"       # float类型声明
    STRING_TYPE = "STRING_TYPE" # string类型声明
    BOOL_TYPE   = "BOOL_TYPE"   # bool类型声明
    
    # 运算符
    OP          = "OP"          # 运算符基类
    
    # 算术运算符
    ADD         = "ADD"         # +
    SUB         = "SUB"         # -
    MUL         = "MUL"         # *
    DIV         = "DIV"         # /
    MOD         = "MOD"         # %
    
    # 比较运算符
    EQ          = "EQ"          # ==
    NE          = "NE"          # !=
    LT          = "LT"          # <
    LE          = "LE"          # <=
    GT          = "GT"          # >
    GE          = "GE"          # >=
    
    # 逻辑运算符
    AND         = "AND"         # &&
    OR          = "OR"          # ||
    NOT         = "NOT"         # !
    
    # 赋值运算符
    ASSIGN      = "ASSIGN"      # =
    
    # 分隔符/标点符号
    PUNCT       = "PUNCT"       # 标点符号基类
    
    # 具体标点符号
    LPAREN      = "LPAREN"      # (
    RPAREN      = "RPAREN"      # )
    LBRACE      = "LBRACE"      # {
    RBRACE      = "RBRACE"      # }
    LBRACK      = "LBRACK"      # [
    RBRACK      = "RBRACK"      # ]
    COMMA       = "COMMA"       # ,
    DOT         = "DOT"         # .
    SEMICOLON   = "SEMICOLON"   # ;
    COLON       = "COLON"       # :
    RANGE       = "RANGE"       # .. (范围)
    
    # 特殊标记
    EOF         = "EOF"         # 文件结束
    NEWLINE     = "NEWLINE"     # 换行符
    INDENT      = "INDENT"      # 缩进
    DEDENT      = "DEDENT"      # 反缩进
    ERROR       = "ERROR"       # 词法错误
```

## 2. Token 类结构设计

```python
@dataclass
class Token:
    """
    Token 基类 - 表示源代码中的一个词法单元
    
    Attributes:
        type: TokenType - Token类型
        value: str - Token的实际值 (字面量内容、标识符名称等)
        line: int - 所在行号 (从1开始)
        column: int - 所在列号 (从1开始)
        position: int - 在源代码中的绝对位置 (从0开始)
    """
    type: TokenType
    value: str
    line: int = 1
    column: int = 1
    position: int = 0
    
    def __str__(self) -> str:
        """可读的字符串表示"""
        return f"Token({self.type}, '{self.value}', {self.line}:{self.column})"
    
    def __repr__(self) -> str:
        """调试用的字符串表示"""
        return self.__str__()
    
    def is_keyword(self) -> bool:
        """检查是否是关键字"""
        return self.type in TokenType.__members__.values() and self.type.name in KEYWORDS
    
    def is_operator(self) -> bool:
        """检查是否是运算符"""
        return self.type in [ADD, SUB, MUL, DIV, MOD, EQ, NE, LT, LE, GT, GE, AND, OR, NOT, ASSIGN]
    
    def is_punctuation(self) -> bool:
        """检查是否是标点符号"""
        return self.type in [LPAREN, RPAREN, LBRACE, RBRACE, LBRACK, RBRACK, 
                           COMMA, DOT, SEMICOLON, COLON, RANGE]
    
    def is_literal(self) -> bool:
        """检查是否是字面量"""
        return self.type in [NUMBER, STRING, BOOL]
    
    def precedence(self) -> int:
        """获取运算符优先级 (数字越大优先级越高)"""
        OPERATOR_PRECEDENCE = {
            ADD: 10, SUB: 10,      # 算术运算符 - 低优先级
            MUL: 20, DIV: 20, MOD: 20,  # 算术运算符 - 中优先级
            EQ: 5, NE: 5, LT: 5, LE: 5, GT: 5, GE: 5,  # 比较运算符
            AND: 3, OR: 3,         # 逻辑运算符 - 最低优先级
            NOT: 15                # 逻辑非 - 高优先级
        }
        return OPERATOR_PRECEDENCE.get(self.type, 0)
    
    def is_left_associative(self) -> bool:
        """检查是否是左结合运算符"""
        return self.type not in [NOT]  # 大部分运算符都是左结合的
    
    def is_assignment(self) -> bool:
        """检查是否是赋值运算符"""
        return self.type == ASSIGN
```

## 3. 关键字表定义

```python
# 关键字映射表：标识符字符串 -> TokenType
KEYWORDS = {
    'fn': TokenType.FN,
    'if': TokenType.IF,
    'else': TokenType.ELSE,
    'while': TokenType.WHILE,
    'for': TokenType.FOR,
    'in': TokenType.IN,
    'return': TokenType.RETURN,
    'true': TokenType.TRUE,
    'false': TokenType.FALSE,
    'int': TokenType.INT,
    'float': TokenType.FLOAT,
    'string': TokenType.STRING_TYPE,
    'bool': TokenType.BOOL_TYPE,
}

# 关键字集合 (用于快速查找)
KEYWORD_SET = set(KEYWORDS.keys())
```

## 4. Token 类的辅助方法

```python
class TokenTypeUtils:
    """TokenType 工具类"""
    
    @staticmethod
    def is_valid_identifier_char(c: str) -> bool:
        """检查字符是否可以作为标识符的一部分"""
        return c.isalnum() or c == '_'
    
    @staticmethod
    def is_digit(c: str) -> bool:
        """检查字符是否是数字"""
        return c.isdigit()
    
    @staticmethod
    def is_hex_digit(c: str) -> bool:
        """检查字符是否是十六进制数字"""
        return c.isdigit() or c.lower() in 'abcdef'
    
    @staticmethod
    def is_whitespace(c: str) -> bool:
        """检查字符是否是空白字符"""
        return c in ' \t\r\v\f'
    
    @staticmethod
    def is_newline(c: str) -> bool:
        """检查字符是否是换行符"""
        return c in '\n\r'
```

## 5. 词法分析器接口设计

```python
class Lexer:
    """词法分析器接口"""
    
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        self.current_char = source[0] if source else None
    
    def next_token(self) -> Token:
        """获取下一个Token"""
        pass
    
    def tokenize(self) -> List[Token]:
        """将整个源代码 tokenize 成Token序列"""
        while self.current_char is not None:
            token = self.next_token()
            if token.type != TokenType.ERROR:
                self.tokens.append(token)
        return self.tokens
    
    def skip_whitespace(self):
        """跳过空白字符"""
        pass
    
    def read_number(self) -> Token:
        """读取数字字面量"""
        pass
    
    def read_string(self) -> Token:
        """读取字符串字面量"""
        pass
    
    def read_identifier(self) -> Token:
        """读取标识符或关键字"""
        pass
    
    def read_operator(self) -> Token:
        """读取运算符"""
        pass
    
    def read_punctuation(self) -> Token:
        """读取标点符号"""
        pass
```

## 6. 设计原则

1. **完整性**: 覆盖所有需要的Token类型
2. **可扩展性**: 支持未来添加新的关键字、运算符
3. **清晰性**: 每个Token类型都有明确的含义和用途
4. **实用性**: 提供实用的辅助方法 (优先级、结合性等)
5. **错误处理**: 支持词法错误的检测和报告

## 7. 测试用例

```python
# 测试Token创建
def test_token_creation():
    token = Token(TokenType.NUMBER, "42", 1, 5, 4)
    assert token.type == TokenType.NUMBER
    assert token.value == "42"
    assert token.line == 1
    assert token.column == 5

# 测试关键字识别
def test_keyword_recognition():
    assert TokenType.FN.is_keyword()
    assert TokenType.IF.is_keyword()
    assert not TokenType.NUMBER.is_keyword()

# 测试运算符优先级
def test_operator_precedence():
    assert TokenType.MUL.precedence() > TokenType.ADD.precedence()
    assert TokenType.NOT.precedence() > TokenType.AND.precedence()
```

这个设计为Lang Ada语言的词法分析器提供了完整的基础架构，支持未来的扩展和功能增强。