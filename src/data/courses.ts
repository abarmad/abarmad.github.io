export interface Course {
  title: string;
  level?: string;
  description: string;
  syllabus?: string;
}

export interface InstitutionPhoto {
  src: string;
  alt: string;
  caption: string;
}

export interface Institution {
  name: string;
  period?: string;
  courses: Course[];
  photo?: InstitutionPhoto; // shown beside (desktop) or after (phone) this institution's courses
}

export const currentCourses: Course[] = [
  {
    title: "Markets",
    level: "Undergraduate",
    description:
      "How do individuals and firms make decisions and how, through market interaction, do these decisions determine the allocation of resources in society? In this course, students will learn what the main forces shaping market outcomes are. There will be in-depth discussions of the effects of government intervention and the situations in which governments can improve overall welfare due to market imperfections.",
    syllabus: "/syllabi/markets.pdf",
  },
  {
    title: "Behavioral Economics",
    level: "Undergraduate",
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
    photo: {
      src: "/images/teaching-photo.jpeg",
      alt: "Giving a lecture at Maastricht University",
      caption:
        "January 2018. Giving a lecture about “Reflections on Academic Discourse” at Maastricht University.",
    },
    courses: [
      {
        title: "Behavioral Economics",
        level: "Undergraduate",
      },
      {
        title: "Internet Economics",
        level: "Master's",
      },
    ],
  },
  {
    name: "Ohio State University",
    courses: [
      {
        title: "Business and Government",
        level: "Undergraduate",
      },
      {
        title: "The American Revenue System",
        level: "Undergraduate",
      }
    ],
  },
];