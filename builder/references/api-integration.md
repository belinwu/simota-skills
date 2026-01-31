# API Integration Patterns Reference

Builder agent's API integration implementation patterns.

## REST Client with Retry

```typescript
interface RetryConfig {
  maxRetries: number;
  baseDelay: number;
  maxDelay: number;
  retryableStatuses: number[];
}

class ApiClient {
  private readonly config: RetryConfig = {
    maxRetries: 3,
    baseDelay: 1000,
    maxDelay: 10000,
    retryableStatuses: [408, 429, 500, 502, 503, 504],
  };

  async request<T>(options: RequestOptions): Promise<Result<T, ApiError>> {
    let lastError: ApiError | null = null;

    for (let attempt = 0; attempt <= this.config.maxRetries; attempt++) {
      try {
        const response = await fetch(options.url, {
          method: options.method,
          headers: {
            'Content-Type': 'application/json',
            ...options.headers,
          },
          body: options.body ? JSON.stringify(options.body) : undefined,
          signal: AbortSignal.timeout(options.timeout ?? 30000),
        });

        if (!response.ok) {
          const shouldRetry = this.config.retryableStatuses.includes(response.status);
          if (shouldRetry && attempt < this.config.maxRetries) {
            await this.delay(attempt);
            continue;
          }
          return err(new ApiError(response.status, await response.text()));
        }

        const data = await response.json();
        return ok(data as T);

      } catch (error) {
        lastError = this.handleError(error);
        if (attempt < this.config.maxRetries) {
          await this.delay(attempt);
          continue;
        }
      }
    }

    return err(lastError ?? new ApiError(0, 'Unknown error'));
  }

  private delay(attempt: number): Promise<void> {
    const delay = Math.min(
      this.config.baseDelay * Math.pow(2, attempt),
      this.config.maxDelay
    );
    return new Promise(resolve => setTimeout(resolve, delay));
  }
}
```

## Rate Limiter

```typescript
class RateLimiter {
  private tokens: number;
  private lastRefill: number;

  constructor(
    private readonly maxTokens: number,
    private readonly refillRate: number // tokens per second
  ) {
    this.tokens = maxTokens;
    this.lastRefill = Date.now();
  }

  async acquire(): Promise<void> {
    this.refill();

    if (this.tokens < 1) {
      const waitTime = (1 - this.tokens) / this.refillRate * 1000;
      await new Promise(resolve => setTimeout(resolve, waitTime));
      this.refill();
    }

    this.tokens -= 1;
  }

  private refill(): void {
    const now = Date.now();
    const elapsed = (now - this.lastRefill) / 1000;
    this.tokens = Math.min(this.maxTokens, this.tokens + elapsed * this.refillRate);
    this.lastRefill = now;
  }
}

// Usage with API client
class RateLimitedApiClient extends ApiClient {
  constructor(private readonly limiter: RateLimiter) {
    super();
  }

  async request<T>(options: RequestOptions): Promise<Result<T, ApiError>> {
    await this.limiter.acquire();
    return super.request(options);
  }
}
```

## GraphQL Client

```typescript
interface GraphQLResponse<T> {
  data?: T;
  errors?: GraphQLError[];
}

class GraphQLClient {
  constructor(
    private readonly endpoint: string,
    private readonly headers: Record<string, string> = {}
  ) {}

  async query<T, V extends Record<string, unknown>>(
    query: string,
    variables?: V
  ): Promise<Result<T, GraphQLClientError>> {
    const response = await fetch(this.endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...this.headers,
      },
      body: JSON.stringify({ query, variables }),
    });

    const result: GraphQLResponse<T> = await response.json();

    if (result.errors && result.errors.length > 0) {
      return err(new GraphQLClientError(result.errors));
    }

    if (!result.data) {
      return err(new GraphQLClientError([{ message: 'No data returned' }]));
    }

    return ok(result.data);
  }

  async mutation<T, V extends Record<string, unknown>>(
    mutation: string,
    variables: V
  ): Promise<Result<T, GraphQLClientError>> {
    return this.query<T, V>(mutation, variables);
  }
}
```

## WebSocket Manager

```typescript
type ConnectionState = 'connecting' | 'connected' | 'disconnected' | 'reconnecting';

class WebSocketManager<TMessage> {
  private ws: WebSocket | null = null;
  private state: ConnectionState = 'disconnected';
  private reconnectAttempts = 0;
  private readonly maxReconnectAttempts = 5;
  private messageQueue: TMessage[] = [];

  constructor(
    private readonly url: string,
    private readonly handlers: {
      onMessage: (message: TMessage) => void;
      onStateChange: (state: ConnectionState) => void;
    }
  ) {}

  connect(): void {
    this.setState('connecting');
    this.ws = new WebSocket(this.url);

    this.ws.onopen = () => {
      this.setState('connected');
      this.reconnectAttempts = 0;
      this.flushQueue();
    };

    this.ws.onmessage = (event) => {
      const message = JSON.parse(event.data) as TMessage;
      this.handlers.onMessage(message);
    };

    this.ws.onclose = () => {
      this.setState('disconnected');
      this.attemptReconnect();
    };

    this.ws.onerror = () => {
      this.ws?.close();
    };
  }

  send(message: TMessage): void {
    if (this.state === 'connected' && this.ws) {
      this.ws.send(JSON.stringify(message));
    } else {
      this.messageQueue.push(message);
    }
  }

  private attemptReconnect(): void {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      return;
    }

    this.setState('reconnecting');
    this.reconnectAttempts++;

    const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
    setTimeout(() => this.connect(), delay);
  }

  private flushQueue(): void {
    while (this.messageQueue.length > 0) {
      const message = this.messageQueue.shift();
      if (message) this.send(message);
    }
  }

  private setState(state: ConnectionState): void {
    this.state = state;
    this.handlers.onStateChange(state);
  }
}
```
