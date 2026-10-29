export interface Variant {
  label: string;          // e.g. "Without externalities"
  instructions: string;   // PDF path inside public/experiments/
  zip?: string;           // only if this variant has its own, separate ZIP
}

export interface Experiment {
  title: string;
  description: string;     // separate paragraphs with a blank line
  objectives?: string[];   // shown as bubbles
  zip?: string;            // the ZIP file name inside public/experiments/
  instructions?: string;   // single preview PDF (for experiments without variants)
  variants?: Variant[];    // use this when there are several versions of the instructions
}

// Add each new experiment to this list.
// Files go in public/experiments/ (the ZIP, and a folder holding the instructions PDF).
export const experiments: Experiment[] = [
  {
    title: "International Trade Deal",
    description: `Participants represent countries that each produce clothes and food. Each country picks its best plan without trade, negotiates a trade deal with a partner, and then chooses a final production plan, to see whether trade can leave both sides better off.

The two countries face different tradeoffs, and their plans are private. Utility depends on both goods (5 times the minimum of clothes and food), so what a country produces and what it trades both matter. Pairs that reach a deal that beats both countries' autarky plans earn a participation point.`,
    objectives: [
      "Gains from trade",
      "Comparative advantage",
      "Opportunity cost",
      "Autarky vs. trade",
      "Negotiation",
    ],
    zip: "tradeDealExp.zip",
    instructions: "tradeDealExp/instructions.pdf",
  },
  {
    title: "Double Auction",
    description: `Participants trade in a competitive market, each playing a buyer with a private value or a seller with a private cost. Everyone submits a single bid or ask, the market clears at one price, and participants see how trades, prices, and profits come about. The experiment has two variants: the first without externalities, and the second with externalities.

Bids are ranked from highest to lowest and asks from lowest to highest, and they are matched until a bid falls below an ask. All trades happen at one market price, the average of the last matched bid and ask. The experiment runs for 10 rounds: participants keep their role for five rounds, then switch, so they experience both sides of the market. A ranking of total profits is shown at the end.

In the first variant, a participant's profit depends only on their own trade. In the second, there is an externality: if every buyer buys a good, every participant receives 10 additional points, so one person's decision affects everyone else's payoff. Comparing the two variants shows how market outcomes change when private incentives and shared benefits diverge.`,
    objectives: [
      "Supply and demand",
      "Market-clearing price",
      "Willingness to pay and cost",
      "Gains from trade",
      "Strategic bidding",
      "Externalities",
    ],
    // One ZIP holds both variants; each variant has its own instructions PDF.
    zip: "doubleAuction.zip",
    variants: [
      {
        label: "Without externalities",
        instructions: "doubleAuction/instructions.pdf",
      },
      {
        label: "With externalities",
        instructions: "doubleAuction/instructions_variant2.pdf",
      },
    ],
  },
  {
    title: "Public Goods Game",
    description: `Participants face a classic social dilemma. Each round, everyone starts with 10 points and privately chooses how many to contribute to a common fund. All contributions are added together, multiplied, and the resulting prize is split equally among all participants, whether or not they contributed. The experiment has two variants: the first without point reductions, and the second with point reductions.

Each point contributed returns less than a point to the contributor, so keeping points is individually profitable, yet the group as a whole earns the most when everyone contributes everything. The experiment runs for 5 rounds with the same group, and participants see the group's contributions after each round. Their ID numbers are reshuffled every round, so they cannot tell who is who. A ranking of total profits is shown at the end.

In the first variant, a participant's profit depends only on their own contribution and the group's total. In the second, participants receive 2 extra points each round that they can use to reduce other participants' profits: paying 1 point removes 3 points from another person. Punishing costs the punisher too, and benefits the whole group, which makes it a public good in its own right. Comparing the two variants shows whether the chance to sanction free-riders sustains cooperation over time.`,
    objectives: [
      "Public goods and free-riding",
      "Social dilemmas",
      "Cooperation vs. self-interest",
      "Nash equilibrium vs. social optimum",
      "Costly punishment",
      "Conditional cooperation and learning",
    ],
    // One ZIP holds both variants; each variant has its own instructions PDF.
    zip: "publicGoods.zip",
    variants: [
      {
        label: "Without point reductions",
        instructions: "publicGoods/instructions.pdf",
      },
      {
        label: "With point reductions",
        instructions: "publicGoods/instructions_variant2.pdf",
      },
    ],
  },

  // ---- Not published yet: these two still need real descriptions. ----
  // Send me each experiment's instructions PDF and I'll write the entry.
  // To publish one, copy the template below, fill it in, and move it above this comment.
  //
  // {
  //   title: "Oligarchy and Collusion",
  //   description: `...`,
  //   objectives: ["...", "..."],
  //   zip: "oligarchyExp.zip",
  //   instructions: "oligarchyExp/instructions.pdf",
  // },
  // {
  //   title: "Public Goods",
  //   description: `...`,
  //   objectives: ["...", "..."],
  //   zip: "publicGoodsExp.zip",
  //   instructions: "publicGoodsExp/instructions.pdf",
  // },
];
