export interface NewsLink {
  label: string;
  href: string;
}

export interface NewsItem {
  date: string; // YYYY-MM-DD
  title: string;
  body?: string; // separate paragraphs with a blank line (\n\n)
  links?: NewsLink[];
}

// Add new items anywhere in the list. The home page sorts them by date
// and shows the most recent ones.
export const news: NewsItem[] = [
  {
    date: "2026-10-01", // change to the real announcement date
    title: "New tool: Communication Annotation Tool (CAT)",
    body:
      "We are pleased to introduce the Communication Annotation Tool (CAT), a browser-based platform that helps experimental social scientists analyze free-form communication using large language models. CAT enables researchers to create flexible coding manuals, annotate messages or complete conversations using multiple LLMs, assess coding reliability, review problematic cases, and generate replication-ready datasets and documentation (all without programming or API expertise).\n\n" +
      "CAT is designed to make rigorous content analysis faster, more affordable, transparent, and reproducible. A guided tutorial and video are available on the CAT website.\n\n" +
      "If you are wondering whether LLMs are reliable for coding communication content in experiments, we answer this methodological question here:",
    links: [
      { label: "Visit CAT", href: "https://ssel.chatkit.nyuad.nyu.edu/coding" },
      { label: "Documentation", href: "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7370379" },
      { label: "Read the paper", href: "/working-papers/llm-reliable-coders.pdf" },
    ],
  },
];