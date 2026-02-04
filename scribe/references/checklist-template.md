# Checklist Templates

## Implementation Checklist Template

```markdown
# Implementation Checklist: [Feature Name]

## Document Info

| Item | Value |
|------|-------|
| Feature | [Feature Name] |
| Related PRD | PRD-[name] |
| Related SRS | SRS-[name] |
| Related Design | HLD/LLD-[name] |
| Author | [Name] |
| Created | YYYY-MM-DD |

---

## Pre-Implementation

### Requirements Verification
- [ ] PRDの要件をすべて確認した
- [ ] SRSの機能要件を理解した
- [ ] 受入条件（Acceptance Criteria）を把握した
- [ ] スコープ外の項目を確認した
- [ ] 依存関係を確認した

### Design Verification
- [ ] HLDのアーキテクチャを理解した
- [ ] LLDのクラス設計を確認した
- [ ] APIインターフェースを確認した
- [ ] データモデルを確認した
- [ ] シーケンス図を確認した

### Environment Setup
- [ ] 開発環境がセットアップされている
- [ ] 必要な依存関係がインストールされている
- [ ] テスト環境にアクセスできる
- [ ] 必要な認証情報を持っている
- [ ] ブランチを作成した

---

## Implementation Phase

### Core Implementation

#### [Component/Module 1]
- [ ] [Task 1.1]: [Description]
- [ ] [Task 1.2]: [Description]
- [ ] [Task 1.3]: [Description]

#### [Component/Module 2]
- [ ] [Task 2.1]: [Description]
- [ ] [Task 2.2]: [Description]

### Data Layer
- [ ] データベースマイグレーションを作成した
- [ ] モデル/エンティティを実装した
- [ ] リポジトリ/DAOを実装した
- [ ] インデックスを確認した

### API Layer
- [ ] エンドポイントを実装した
- [ ] リクエストバリデーションを実装した
- [ ] レスポンスフォーマットを実装した
- [ ] エラーハンドリングを実装した
- [ ] 認証/認可を実装した

### Business Logic
- [ ] サービス層を実装した
- [ ] ビジネスルールを実装した
- [ ] エッジケースを処理した
- [ ] トランザクション管理を実装した

### UI Layer (if applicable)
- [ ] コンポーネントを実装した
- [ ] 状態管理を実装した
- [ ] フォームバリデーションを実装した
- [ ] エラー表示を実装した
- [ ] ローディング状態を実装した

---

## Quality Assurance

### Code Quality
- [ ] コードがLintを通過する
- [ ] コードがフォーマッターを通過する
- [ ] 型エラーがない（TypeScript/静的型付け言語の場合）
- [ ] コードレビューコメントに対応した

### Testing
- [ ] 単体テストを作成した
- [ ] 統合テストを作成した
- [ ] E2Eテストを作成した（必要な場合）
- [ ] すべてのテストが通過する
- [ ] カバレッジ目標を達成した

### Security
- [ ] 入力バリデーションを実装した
- [ ] SQLインジェクション対策を確認した
- [ ] XSS対策を確認した
- [ ] CSRF対策を確認した
- [ ] 認証/認可が正しく動作する
- [ ] 機密情報がログに出力されていない

### Performance
- [ ] N+1クエリがない
- [ ] 適切なインデックスが設定されている
- [ ] キャッシュを適切に使用している
- [ ] パフォーマンス目標を満たしている

---

## Pre-Deployment

### Documentation
- [ ] コードにコメントを追加した
- [ ] APIドキュメントを更新した
- [ ] READMEを更新した
- [ ] 変更履歴を記録した

### Review & Approval
- [ ] セルフレビューを完了した
- [ ] コードレビューを受けた
- [ ] レビューコメントに対応した
- [ ] 承認を得た

### Deployment Preparation
- [ ] マイグレーションスクリプトを確認した
- [ ] ロールバック手順を確認した
- [ ] 環境変数/設定を確認した
- [ ] デプロイ手順を確認した

---

## Sign-off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Developer | | | |
| Reviewer | | | |
| QA | | | |
| Product Owner | | | |

---

## Notes

[Any additional notes, discovered issues, or follow-up items]

---

## Follow-up Items

| Item | Priority | Owner | Due Date |
|------|----------|-------|----------|
| [Item 1] | High/Med/Low | [Name] | YYYY-MM-DD |
```

---

## Review Checklist Template

```markdown
# Code Review Checklist: [PR/MR Title]

## Review Info

| Item | Value |
|------|-------|
| PR/MR Number | #[number] |
| Author | [Name] |
| Reviewer | [Name] |
| Review Date | YYYY-MM-DD |
| Related Issue | [Issue link] |

---

## Functional Review

### Requirements Compliance
- [ ] 要件どおりに実装されている
- [ ] 受入条件を満たしている
- [ ] エッジケースが処理されている
- [ ] エラーケースが適切に処理されている

### Business Logic
- [ ] ビジネスルールが正しく実装されている
- [ ] 計算ロジックが正確である
- [ ] 状態遷移が正しい
- [ ] データの整合性が保たれている

---

## Code Quality Review

### Readability
- [ ] コードが理解しやすい
- [ ] 変数名/関数名が適切
- [ ] コメントが適切に使用されている
- [ ] 複雑なロジックに説明がある

### Structure
- [ ] 関数/メソッドが適切なサイズ
- [ ] 単一責任の原則に従っている
- [ ] 適切な抽象化レベル
- [ ] 重複コードがない

### Consistency
- [ ] プロジェクトの規約に従っている
- [ ] 既存のパターンと一貫している
- [ ] 命名規則に従っている
- [ ] フォーマットが統一されている

---

## Technical Review

### Architecture
- [ ] アーキテクチャに適合している
- [ ] 適切なレイヤーに実装されている
- [ ] 依存関係の方向が正しい
- [ ] モジュール間の結合度が適切

### Error Handling
- [ ] 例外が適切に処理されている
- [ ] エラーメッセージが適切
- [ ] エラーがログに記録される
- [ ] リカバリー処理がある（必要な場合）

### Performance
- [ ] 明らかな性能問題がない
- [ ] N+1クエリがない
- [ ] 不要なループ/計算がない
- [ ] メモリリークの可能性がない

### Security
- [ ] 入力バリデーションがある
- [ ] インジェクション攻撃対策がある
- [ ] 認証/認可が正しい
- [ ] 機密情報が露出していない

---

## Testing Review

### Test Coverage
- [ ] 単体テストが十分
- [ ] エッジケースがテストされている
- [ ] エラーケースがテストされている
- [ ] 統合テストがある（必要な場合）

### Test Quality
- [ ] テストが独立している
- [ ] テストが明確で理解しやすい
- [ ] モックの使用が適切
- [ ] アサーションが適切

---

## Documentation Review

- [ ] コードコメントが適切
- [ ] APIドキュメントが更新されている
- [ ] READMEが更新されている（必要な場合）
- [ ] 変更内容がPR説明に記載されている

---

## Review Result

### Status
- [ ] Approved
- [ ] Request Changes
- [ ] Comment

### Summary

**Good Points:**
- [Good point 1]
- [Good point 2]

**Issues Found:**
| Severity | Location | Issue | Suggestion |
|----------|----------|-------|------------|
| Critical/Major/Minor | file:line | [Issue] | [Suggestion] |

### Comments
[Additional comments]

---

## Sign-off

| Reviewer | Decision | Date |
|----------|----------|------|
| [Name] | Approved/Request Changes | YYYY-MM-DD |
```

---

## Quick Checklist (Minimal)

For smaller changes, use this minimal checklist:

```markdown
# Quick Implementation Checklist: [Feature]

## Before Coding
- [ ] 要件を理解した
- [ ] 影響範囲を確認した
- [ ] ブランチを作成した

## Implementation
- [ ] 機能を実装した
- [ ] エラーハンドリングを追加した
- [ ] テストを作成した

## Before PR
- [ ] Lint/Formatが通る
- [ ] テストが通る
- [ ] セルフレビューした
- [ ] PR説明を書いた

## Notes
[Any notes]
```

---

## Checklist Quality Guidelines

### Good Checklist Items
- 具体的で検証可能
- 1つのアクションに対応
- 完了/未完了が明確
- 担当者が判断できる

### Bad Checklist Items (Avoid)
- ❌ 「コードがきれい」（主観的）
- ❌ 「パフォーマンスが良い」（曖昧）
- ❌ 「すべてのケースをテスト」（検証不能）
- ❌ 「適切に実装」（不明確）

### Better Alternatives
- ✅ 「ESLintエラーが0件」
- ✅ 「p95レイテンシが200ms以下」
- ✅ 「正常系・異常系・境界値のテストがある」
- ✅ 「SRS FR-001の仕様どおりに実装」
