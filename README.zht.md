# Tuvix Shih（ninthday）的 Skills

由 [Tuvix Shih](https://github.com/ninthday) 整理、供實務軟體開發工作流程使用的 [Agent Skills](https://agentskills.io/)。

## 安裝

安裝所有已封裝的 skill：

```bash
npx skills@latest add ninthday/skills-base
```

全域安裝所有 skill：

```bash
npx skills@latest add ninthday/skills-base -g
```

## Skills

### 自行維護的 Skills

由 Tuvix Shih 依個人偏好、經驗與建議維護的 skill。

| Skill | 說明 | 來源 |
|-------|------|------|
| [nice-commit](skills/nice-commit/SKILL.md) | 為目前的 Git 變更產生 Conventional Commit 訊息；預設使用正體中文。 | Tuvix Shih |

### 匯入的 Skills

以下 skill 目前已封裝於 `skills/`。

| Skill | 說明 | 來源 |
|-------|------|------|
| [grill-with-docs](skills/grill-with-docs/SKILL.md) | 在建立 ADR 與術語表條目的同時，嚴格檢驗計畫或設計。 | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [grilling](skills/grilling/SKILL.md) | 不斷質疑計畫、決策或想法，以揭露尚未解決的假設。 | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [domain-modeling](skills/domain-modeling/SKILL.md) | 建立並完善專案的領域模型、術語與架構決策。 | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [tdd](skills/tdd/SKILL.md) | 以測試驅動開發工作流程建立功能與修正問題。 | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [diagnosing-bugs](skills/diagnosing-bugs/SKILL.md) | 對錯誤與效能退化採用嚴謹的診斷迴圈。 | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [improve-codebase-architecture](skills/improve-codebase-architecture/SKILL.md) | 找出可深化程式碼庫架構的機會，並以視覺化報告呈現。 | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [prototype](skills/prototype/SKILL.md) | 建立一次性原型以回答設計問題。 | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [to-spec](skills/to-spec/SKILL.md) | 將目前對話彙整為規格，並發布到議題追蹤系統。 | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [handoff](skills/handoff/SKILL.md) | 將目前對話濃縮為供其他 agent 使用的交接文件。 | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [writing-great-skills](skills/writing-great-skills/SKILL.md) | 撰寫或編輯 skill 時，採用可預期的詞彙與原則。 | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [chinese-content-writing-guideline](skills/chinese-content-writing-guideline/SKILL.md) | 使用臺灣術語與慣例撰寫及審閱正體中文內容。 | [jim60105/copilot-prompt](https://github.com/jim60105/copilot-prompt) |
| [drawio-diagrams-enhanced](skills/drawio-diagrams-enhanced/SKILL.md) | 建立 draw.io 圖表，包括流程圖、UML、WBS 與 RACI 矩陣。 | [jim60105/copilot-prompt](https://github.com/jim60105/copilot-prompt) |
| [python-security](skills/python-security/SKILL.md) | 依循 OWASP 指引設計、實作及驗證安全的 Python 應用程式。 | [jim60105/copilot-prompt](https://github.com/jim60105/copilot-prompt) |
| [git-commit](skills/git-commit/SKILL.md) | 分析變更、以合乎邏輯的方式暫存，並建立 Conventional Commit。 | [github/awesome-copilot](https://github.com/github/awesome-copilot) |
| [readme-blueprint-generator](skills/readme-blueprint-generator/SKILL.md) | 根據專案文件與慣例產生儲存庫 README 檔案。 | [github/awesome-copilot](https://github.com/github/awesome-copilot) |

## 使用方式

依名稱安裝單一 skill：

```bash
npx skills@latest add ninthday/skills-base --skill git-commit
```

安裝後，agent 會在 skill 的描述符合任務時載入它。請閱讀各 skill 的 `SKILL.md`，了解其觸發條件與工作流程。

## 產生 Skills

1. 複製此儲存庫。
2. 安裝相依套件：

   ```bash
   uv sync
   ```

3. 在 `meta.py` 設定 skill 來源。
4. 初始化已設定的 Git submodule：

   ```bash
   uv run skills-manager init --yes
   ```

5. 從已初始化的 submodule 同步匯入的 skill：

   ```bash
   uv run skills-manager sync
   ```

6. 對於需產生 skill 的來源專案，依據 [AGENTS.md](AGENTS.md) 建立或更新 skill。

## 封存上游失效 skill

當上游移除某個匯入的 skill 時，`skills-manager` 不會直接刪除本地內容，而是在下一次 `check` 或 `sync` 時記錄此事，並將本地副本封存為歷史快照，使歷程得以保留。

### 偵測

`uv run skills-manager check` 在回報前一定會先 fetch 遠端 tracking ref。任何在 `meta.py` 中設定、但 `skills/<source>` 目錄已從 `@{u}` 消失的匯入來源，都會列在 `Invalid vendor skills:` 區塊內，例如：

```text
All submodules are up to date
Invalid vendor skills:
- example-skill: vendor/example/skills/engineering/example
```

`check` 仍會回傳 exit code `0`，這類訊息僅供參考。

### 封存

`uv run skills-manager sync` 會以更新後的工作樹比對同一份來源清單。針對每個缺失的來源，它會：

1. 在該 skill 的 `SYNC.md` 附加一行 `- **Upstream Removed:** <timestamp>`（UTC 時間，格式為 `YYYYMMDDTHHMMSSZ`）。若已有封存紀錄了失效時間，會直接沿用該時間，確保快照具冪等性。
2. 將仍位於 `skills/<output>/` 的目錄搬移至 `archived-skills/<output>/<timestamp>/`。若該時間戳的資料夾已存在，會自動加上 `-2`、`-3`… 後綴，封存永遠不會被覆寫。
3. 輸出 `Archived invalid vendor skill: <output> → archived-skills/<output>/<timestamp>`。

若來源仍未恢復就再次執行 `sync`，會輸出 `Already archived invalid vendor skill: <output>`，並保留封存不動：

```text
Archived invalid vendor skill: example-skill → archived-skills/example-skill/20260725T120000Z
```

若 active 輸出已不存在、且先前也沒有封存，則 `sync` 會輸出 `Invalid vendor skill has no local output: <output>`，並不會建立空資料夾。

### 行為保證

- 歷史封存不可變動。若上游日後重新提供同名 skill，現有的同步流程會在 `skills/<output>/` 重新建置內容；先前的封存不會被覆寫或刪除。
- `uv run skills-manager cleanup --yes` 只會檢查 `skills/` 中未列於 `meta.py` 的目錄，因此 `archived-skills/` 永遠不會被列為清理候選。


## 致謝

- Skills Manager CLI 改編自 [antfu/skills](https://github.com/antfu/skills)，感謝 [Anthony Fu](https://github.com/antfu)。
- 感謝 [Lucas Yang](https://github.com/ycs77) 與 [ycs77/skills](https://github.com/ycs77/skills) 在想法上的幫忙。

## 作者

Tuvix Shih（tuvix@ninthday.info）

## 授權條款

[GNU Free Documentation License 1.3](LICENSE.md)
