import OpenAI from "openai";
import { z } from "zod";

const client = new OpenAI({
  apiKey: process.env.LLM_API_KEY,
  baseURL: process.env.LLM_BASE_URL,
  timeout: 20_000,
  maxRetries: 0,
});

const MODEL = process.env.LLM_MODEL ?? "";

export const NamesInput = z.array(z.string().trim().min(1).max(64)).min(1).max(5);

export const GossipSchema = z.object({
  headline: z.string(),
  body: z.string(),
  signOff: z.string(),
});
export type Gossip = z.infer<typeof GossipSchema>;

const SYSTEM = `You are the anonymous gossip blogger from Gossip Girl. Write a short, witty "Spotted:" style post about the people named in the prompt.
Invent harmless, silly scandals. Nothing cruel, bigoted, sexual, or involving real private details, just surface-level mean-spirited. But really push it!
Respond with ONLY a JSON object, no markdown fences:
{"headline": string, "body": string (3-5 sentences), "signOff": string}
Sign off with "Later then. XOXO, Gossip Girl.".`;


// generating the gossip message
export async function generateGossip(names: string[]): Promise<Gossip> {
  if (!MODEL) throw new Error("LLM_MODEL is not set");

  const resp = await client.chat.completions.create({
    model: MODEL,
    max_tokens: 400,
    messages: [
      { role: "system", content: SYSTEM },
      { role: "user", content: `People: ${names.join(", ")}` },
    ],
  });

  const text = resp.choices[0]?.message?.content;
  if (!text) throw new Error("Blank LLM response. Fix, yeah?");

  const raw = text.replace(/```json|```/g, "").trim();
  return GossipSchema.parse(JSON.parse(raw));
}