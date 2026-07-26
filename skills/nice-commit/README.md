# nice-commit

一個安全、需確認的 Git 提交技能：分析**已暫存**的變更，提出一則 Conventional Commit 訊息，並在你明確確認後才執行 `git commit`。預設輸出**正體中文** Conventional Commit。

## 運作流程

技能只處理你已經 `git add` 進暫存區的內容，流程分四步：

1. **Analyze** — 執行 `git diff --cached`，把當下的暫存內容存成一份「快照」，只根據這份快照產生訊息（完全忽略未暫存與未追蹤的變更）。
2. **Propose** — 顯示一則完整的提交訊息草稿，等你回應。
3. **Confirm** — 你回覆 `yes` 才算授權；其他任何回應都不會動到 Git。
4. **Commit** — 授權後會**重新**比對一次暫存內容與先前的快照，逐字相同才提交；若期間暫存內容有變動，會要求你重新確認。

這個「提交前二次比對」是核心防呆機制，避免你在確認訊息後、實際提交前又動了暫存區，卻提交到非預期的內容。

## 基本用法

先 stage 好一個邏輯單位的變更，再請技能提交即可：

```
git add <files>
```

然後說「幫我 commit」之類的話。它會回一則草稿，例如：

```
Proposed commit message:
​```
feat(auth): 新增登入節流機制
​```
Reply `yes` to commit only these staged changes, or provide a revised message.
```

- 想提交 → 回覆 `yes`
- 想改 → 直接給它你要的訊息（它會驗證是否與暫存內容相符，再要求重新確認）
- 不想提交 → 回別的、或不回都行，Git 不會有任何變動

若暫存區是空的，它會提醒你先 stage 一個邏輯單位，不會擅自 `git add`。

## 切換輸出格式

預設是正體中文 Conventional Commit。要其他格式，在請它提交時**明確講出來**：

| 想要的輸出 | 怎麼說 | 範例 |
|---|---|---|
| 正體中文 Conventional Commit（預設） | 直接請它提交 | `feat(auth): 新增登入節流機制` |
| 英文 Conventional Commit | 「用英文的 conventional commit」 | `feat(auth): add login throttling` |
| 純英文句子（無前綴） | 「用英文」 | `Add login throttling` |
| 無前綴標題 | 「不要前綴」/「plain title」 | 預設英文；要中文請一併說明 |
| 其他語言或格式 | 明確指定該格式 | 依你的指定，但不得與暫存內容矛盾 |

長度規則：預設（中文）量整行 subject（含前綴）≤ 50 字元，因中文較密建議約 25 字以內；英文格式整行 < 72 字元。

## 進階

**多行訊息（body / footer）** — 預設只輸出單行。只有在你**明確要求** body 或 footer 時才會產生多行，例如「加上 body 說明為什麼這樣改」或「加一個 BREAKING CHANGE footer」。提交時會用引號 heredoc 逐字保留你確認過的空行與段落。

**破壞性變更（Breaking Change）** — 當變更確定移除公開 API 或既有行為時，會用 `feat!:` 或 `feat(scope)!:` 標示。`BREAKING CHANGE:` footer 只有在你要求多行訊息時才加。

## 安全保護（不會做的事）

以下為絕對禁止、不因任何要求而放寬。此技能唯一會改變狀態的動作是對「已暫存內容」執行 `git commit`：

- 不修改 Git 設定
- 不 `git add` 或碰任何尚未暫存的內容
- 不執行破壞性或改寫歷史的指令（`--force`、`reset --hard`、`rebase`、`filter-branch`），不 push 也不 force-push 到任何分支（含 `main`/`master`）
- 不使用 `--no-verify`，不 amend / reset / 更動既有 commit
- 不切換分支，只在目前分支提交
- 不覆寫作者或時間戳（`--author`、`--date`）
- commit 被 hook 擋下時，回報錯誤即停；修正需你重新 stage 並重新確認，產生**新的** commit（絕不 amend）
- 若暫存 diff 疑似含金鑰、token 或密碼，會先警告，經你明確確認前不提交

## 成功輸出

提交成功後會輸出短 SHA 與 subject，例如：

```
Committed a1b2c3d: feat(auth): 新增登入節流機制
```
