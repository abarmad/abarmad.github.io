export interface PubLink {
  label: string;
  href: string;
}

export interface Publication {
  title: string;
  coauthors?: string;
  journal?: string;
  details?: string;
  status?: string;
  links?: PubLink[];
}

export const published: Publication[] = [
  {
    title: "Competing for Power in Multilateral Negotiations under Majority and Unanimity Rules",
    coauthors: "Ernesto Reuben",
    journal: "Games and Economic Behavior",
    status: "Accepted",
    links: [{ label: "PDF", href: "/papers/competing-for-power.pdf" }],
  },
  {
    title: "Exclusionary Bargaining Behavior in 14 Countries: Prevalence and Predictors",
    coauthors: "Nick Haas",
    journal: "PNAS Nexus",
    details: "4(1), 2025",
    links: [{ label: "Publisher page", href: "https://academic.oup.com/pnasnexus/article/4/1/pgae553/7960037" }],
  },
  {
    title: "Sharing the Burden of Negative Externalities: A Tale of Gridlock and Accountability Elusion",
    coauthors: "Duk-Gyoo Kim",
    journal: "Ecological Economics",
    details: "224 (2024): 108264",
    links: [{ label: "PDF", href: "/papers/sharing-the-burden.pdf" }],
  },
  {
    title: "An Experiment on Gender Representation in Majoritarian Bargaining",
    coauthors: "Diogo Geraldes, Ada Kovaliukaite, and James Tremewan",
    journal: "Management Science",
    details: "70(10), 2024: 6622–6636",
    links: [{ label: "PDF", href: "/papers/gender-representation.pdf" }],
  },
  {
    title: "The Timing of Communication and Retaliation in Bargaining: An Experimental Study",
    coauthors: "Nick Haas",
    journal: "Journal of Economic Psychology",
    details: "96 (2023): 102621",
    links: [{ label: "PDF", href: "/papers/timing-of-communication.pdf" }],
  },
  {
    title: "Pork versus Policy: Experimental Evidence on Majoritarian Bargaining with Real-World Consequences",
    coauthors: "Nicholas Haas and Rebecca Morton",
    journal: "The Journal of Politics",
    details: "85(2), 2023: 537–552",
    links: [{ label: "PDF", href: "/papers/pork-versus-policy.pdf" }],
  },
  {
    title: "Communication in Multilateral Bargaining with Joint Production",
    coauthors: "Caleb Cox",
    journal: "Experimental Economics",
    details: "26 (2023): 55–77",
    links: [{ label: "PDF", href: "/papers/communication-joint-production.pdf" }],
  },
  {
    title: "The Determinants of Multilateral Bargaining: A Comprehensive Analysis of Baron and Ferejohn Majoritarian Bargaining Experiments",
    coauthors: "Rebecca Morton",
    journal: "Experimental Economics",
    details: "25(4), 2022: 1079–1108",
    links: [{ label: "PDF", href: "/papers/determinants-of-bargaining.pdf" }],
  },
  {
    title: "Endogenous Claims and Collective Production: An Experimental Study on the Timing of Profit-Sharing Negotiations and Production",
    journal: "Experimental Economics",
    details: "22(4), 2019: 857–884",
    links: [{ label: "Publisher page", href: "https://link.springer.com/article/10.1007/s10683-018-9591-2" }],
  },
  {
    title: "Voluntary Contributions and Collective Redistribution",
    journal: "American Economic Journal: Microeconomics",
    details: "8(4), 2016: 149–173",
    links: [{ label: "Publisher page", href: "https://www.aeaweb.org/articles?id=10.1257/mic.20140240" }],
  },
  {
    title: "Communication in Legislative Bargaining",
    coauthors: "John H. Kagel",
    journal: "Journal of the Economic Science Association",
    details: "1(1), 2015: 59–71",
    links: [
      { label: "Publisher page", href: "https://link.springer.com/article/10.1007/s40881-015-0011-5" },
      { label: "Data", href: "/data/communication_data.csv" },
    ],
  },
];

export const workingPapers: Publication[] = [
  {
    title: "Are LLMs Reliable Coders of Communication Content in Economic Experiments?",
    coauthors: "David Cooper and Jeong Kyu Lee",
    status: "Under review",
    links: [
      { label: "PDF", href: "/working-papers/llm-reliable-coders.pdf" },
      { label: "CAT tool", href: "https://ssel.chatkit.nyuad.nyu.edu/coding" },
    ],
  },
  {
    title: "Who Is Watching? Gender Composition of Observers and Risk Taking",
    coauthors: "Prinsa Chauhan and Aurelie Dariel",
    status: "Under review",
    links: [{ label: "PDF", href: "/working-papers/who-is-watching.pdf" }],
  },
  {
    title: "The Role of Fairness Ideals in Coordination Failure and Success",
    coauthors: "Ernesto Reuben and Arno Riedl",
    status: "Under review",
    links: [{ label: "PDF", href: "/working-papers/fairness-ideals.pdf" }],
  },
  {
    title: "Coordination through Bargaining in Weakest-link Games",
    coauthors: "Lina Lozano and Nikos Nikiforakis",
    links: [{ label: "PDF", href: "/working-papers/weakest-link-coordination.pdf" }],
  },
  {
    title: "The Effect of Competition in Contests: A Unifying Approach",
    coauthors: "Sumit Goel",
    status: "Under review",
    links: [{ label: "PDF", href: "/working-papers/competition-in-contests.pdf" }],
  },
  {
    title: "The Recency Bias in the Attribution of Credit and Blame for Joint Work Outcomes",
    coauthors: "Manu Muñoz",
    status: "Reject and resubmit",
    links: [{ label: "PDF", href: "/working-papers/recency-bias.pdf" }],
  },
];

export const inProgress: Publication[] = [
  { title: "The Life Cycle of Beliefs", coauthors: "Larbi Alaoui" },
  { title: "Bargaining over Profit-sharing Agreements: Theory and Experiments", coauthors: "Hulya Eraslan" },
  { title: "Communication behind the Veil of Ignorance", coauthors: "Nick Haas and Hyoeun Park" },
  { title: "Beyond the Binary: Self Perception of Gender Identity and Bargaining Behavior", coauthors: "Nicholas Haas" },
  { title: "Contingent Reasoning in Conflict Resolution", coauthors: "Caleb Cox" },
  { title: "The Decision to Enter Negotiations", coauthors: "Marco Palma" },
];
