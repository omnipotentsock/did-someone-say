import "dotenv/config";
import { createServer } from "node:http";
import { createSchema, createYoga } from "graphql-yoga";
import { GraphQLError } from "graphql";
import { NamesInput, generateGossip, type Gossip } from "./llm.js";

const typeDefs = `
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
`;

const schema = createSchema({
  typeDefs,
  resolvers: {
    Query: {
      health: () => "ok",
    },

    Mutation: {
      generateGossip: async (
        _: unknown,
        args: { names: string[] }
      ): Promise<Gossip> => {
        const parsed = NamesInput.safeParse(args.names);

        if (!parsed.success) {
          throw new GraphQLError("names must be 1-5 non-empty strings.");
        }
        try {
          return await generateGossip(parsed.data);
        } catch (err) {
          console.error(err);
          throw new GraphQLError("Gossip generation failed, try again.");
        }
      },
    },
  },
});

// just testing for now
const yoga = createYoga({ schema });
const port = Number(process.env.PORT ?? 4000);

createServer(yoga).listen(port, () => {
  console.log(`GraphQL service ready at http://localhost:${port}/graphql`);
});