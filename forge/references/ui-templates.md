# Forge UI Component Templates

Rapid prototyping UI templates for common patterns.

---

## Basic Form Component

```tsx
// components/prototypes/ContactForm.tsx
import { useState, FormEvent } from 'react';

interface FormData {
  name: string;
  email: string;
  message: string;
}

const INITIAL_STATE: FormData = {
  name: '',
  email: '',
  message: '',
};

export function ContactForm() {
  const [form, setForm] = useState<FormData>(INITIAL_STATE);
  const [errors, setErrors] = useState<Partial<FormData>>({});
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');

  const validate = (): boolean => {
    const newErrors: Partial<FormData> = {};
    if (!form.name) newErrors.name = 'Name is required';
    if (!form.email) newErrors.email = 'Email is required';
    if (form.email && !form.email.includes('@')) newErrors.email = 'Invalid email';
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!validate()) return;

    setStatus('loading');
    // TODO: Replace with actual API call
    console.log('Submitting:', form);
    await new Promise(r => setTimeout(r, 1000)); // Simulate network
    setStatus('success');
  };

  return (
    <form onSubmit={handleSubmit} style={{ maxWidth: 400, margin: '0 auto' }}>
      <div style={{ marginBottom: 16 }}>
        <label style={{ display: 'block', marginBottom: 4 }}>Name</label>
        <input
          type="text"
          value={form.name}
          onChange={e => setForm({ ...form, name: e.target.value })}
          style={{ width: '100%', padding: 8, border: '1px solid #ccc' }}
        />
        {errors.name && <span style={{ color: 'red', fontSize: 12 }}>{errors.name}</span>}
      </div>

      <div style={{ marginBottom: 16 }}>
        <label style={{ display: 'block', marginBottom: 4 }}>Email</label>
        <input
          type="email"
          value={form.email}
          onChange={e => setForm({ ...form, email: e.target.value })}
          style={{ width: '100%', padding: 8, border: '1px solid #ccc' }}
        />
        {errors.email && <span style={{ color: 'red', fontSize: 12 }}>{errors.email}</span>}
      </div>

      <div style={{ marginBottom: 16 }}>
        <label style={{ display: 'block', marginBottom: 4 }}>Message</label>
        <textarea
          value={form.message}
          onChange={e => setForm({ ...form, message: e.target.value })}
          style={{ width: '100%', padding: 8, border: '1px solid #ccc', minHeight: 100 }}
        />
      </div>

      <button
        type="submit"
        disabled={status === 'loading'}
        style={{ padding: '8px 16px', cursor: 'pointer' }}
      >
        {status === 'loading' ? 'Sending...' : 'Submit'}
      </button>

      {status === 'success' && <p style={{ color: 'green' }}>Sent successfully!</p>}
      {status === 'error' && <p style={{ color: 'red' }}>Failed to send</p>}
    </form>
  );
}
```

---

## List with Search and Pagination

```tsx
// components/prototypes/UserList.tsx
import { useState, useMemo } from 'react';

interface User {
  id: string;
  name: string;
  email: string;
  role: string;
}

// Mock data - replace with API call later
const MOCK_USERS: User[] = [
  { id: '1', name: 'Alice Johnson', email: 'alice@example.com', role: 'Admin' },
  { id: '2', name: 'Bob Smith', email: 'bob@example.com', role: 'User' },
  { id: '3', name: 'Carol Williams', email: 'carol@example.com', role: 'User' },
  { id: '4', name: 'David Brown', email: 'david@example.com', role: 'Moderator' },
  { id: '5', name: 'Eve Davis', email: 'eve@example.com', role: 'User' },
];

const PAGE_SIZE = 3;

export function UserList() {
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(1);
  const [sortBy, setSortBy] = useState<'name' | 'email'>('name');

  const filteredUsers = useMemo(() => {
    return MOCK_USERS
      .filter(u =>
        u.name.toLowerCase().includes(search.toLowerCase()) ||
        u.email.toLowerCase().includes(search.toLowerCase())
      )
      .sort((a, b) => a[sortBy].localeCompare(b[sortBy]));
  }, [search, sortBy]);

  const paginatedUsers = filteredUsers.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE);
  const totalPages = Math.ceil(filteredUsers.length / PAGE_SIZE);

  return (
    <div style={{ maxWidth: 600, margin: '0 auto' }}>
      {/* Search */}
      <input
        type="text"
        placeholder="Search users..."
        value={search}
        onChange={e => { setSearch(e.target.value); setPage(1); }}
        style={{ width: '100%', padding: 8, marginBottom: 16 }}
      />

      {/* Sort */}
      <select
        value={sortBy}
        onChange={e => setSortBy(e.target.value as 'name' | 'email')}
        style={{ marginBottom: 16, padding: 4 }}
      >
        <option value="name">Sort by Name</option>
        <option value="email">Sort by Email</option>
      </select>

      {/* List */}
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {paginatedUsers.map(user => (
          <li key={user.id} style={{ padding: 12, borderBottom: '1px solid #eee' }}>
            <strong>{user.name}</strong>
            <span style={{ marginLeft: 8, color: '#666' }}>{user.email}</span>
            <span style={{
              marginLeft: 8,
              padding: '2px 6px',
              background: '#e0e0e0',
              borderRadius: 4,
              fontSize: 12
            }}>
              {user.role}
            </span>
          </li>
        ))}
      </ul>

      {/* Empty state */}
      {paginatedUsers.length === 0 && (
        <p style={{ textAlign: 'center', color: '#666' }}>No users found</p>
      )}

      {/* Pagination */}
      <div style={{ display: 'flex', justifyContent: 'center', gap: 8, marginTop: 16 }}>
        <button disabled={page === 1} onClick={() => setPage(p => p - 1)}>
          Previous
        </button>
        <span>Page {page} of {totalPages || 1}</span>
        <button disabled={page >= totalPages} onClick={() => setPage(p => p + 1)}>
          Next
        </button>
      </div>
    </div>
  );
}
```

---

## Modal/Dialog Component

```tsx
// components/prototypes/Modal.tsx
import { ReactNode, useEffect } from 'react';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: ReactNode;
}

export function Modal({ isOpen, onClose, title, children }: ModalProps) {
  // Close on Escape key
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      document.body.style.overflow = 'hidden';
    }
    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = 'unset';
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        background: 'rgba(0,0,0,0.5)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 1000,
      }}
      onClick={onClose}
    >
      <div
        style={{
          background: 'white',
          borderRadius: 8,
          padding: 24,
          maxWidth: 500,
          width: '90%',
          maxHeight: '80vh',
          overflow: 'auto',
        }}
        onClick={e => e.stopPropagation()}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 16 }}>
          <h2 style={{ margin: 0 }}>{title}</h2>
          <button onClick={onClose} style={{ border: 'none', background: 'none', cursor: 'pointer', fontSize: 20 }}>
            ×
          </button>
        </div>
        {children}
      </div>
    </div>
  );
}

// Usage example
export function ModalDemo() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <button onClick={() => setIsOpen(true)}>Open Modal</button>
      <Modal isOpen={isOpen} onClose={() => setIsOpen(false)} title="Confirm Action">
        <p>Are you sure you want to proceed?</p>
        <div style={{ display: 'flex', gap: 8, justifyContent: 'flex-end' }}>
          <button onClick={() => setIsOpen(false)}>Cancel</button>
          <button onClick={() => { console.log('Confirmed!'); setIsOpen(false); }}>
            Confirm
          </button>
        </div>
      </Modal>
    </>
  );
}
```

---

## Card Layout

```tsx
// components/prototypes/ProductCard.tsx
interface Product {
  id: string;
  name: string;
  price: number;
  image: string;
  description: string;
}

const MOCK_PRODUCTS: Product[] = [
  { id: '1', name: 'Wireless Headphones', price: 99.99, image: 'https://via.placeholder.com/200', description: 'High-quality wireless headphones' },
  { id: '2', name: 'Smart Watch', price: 199.99, image: 'https://via.placeholder.com/200', description: 'Feature-rich smart watch' },
  { id: '3', name: 'Laptop Stand', price: 49.99, image: 'https://via.placeholder.com/200', description: 'Ergonomic laptop stand' },
];

function ProductCard({ product }: { product: Product }) {
  return (
    <div style={{
      border: '1px solid #ddd',
      borderRadius: 8,
      overflow: 'hidden',
      transition: 'box-shadow 0.2s',
    }}>
      <img src={product.image} alt={product.name} style={{ width: '100%', height: 150, objectFit: 'cover' }} />
      <div style={{ padding: 16 }}>
        <h3 style={{ margin: '0 0 8px' }}>{product.name}</h3>
        <p style={{ color: '#666', fontSize: 14, margin: '0 0 12px' }}>{product.description}</p>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span style={{ fontWeight: 'bold', fontSize: 18 }}>${product.price}</span>
          <button style={{ padding: '8px 16px', cursor: 'pointer' }}>Add to Cart</button>
        </div>
      </div>
    </div>
  );
}

export function ProductGrid() {
  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))',
      gap: 24,
      padding: 24,
    }}>
      {MOCK_PRODUCTS.map(product => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
}
```

---

## Loading and Error States

```tsx
// components/prototypes/AsyncContent.tsx
import { useState, useEffect, ReactNode } from 'react';

type Status = 'loading' | 'success' | 'error';

interface AsyncContentProps<T> {
  fetchFn: () => Promise<T>;
  children: (data: T) => ReactNode;
}

export function AsyncContent<T>({ fetchFn, children }: AsyncContentProps<T>) {
  const [status, setStatus] = useState<Status>('loading');
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<string>('');

  const load = async () => {
    setStatus('loading');
    try {
      const result = await fetchFn();
      setData(result);
      setStatus('success');
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Unknown error');
      setStatus('error');
    }
  };

  useEffect(() => { load(); }, []);

  if (status === 'loading') {
    return (
      <div style={{ textAlign: 'center', padding: 40 }}>
        <div style={{
          width: 40,
          height: 40,
          border: '4px solid #f3f3f3',
          borderTop: '4px solid #3498db',
          borderRadius: '50%',
          animation: 'spin 1s linear infinite',
          margin: '0 auto',
        }} />
        <p>Loading...</p>
        <style>{`@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }`}</style>
      </div>
    );
  }

  if (status === 'error') {
    return (
      <div style={{ textAlign: 'center', padding: 40, color: '#e74c3c' }}>
        <p>Error: {error}</p>
        <button onClick={load}>Retry</button>
      </div>
    );
  }

  return <>{data && children(data)}</>;
}

// Usage
export function AsyncDemo() {
  const fetchUsers = async () => {
    await new Promise(r => setTimeout(r, 1500)); // Simulate delay
    return [{ id: '1', name: 'Test User' }];
  };

  return (
    <AsyncContent fetchFn={fetchUsers}>
      {users => (
        <ul>
          {users.map(u => <li key={u.id}>{u.name}</li>)}
        </ul>
      )}
    </AsyncContent>
  );
}
```
