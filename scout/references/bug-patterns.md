# Scout Bug Pattern Catalog Reference

Common bug patterns with symptoms, investigation approaches, and typical causes.

## Null/Undefined Reference

**Symptoms:**
- TypeError: Cannot read property 'x' of undefined/null
- Unexpected undefined values in output

**Investigation Approach:**
1. Trace the variable back to its source
2. Check all code paths that can set this variable
3. Look for missing null checks or optional chaining
4. Check async timing (data not loaded yet)

**Common Causes:**
- Missing API response handling
- Race condition in data loading
- Optional property accessed without check
- Array index out of bounds

---

## Race Condition

**Symptoms:**
- Intermittent failures
- "Works sometimes"
- Different results on fast vs slow machines
- Flaky tests

**Investigation Approach:**
1. Add timestamps to logs to identify order of operations
2. Look for shared mutable state
3. Check useEffect cleanup functions
4. Look for missing await/Promise handling
5. Check for event listener cleanup

**Common Causes:**
- Missing await on async operation
- Stale closure capturing old state
- Component unmount during async operation
- Multiple rapid state updates

---

## Off-by-One Error

**Symptoms:**
- Missing first or last item
- Index out of bounds
- Loop runs one too many/few times

**Investigation Approach:**
1. Check loop boundaries (< vs <=)
2. Check array indexing (0-based vs 1-based)
3. Check slice/substring parameters
4. Verify length calculations

**Common Causes:**
- Confusion between length and last index
- Inclusive vs exclusive range
- Fence post error in loops

---

## State Synchronization Issue

**Symptoms:**
- UI shows stale data
- Updates don't reflect immediately
- Inconsistent state across components

**Investigation Approach:**
1. Trace state flow from source to consumer
2. Check for multiple sources of truth
3. Verify state update triggers re-render
4. Look for shallow vs deep comparison issues

**Common Causes:**
- Mutating state instead of creating new reference
- Missing dependency in useEffect
- Derived state out of sync with source
- Cache invalidation issues

---

## Memory Leak

**Symptoms:**
- Performance degrades over time
- Browser/app becomes slow
- Increasing memory usage in DevTools

**Investigation Approach:**
1. Use DevTools Memory tab to take heap snapshots
2. Compare snapshots before/after suspected operation
3. Look for detached DOM nodes
4. Check for unremoved event listeners

**Common Causes:**
- Event listeners not removed on cleanup
- Intervals/timeouts not cleared
- Closures holding references to large objects
- Circular references preventing GC

---

## Infinite Loop/Recursion

**Symptoms:**
- Browser freezes
- Maximum call stack exceeded
- CPU spikes to 100%

**Investigation Approach:**
1. Add counter to suspected loops
2. Check recursion base case
3. Look for circular dependencies
4. Check useEffect dependency arrays

**Common Causes:**
- Missing or incorrect base case
- State update triggering re-render that updates state
- Circular import/dependency
- Infinite re-render cycle

---

## Quick Pattern Identification

| Pattern | Key Symptom | First Check |
|---------|-------------|-------------|
| Null/Undefined | TypeError property access | Stack trace location |
| Race Condition | Intermittent failure | Timing/async code |
| Off-by-One | Missing first/last | Loop boundaries |
| State Sync | Stale UI | State mutation |
| Memory Leak | Slow over time | Event listeners |
| Infinite Loop | Browser freeze | Dependency arrays |
