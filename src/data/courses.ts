export interface Course {
  title: string;
  level?: string;
  description: string;
  syllabus?: string;
}

export interface Institution {
  name: string;
  period?: string;
  courses: Course[];
}

export const currentCourses: Course[] = [
  {
    title: "Markets and Information",
    description:
      "How do individuals and firms make decisions and how, through market interaction, do these decisions determine the allocation of resources in society? In this course, students will learn what the main forces shaping market outcomes are. There will be in-depth discussions of the effects of government intervention and the situations in which governments can improve overall welfare due to market imperfections.",
    syllabus: "/syllabi/markets.pdf",
  },
  {
    title: "Behavioral Economics",
    description:
      "This course introduces students to the field of behavioral economics, which seeks to combine standard economic modeling with more psychologically plausible assumptions about human behavior. This is accomplished by making nonstandard assumptions about human preferences, exploring nonstandard beliefs, and emphasizing the limitations of our decision-making faculties.",
    syllabus: "/syllabi/behavioral-econ.pdf",  // add once he provides it
  },
  {
    title: "Fairness",
    level: "Colloquium",
    description:
      "What is fair and what is unfair? Is fairness universal? Are equality and fairness synonyms? How can we build a fairer world? The plurality of fairness ideals may lead to breakdown in negotiations, social conflict, or other undesirable outcomes. This colloquium draws from philosophy, psychology, political science, economics, and organizational behavior to question our own notions and judgments and arrive at a holistic understanding of fairness as a concept.",
    syllabus: "/syllabi/fairness.pdf",
  },
];

export const previousTeaching: Institution[] = [
  {
    name: "Maastricht University",
    period: "2015–2018",
    courses: [
      {
        title: "Behavioral Economics",
        level: "Undergraduate",
        description:
          "Covers individual decision-making (violations of expected utility theory, time-inconsistent preferences) and behavioral theories that better explain commonly observed phenomena. Also analyzes models of other-regarding preferences, experiments on coordination in games with multiple equilibria, and level-k reasoning. The main topics are motivated via in-class experiments.",
      },
      {
        title: "Internet Economics",
        level: "Master's",
        description:
          "Covers two-sided markets, networks, price discrimination, and auctions, with direct applications to internet-based businesses and activities.",
      },
    ],
  },
  {
    name: "Ohio State University",
    courses: [
      {
        title: "Business and Government",
        level: "Undergraduate",
        description:
          "Provided students with a theoretical framework for understanding how changes in government regulation (taxes, subsidies, pollution quotas, antitrust laws) affect businesses' productive decisions. We studied incentives to lobby and generate favorable regulation.",
      },
      {
        title: "The American Revenue System",
        level: "Undergraduate",
        description:
          "A course on public finance and taxation with emphasis on the American fiscal system. Taught during the 2012 presidential campaign, so an essential part of the course was studying the different tax cuts proposed by Obama and Romney, as well as the focus of their government spending.",
      },
    ],
  },
];
