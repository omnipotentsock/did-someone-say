# Did Someone Say...?

A Discord bot that chimes in when it's least expected: it replies to trigger phrases, flips coins, and writes Gossip Girl-style "Spotted" posts about random members of your server using an LLM.

## Architecture

```
Discord  <-->  dss.py  (Python, discord.py)
                 |
                 |  GraphQL over HTTP (aiohttp)
                 v
              service/  (TypeScript, GraphQL Yoga, zod)
                 |
                 |  OpenAI-compatible chat API
                 v
              LLM provider (e.g. Gemini free tier)
```

- **`dss.py`** is the Discord front end: event handling, trigger replies, and slash commands.
- **`service/`** is a typed GraphQL API that owns the prompts, the LLM call, and validation of both the request and the model's reply. See [`service/README.md`](service/README.md).

Keeping the LLM logic in its own service means API keys live in one place and the bot stays a thin client.

## Commands

| Command | What it does |
|---|---|
| `dss wyd` | Lists everything the bot can do |
| `dss triggers` | Lists the words the bot replies to |
| `heads or tails` | Flips a coin |
| `blackjack me off` | Blackjack (in development) |
| `/gengossipgirl` | Generates a "Spotted" gossip post about random server members |

## Privacy

`/gengossipgirl` sends only members' **display names** to the LLM. Message content is never sent, and the generated post is posted with mentions disabled so nobody gets pinged.

## Setup

### Requirements
- Python 3.10+
- Node.js 18+ (for the service)
- A Discord application with a bot token
- An API key for an OpenAI-compatible LLM provider (Gemini and Groq both have free tiers)

### 1. Discord application
In the [Discord Developer Portal](https://discord.com/developers/applications), open your application, go to **Bot**, and enable these privileged intents:
- **Message Content Intent**
- **Server Members Intent**

### 2. Start the service
Follow [`service/README.md`](service/README.md) and confirm it is running at `http://localhost:4000/graphql`.

### 3. Run the bot
```bash
pip install -r requirements.txt
```

Create a `.env` file in the repo root:
```
DISCORD_TOKEN=your-bot-token
# Optional, defaults to http://localhost:4000/graphql
SERVICE_URL=http://localhost:4000/graphql
```

Then:
```bash
python dss.py
```

## Environment variables

| Where | Variable | Purpose |
|---|---|---|
| repo root `.env` | `DISCORD_TOKEN` | Discord bot token |
| repo root `.env` | `SERVICE_URL` | GraphQL endpoint of the service |
| `service/.env` | `LLM_API_KEY`, `LLM_BASE_URL`, `LLM_MODEL` | LLM provider settings |
| `service/.env` | `PORT` | Service port (default 4000) |

Never commit a `.env` file.

## Deployment

The bot includes a `Procfile`. The service includes a `Dockerfile` and reads its port from `PORT`, so it can be hosted anywhere that runs containers. If you host the service, keep it on a private network or add authentication: the GraphQL endpoint has none, and an exposed one would let anyone spend your LLM quota.

## Project structure

```
dss.py            Discord bot
requirements.txt  Python dependencies
Procfile          Process definition for hosting
service/          TypeScript GraphQL service
```

## License

See [LICENSE](LICENSE).