# dss-service

A small TypeScript GraphQL API for the "Did Someone Say...?" Discord bot. It generates the LLM-written gossip posts and keeps prompts, API keys, and output validation out of the Python bot.

## Stack
- **GraphQL Yoga** for the server
- **zod** to validate incoming names and the LLM's JSON reply; the `Gossip` type is derived from the same schema
- **openai** SDK pointed at any OpenAI-compatible provider (Gemini, Groq, OpenRouter, OpenAI), so switching provider is an `.env` change
- **dotenv** for local configuration

## Setup

Requires Node.js 18+.

```bash
npm install
cp .env.example .env   # then fill in your values
npm run dev
```

The server starts at `http://localhost:4000/graphql`.

### Environment variables

| Variable | Description |
|---|---|
| `LLM_API_KEY` | Key from your provider |
| `LLM_BASE_URL` | Provider's OpenAI-compatible base URL |
| `LLM_MODEL` | Model name exactly as the provider lists it (no `models/` prefix) |
| `PORT` | Port to listen on (default 4000) |

Example base URLs:
- Gemini: `https://generativelanguage.googleapis.com/v1beta/openai/`
- Groq: `https://api.groq.com/openai/v1`

## API

```graphql
type Gossip {
  headline: String!
  body: String!
  signOff: String!
}

type Query {
  health: String!
}

type Mutation {
  generateGossip(names: [String!]!): Gossip!
}
```

`names` must contain 1 to 5 non-empty strings of at most 32 characters.

### Try it

In the GraphiQL page at `/graphql`:

```graphql
mutation {
  generateGossip(names: ["Sam", "Priya"]) {
    headline
    body
    signOff
  }
}
```

Or from the terminal:

```bash
curl -s http://localhost:4000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"mutation { generateGossip(names: [\"Sam\", \"Priya\"]) { headline body signOff } }"}'
```

## Scripts

| Command | What it does |
|---|---|
| `npm run dev` | Run with auto-reload |
| `npm run build` | Compile TypeScript to `dist/` |
| `npm start` | Run the compiled build |

## Docker

```bash
docker build -t dss-service .
docker run -p 4000:4000 --env-file .env dss-service
```

## Security

The API has **no authentication**. Run it locally or on a private network. Don't expose it publicly, or anyone can spend your LLM quota.

## Troubleshooting

- **"Gossip generation failed"** is the generic error returned to clients. The real reason is printed in the service's terminal.
- **404 "model not found"**: the model name is wrong or unavailable to your account. List the models your key can use with a `GET` to `<LLM_BASE_URL>/models`.
- **Requests hang**: some models are slow or overloaded on free tiers. Try another model from the list, preferably a "flash-lite" style one.
- **Your `.env` changes seem ignored**: variables already set in your shell override `.env`. Run `unset LLM_MODEL LLM_API_KEY LLM_BASE_URL` and restart.