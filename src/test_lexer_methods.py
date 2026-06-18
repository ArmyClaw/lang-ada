"""
测试新的词法分析方法
"""

from lang_token import Lexer, Token, TokenType

def test_read_operator():
    """测试运算符识别"""
    print("\n=== 测试运算符识别 ===")
    
    # 测试单字符运算符
    lexer = Lexer("+ - * / % ! =")
    tokens = lexer.tokenize()
    expected_types = [
        TokenType.ADD, TokenType.SUB, TokenType.MUL, TokenType.DIV, 
        TokenType.MOD, TokenType.NOT, TokenType.ASSIGN, TokenType.EOF
    ]
    
    for i, (token, expected) in enumerate(zip(tokens, expected_types)):
        assert token.type == expected, f"Token {i}: 期望 {expected}, 实际 {token.type}"
        print(f"✅ {token.value} -> {token.type.name}")
    
    # 测试双字符运算符
    lexer = Lexer("== != <= >= && ||")
    tokens = lexer.tokenize()
    expected_types = [
        TokenType.EQ, TokenType.NE, TokenType.LE, TokenType.GE,
        TokenType.AND, TokenType.OR, TokenType.EOF
    ]
    
    for i, (token, expected) in enumerate(zip(tokens, expected_types)):
        assert token.type == expected, f"Token {i}: 期望 {expected}, 实际 {token.type}"
        print(f"✅ {token.value} -> {token.type.name}")

def test_read_punct():
    """测试标点符号识别"""
    print("\n=== 测试标点符号识别 ===")
    
    # 测试基本标点符号
    lexer = Lexer("( ) { } [ ] , . ; : ..")
    tokens = lexer.tokenize()
    expected_types = [
        TokenType.LPAREN, TokenType.RPAREN, TokenType.LBRACE, TokenType.RBRACE,
        TokenType.LBRACK, TokenType.RBRACK, TokenType.COMMA, TokenType.DOT,
        TokenType.SEMICOLON, TokenType.COLON, TokenType.RANGE, TokenType.EOF
    ]
    
    for i, (token, expected) in enumerate(zip(tokens, expected_types)):
        assert token.type == expected, f"Token {i}: 期望 {expected}, 实际 {token.type}"
        print(f"✅ {token.value} -> {token.type.name}")

def test_match_keyword():
    """测试关键字匹配"""
    print("\n=== 测试关键字匹配 ===")
    
    lexer = Lexer("fn if else while for in return true false int float string bool")
    tokens = lexer.tokenize()
    expected_types = [
        TokenType.FN, TokenType.IF, TokenType.ELSE, TokenType.WHILE,
        TokenType.FOR, TokenType.IN, TokenType.RETURN, TokenType.TRUE,
        TokenType.FALSE, TokenType.INT, TokenType.FLOAT, TokenType.STRING_TYPE,
        TokenType.BOOL_TYPE, TokenType.EOF
    ]
    
    for i, (token, expected) in enumerate(zip(tokens, expected_types)):
        assert token.type == expected, f"Token {i}: 期望 {expected}, 实际 {token.type}"
        print(f"✅ {token.value} -> {token.type.name}")

def test_combined_expression():
    """测试组合表达式"""
    print("\n=== 测试组合表达式 ===")
    
    source = """
    fn main() {
        let x = 42 + 3.14 * 2;
        if x > 100 {
            return "Hello, World!";
        } else {
            return "Too small";
        }
    }
    """
    
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    # 检查一些关键token
    important_tokens = [
        (0, TokenType.FN),      # fn
        (1, TokenType.IDENT, "main"),  # main
        (2, TokenType.LPAREN),   # (
        (3, TokenType.RPAREN),   # )
        (4, TokenType.LBRACE),   # {
        (5, TokenType.IDENT, "let"),   # let
        (6, TokenType.IDENT, "x"),    # x
        (7, TokenType.ASSIGN),   # =
        (8, TokenType.INT, "42"),     # 42
        (9, TokenType.ADD),      # +
        (10, TokenType.FLOAT, "3.14"), # 3.14
        (11, TokenType.MUL),     # *
        (12, TokenType.INT, "2"),     # 2
    ]
    
    for idx, (token_type, *kwargs) in enumerate(important_tokens):
        token = tokens[idx]
        assert token.type == token_type
        if len(kwargs) > 0 and kwargs[0] is not None:
            assert token.value == kwargs[0]
        print(f"✅ {idx}: {token} -> {token.type.name}")

if __name__ == "__main__":
    test_read_operator()
    test_read_punct()
    test_match_keyword()
    test_combined_expression()
    print("\n🎉 所有新方法测试通过！")