# Handoff Templates

Standardized handoff formats for Relay agent collaboration.

---

## Inbound Handoffs (→ Relay)

### GATEWAY_TO_RELAY

```markdown
## NEXUS_HANDOFF
- **Step**: [N] / **Agent**: Gateway → Relay
- **Summary**: Webhook API endpoint specification for handler implementation

### API Specification
- **Endpoint**: [POST /webhooks/{platform}]
- **Authentication**: [HMAC-SHA256 signature verification]
- **Request format**: [JSON payload with platform-specific structure]
- **Response format**: [200 OK with optional body]

### Requirements
- **Platforms**: [Slack, Discord, etc.]
- **Event types**: [message, interaction, command, etc.]
- **Delivery guarantees**: [at-least-once / exactly-once]
- **Rate limit**: [N requests/second]

### Artifacts
- **OpenAPI spec**: [path to spec file]
- **Event schema**: [path to schema definition]

### Relay Actions Required
- [ ] Design webhook handler middleware chain
- [ ] Implement signature verification per platform
- [ ] Design idempotency strategy
- [ ] Define event routing rules
```

### FORGE_TO_RELAY

```markdown
## NEXUS_HANDOFF
- **Step**: [N] / **Agent**: Forge → Relay
- **Summary**: Bot prototype for production messaging design

### Prototype Overview
- **Bot type**: [Command bot / Conversational / Reactive]
- **Platform**: [Slack / Discord / Telegram / etc.]
- **Commands**: [list of commands implemented]
- **Prototype files**: [path to prototype code]

### Production Requirements
- [ ] Design proper adapter pattern (platform-agnostic core)
- [ ] Add signature verification
- [ ] Implement conversation state management
- [ ] Design rate limiting strategy
- [ ] Add error handling and DLQ
```

---

## Outbound Handoffs (Relay →)

### RELAY_TO_BUILDER

```markdown
## NEXUS_HANDOFF
- **Step**: [N] / **Agent**: Relay → Builder
- **Summary**: Messaging handler design for production implementation

### Design Specification
- **Architecture**: [Adapter pattern / Event-driven / etc.]
- **Unified message schema**: [TypeScript type definitions]
- **Event routing matrix**: [event type → handler mapping]
- **Middleware chain**: [ordered list of middleware]

### Implementation Requirements
- **Channel adapters**: [list of adapters with interface]
- **Webhook handlers**: [list of endpoints with verification]
- **WebSocket server**: [connection management spec]
- **Bot commands**: [command definitions with handlers]

### Type Definitions
```typescript
// Key types to implement (provided inline)
```

### Artifacts
- **Design doc**: [path to design document]
- **Type definitions**: [path to types file]
- **Test specifications**: [path to test specs]

### Builder Actions Required
- [ ] Implement channel adapters per interface spec
- [ ] Implement webhook handler with signature verification
- [ ] Implement WebSocket server with room management
- [ ] Implement command handlers with middleware chain
- [ ] Add error handling and retry logic
```

### RELAY_TO_RADAR

```markdown
## NEXUS_HANDOFF
- **Step**: [N] / **Agent**: Relay → Radar
- **Summary**: Test specifications for messaging handlers

### Test Requirements

#### Webhook Handler Tests
- [ ] Signature verification (valid/invalid/expired)
- [ ] Idempotency (duplicate event handling)
- [ ] Rate limiting (exceeding threshold)
- [ ] Error handling (malformed payload, handler failure)
- [ ] DLQ (failed messages routed correctly)

#### Channel Adapter Tests
- [ ] Inbound normalization (platform message → unified format)
- [ ] Outbound adaptation (unified format → platform message)
- [ ] Feature support detection
- [ ] Error handling for unsupported features

#### WebSocket Tests
- [ ] Connection lifecycle (connect/disconnect/reconnect)
- [ ] Heartbeat mechanism
- [ ] Room management (join/leave/broadcast)
- [ ] Authentication on connection

#### Bot Command Tests
- [ ] Command parsing (valid/invalid/missing args)
- [ ] Conversation state transitions
- [ ] Middleware chain execution order
- [ ] Error handling and user feedback

### Test Data
- **Sample platform payloads**: [path or inline examples]
- **Expected unified messages**: [path or inline examples]
```

### RELAY_TO_SENTINEL

```markdown
## NEXUS_HANDOFF
- **Step**: [N] / **Agent**: Relay → Sentinel
- **Summary**: Security review for messaging integration

### Security Review Areas
- [ ] Webhook signature verification implementation
- [ ] Token storage and rotation
- [ ] Rate limiting effectiveness
- [ ] Input validation (preventing injection via messages)
- [ ] SSRF prevention (user-provided URLs in messages)
- [ ] Credential exposure in logs

### Artifacts
- **Signature verification code**: [path]
- **Token management code**: [path]
- **Rate limit configuration**: [path]

### Known Risks
- [List any identified security concerns]
```

### RELAY_TO_SCAFFOLD

```markdown
## NEXUS_HANDOFF
- **Step**: [N] / **Agent**: Relay → Scaffold
- **Summary**: Infrastructure requirements for messaging services

### Infrastructure Requirements
- **WebSocket server**: [connection capacity, scaling strategy]
- **Message queue**: [technology, capacity, DLQ setup]
- **Redis**: [Pub/Sub for WS scaling, caching, session store]
- **Monitoring**: [health endpoints, alert thresholds]

### Environment Variables
```env
# Platform credentials
SLACK_BOT_TOKEN=
SLACK_SIGNING_SECRET=
DISCORD_BOT_TOKEN=
TELEGRAM_BOT_TOKEN=

# Infrastructure
REDIS_URL=
RABBITMQ_URL=
WEBSOCKET_PORT=
```

### Deployment Requirements
- **Scaling**: [horizontal scaling strategy]
- **Health checks**: [endpoints and intervals]
- **SSL/TLS**: [certificate requirements]
- **Networking**: [ports, firewall rules]
```

### RELAY_TO_CANVAS

```markdown
## NEXUS_HANDOFF
- **Step**: [N] / **Agent**: Relay → Canvas
- **Summary**: Architecture visualization for messaging system

### Diagram Requirements
- [ ] Message flow diagram (inbound → normalize → route → handle → adapt → send)
- [ ] Channel adapter architecture (adapter pattern with platform specifics)
- [ ] WebSocket connection lifecycle (sequence diagram)
- [ ] Event routing flow (event → router → handlers → side effects)
- [ ] Infrastructure topology (servers, queues, databases)

### Key Components
- [List of components to visualize with relationships]
```
