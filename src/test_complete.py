"""
完整的词法分析器单元测试
覆盖：数字/字符串/标识符/关键字/运算符/边界情况（空输入/非法字符）
"""

import unittest
from lang_token import Lexer, Token, TokenType


class TestLexerNumbers(unittest.TestCase):
    """测试数字识别"""
    
    def test_integers(self):
        """测试整数识别"""
        lexer = Lexer("0 123 456789 007")
        tokens = lexer.tokenize()
        
        # 移除EOF token进行测试
        actual_tokens = [t for t in tokens if t.type != TokenType.EOF]
        
        self.assertEqual(len(actual_tokens), 4)
        self.assertEqual(actual_tokens[0].type, TokenType.INT)
        self.assertEqual(actual_tokens[0].value, "0")
        self.assertEqual(actual_tokens[1].type, TokenType.INT)
        self.assertEqual(actual_tokens[1].value, "123")
        self.assertEqual(actual_tokens[2].type, TokenType.INT)
        self.assertEqual(actual_tokens[2].value, "456789")
        self.assertEqual(actual_tokens[3].type, TokenType.INT)
        self.assertEqual(actual_tokens[3].value, "007")
    
    def test_floats(self):
        """测试浮点数识别"""
        lexer = Lexer("0.0 3.14 0.5 123.456 .789")
        tokens = lexer.tokenize()
        actual_tokens = [t for t in tokens if t.type != TokenType.EOF]
        
        self.assertEqual(len(actual_tokens), 5)
        self.assertEqual(actual_tokens[0].type, TokenType.FLOAT)
        self.assertEqual(actual_tokens[0].value, "0.0")
        self.assertEqual(actual_tokens[1].type, TokenType.FLOAT)
        self.assertEqual(actual_tokens[1].value, "3.14")
        self.assertEqual(actual_tokens[2].type, TokenType.FLOAT)
        self.assertEqual(actual_tokens[2].value, "0.5")
        self.assertEqual(actual_tokens[3].type, TokenType.FLOAT)
        self.assertEqual(actual_tokens[3].value, "123.456")
        self.assertEqual(actual_tokens[4].type, TokenType.FLOAT)
        self.assertEqual(actual_tokens[4].value, ".789")


class TestLexerStrings(unittest.TestCase):
    """测试字符串识别"""
    
    def test_double_quoted_strings(self):
        """测试双引号字符串"""
        lexer = Lexer('"hello" "world" "123" "with space"')
        tokens = lexer.tokenize()
        actual_tokens = [t for t in tokens if t.type != TokenType.EOF]
        
        self.assertEqual(len(actual_tokens), 4)
        self.assertEqual(actual_tokens[0].type, TokenType.STRING)
        self.assertEqual(actual_tokens[0].value, "hello")
        self.assertEqual(actual_tokens[1].type, TokenType.STRING)
        self.assertEqual(actual_tokens[1].value, "world")
        self.assertEqual(actual_tokens[2].type, TokenType.STRING)
        self.assertEqual(actual_tokens[2].value, "123")
        self.assertEqual(actual_tokens[3].type, TokenType.STRING)
        self.assertEqual(actual_tokens[3].value, "with space")
    
    def test_single_quoted_strings(self):
        """测试单引号字符串"""
        lexer = Lexer("'hello' 'world' '123' 'with space'")
        tokens = lexer.tokenize()
        actual_tokens = [t for t in tokens if t.type != TokenType.EOF]
        
        self.assertEqual(len(actual_tokens), 4)
        self.assertEqual(actual_tokens[0].type, TokenType.STRING)
        self.assertEqual(actual_tokens[0].value, "hello")
        self.assertEqual(actual_tokens[1].type, TokenType.STRING)
        self.assertEqual(actual_tokens[1].value, "world")
        self.assertEqual(actual_tokens[2].type, TokenType.STRING)
        self.assertEqual(actual_tokens[2].value, "123")
        self.assertEqual(actual_tokens[3].type, TokenType.STRING)
        self.assertEqual(actual_tokens[3].value, "with space")
    
    def test_escaped_strings(self):
        """测试转义字符字符串"""
        lexer = Lexer(r'"hello\nworld" "tab\ttest" "quote\""')
        tokens = lexer.tokenize()
        actual_tokens = [t for t in tokens if t.type != TokenType.EOF]
        
        self.assertEqual(len(actual_tokens), 3)
        self.assertEqual(actual_tokens[0].type, TokenType.STRING)
        self.assertEqual(actual_tokens[0].value, "hello\nworld")
        self.assertEqual(actual_tokens[1].type, TokenType.STRING)
        self.assertEqual(actual_tokens[1].value, "tab\ttest")
        self.assertEqual(actual_tokens[2].type, TokenType.STRING)
        self.assertEqual(actual_tokens[2].value, "quote\"")


class TestLexerIdentifiers(unittest.TestCase):
    """测试标识符识别"""
    
    def test_valid_identifiers(self):
        """测试有效标识符"""
        lexer = Lexer("variable _private _123 abc def ghi")
        tokens = lexer.tokenize()
        actual_tokens = [t for t in tokens if t.type != TokenType.EOF]
        
        self.assertEqual(len(actual_tokens), 6)
        for i, token in enumerate(actual_tokens):
            self.assertEqual(token.type, TokenType.IDENT)
            expected_values = ["variable", "_private", "_123", "abc", "def", "ghi"]
            self.assertEqual(token.value, expected_values[i])
    
    def test_mixed_identifiers(self):
        """测试混合标识符"""
        lexer = Lexer("a1 b2 c3 var1 var2 var3")
        tokens = lexer.tokenize()
        actual_tokens = [t for t in tokens if t.type != TokenType.EOF]
        
        self.assertEqual(len(actual_tokens), 6)
        for i, token in enumerate(actual_tokens):
            self.assertEqual(token.type, TokenType.IDENT)
            expected_values = ["a1", "b2", "c3", "var1", "var2", "var3"]
            self.assertEqual(token.value, expected_values[i])


class TestLexerKeywords(unittest.TestCase):
    """测试关键字识别"""
    
    def test_all_keywords(self):
        """测试所有关键字"""
        keywords = "fn if else while for in return true false int float string bool"
        lexer = Lexer(keywords)
        tokens = lexer.tokenize()
        actual_tokens = [t for t in tokens if t.type != TokenType.EOF]
        
        expected_types = [
            TokenType.FN, TokenType.IF, TokenType.ELSE, TokenType.WHILE,
            TokenType.FOR, TokenType.IN, TokenType.RETURN, TokenType.TRUE,
            TokenType.FALSE, TokenType.INT, TokenType.FLOAT, TokenType.STRING_TYPE,
            TokenType.BOOL_TYPE
        ]
        
        self.assertEqual(len(actual_tokens), len(expected_types))
        for i, (token, expected_type) in enumerate(zip(actual_tokens, expected_types)):
            self.assertEqual(token.type, expected_type)
            print(f"✅ {token.value} -> {token.type.name}")


class TestLexerOperators(unittest.TestCase):
    """测试运算符识别"""
    
    def test_single_character_operators(self):
        """测试单字符运算符"""
        operators = "+ - * / % ! ="
        lexer = Lexer(operators)
        tokens = lexer.tokenize()
        actual_tokens = [t for t in tokens if t.type != TokenType.EOF]
        
        expected_types = [
            TokenType.ADD, TokenType.SUB, TokenType.MUL, TokenType.DIV,
            TokenType.MOD, TokenType.NOT, TokenType.ASSIGN
        ]
        
        self.assertEqual(len(actual_tokens), len(expected_types))
        for i, (token, expected_type) in enumerate(zip(actual_tokens, expected_types)):
            self.assertEqual(token.type, expected_type)
            print(f"✅ {token.value} -> {token.type.name}")
    
    def test_two_character_operators(self):
        """测试双字符运算符"""
        operators = "== != <= >= && ||"
        lexer = Lexer(operators)
        tokens = lexer.tokenize()
        actual_tokens = [t for t in tokens if t.type != TokenType.EOF]
        
        expected_types = [
            TokenType.EQ, TokenType.NE, TokenType.LE, TokenType.GE,
            TokenType.AND, TokenType.OR
        ]
        
        self.assertEqual(len(actual_tokens), len(expected_types))
        for i, (token, expected_type) in enumerate(zip(actual_tokens, expected_types)):
            self.assertEqual(token.type, expected_type)
            print(f"✅ {token.value} -> {token.type.name}")


class TestLexerPunctuation(unittest.TestCase):
    """测试标点符号识别"""
    
    def test_basic_punctuation(self):
        """测试基本标点符号"""
        punct = "( ) { } [ ] , . ; :"
        lexer = Lexer(punct)
        tokens = lexer.tokenize()
        actual_tokens = [t for t in tokens if t.type != TokenType.EOF]
        
        expected_types = [
            TokenType.LPAREN, TokenType.RPAREN, TokenType.LBRACE, TokenType.RBRACE,
            TokenType.LBRACK, TokenType.RBRACK, TokenType.COMMA, TokenType.DOT,
            TokenType.SEMICOLON, TokenType.COLON
        ]
        
        self.assertEqual(len(actual_tokens), len(expected_types))
        for i, (token, expected_type) in enumerate(zip(actual_tokens, expected_types)):
            self.assertEqual(token.type, expected_type)
            print(f"✅ {token.value} -> {token.type.name}")
    
    def test_range_operator(self):
        """测试范围运算符"""
        lexer = Lexer("...")
        tokens = lexer.tokenize()
        actual_tokens = [t for t in tokens if t.type != TokenType.EOF]
        
        self.assertEqual(len(actual_tokens), 1)
        self.assertEqual(actual_tokens[0].type, TokenType.RANGE)
        self.assertEqual(actual_tokens[0].value, "..")
        print(f"✅ .. -> {actual_tokens[0].type.name}")


class TestLexerBoundaryCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_empty_input(self):
        """测试空输入"""
        lexer = Lexer("")
        tokens = lexer.tokenize()
        
        # 空输入应该只有一个EOF token
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.EOF)
        self.assertEqual(tokens[0].value, "")
        print("✅ 空输入测试通过")
    
    def test_whitespace_only(self):
        """测试只有空白字符"""
        lexer = Lexer("   \t\n\r\v\f")
        tokens = lexer.tokenize()
        
        # 只有空白字符应该只有一个EOF token
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.EOF)
        print("✅ 空白字符测试通过")
    
    def test_invalid_characters(self):
        """测试非法字符"""
        invalid_chars = "@#$^`~"
        lexer = Lexer(invalid_chars)
        tokens = lexer.tokenize()
        actual_tokens = [t for t in tokens if t.type != TokenType.EOF]
        
        self.assertEqual(len(actual_tokens), len(invalid_chars))
        for i, token in enumerate(actual_tokens):
            self.assertEqual(token.type, TokenType.ERROR)
            self.assertEqual(token.value, invalid_chars[i])
            print(f"✅ '{invalid_chars[i]}' -> {token.type.name}")
    
    def test_unterminated_string(self):
        """测试未闭合的字符串"""
        lexer = Lexer('"unterminated string')
        tokens = lexer.tokenize()
        actual_tokens = [t for t in tokens if t.type != TokenType.EOF]
        
        self.assertEqual(len(actual_tokens), 1)
        self.assertEqual(actual_tokens[0].type, TokenType.ERROR)
        self.assertEqual(actual_tokens[0].value, '"unterminated string')
        print("✅ 未闭合字符串测试通过")
    
    def test_invalid_identifier_start(self):
        """测试无效的标识符开头"""
        invalid_identifiers = "123 1abc @var #test"
        lexer = Lexer(invalid_identifiers)
        tokens = lexer.tokenize()
        actual_tokens = [t for t in tokens if t.type != TokenType.EOF]
        
        # 123 -> INT, 1abc -> ERROR, @var -> ERROR, #test -> ERROR
        expected_types = [TokenType.INT, TokenType.ERROR, TokenType.ERROR, TokenType.ERROR]
        expected_values = ["123", "1abc", "@var", "#test"]
        
        self.assertEqual(len(actual_tokens), 4)
        for i, (token, expected_type, expected_value) in enumerate(zip(actual_tokens, expected_types, expected_values)):
            self.assertEqual(token.type, expected_type)
            self.assertEqual(token.value, expected_value)
            print(f"✅ {expected_value} -> {token.type.name}")


class TestLexerComplexExpressions(unittest.TestCase):
    """测试复杂表达式"""
    
    def test_arithmetic_expression(self):
        """测试算术表达式"""
        expression = "let result = 10 + 20 * 3;"
        lexer = Lexer(expression)
        tokens = lexer.tokenize()
        actual_tokens = [t for t in tokens if t.type != TokenType.EOF]
        
        # 检查一些关键token
        self.assertEqual(actual_tokens[0].type, TokenType.IDENT)  # let
        self.assertEqual(actual_tokens[0].value, "let")
        self.assertEqual(actual_tokens[1].type, TokenType.IDENT)  # result
        self.assertEqual(actual_tokens[1].value, "result")
        self.assertEqual(actual_tokens[2].type, TokenType.ASSIGN)  # =
        self.assertEqual(actual_tokens[3].type, TokenType.INT)     # 10
        self.assertEqual(actual_tokens[3].value, "10")
        self.assertEqual(actual_tokens[4].type, TokenType.ADD)     # +
        self.assertEqual(actual_tokens[5].type, TokenType.INT)     # 20
        self.assertEqual(actual_tokens[6].type, TokenType.MUL)     # *
        self.assertEqual(actual_tokens[7].type, TokenType.INT)     # 3
        print("✅ 算术表达式测试通过")
    
    def test_function_definition(self):
        """测试函数定义"""
        function = """
        fn calculate(a: int, b: int) -> int {
            return a + b;
        }
        """
        lexer = Lexer(function)
        tokens = lexer.tokenize()
        
        # 检查关键字
        fn_token = next((t for t in tokens if t.type == TokenType.FN), None)
        self.assertIsNotNone(fn_token)
        self.assertEqual(fn_token.value, "fn")
        
        self_token = next((t for t in tokens if t.type == TokenType.RETURN), None)
        self.assertIsNotNone(self_token)
        self.assertEqual(self_token.value, "return")
        
        print("✅ 函数定义测试通过")


class TestLexerEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_consecutive_operators(self):
        """测试连续运算符"""
        expr = "a = b + c - d * e / f"
        lexer = Lexer(expr)
        tokens = lexer.tokenize()
        actual_tokens = [t for t in tokens if t.type != TokenType.EOF]
        
        # 检查运算符顺序
        operator_tokens = [t for t in actual_tokens if t.type in [TokenType.ASSIGN, TokenType.ADD, TokenType.SUB, TokenType.MUL, TokenType.DIV]]
        expected_operators = ["=", "+", "-", "*", "/"]
        
        self.assertEqual(len(operator_tokens), len(expected_operators))
        for i, (token, expected) in enumerate(zip(operator_tokens, expected_operators)):
            self.assertEqual(token.value, expected)
        
        print("✅ 连续运算符测试通过")
    
    def test_nested_brackets(self):
        """测试嵌套括号"""
        expr = "{ [ ( ) ] }"
        lexer = Lexer(expr)
        tokens = lexer.tokenize()
        actual_tokens = [t for t in tokens if t.type != TokenType.EOF]
        
        expected_types = [
            TokenType.LBRACE, TokenType.LBRACK, TokenType.LPAREN, 
            TokenType.RPAREN, TokenType.RBRACK, TokenType.RBRACE
        ]
        
        self.assertEqual(len(actual_tokens), len(expected_types))
        for i, (token, expected_type) in enumerate(zip(actual_tokens, expected_types)):
            self.assertEqual(token.type, expected_type)
        
        print("✅ 嵌套括号测试通过")


if __name__ == "__main__":
    # 创建测试套件
    test_suite = unittest.TestSuite()
    
    # 添加所有测试类
    test_classes = [
        TestLexerNumbers,
        TestLexerStrings, 
        TestLexerIdentifiers,
        TestLexerKeywords,
        TestLexerOperators,
        TestLexerPunctuation,
        TestLexerBoundaryCases,
        TestLexerComplexExpressions,
        TestLexerEdgeCases
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # 输出总结
    if result.wasSuccessful():
        print("\n🎉 所有测试通过！")
    else:
        print(f"\n❌ 测试失败: {len(result.failures)} 个失败, {len(result.errors)} 个错误")
        
        # 输出失败信息
        for test, traceback in result.failures:
            print(f"\n失败: {test}")
            print(traceback)
        
        for test, traceback in result.errors:
            print(f"\n错误: {test}")
            print(traceback)