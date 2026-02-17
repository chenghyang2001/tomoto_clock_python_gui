<!--
=== Sync Impact Report ===
Version change: N/A → 1.0.0 (initial ratification)
Modified principles: N/A (first version)
Added sections:
  - Core Principles (3): 簡潔優先、標準庫優先、可維護性
  - 技術約束
  - 開發流程
  - Governance
Removed sections: N/A
Templates requiring updates:
  - .specify/templates/plan-template.md ✅ compatible (Constitution Check section is generic)
  - .specify/templates/spec-template.md ✅ compatible (no principle-specific references)
  - .specify/templates/tasks-template.md ✅ compatible (phase structure is generic)
Follow-up TODOs: None
===========================
-->

# 番茄時鐘 Constitution

## Core Principles

### I. 簡潔優先 (Simplicity First)

所有功能實作 MUST 選擇最簡單且能正確運作的方案。

- 嚴格遵守 YAGNI（You Aren't Gonna Need It）原則：
  不為假設性的未來需求撰寫程式碼
- 每個函式 MUST 只做一件事，且該件事 MUST 能用一句話描述
- 新增抽象層之前 MUST 先確認至少有三處重複邏輯，
  否則直接撰寫具體實作
- 程式碼行數本身不是目標，但冗餘程式碼 MUST 被刪除

**理由**：番茄時鐘是一個聚焦型桌面工具，複雜度應與其用途
相稱。過度設計會拖慢開發節奏且增加維護負擔。

### II. 標準庫優先 (Standard Library First)

GUI 框架使用 Tkinter，其餘功能 MUST 優先使用 Python 標準庫。

- GUI 層 MUST 使用 Tkinter（Python 內建，零外部依賴）
- 引入任何第三方套件之前 MUST 先確認標準庫無法滿足需求，
  並在 commit message 或 PR 中記錄引入理由
- 若必須使用第三方套件，SHOULD 優先選擇無額外子依賴的
  純 Python 套件
- 打包與發佈 SHOULD 確保使用者無需手動安裝額外依賴即可執行

**理由**：最小化依賴可降低安裝門檻、減少版本衝突風險，
並確保專案在各 Python 版本間的可攜性。

### III. 可維護性 (Maintainability)

程式碼結構 MUST 讓任何熟悉 Python 的開發者能在 10 分鐘內
理解單一模組的用途與邊界。

- 模組劃分 MUST 遵循單一職責原則：UI 邏輯、計時邏輯、
  設定管理各自獨立
- 變數與函式命名 MUST 使用描述性英文名稱，遵循 PEP 8
- 註解與 docstring MUST 使用繁體中文，說明「為什麼」
  而非「做了什麼」
- 任何超過 50 行的函式 SHOULD 被拆分為更小的子函式

**理由**：清晰的結構與命名讓未來的修改與除錯成本可預測，
避免「只有原作者看得懂」的窘境。

## 技術約束

- **語言**：Python 3.10+
- **GUI 框架**：Tkinter（標準庫內建）
- **目標平台**：Windows（主要），macOS / Linux（次要）
- **程式碼風格**：PEP 8，使用 `ruff` 或 `flake8` 做靜態檢查
- **型別提示**：公開介面 MUST 附帶型別提示（type hints），
  內部輔助函式 SHOULD 附帶
- **文件語言**：繁體中文（程式碼本體保留英文，
  註解與文件使用繁體中文）

## 開發流程

- 每次功能變更 MUST 對應一個清晰的 commit，
  commit message 使用繁體中文
- 合併前 MUST 確認程式可正常啟動且核心功能運作正常
- 重構 MUST 與功能變更分開提交，不可混在同一個 commit
- 發現 bug 時 SHOULD 先撰寫重現測試再修復

## Governance

本憲法為番茄時鐘專案的最高開發準則。所有設計決策與程式碼
變更 MUST 符合上述原則。

- **修訂流程**：任何原則的新增、移除或重新定義 MUST 更新
  本憲法並遞增版本號
- **版本策略**：遵循語意版本（SemVer）——
  MAJOR：原則移除或不相容的重新定義；
  MINOR：新增原則或大幅擴充指引；
  PATCH：措辭修正、錯字修復、非語意性調整
- **合規檢查**：每次 `/speckit.plan` 執行時 MUST 在
  Constitution Check 階段驗證設計是否符合本憲法

**Version**: 1.0.0 | **Ratified**: 2026-02-17 | **Last Amended**: 2026-02-17
