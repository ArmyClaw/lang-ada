"""
Lang Ada Token 类型定义和实现
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Set


class TokenType(Enum):
    """Token 类型枚举"""
    
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
        return self.type in KEYWORDS.values()
    
    def is_operator(self) -> bool:
        """检查是否是运算符"""
        return self.type in [TokenType.ADD, TokenType.SUB, TokenType.MUL, TokenType.DIV, TokenType.MOD,
                            TokenType.EQ, TokenType.NE, TokenType.LT, TokenType.LE, TokenType.GT, TokenType.GE,
                            TokenType.AND, TokenType.OR, TokenType.NOT, TokenType.ASSIGN]
    
    def is_punctuation(self) -> bool:
        """检查是否是标点符号"""
        return self.type in [TokenType.LPAREN, TokenType.RPAREN, TokenType.LBRACE, TokenType.RBRACE,
                           TokenType.LBRACK, TokenType.RBRACK, TokenType.COMMA, TokenType.DOT,
                           TokenType.SEMICOLON, TokenType.COLON, TokenType.RANGE]
    
    def is_literal(self) -> bool:
        """检查是否是字面量"""
        return self.type in [TokenType.NUMBER, TokenType.STRING, TokenType.BOOL]
    
    def precedence(self) -> int:
        """获取运算符优先级 (数字越大优先级越高)"""
        OPERATOR_PRECEDENCE = {
            TokenType.ADD: 10, TokenType.SUB: 10,      # 算术运算符 - 低优先级
            TokenType.MUL: 20, TokenType.DIV: 20, TokenType.MOD: 20,  # 算术运算符 - 中优先级
            TokenType.EQ: 5, TokenType.NE: 5, TokenType.LT: 5, TokenType.LE: 5,
            TokenType.GT: 5, TokenType.GE: 5,         # 比较运算符
            TokenType.AND: 3, TokenType.OR: 3,       # 逻辑运算符 - 最低优先级
            TokenType.NOT: 15                         # 逻辑非 - 高优先级
        }
        return OPERATOR_PRECEDENCE.get(self.type, 0)
    
    def is_left_associative(self) -> bool:
        """检查是否是左结合运算符"""
        return self.type != TokenType.NOT  # 大部分运算符都是左结合的
    
    def is_assignment(self) -> bool:
        """检查是否是赋值运算符"""
        return self.type == TokenType.ASSIGN


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


# 关键字映射表：标识符字符串 -> TokenType
KEYWORDS: Dict[str, TokenType] = {
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
KEYWORD_SET: Set[str] = set(KEYWORDS.keys())


def test_token_creation():
    """测试Token创建"""
    token = Token(TokenType.NUMBER, "42", 1, 5, 4)
    assert token.type == TokenType.NUMBER
    assert token.value == "42"
    assert token.line == 1
    assert token.column == 5
    print("✅ Token创建测试通过")


def test_keyword_recognition():
    """测试关键字识别"""
    assert Token(TokenType.FN, "fn").is_keyword()
    assert Token(TokenType.IF, "if").is_keyword()
    assert not Token(TokenType.NUMBER, "42").is_keyword()
    print("✅ 关键字识别测试通过")


def test_operator_precedence():
    """测试运算符优先级"""
    assert Token(TokenType.MUL, "*").precedence() > Token(TokenType.ADD, "+").precedence()
    assert Token(TokenType.NOT, "!").precedence() > Token(TokenType.AND, "&&").precedence()
    print("✅ 运算符优先级测试通过")


class Lexer:
    """词法分析器类"""
    
    def __init__(self, source_code: str):
        """初始化词法分析器"""
        self.source_code = source_code
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
    
    def peek(self) -> str:
        """查看当前字符但不移动位置"""
        if self.position >= len(self.source_code):
            return '\0'
        return self.source_code[self.position]
    
    def advance(self) -> str:
        """向前移动一个字符并返回该字符"""
        if self.position >= len(self.source_code):
            return '\0'
        char = self.source_code[self.position]
        self.position += 1
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char
    
    def skip_whitespace(self):
        """跳过空白字符"""
        while self.peek() in ' \t\r\v\f':
            self.advance()
    
    def read_number(self) -> Token:
        """读取数字字面量"""
        start_pos = self.position
        start_column = self.column
        
        # 读取整数部分
        while self.peek().isdigit():
            self.advance()
        
        # 检查是否有小数部分
        if self.peek() == '.':
            self.advance()  # 跳过小数点
            while self.peek().isdigit():
                self.advance()
            token_type = TokenType.FLOAT
        else:
            token_type = TokenType.INT
        
        value = self.source_code[start_pos:self.position]
        return Token(token_type, value, self.line, start_column, start_pos)
    
    def read_string(self) -> Token:
        """读取字符串字面量"""
        quote_char = self.advance()  # 读入引号
        if quote_char not in ['"', "'"]:
            raise ValueError(f"期望引号，但得到 '{quote_char}'")
        
        start_pos = self.position
        start_column = self.column
        
        while self.peek() != quote_char and self.peek() != '\0':
            current_char = self.advance()
            # 处理转义字符
            if current_char == '\\':
                if self.peek() == '\0':
                    raise ValueError("字符串未闭合")
                self.advance()  # 跳过转义字符
        
        if self.peek() == '\0':
            raise ValueError("字符串未闭合")
        
        self.advance()  # 跳过结束引号
        value = self.source_code[start_pos:self.position - 1]
        return Token(TokenType.STRING, value, self.line, start_column, start_pos)
    
    def read_identifier(self) -> Token:
        """读取标识符"""
        start_pos = self.position
        start_column = self.column
        
        # 第一个字符必须是字母或下划线
        first_char = self.peek()
        if not (first_char.isalpha() or first_char == '_'):
            raise ValueError(f"标识符必须以字母或下划线开头，但得到 '{first_char}'")
        
        self.advance()
        
        # 后续字符可以是字母、数字或下划线
        while self.peek() != '\0' and TokenTypeUtils.is_valid_identifier_char(self.peek()):
            self.advance()
        
        value = self.source_code[start_pos:self.position]
        
        # 使用 match_keyword 方法来匹配关键字
        return self.match_keyword(value)
    
    def read_operator(self) -> Token:
        """读取运算符"""
        start_pos = self.position
        start_column = self.column
        char = self.peek()
        
        # 先读取第一个字符
        self.advance()
        
        # 检查是否有第二个字符组成复合运算符
        next_char = self.peek()
        
        # 处理双字符运算符
        if char == '=' and next_char == '=':
            token_type = TokenType.EQ
            self.advance()  # 读取第二个 '='
        elif char == '!' and next_char == '=':
            token_type = TokenType.NE
            self.advance()  # 读取第二个 '='
        elif char == '<' and next_char == '=':
            token_type = TokenType.LE
            self.advance()  # 读取第二个 '='
        elif char == '>' and next_char == '=':
            token_type = TokenType.GE
            self.advance()  # 读取第二个 '='
        elif char == '&' and next_char == '&':
            token_type = TokenType.AND
            self.advance()  # 读取第二个 '&'
        elif char == '|' and next_char == '|':
            token_type = TokenType.OR
            self.advance()  # 读取第二个 '|'
        # 处理单字符运算符
        elif char == '+':
            token_type = TokenType.ADD
        elif char == '-':
            token_type = TokenType.SUB
        elif char == '*':
            token_type = TokenType.MUL
        elif char == '/':
            token_type = TokenType.DIV
        elif char == '%':
            token_type = TokenType.MOD
        elif char == '!':
            token_type = TokenType.NOT
        elif char == '=':
            token_type = TokenType.ASSIGN
        else:
            # 不是合法的运算符，返回错误
            token_type = TokenType.ERROR
            # 不移动位置，让调用者处理
            self.position = start_pos
            self.column = start_column
            return Token(TokenType.ERROR, char, self.line, start_column, start_pos)
        
        value = self.source_code[start_pos:self.position]
        return Token(token_type, value, self.line, start_column, start_pos)
    
    def read_punct(self) -> Token:
        """读取标点符号"""
        start_pos = self.position
        start_column = self.column
        char = self.peek()
        
        # 确定标点符号类型
        if char == '(':
            token_type = TokenType.LPAREN
        elif char == ')':
            token_type = TokenType.RPAREN
        elif char == '{':
            token_type = TokenType.LBRACE
        elif char == '}':
            token_type = TokenType.RBRACE
        elif char == '[':
            token_type = TokenType.LBRACK
        elif char == ']':
            token_type = TokenType.RBRACK
        elif char == ',':
            token_type = TokenType.COMMA
        elif char == '.':
            # 检查是否是范围运算符 ..
            if self.peek() == '.':
                token_type = TokenType.RANGE
                # advance 两次 (两个点)
                self.advance()
                self.advance()
            else:
                token_type = TokenType.DOT
                # advance 一次 (单个点)
                self.advance()
        elif char == ';':
            token_type = TokenType.SEMICOLON
            self.advance()
        elif char == ':':
            token_type = TokenType.COLON
            self.advance()
        else:
            # 不是合法的标点符号，返回错误
            token_type = TokenType.ERROR
            # 不移动位置，让调用者处理
            self.position = start_pos
            self.column = start_column
            return Token(TokenType.ERROR, char, self.line, start_column, start_pos)
        
        value = self.source_code[start_pos:self.position]
        return Token(token_type, value, self.line, start_column, start_pos)
    
    def match_keyword(self, identifier: str) -> Token:
        """匹配关键字"""
        start_pos = self.position - len(identifier)  # 因为标识符已经读取完了
        start_column = self.column - len(identifier)
        
        if identifier in KEYWORD_SET:
            token_type = KEYWORDS[identifier]
        else:
            token_type = TokenType.IDENT
        
        return Token(token_type, identifier, self.line, start_column, start_pos)
    
    def tokenize(self) -> List[Token]:
        """将源代码转换为token列表"""
        self.tokens = []
        
        while self.peek() != '\0':
            self.skip_whitespace()
            
            if self.peek() == '\0':
                break
            
            char = self.peek()
            
            # 根据字符类型调用相应的读取方法
            try:
                if char.isdigit():
                    token = self.read_number()
                elif char in ['"', "'"]:
                    token = self.read_string()
                elif char.isalpha() or char == '_':
                    token = self.read_identifier()
                elif char in '+-*/%=!<>|&!':
                    token = self.read_operator()
                elif char in '(){}[],.;:':
                    token = self.read_punct()
                else:
                    # 其他字符作为ERROR token处理
                    start_pos = self.position
                    start_column = self.column
                    self.advance()
                    value = self.source_code[start_pos:self.position]
                    token = Token(TokenType.ERROR, value, self.line, start_column, start_pos)
            except ValueError as e:
                # 错误处理
                start_pos = self.position
                start_column = self.column
                self.advance()
                value = self.source_code[start_pos:self.position]
                token = Token(TokenType.ERROR, value, self.line, start_column, start_pos)
            
            self.tokens.append(token)
        
        # 添加EOF token
        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column, self.position))
        return self.tokens


def test_lexer():
    """测试词法分析器"""
    # 测试数字识别
    lexer = Lexer("42 3.14 123")
    tokens = lexer.tokenize()
    assert len(tokens) == 4  # 3个数字 + EOF
    assert tokens[0].type == TokenType.INT and tokens[0].value == "42"
    assert tokens[1].type == TokenType.FLOAT and tokens[1].value == "3.14"
    assert tokens[2].type == TokenType.INT and tokens[2].value == "123"
    
    # 测试字符串识别
    lexer = Lexer('"hello" \'world\'')
    tokens = lexer.tokenize()
    assert len(tokens) == 3  # 2个字符串 + EOF
    assert tokens[0].type == TokenType.STRING and tokens[0].value == "hello"
    assert tokens[1].type == TokenType.STRING and tokens[1].value == "world"
    
    # 测试标识符识别
    lexer = Lexer("variable1 _func if int")
    tokens = lexer.tokenize()
    assert len(tokens) == 5  # 4个标识符 + EOF
    assert tokens[0].type == TokenType.IDENT and tokens[0].value == "variable1"
    assert tokens[1].type == TokenType.IDENT and tokens[1].value == "_func"
    assert tokens[2].type == TokenType.IF  # 关键字
    assert tokens[3].type == TokenType.INT  # 关键字
    
    print("✅ 词法分析器测试通过")


if __name__ == "__main__":
    # 运行测试
    test_token_creation()
    test_keyword_recognition()
    test_operator_precedence()
    test_lexer()
    print("🎉 所有测试通过！")