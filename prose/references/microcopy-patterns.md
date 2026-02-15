# Microcopy Patterns

ボタンラベル、ツールチップ、空状態パターンのリファレンス。

---

## Button Labels

### Action Button Patterns

| Pattern | Good | Bad | Why |
|---------|------|-----|-----|
| **Specific verb** | "Save changes" | "Submit" | User knows what happens |
| **Object included** | "Delete account" | "Delete" | Clear what's affected |
| **Outcome-focused** | "Get started" | "Continue" | Motivates action |
| **Confirm context** | "Yes, cancel order" | "OK" | Prevents mistakes |

### Primary Action Guidelines

```markdown
## Rules
1. Use verb + noun: "Create project", "Send invite"
2. Match the page context: billing page → "Update payment method"
3. Limit to 3-4 words maximum
4. Use sentence case, not Title Case or ALL CAPS
5. Avoid generic labels: "Submit", "OK", "Click here"

## Destructive Actions
- Use specific consequence: "Delete 3 files" not "Delete"
- Pair with confirmation: "This cannot be undone"
- Use warning color (red) + explicit label
```

### Button State Text

| State | Label | Example |
|-------|-------|---------|
| **Default** | Action verb | "Save changes" |
| **Loading** | Progressive verb + ... | "Saving..." |
| **Success** | Past tense + check | "Saved ✓" |
| **Error** | "Try again" or specific | "Retry save" |
| **Disabled** | Same as default (grey) | "Save changes" (greyed) |

---

## Tooltips

### When to Use Tooltips

| Use | Don't Use |
|-----|-----------|
| Icon-only buttons need text labels | Critical information (use inline text) |
| Abbreviated or truncated text | Form field instructions (use help text) |
| Additional context for power users | Mobile-primary interfaces |
| Keyboard shortcut hints | Content that needs to be read fully |

### Tooltip Writing Guidelines

```markdown
1. Keep under 150 characters (1-2 short sentences)
2. Start with a verb for actions: "Edit your profile name"
3. Use noun phrase for info: "Your current subscription plan"
4. No period for single phrases; period for full sentences
5. Don't repeat the visible label
```

### Examples

| Element | Visible | Tooltip |
|---------|---------|---------|
| Icon button | 🔔 | "Notification settings" |
| Truncated text | "Project Al..." | "Project Alpha Release v2.1" |
| Status badge | "Pro" | "Pro plan — 50 GB storage, priority support" |
| Shortcut | "Save" | "Save changes (⌘S)" |

---

## Empty States

### Empty State Structure

```
┌─────────────────────────────────────┐
│          [Illustration]             │
│                                     │
│     Primary message (what)          │
│   Secondary message (why/how)       │
│                                     │
│      [Primary CTA button]          │
│       Secondary action link         │
└─────────────────────────────────────┘
```

### Empty State Types

| Type | Tone | Example |
|------|------|---------|
| **First use** | Welcoming, encouraging | "Create your first project to get started" |
| **No results** | Helpful, suggestive | "No results for 'xyz'. Try different keywords" |
| **Cleared** | Positive, accomplished | "All caught up! No new notifications" |
| **Error** | Empathetic, actionable | "Couldn't load your data. Check your connection" |
| **Permission** | Clear, directing | "You need admin access to view this page" |

### Empty State Copy Template

```markdown
## [Feature] Empty State

### Primary message
[What the user sees — clear, concise statement]

### Secondary message
[Why it's empty OR how to fill it — 1-2 sentences max]

### CTA
[Specific action button: "Create first [item]" / "Import [items]"]

### Example:
Primary: "No team members yet"
Secondary: "Invite your team to collaborate on projects together."
CTA: "Invite team members"
```

---

## Form Labels & Help Text

### Label Patterns

| Pattern | Example | Use |
|---------|---------|-----|
| **Noun label** | "Email address" | Standard form fields |
| **Question label** | "What's your company name?" | Conversational forms |
| **Action label** | "Choose a password" | Onboarding flows |

### Help Text Guidelines

```markdown
## Rules
1. Place below the field, not in placeholder
2. Show before the user needs it (not after error)
3. Keep to one line (under 80 characters)
4. Use specific constraints: "8+ characters with a number"
5. Never duplicate the label

## Examples
✅ "We'll use this to send you order updates"
✅ "Must be at least 8 characters"
❌ "Enter your email" (duplicates label)
❌ "This field is required" (show only on error)
```

### Placeholder Text

| Do | Don't |
|----|-------|
| Show format: "MM/DD/YYYY" | Repeat the label: "Enter email" |
| Show example: "e.g., Acme Corp" | Put instructions in placeholder |
| Keep shorter than the field width | Use placeholder as the only label |
