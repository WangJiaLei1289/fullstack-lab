# 编写好的测试

**在以下情况加载这份参考：** 编写或修改测试、添加 mock，或为测试添加清理/辅助方法时。

## 概览

一个测试存在的意义是抓住某一次具体的破坏。这里的一切都服从两条原则：

```
1. Every test names the break it catches
2. Every test exercises the real thing
```

严格的 TDD 会自然产生这两点：先写、并亲眼看着它在真实代码上失败的测试，已经证明了自己能失败；也只有当真实依赖被证明缓慢或是外部依赖时，它才配得上一个 mock。

## 原则 1：说出它抓住的破坏

在写测试主体之前，先回答：**哪一处生产代码改动应该让这个测试失败——而那个改动是一个 bug，还是一个决策？** 测试靠抓住错误分支、缺失的副作用、错误的参数、边界情况或破坏的契约来证明自己的价值。

**独立推导期望值。** 使用字面量和手工核对的测试夹具；带字面量 `want` 值的表驱动测试是首选形态。由被测代码——或它的辅助函数——计算出来的期望值，无论那段代码做什么都会通过：

```typescript
// ❌ Mirror assertion: the same builder computes both sides — always true
const expected = buildSearchQuery({ tag: 'urgent' });
expect(buildSearchQuery({ tag: 'urgent' })).toBe(expected);

// ✅ Hand-derived literal
expect(buildSearchQuery({ tag: 'urgent' })).toBe('tag:"urgent"');
```

**不要写变更探测器。** 如果只有刻意的决策才能让测试失败——常量的值、消息的确切措辞、私有结构——那么它会在重新设计时误报，却对真正的 bug 视而不见。要测依赖该决策的行为：不是 `expect(MAX_RETRIES).toBe(5)`，而是「一次失败的调用会重试 5 次，第 6 次永远不会发生」。

**测行为，不测文本。** 断言某个脚本、技能或配置包含某一行确切文本，只能证明源码就是源码。让脚本在受控输入上运行，断言输出、副作用或退出码。指导代理的文档要由消费它的代理的行为来测试（superpowers:writing-skills）；面向人的普通文字根本不配得到测试。

**测你的代码，不测框架。** 测试你的代码在边界上做出的契约——你注册的路由、你发出的查询、你生成的载荷。上游的机制是它们维护者该写的测试（经典案例：断言你的路由器调用了某个已注册的处理器——那是框架的测试，不是你的）。当上游行为确实让你意外时，写一个窄小的特征测试（characterization test），把那个假设命名出来。同样的边界也适用于你的代码内部：构造函数、getter、常量与简单的转发，只有在它们做校验、归一化、设默认值、推导、强制约束或产生副作用时，才值得为它们写测试——否则就去断言第一个依赖它们的、消费者可见的结果。

### 门禁函数

```
BEFORE writing the test body:
  Name the production change that would make this test fail.

  Cannot name one            → redesign around an observable behavior
  "The source text changed"  → run the artifact and assert its effects
  Only intentional decisions → change detector; test the behavior
                               that depends on the decision

  Confirm the expected value is derived without the code under test.
  IF it reuses the code's logic or helpers:
    Replace it with a literal or hand-checked fixture
```

## 原则 2：测真实的东西

**mock 不配得到断言。** mock 断言在 mock 存在时通过、在 mock 缺席时失败——它对组件本身什么也没说。要断言真实组件的行为；如果你检查的正是 mock，那就取消 mock，或者删掉这条断言。

```typescript
// ✅ Real behavior
expect(screen.getByRole('navigation')).toBeInTheDocument();

// ❌ Mock existence
expect(screen.getByTestId('sidebar-mock')).toBeInTheDocument();
```

**你的搭档的纠正：**「我们是在测 mock 的行为吗？」

**在正确的层级上 mock。** 在替换真实方法之前，先弄清它的每一个副作用；mock 掉缓慢或外部的操作，保留测试所依赖的真实部分。拿不准时，先让测试跑在真实实现上，观察实际需要发生什么。

```typescript
// ❌ The mock swallows the config write that duplicate detection reads
vi.mock('ToolCatalog', () => ({
  discoverAndCacheTools: vi.fn().mockResolvedValue(undefined)
}));

// ✅ Mock only the slow server startup; the config write stays real
vi.mock('MCPServerManager');
```

**让替身足够具体。** 当参数、调用次数或顺序属于契约的一部分时，就要断言它们——一个什么参数都接受的假实现什么都验证不了。给每个分支（成功、错误、格式非法）各自的夹具或 spy，这样错误的分支就无法满足期望。

**完整镜像真实数据。** 按现实中存在的完整结构来 mock——所有有文档的字段——而不只是你的测试读取的那几个。当下游代码读取被省略的字段时，残缺的 mock 会无声地失败：测试通过，集成却坏了。

**生产类只携带生产方法。** 只有测试才需要的清理逻辑放在测试工具里，绝不要做成生产类上的 `destroy()`。问自己：这个方法只有测试在调用吗？这个类真的拥有这个资源的生命周期吗？答案是否定的 → 放进测试工具。

**优先用真实组件，而不是复杂的 mock。** 当 mock 的搭建比测试逻辑还庞大、mock 缺少真实组件的方法、或者 mock 一改测试就坏时，改用真实组件的集成测试。**你的搭档的问题：**「这里需要用到 mock 吗？」

### 门禁函数

```
BEFORE adding a mock or test helper:
  List the real method's side effects; keep the ones the test
  depends on real — mock the slow/external level below them.

  Mock responses mirror the complete real structure.

  A method only tests call lives in test utilities, not production.

  About to assert on the mock itself?
    Unmock it or delete the assertion.
```

## 测试随实现一起交付

TDD 循环——失败的测试、最小的实现、重构——就是「完成」的含义。交付行为所需要的测试，且只交付这些：琐碎的代码和给人看的文字不值得为它们写测试，而为了满足流程写出来的测试，要在维护上付出永久的代价。

## 变异检查

在完成之前，在脑子里对生产代码做变异；每一种现实的变异都应该至少让一个测试失败：

- 常量或参数写错
- 分支处理器写错
- 缺少状态变更或副作用
- 返回空值或默认值
- 缺少对零值、空值、nil、未授权或格式非法输入的校验

没有任何测试抓住的变异，说明该行为未受保护——或者说明那个测试是同义反复。

## 快速参考

| 当你…… | 要做 |
|-------------|-----|
| 写任何测试 | 说出它抓住的破坏——是一个 bug，而不是一个决策 |
| 构造期望值 | 手工推导；绝不用被测代码来算 |
| 测试脚本或文档 | 运行它 / 对它的消费者做压力测试；绝不 grep 它的文本 |
| 想给依赖写测试 | 测你的边界契约，不测它们有文档的机制 |
| 想对某个 mock 元素做断言 | 测真实组件，或者取消 mock |
| 即将 mock 一个方法 | 弄清它的副作用；mock 缓慢/外部的那一层 |
| 构造 mock 响应 | 完整镜像真实结构 |
| 需要只有测试用到的清理逻辑 | 放进测试工具 |
| 看着 mock 搭建越来越庞大 | 改用真实组件的集成测试 |
| 写完一个测试文件 | 跑一遍变异检查 |

## 警告信号

- 搭建与断言共用同一个对象，保证了两者相等
- 只有 panic、崩溃或找不到选择器时测试才会失败
- 每次刻意的改动都让测试失败，真正的意外破坏却从不被抓住
- 期望值藏在循环、构建器或辅助函数后面
- 测试 grep 源码文本，或断言某个已删除的符号仍然被删除
- 如果只剩下框架、这个测试还照样有意义
- 这个测试是为覆盖率而存在的，没有检查任何副作用或结果
- 断言检查的是一个 `*-mock` 测试 ID，或者一旦移除 mock 就会失败
- 某个方法只有测试文件在调用
- mock 搭建超过测试的一半，或者你解释不清为什么需要这个 mock
- 为了「保险起见」而 mock
