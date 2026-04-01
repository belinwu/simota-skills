# Form Interaction Patterns

Purpose: Choose the right validation strategy, error display, step flow, defaults, and submission feedback for forms.

## Contents

- Validation strategy
- Error display
- Multi-step forms
- Affordances and help
- Defaults
- Submission and unsaved changes
- Accessibility checklist

## Validation Strategy

| Strategy | Use it for | Trade-off |
|----------|------------|-----------|
| Real-time | format-specific fields such as email, URL, phone, password strength | immediate help, but can interrupt typing |
| On-blur | most text fields | low interruption, still timely |
| On-submit | cross-field or complex validation | all issues at once |
| Debounced | async checks such as username availability | slower, but avoids request spam |

Rules:

- use `aria-invalid` on invalid fields
- connect errors with `aria-describedby`
- announce blocking errors via `role="alert"` or `aria-live`

## Error Display

- keep field-level errors specific and actionable
- use an error summary when submit-time validation returns multiple errors
- provide recovery actions for non-field failures

Preferred pattern:

1. identify the field or action
2. explain what is wrong
3. tell the user how to fix it

## Multi-Step Forms

- show clear step progress
- allow safe back navigation
- persist step data
- avoid more than `7+` steps before reconsidering the flow design

## Affordances And Help

- use real labels; placeholder is not a label
- add helper text when the format is non-obvious
- use character counters only when limits matter
- use tooltips for optional help, not critical instructions

## Defaults

- prefer smart defaults when confidence is high
- make defaults easy to inspect and change
- never hide risky auto-filled values

## Submission And Unsaved Changes

- submit buttons need idle, loading, success, and error states
- disable duplicate submission while the request is active
- warn before discarding unsaved changes
- for destructive form actions, prefer confirm or undo patterns

## Passkeys and Modern Authentication

Prefer passwordless flows when the platform supports them.

| Flow | Trigger | Notes |
|------|---------|-------|
| Passkey creation | registration or settings | use `navigator.credentials.create()` with WebAuthn |
| Passkey sign-in | login page | use `navigator.credentials.get()` with conditional UI |
| Magic link | fallback for unsupported devices | send to email, expire after single use |
| OTP fallback | SMS or TOTP app | add `autocomplete="one-time-code"` to the input |

Identifier-first flow: collect email or username on step 1, then determine the best credential method on step 2. Do not reveal whether an account exists during step 1 (prevents account enumeration).

WebAuthn Conditional UI (autofill-based passkey prompt):

```typescript
if (
  window.PublicKeyCredential &&
  PublicKeyCredential.isConditionalMediationAvailable
) {
  const available = await PublicKeyCredential.isConditionalMediationAvailable();
  if (available) {
    // Add autocomplete="username webauthn" to the username input
    // Then call get() with mediation: 'conditional'
    const credential = await navigator.credentials.get({
      publicKey: {
        challenge: serverChallenge,
        rpId: window.location.hostname,
        userVerification: 'preferred',
        allowCredentials: [],
      },
      mediation: 'conditional',
    });
  }
}
```

UX rules:

- always offer a visible alternative (password or magic link) alongside passkeys
- do not block password-manager autofill — use standard `autocomplete` attributes
- show clear error messages when biometric verification fails, with a retry path
- never require the user to remember a passkey ID — device handles it

## Accessibility Checklist

- labels and grouping are explicit
- errors are announced
- tab order is logical
- instructions remain visible
- the form works with keyboard only
