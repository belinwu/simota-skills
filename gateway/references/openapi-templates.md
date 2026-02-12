# OpenAPI Templates

## Minimal OpenAPI 3.0 Template

```yaml
openapi: '3.0.3'
info:
  title: API Name
  version: '1.0.0'
  description: API description
servers:
  - url: https://api.example.com/v1
paths:
  /resources:
    get:
      summary: List resources
      parameters:
        - $ref: '#/components/parameters/PageParam'
        - $ref: '#/components/parameters/LimitParam'
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ResourceList'
components:
  parameters:
    PageParam:
      name: page
      in: query
      schema: { type: integer, default: 1 }
    LimitParam:
      name: limit
      in: query
      schema: { type: integer, default: 20, maximum: 100 }
  schemas:
    ResourceList:
      type: object
      properties:
        data:
          type: array
          items: { $ref: '#/components/schemas/Resource' }
        pagination:
          $ref: '#/components/schemas/Pagination'
```

## Error Response (RFC 7807)

```yaml
ErrorResponse:
  type: object
  properties:
    type: { type: string, format: uri }
    title: { type: string }
    status: { type: integer }
    detail: { type: string }
    instance: { type: string, format: uri }
```

---

## Full OpenAPI 3.1 Structure

```yaml
openapi: 3.1.0
info:
  title: [API Name]
  description: |
    [API description with key features]
  version: 1.0.0
  contact:
    name: API Support
    email: api-support@example.com
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://staging-api.example.com/v1
    description: Staging
  - url: http://localhost:3000/v1
    description: Local development

tags:
  - name: Users
    description: User management operations
  - name: Orders
    description: Order management operations

paths:
  # Endpoints defined here

components:
  schemas:
    # Data models defined here
  securitySchemes:
    # Authentication defined here
  responses:
    # Common responses defined here
```

## Endpoint Definition Template

```yaml
paths:
  /users:
    get:
      tags:
        - Users
      summary: List all users
      description: |
        Retrieve a paginated list of users.
        Supports filtering by status and sorting.
      operationId: listUsers
      parameters:
        - $ref: '#/components/parameters/limitParam'
        - $ref: '#/components/parameters/offsetParam'
        - name: status
          in: query
          description: Filter by user status
          schema:
            type: string
            enum: [active, inactive, pending]
        - name: sort
          in: query
          description: Sort field and direction
          schema:
            type: string
            example: created_at:desc
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'
              example:
                data:
                  - id: "usr_123"
                    name: "John Doe"
                    email: "john@example.com"
                    status: "active"
                meta:
                  total: 100
                  limit: 10
                  offset: 0
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
      security:
        - bearerAuth: []

    post:
      tags:
        - Users
      summary: Create a new user
      description: Create a new user account
      operationId: createUser
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
            example:
              name: "John Doe"
              email: "john@example.com"
              password: "securePassword123"
      responses:
        '201':
          description: User created successfully
          headers:
            Location:
              description: URL of created resource
              schema:
                type: string
                example: /api/v1/users/usr_123
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          $ref: '#/components/responses/BadRequest'
        '409':
          $ref: '#/components/responses/Conflict'
      security:
        - bearerAuth: []
```

## Schema Definition Template

```yaml
components:
  schemas:
    User:
      type: object
      required:
        - id
        - name
        - email
        - status
        - createdAt
      properties:
        id:
          type: string
          description: Unique user identifier
          example: "usr_123abc"
          readOnly: true
        name:
          type: string
          description: User's full name
          minLength: 1
          maxLength: 100
          example: "John Doe"
        email:
          type: string
          format: email
          description: User's email address
          example: "john@example.com"
        status:
          type: string
          enum: [active, inactive, pending]
          description: Account status
          example: "active"
        createdAt:
          type: string
          format: date-time
          description: Account creation timestamp
          readOnly: true
          example: "2024-01-15T10:30:00Z"
        updatedAt:
          type: string
          format: date-time
          description: Last update timestamp
          readOnly: true

    CreateUserRequest:
      type: object
      required:
        - name
        - email
        - password
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 100
        email:
          type: string
          format: email
        password:
          type: string
          format: password
          minLength: 8
          maxLength: 128
          writeOnly: true

    UserList:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/User'
        meta:
          $ref: '#/components/schemas/PaginationMeta'

    PaginationMeta:
      type: object
      properties:
        total:
          type: integer
          description: Total number of items
        limit:
          type: integer
          description: Items per page
        offset:
          type: integer
          description: Current offset

    Error:
      type: object
      required:
        - code
        - message
      properties:
        code:
          type: string
          description: Error code
          example: "VALIDATION_ERROR"
        message:
          type: string
          description: Human-readable message
          example: "Email format is invalid"
        details:
          type: array
          items:
            type: object
            properties:
              field:
                type: string
              message:
                type: string
```

## Common Components Template

```yaml
components:
  parameters:
    limitParam:
      name: limit
      in: query
      description: Maximum number of items to return
      schema:
        type: integer
        minimum: 1
        maximum: 100
        default: 10

    offsetParam:
      name: offset
      in: query
      description: Number of items to skip
      schema:
        type: integer
        minimum: 0
        default: 0

    idParam:
      name: id
      in: path
      required: true
      description: Resource identifier
      schema:
        type: string

  responses:
    BadRequest:
      description: Invalid request
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: "BAD_REQUEST"
            message: "Invalid request parameters"

    Unauthorized:
      description: Authentication required
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: "UNAUTHORIZED"
            message: "Authentication required"

    Forbidden:
      description: Access denied
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: "FORBIDDEN"
            message: "You don't have permission to access this resource"

    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: "NOT_FOUND"
            message: "Resource not found"

    Conflict:
      description: Resource conflict
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: "CONFLICT"
            message: "Resource already exists"

    TooManyRequests:
      description: Rate limit exceeded
      headers:
        Retry-After:
          description: Seconds until rate limit resets
          schema:
            type: integer
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: JWT authentication token

    apiKey:
      type: apiKey
      in: header
      name: X-API-Key
      description: API key for service-to-service calls
```
