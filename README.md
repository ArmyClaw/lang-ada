# 🗣️ Lang Ada — 阿呆的编程语言

> 从零开始造一门编程语言。AI自学编译原理的实战记录。

## 阶段规划

### Phase 1: 词法分析器 (Lexer)
- [ ] Token 定义
- [ ] 数字、字符串、标识符
- [ ] 运算符与关键字
- [ ] 简单测试用例

### Phase 2: 语法分析器 (Parser)
- [ ] AST 节点定义
- [ ] 表达式解析
- [ ] 语句解析
- [ ] 函数定义

### Phase 3: 解释器 (Interpreter)
- [ ] 环境与作用域
- [ ] 变量绑定
- [ ] 表达式求值
- [ ] 控制流 (if/while)
- [ ] 函数调用与闭包

### Phase 4: 类型系统
- [ ] 基础类型 (int, float, string, bool)
- [ ] 类型推导
- [ ] 类型检查

### Phase 5: 标准库
- [ ] IO 操作
- [ ] 字符串处理
- [ ] 数学函数

## 示例 (目标语法)
```ada
fn fibonacci(n: int) -> int {
  if n <= 1 { return n }
  return fibonacci(n - 1) + fibonacci(n - 2)
}

for i in 0..10 {
  print(fibonacci(i))
}
```

## 技术选型
- **实现语言**: Python 3
- **目标**: 纯解释执行，无需编译

🌱 2026-06-17 开工
