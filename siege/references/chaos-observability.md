# Chaos Engineering & Observability Integration

> カオスエンジニアリングのオブザーバビリティ統合、CI/CD 統合、Game Day 実践知、アンチパターン

## 1. オブザーバビリティ 3 本柱 × カオス実験

### カオス実験における各柱の役割

| Pillar | カオス実験での役割 | 収集すべきデータ |
|--------|-----------------|-----------------|
| **Metrics** | 定常状態のベースライン定義 + 影響の定量測定 | レイテンシ、スループット、エラー率、CPU/メモリ、キューの深さ |
| **Logs** | 障害伝播の詳細追跡 + エラーコンテキスト | 影響サービス、エラーメッセージ内容、リトライ/フェイルオーバー動作 |
| **Traces** | リクエストパスの障害影響可視化 | サービス間依存、障害伝播パス、ボトルネック箇所 |

### Monitoring vs Observability

```
Monitoring（監視）:
  - 既知の障害をアラートで検出
  - 事前定義したダッシュボードで監視
  - 「何が壊れたか」を教えてくれる

Observability（可観測性）:
  - 未知の障害モードを発見
  - システム全体のテレメトリから分析
  - 「なぜ壊れたか」を教えてくれる

カオスエンジニアリングに必要なのは Observability
  → 予測不能な障害連鎖を理解するため
```

---

## 2. カオス実験の CI/CD 統合

### 成熟度別の統合パターン

| Level | 統合方式 | 自動化度 | 環境 |
|-------|---------|---------|------|
| **L1** | 手動 Game Day | なし | ステージング |
| **L2** | リリース前ゲート | 半自動 | ステージング |
| **L3** | PR/Merge パイプライン | 自動 | テスト環境 |
| **L4** | 継続的カオス | 完全自動 | カナリア + 本番 |
| **L5** | AI 駆動カオス | 自律的 | 全環境 |

### L3 統合例（GitHub Actions）

```yaml
resilience-gate:
  runs-on: ubuntu-latest
  needs: [unit-tests, integration-tests]
  steps:
    - name: Deploy to test environment
      run: kubectl apply -f k8s/test/
    - name: Wait for healthy state
      run: kubectl wait --for=condition=ready pod -l app=myapp --timeout=120s
    - name: Capture baseline metrics (5 min)
      run: ./scripts/capture-metrics.sh --duration 300 --output baseline.json
    - name: Inject fault (pod kill)
      run: |
        kubectl delete pod -l app=myapp --wait=false
        sleep 30
    - name: Verify recovery
      run: |
        ./scripts/verify-steady-state.sh --baseline baseline.json --tolerance 10%
    - name: Inject fault (network latency)
      run: |
        kubectl exec deploy/myapp -- tc qdisc add dev eth0 root netem delay 200ms
        sleep 60
        kubectl exec deploy/myapp -- tc qdisc del dev eth0 root
    - name: Verify SLO compliance
      run: ./scripts/check-slo.sh --error-rate 0.1 --p99-latency 1000
```

---

## 3. Game Day 実践知

### 成功する Game Day の 7 原則

| # | 原則 | 実践 |
|---|------|------|
| 1 | **Blameless Culture** | 「誰が」ではなく「何が」にフォーカス、心理的安全性の確保 |
| 2 | **2PM not 2AM** | アラート状態ではなく集中できる時間帯に学ぶ |
| 3 | **3-6 ヶ月前から準備** | SLO 更新、Runbook 整備、オンコール体制確認 |
| 4 | **段階的エスカレーション** | 単一サービス → マルチサービス → ゾーン障害 |
| 5 | **全員参加** | エンジニアだけでなくプロダクト/ビジネスチームも |
| 6 | **定期開催** | 月次/四半期で筋肉記憶を構築、MTTR 30 分以内を目標 |
| 7 | **タイムライン記録** | 全アクションの時系列記録 → ポストモーテムの基礎データ |

### Game Day 失敗パターン

| 失敗パターン | 結果 | 予防策 |
|------------|------|--------|
| **Kill switch 未テスト** | 障害注入を停止できず本番影響 | 事前に kill switch の動作確認必須 |
| **ステークホルダー未通知** | カオス実験がインシデントとして報告される | 事前に全関係者に通知 |
| **回復手順が不明確** | 注入後の復旧に時間がかかる | 各実験に rollback 手順を文書化 |
| **メトリクス不足** | 影響の有無が判断できない | 実験前にオブザーバビリティを確認 |
| **スコープ過大** | 予期しないカスケード障害 | 最小ブラストラディウスから開始 |

---

## 4. カオスエンジニアリング・アンチパターン

| # | アンチパターン | 説明 | 対策 |
|---|-------------|------|------|
| **CA-01** | **Blindfolded Chaos** | オブザーバビリティなしでの実験 | メトリクス/ログ/トレース基盤を先に構築 |
| **CA-02** | **Big Bang Experiment** | 最初から本番で大規模障害注入 | ステージング → カナリア → 本番の段階的拡大 |
| **CA-03** | **Chaos without Hypothesis** | 仮説なしの「壊してみよう」 | 実験前に定常状態仮説を必ず定義 |
| **CA-04** | **One-Off Game Day** | 年 1 回の Game Day で満足 | 月次開催 + CI/CD 統合で継続的カオス |
| **CA-05** | **Findings Without Actions** | 発見した弱点を修正しない | 各発見に P0-P3 の修正アクションを割り当て |
| **CA-06** | **Copy-Paste Experiments** | 他社の実験をそのまま適用 | 自社アーキテクチャ固有の障害モードから設計 |
| **CA-07** | **Chaos as Blame Tool** | 障害検出を個人の責任追及に利用 | Blameless 文化の徹底 |

---

## 5. AI 駆動カオスエンジニアリング（2024-2025 トレンド）

```
最新のプラットフォームでの AI 活用:
  1. アーキテクチャ分析から障害シナリオを自動生成
  2. 過去のインシデントデータから高リスク領域を推定
  3. 実験結果からの自動洞察抽出
  4. 異常検出の自動化（人間が見落とすパフォーマンス劣化を検出）

ツール例:
  - Steadybit: 実験の自動設計 + 実行
  - Gremlin: AI-based scenario recommendation
  - Litmus 3.0: GitOps ベースの継続的カオス
```

**Source:** [Last9: Observability + Chaos Engineering](https://last9.io/blog/how-to-build-observability-into-chaos-engineering/) · [DevOps Institute: Chaos Engineering Observability](https://www.devopsinstitute.com/the-practice-of-chaos-engineering-observability/) · [Steadybit: Chaos Experiments](https://steadybit.com/blog/chaos-experiments/) · [PYMNTS: AWS Game Day](https://www.pymnts.com/news/security-and-risk/2024/chaos-engineering-aws-chief-technologist-on-preparing-for-the-unexpected/) · [InfoQ: Chaos Conf](https://www.infoq.com/articles/chaos-conf-learning-leading-experiments/)
