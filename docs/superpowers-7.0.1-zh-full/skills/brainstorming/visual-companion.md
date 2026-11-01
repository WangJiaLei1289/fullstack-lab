# 可视化伴侣指南

基于浏览器的可视化头脑风暴伴侣，用来展示模型稿、示意图和选项。

## 何时使用

逐题判断，而不是逐会话判断。判断标准：**用户看见它，会不会比读它更有助于理解？**

**用浏览器**——当内容本身是视觉性的：

- **UI 模型稿** —— 线框图、布局、导航结构、组件设计
- **架构图** —— 系统组件、数据流、关系图
- **并排视觉对比** —— 比较两种布局、两套配色、两个设计方向
- **设计打磨** —— 当问题关乎观感与手感、间距、视觉层级时
- **空间关系** —— 状态机、流程图、以图形呈现的实体关系

**用终端**——当内容属于文字或表格时：

- **需求与范围问题** —— 「X 是什么意思？」「哪些功能在范围内？」
- **概念性的 A/B/C 选择** —— 在文字描述的做法之间做取舍
- **权衡清单** —— 优缺点、对比表格
- **技术决策** —— API 设计、数据建模、架构方案选择
- **澄清式提问** —— 凡是答案是一段话、而不是视觉偏好的问题

*关于* UI 话题的问题，并不自动就是可视化问题。「你想要什么样的向导？」是概念问题——用终端。「这几种向导布局里，哪个感觉对？」是可视化问题——用浏览器。

## 运作方式

服务器监视一个目录里的 HTML 文件，把最新的一个送给浏览器。你把 HTML 内容写进 `screen_dir`，用户在浏览器里看到它，可以点选选项。选择会被记录到 `state_dir/events`，你在下一个回合读取它。

**内容片段 vs 完整文档：** 如果你的 HTML 文件以 `<!DOCTYPE` 或 `<html` 开头，服务器就原样送出（只注入辅助脚本）。否则，服务器会把你的内容自动包进框架模板——加上页头、CSS 主题、连接状态和全部交互基础设施。**默认写内容片段。** 只有需要完全掌控页面时，才写完整文档。

## 启动会话

```bash
# Start AFTER the user approves the companion. --open auto-opens their browser on
# the first screen; --project-dir persists mockups and enables same-port restart.
bash scripts/start-server.sh --project-dir /path/to/project --open

# Returns: {"type":"server-started","port":52341,
#           "url":"http://localhost:52341/?key=ab12…",
#           "screen_dir":"/path/to/project/.superpowers/brainstorm/12345-1706000000/content",
#           "state_dir":"/path/to/project/.superpowers/brainstorm/12345-1706000000/state"}
```

从返回结果里记下 `screen_dir` 和 `state_dir`。用 `--open` 时，你推第一屏时浏览器会自己打开——不需要请用户去打开，但仍要把 URL 发出去做兜底（无头/远程环境不会自动打开）。

**URL 里含会话密钥（`?key=…`）。** 服务器会拒绝任何不带它的请求，所以始终要把 `url` 字段里的**完整** URL 给用户——绝不剥掉查询串，也绝不要给出一个光秃秃的 `http://host:port`。这把密钥把守着 HTTP 和 WebSocket 访问，这样误开的浏览器标签页或网络上的另一台机器就无法读取这些屏幕或注入事件。首次加载之后，浏览器会通过 cookie 记住密钥，所以刷新和 `/files/*` 资源都不必再带它。

**找到连接信息：** 服务器会把启动 JSON 写进 `$STATE_DIR/server-info`。如果你在后台启动了服务器、没抓到 stdout，就读这个文件拿到 URL 和端口。用 `--project-dir` 时，去 `<project>/.superpowers/brainstorm/` 下找会话目录。

**注意：** 把项目根目录作为 `--project-dir` 传进去，这样模型稿会留在 `.superpowers/brainstorm/` 里，服务器重启也还在。不传的话，文件会落到 `/tmp`，然后被清理掉。提醒用户把 `.superpowers/` 加进 `.gitignore`（如果还没有的话）。

**按平台启动服务器：**

**Claude Code：**
```bash
# Default mode works — the script backgrounds the server itself.
bash scripts/start-server.sh --project-dir /path/to/project --open
```

在 Windows 上，脚本会自动检测并切到前台模式（那会阻塞工具调用）。在你的 Bash 工具调用上用 `run_in_background: true`，让服务器能跨对话回合存活，然后在下一个回合读 `$STATE_DIR/server-info` 拿到 URL 和端口。

**Codex：**
```bash
# Codex reaps background processes. The script auto-detects CODEX_CI and
# switches to foreground mode. Run it normally — no extra flags needed.
bash scripts/start-server.sh --project-dir /path/to/project --open
```

**Gemini CLI：**
```bash
# Use --foreground and set is_background: true on your shell tool call
# so the process survives across turns
bash scripts/start-server.sh --project-dir /path/to/project --open --foreground
```

**Copilot CLI：**
```bash
# Start it with Copilot CLI's non-blocking/background shell mechanism so the
# server survives across turns. Keep --foreground so the harness, not the
# script, owns backgrounding. The launcher is a .sh, so invoke it via bash
# (on Windows, call Git Bash's bash.exe from the PowerShell tool).
bash scripts/start-server.sh --project-dir /path/to/project --open --foreground
```

**其它环境：** 服务器必须在后台持续运行，跨过对话回合。如果你的环境会回收脱离的进程，就用 `--foreground`，并用你平台的背景执行机制来启动这条命令。

如果你的浏览器访问不到这个 URL（远程/容器化环境里很常见），就绑定一个非回环的主机地址：

```bash
bash scripts/start-server.sh \
  --project-dir /path/to/project \
  --host 0.0.0.0 \
  --url-host localhost
```

用 `--url-host` 控制返回的 URL JSON 里打印什么主机名。

## 循环

1. **确认服务器还活着**，然后把 **HTML 写**到 `screen_dir` 里的一个新文件：
   - **必须：在引用 URL 或推送屏幕之前，先确认服务器还活着。** 检查 `$STATE_DIR/server-info` 存在、而 `$STATE_DIR/server-stopped` 不存在。如果它已经关掉了，就用**同一个 `--project-dir`** 通过 `start-server.sh` 重启——它会复用同一个端口，所以用户开着的标签页会自己重连（服务器停着时它显示「已暂停」的浮层），你不需要再发一个新 URL。服务器空闲 4 小时后会自动退出（可用 `--idle-timeout-minutes` 调整）。
   - 用有语义的文件名：`platform.html`、`visual-style.html`、`layout.html`
   - **绝不要复用文件名**——每一屏都用新文件
   - 用你的文件创建工具——**绝不要用 cat/heredoc**（会把噪音灌进终端）
   - 服务器会自动送出最新的文件

2. **告诉用户预期是什么，然后结束你的回合：**
   - 每一步都提醒 URL（不只是第一步）
   - 用简短文字总结屏幕上是什么（例如「正在展示首页的 3 种布局方案」）
   - 请他们在终端里回复：「看一眼，告诉我你觉得怎么样。想选的话点一下选项。」

3. **在你的下一个回合**——用户在终端回复之后：
   - 如果 `$STATE_DIR/events` 存在就读它——里面是用户在浏览器里的交互（点击、选择），按 JSON 行记录
   - 和用户在终端里写的话合并，才能看到全貌
   - 终端里的消息是主要反馈；`state_dir/events` 提供结构化的交互数据

4. **迭代或推进**——如果反馈要改当前这一屏，就写一个新文件（例如 `layout-v2.html`）。当前这一步被确认之后，才进入下一个问题。

5. **回到终端时卸载**——当下一个步骤不需要浏览器（例如一个澄清问题、一场权衡讨论），就推一个等待屏，把过时的内容清掉：

   ```html
   <!-- filename: waiting.html (or waiting-2.html, etc.) -->
   <div style="display:flex;align-items:center;justify-content:center;min-height:60vh">
     <p class="subtitle">Continuing in terminal...</p>
   </div>
   ```

   这能避免用户盯着一个已经解决的选择，而对话已经往前走了。下一个视觉问题到来时，像往常一样推一个新的内容文件。

6. 重复，直到完成。

## 编写内容片段

只写页面内部的内容。服务器会自动把它包进框架模板（页头、主题 CSS、连接状态和全部交互基础设施）。

**最小示例：**

```html
<h2>Which layout works better?</h2>
<p class="subtitle">Consider readability and visual hierarchy</p>

<div class="options">
  <div class="option" data-choice="a" onclick="toggleSelect(this)">
    <div class="letter">A</div>
    <div class="content">
      <h3>Single Column</h3>
      <p>Clean, focused reading experience</p>
    </div>
  </div>
  <div class="option" data-choice="b" onclick="toggleSelect(this)">
    <div class="letter">B</div>
    <div class="content">
      <h3>Two Column</h3>
      <p>Sidebar navigation with main content</p>
    </div>
  </div>
</div>
```

就这样。不需要 `<html>`、不需要 CSS、不需要 `<script>` 标签。这些服务器全都提供了。

## 可用的 CSS 类

框架模板为你的内容提供这些 CSS 类：

### 选项（A/B/C 选择）

```html
<div class="options">
  <div class="option" data-choice="a" onclick="toggleSelect(this)">
    <div class="letter">A</div>
    <div class="content">
      <h3>Title</h3>
      <p>Description</p>
    </div>
  </div>
</div>
```

**多选：** 给容器加上 `data-multiselect`，用户就能选多个选项。每次点击会切换该项的选中样式。

```html
<div class="options" data-multiselect>
  <!-- same option markup — users can select/deselect multiple -->
</div>
```

### 卡片（视觉设计）

```html
<div class="cards">
  <div class="card" data-choice="design1" onclick="toggleSelect(this)">
    <div class="card-image"><!-- mockup content --></div>
    <div class="card-body">
      <h3>Name</h3>
      <p>Description</p>
    </div>
  </div>
</div>
```

### 模型稿容器

```html
<div class="mockup">
  <div class="mockup-header">Preview: Dashboard Layout</div>
  <div class="mockup-body"><!-- your mockup HTML --></div>
</div>
```

### 分栏视图（并排）

```html
<div class="split">
  <div class="mockup"><!-- left --></div>
  <div class="mockup"><!-- right --></div>
</div>
```

### 优缺点

```html
<div class="pros-cons">
  <div class="pros"><h4>Pros</h4><ul><li>Benefit</li></ul></div>
  <div class="cons"><h4>Cons</h4><ul><li>Drawback</li></ul></div>
</div>
```

### 模拟元素（线框积木）

```html
<div class="mock-nav">Logo | Home | About | Contact</div>
<div style="display: flex;">
  <div class="mock-sidebar">Navigation</div>
  <div class="mock-content">Main content area</div>
</div>
<button class="mock-button">Action Button</button>
<input class="mock-input" placeholder="Input field">
<div class="placeholder">Placeholder area</div>
```

### 排版与分区

- `h2` —— 页面标题
- `h3` —— 分区标题
- `.subtitle` —— 标题下方的次要文字
- `.section` —— 带下边距的内容块
- `.label` —— 小号大写的标签文字

## 浏览器事件格式

当用户在浏览器里点击选项时，他们的交互会记录到 `$STATE_DIR/events`（每行一个 JSON 对象）。你推新屏幕时，这个文件会被自动清空。

```jsonl
{"type":"click","choice":"a","text":"Option A - Simple Layout","timestamp":1706000101}
{"type":"click","choice":"c","text":"Option C - Complex Grid","timestamp":1706000108}
{"type":"click","choice":"b","text":"Option B - Hybrid","timestamp":1706000115}
```

完整的事件流展示了用户的探索路径——他们可能在敲定之前点了多个选项。最后一个 `choice` 事件通常就是最终选择，但点击的序列也能透露出犹豫或偏好，值得追问。

如果 `$STATE_DIR/events` 不存在，说明用户没有在浏览器里操作——只用他们终端里的文字。

## 设计提示

- **保真度随问题而定**——布局问题用线框图，打磨问题就用打磨过的稿
- **在每一页上解释问题**——写「哪种布局更专业？」而不是只写「选一个」
- **先迭代再推进**——如果反馈要改当前屏，就写一个新版本
- 每屏最多 **2-4 个选项**
- **该用真实内容时就用**——做摄影作品集就用真实图片（Unsplash）。占位内容会掩盖设计问题。
- **让模型稿保持简单**——聚焦布局与结构，不要追求像素级完美的设计

## 文件命名

- 用有语义的名字：`platform.html`、`visual-style.html`、`layout.html`
- 绝不要复用文件名——每一屏必须是新文件
- 迭代时：加版本后缀，例如 `layout-v2.html`、`layout-v3.html`
- 服务器按修改时间送出最新的文件

## 清理

```bash
bash scripts/stop-server.sh $SESSION_DIR
```

如果这个会话用了 `--project-dir`，模型稿文件会留在 `.superpowers/brainstorm/` 里，供以后参考。只有 `/tmp` 下的会话会在停止时被删除。

## 参考

- 框架模板（CSS 参考）：`scripts/frame-template.html`
- 辅助脚本（客户端）：`scripts/helper.js`
