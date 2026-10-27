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
  abstract?: string;   // new
  links?: PubLink[];
}

export const published: Publication[] = [
  {
    title: "Competing for Power in Multilateral Negotiations under Majority and Unanimity Rules",
    coauthors: "Ernesto Reuben",
    journal: "Games and Economic Behavior",
    status: "Accepted",
    abstract: `Competition for power is a costly practice present in organizations and groups where collective
      decisions are made. In a multilateral bargaining experiment, we study how different agreement
      rules affect competition for power through a contest for the right to propose a distribution of
      benefits. Although unanimity leads to less wasteful competition investments, it also generates
      a greater delay in negotiations and a higher likelihood of disagreement. These opposing inefficiencies offset each other across a wide range of bargaining horizons, contest technologies,
      voting procedures, and subject pools. We find no statistically significant evidence of efficiency
      dominance by either rule over the parameters studied once competition for power is taken into
      account. Under equal proposal rights absent a contest, agreements are reached more quickly,
      demonstrating the causal effect of competition for power on bargaining gridlock and its compounding effect on efficiency losses. In addition, we find that bargaining behavior is conditioned
      on prior power-seeking efforts: subjects reward higher effort with higher shares, indicating that
      efforts enter fairness considerations despite their unproductive and competitive nature.`,
    links: [{ label: "PDF", href: "/papers/competing-for-power.pdf" },
    ],
  },
  {
    title: "Exclusionary Bargaining Behavior in 14 Countries: Prevalence and Predictors",
    coauthors: "Nick Haas",
    journal: "PNAS Nexus",
    details: "4(1), 2025",
    abstract: `
    Primates are known to engage in exclusionary behavior, forming alliances to block a minority from accessing scarce resources. Humans
    are no exception, and examples of exclusionary behavior abound in political, business, and social settings. However, despite its socioeconomic relevance, little is known about the prevalence and determinants of such behavior worldwide. Conducting an experimental
    game in which a group divides resources by majority rule, we document considerable global heterogeneity in exclusionary behavior.
    Whereas exclusion is modal in some countries, inclusive behavior is the norm in others. Despite significant cross-country variability,
    we nevertheless find that individual-level characteristics matter similarly across contexts. Men, individuals with a deliberative
    reasoning style, and ideologically right-leaning individuals, are consistently and substantially more exclusionary. Cross-country
    differences in the formation of exclusionary alliances correlate with an original Hierarchy Tolerance Index, derived from variables
    measuring cultural acceptance of power inequalities. Our findings carry important implications for decision-making bodies, as they
    indicate that the identity of decision-makers and the culture in which they are embedded can affect how equitably resources are divided.`,
    links: [{ label: "PDF", href: "/papers/exclusionary-bargaining.pdf" }],
  },
  {
    title: "Sharing the Burden of Negative Externalities: A Tale of Gridlock and Accountability Elusion",
    coauthors: "Duk-Gyoo Kim",
    journal: "Ecological Economics",
    details: "224 (2024): 108264",
    abstract: `We report the results of a Öeld-in-the-lab experiment in which subjects bargain
    over a two-dimensional agenda: a donation to a political interest group and the
    division of a sum of money. We show that subjects sacriÖce monetary gains to
    secure preferred policies and that behaviorally elicited preference intensity correlates
    with bargaining behavior. We Önd an ideological majority advantage and a statusquo premium. Minorities beneÖt most from negotiating on two dimensions because
    the budgetary division problem allows compromise. Finally, we show that induced
    preferences over artiÖcial policies fail to capture the bargaining dynamics that arise
    when real ideological choices are involved.`,
    links: [{ label: "PDF", href: "/papers/sharing-the-burden.pdf" }],
  },
  {
    title: "An Experiment on Gender Representation in Majoritarian Bargaining",
    coauthors: "Diogo Geraldes, Ada Kovaliukaite, and James Tremewan",
    journal: "Management Science",
    details: "70(10), 2024: 6622–6636",
    abstract: `Women are underrepresented in business, academic, and political decision-making bodies
    across the world. To investigate the causal effect of gender representation on multilateral negotiations, we experimentally manipulate the composition of triads in a majoritarian, divide-the-dollar
    game. We document a robust gender gap in earnings, driven largely by the exclusion of women
    from alliances rather than differential shares within alliances. Experiments with different subject pools show that distinct bargaining dynamics can underlie the same inequitable outcomes:
    gender-biased outcomes can be caused by outright discrimination, but they can also be driven by
    more complex dynamics related to differences in bargaining strategies. While replacing the male
    with a female majority all but eliminates the gap in one pool, it has minimal effect in the other.
    These findings show that there is no “one-size-fits-all” solution to the gender gap we uncovered
    and highlight the importance of studying bargaining dynamics in detail.`,
    links: [{ label: "PDF", href: "/papers/gender-representation.pdf" }],
  },
  {
    title: "The Timing of Communication and Retaliation in Bargaining: An Experimental Study",
    coauthors: "Nick Haas",
    journal: "Journal of Economic Psychology",
    details: "96 (2023): 102621",
    abstract: `We conduct an experiment to investigate how the timing of communication affects bargaining outcomes and dynamics in a majoritarian, sequential bargaining game. Our data show that
    allowing for free-form written communication at the proposal-making stage leads to higher proposer power and minimum winning coalitions compared to when communication is possible at
    the voting stage only. Absent communication, outcomes fall in between both communication
    timings. Voting patterns reveal that the timing of communication affects how subjects evaluate
    proposals, as they are more likely to vote in favor under proposal-stage communication than
    under voting-stage communication all else equal. In general, communication affects bargaining dynamics in that voters retaliate more strongly against failed proposers, compared to the
    no communication baseline. We provide a detailed description of communication content, the
    medium utilized to communicate, and how the volume and timing of messages affects outcomes.
    Our results underscore the importance of an in-depth analysis of processes and dynamics to
    understand bargaining behavior, because even when communication may lead to outcomes that
    resemble equilibrium, the strategies employed by subjects need not.`,
    links: [{ label: "PDF", href: "/papers/timing-of-communication.pdf" }],
  },
  {
    title: "Pork versus Policy: Experimental Evidence on Majoritarian Bargaining with Real-World Consequences",
    coauthors: "Nicholas Haas and Rebecca Morton",
    journal: "The Journal of Politics",
    details: "85(2), 2023: 537–552",
    abstract: `Pork-barrel politics has long attracted controversy; difficult to prove and vigorously denied by those accused of it, the practice is nevertheless defended by others
    who argue that pork facilitates compromise. We design a novel field-in-the-lab experiment to study how legislators bargain over pork and real-world policy. We first
    introduce a new incentivized method to measure subjects’ ideological peak preferences and attitudinal strength. Subjects then bargain over a two-dimensional
    agenda: a donation to a political interest group and the division of a sum of money.
    Consistent with our theoretical model, we find that subjects trade off monetary and
    policy considerations. Subjects who are in the ideological majority and who prefer
    status quo policies extract better bargains, but minorities gain most from the possibility of compromise afforded by two dimensions. Finally, we show that artificiallyinduced preferences fail to fully capture the bargaining dynamics observed using
    naturally-occurring preferences.`,
    links: [{ label: "PDF", href: "/papers/pork-versus-policy.pdf" }],
  },
  {
    title: "Communication in Multilateral Bargaining with Joint Production",
    coauthors: "Caleb Cox",
    journal: "Experimental Economics",
    details: "26 (2023): 55–77",
    abstract: `We experimentally investigate the effect of pre-bargaining communication on productive
    incentives in a multilateral bargaining game with joint production under two conditions: observable and unobservable investments. In both conditions, communication fosters fair sharing
    and is rarely used to pit individuals against each other. Proportional sharing arises with observable investments with or without communication, leading to high efficiency gains. Without
    investment observability, communication is widely used to truthfully report investments and call
    for equitable sharing, allowing substantial efficiency gains. Since communication occurs after
    production, our results highlight a novel indirect channel through which communication can
    enhance efficiency in social dilemmas. Our results contrast with previous findings on bargaining
    over an exogenous fund, where communication leads to highly unequal outcomes, competitive
    messages, and virtually no appeals to fairness.`,
    links: [{ label: "PDF", href: "/papers/communication-joint-production.pdf" }],
  },
  {
    title: "The Determinants of Multilateral Bargaining: A Comprehensive Analysis of Baron and Ferejohn Majoritarian Bargaining Experiments",
    coauthors: "Rebecca Morton",
    journal: "Experimental Economics",
    details: "25(4), 2022: 1079–1108",
    abstract: `We analyze the data sets of all majoritarian Baron and Ferejohn (1989 Am. Pol.
    Sci. Rev.) experiments through 2018. By exploiting the variation of the experimental
    parameters, we are able to identify how group size, discount factor (cost of agreement
    delay), voting weights, and communication affect bargaining outcomes and dynamics.
    The outcomes are qualitatively in line with the stationary subgame perfect equilibrium, i.e., minimum winning coalitions are modal; proposers demand larger shares
    than non-proposers; and most agreements are reached without delay. Experience and
    communication between players move outcomes closer to the equilibrium. However,
    bargaining dynamics are not stationary. Behavior following a disagreement is historydependent in the form of retaliation towards failed proposers and their supporters,
    which, if rationally expected, may deter proposers from demanding high shares.`,
    links: [{ label: "PDF", href: "/papers/determinants-of-bargaining.pdf" }],
  },
  {
    title: "Endogenous Claims and Collective Production: An Experimental Study on the Timing of Profit-Sharing Negotiations and Production",
    journal: "Experimental Economics",
    details: "22(4), 2019: 857–884",
    abstract: `We explore the efficiency and distributive implications of a multilateral bargaining model with endogenous production of the surplus under two different timings:
    ex ante and ex post bargaining. Both timings are commonly observed in business
    partnerships and alliance formations. The theoretical predictions confirm an intuitive economic tenet: in ex post bargaining, effort is considered sunk and opportunistic bargaining behavior will dissuade players from producing. On the other hand,
    ex ante bargaining entails an allocation of ownership shares that induces at least
    certain members to invest in the common fund because their return is guaranteed.
    Experiments show opposite results: ex post bargaining yields almost fully efficient
    outcomes while the reverse timing entails near zero efficiency. The psychological
    theory of inequity is useful in reconciling these divergent results.`,
    links: [{ label: "PDF", href: "/papers/endogenous-claims.pdf" }],
  },
  {
    title: "Voluntary Contributions and Collective Redistribution",
    journal: "American Economic Journal: Microeconomics",
    details: "8(4), 2016: 149–173",
    abstract: `I study a multilateral bargaining game in which committee members
    invest in a common project prior to redistributing the total value of
    production. The game corresponds to a Baron and Ferejohn (1989)
    legislative bargaining model preceded by a production stage that is
    similar to a voluntary contribution mechanism. In this game, contributions reach almost full efficiency in a random rematching experimental design. Bargaining outcomes tend to follow an equity standard
    of proportionality: higher contributors obtain higher shares. Unlike
    other bargaining experiments with an exogenous fund, allocations
    involving payments to all members are modal instead of minimum
    winning coalitions, and proposer power is quite low.`,
    links: [{ label: "PDF", href: "/papers/voluntary-contributions.pdf" }],
  },
  {
    title: "Communication in Legislative Bargaining",
    coauthors: "John H. Kagel",
    journal: "Journal of the Economic Science Association",
    details: "1(1), 2015: 59–71",
    abstract: `We investigate the Baron-Ferejohn (The American Political Science
    Review 83(4): 1181–1206, 1989) model of legislative bargaining with cheap talk
    between the designated proposer and potential coalition partners. Communication
    results in substantially increased proposer power close to the stationary subgame
    perfect equilibrium prediction. This is achieved primarily through voters competing
    with each other to get the proposer to include them in the winning coalition, while
    arguing for a zero allocation for redundant voters. Voters typically follow through
    on their stated reservation shares, but proposers often fail to partner with voters
    making excessively low offers, as these are more likely to be reneged on.`,
    links: [
      { label: "PDF", href: "/papers/legislative-bargaining.pdf" },
      { label: "Data", href: "/data/communication_data.csv" },
    ],
  },
];

export const workingPapers: Publication[] = [
  {
    title: "Are LLMs Reliable Coders of Communication Content in Economic Experiments?",
    coauthors: "David Cooper and Jeong Kyu Lee",
    status: "Under review",
    abstract: `Analysis of free-form communication from experiments has largely relied on manual coding
    by research assistants (RAs), a costly and time-consuming process. We outline an easily
    implemented method for coding communication data using large language models (LLMs)
    and propose a novel standard for evaluating the performance of LLM-based coding (“reliability”). Using data from three published articles, we find that LLM-based coding meets our
    two reliability conditions: (1) differences between LLM-based and RA-based coding are no
    larger than differences between the RA-based and original coding and (2) the LLM-based
    coding largely replicates qualitative conclusions from the original papers. That said, there
    are cases where the LLM-based coding agrees poorly with the RA-based coding or fails to
    replicate statistical results from the original papers. We demonstrate that these problems
    can be ameliorated with better prompt design. We conclude that use of LLMs can reduce
    research costs and time without sacrificing reliability, making content analysis a more accessible tool for experimental economists. However, only with a combination of test coding by
    RAs and prompt design by researchers can we avoid significant problems with LLM-based
    coding, highlighting the continued importance of human input.`,
    links: [
      { label: "PDF", href: "/working-papers/llm-reliable-coders.pdf" },
      { label: "CAT tool", href: "https://ssel.chatkit.nyuad.nyu.edu/coding" },
    ],
  },
  {
    title: "Who Is Watching? Gender Composition of Observers and Risk Taking",
    coauthors: "Prinsa Chauhan and Aurelie Dariel",
    status: "Under review",
    abstract: `We experimentally investigate whether the gender composition of an observing peer
    group affects individual risk-taking. Participants are randomly assigned to three-person
    groups differing only in gender composition. They complete an incentivized lottery task
    knowing that their choices will be observed by the other group members. We find that
    men’s willingness to choose the riskiest lottery increases monotonically with the number of female observers, whereas women exhibit no comparable response to the number
    of male observers. Men in all-male groups display levels of risk-taking statistically indistinguishable from those of women in all-female groups, indicating that the observed
    gender gap emerges primarily in mixed-gender groups. A mating-motivated signaling
    mechanism is consistent with our results.`,
    links: [{ label: "PDF", href: "/working-papers/who-is-watching.pdf" }],
  },
  {
    title: "The Role of Fairness Ideals in Coordination Failure and Success",
    coauthors: "Ernesto Reuben and Arno Riedl",
    status: "Under review",
    abstract: `In a laboratory experiment, we study the role of fairness ideals as focal points in coordination problems in homogeneous and heterogeneous groups. We elicit the normatively
    preferred behavior about how a subsequent coordination game should be played. In homogeneous groups, people share a unique fairness ideal for how to solve the coordination
    problem, whereas in heterogeneous groups, multiple conflicting fairness ideals prevail. In
    the coordination game, homogeneous groups are significantly more likely than their heterogeneous counterparts to sustain efficient coordination. The reason is that homogeneous
    groups coordinate on the unique fairness ideal, whereas heterogeneous groups disagree on
    the fairness ideal to be played. In both types of groups, equilibria consistent with fairness
    ideals are most stable. Hence, the difference in coordination success between homogeneous
    and heterogeneous groups occurs because of the normative disagreement in the latter types
    of group, making it much harder to reach an equilibrium at a fairness ideal.`,
    links: [{ label: "PDF", href: "/working-papers/fairness-ideals.pdf" }],
  },
  {
    title: "Coordination through Bargaining in Weakest-link Games",
    coauthors: "Lina Lozano and Nikos Nikiforakis",
    abstract: `Coordination problems are often modeled as weakest-link games, where the minimumcontributing agent determines their group’s surplus to be shared in equal parts. Yet
    in many settings, the sharing of a jointly-produced surplus occurs through bargaining,
    which acts as a double-edged sword: It can promote effort by disciplining low contributors or deter it through the added uncertainty of returns. We present experimental
    evidence that bargaining improves coordination by promoting equitable divisions that
    reward higher contributions, even in one-shot interactions. High contributors are more
    likely than low contributors to propose allocations that reward effort, creating a virtuous cycle that increases efficiency. Allowing groups to endogenously select who can act
    as proposers can backfire: Efficiency increases when high contributors are endorsed but
    falls otherwise. These results highlight the scope and limits of participatory surplus
    division mechanisms in providing incentives for efficient coordination.`,
    links: [{ label: "PDF", href: "/working-papers/weakest-link-coordination.pdf" }],
  },
  {
    title: "The Effect of Competition in Contests: A Unifying Approach",
    coauthors: "Sumit Goel",
    status: "Under review",
    abstract: `We study all-pay contests with a general finite type-space and show that the most
    competitive winner-takes-all contest maximizes both total and maximum effort under
    linear or concave costs, resolving a long-standing open question in contest design.
    However, the effect of competition is nuanced, as we uncover an interior discouragement
    effect: making prizes more unequal may reduce effort if relatively inefficient types
    are sufficiently likely. An experiment provides qualitative support for these findings.
    Our analysis develops a novel methodology based on characterizing equilibrium effort
    through the probability of outperforming an arbitrary opponent, offering a broadly
    applicable tool particularly useful in settings where mixed equilibria hinder analysis.
    Moreover, it provides a unifying framework that reconciles contrasting results under
    complete information and continuum type-space environments (for which we establish
    an equilibrium convergence result).`,
    links: [{ label: "PDF", href: "/working-papers/competition-in-contests.pdf" }],
  },
  {
    title: "Order Bias in Performance Evaluation: An Experiment with Sequential Contributors",
    coauthors: "Manu Muñoz",
    status: "Under Review",
    abstract: `Managers allocate jobs, positions, tasks and rewards based on performance evaluations.
    When evaluations respond to irrelevant features of production, personnel decisions may
    become inefficient. We test whether the sequential order of contributions to task affects
    evaluations using 1,811 evaluators acting as managers. Managers watch videos of workers
    contributing sequentially to a common output and make an incentivized hiring decision.
    Workers’ positions in the sequence are randomly assigned and uninformative about performance. We find a systematic order bias favoring first contributors: they are hired 52.5%
    of the time, compared with 18.1% for last contributors. The resulting hiring decisions are
    also inefficient: selected workers are, on average, 38.4% less productive than the most
    productive available worker. The order bias remains after controlling for perceived contribution, perceived difficulty associated with each position, and actual productivity, and
    persists across seven additional treatments varying information and incentives.`,
    links: [{ label: "PDF", href: "/working-papers/order-bias-manuscript.pdf" }],
  },
];

export const inProgress: Publication[] = [
  { title: "The Life Cycle of Beliefs", coauthors: "Larbi Alaoui" },
  { title: "Bargaining over Profit-sharing Agreements: Theory and Experiments", coauthors: "Hulya Eraslan" },
  { title: "Communication behind the Veil of Ignorance", coauthors: "Nick Haas and Hyoeun Park" },
  { title: "Beyond the Binary: Self Perception of Gender Identity and Bargaining Behavior", coauthors: "Nicholas Haas" },
  { title: "Contingent Reasoning in Conflict Resolution", coauthors: "Caleb Cox" },
  { title: "The Decision to Enter Negotiations", coauthors: "Marco Palma" },
  { title: "Cultural Determinants of Exclusion", coauthors: "Hagai Rabinovitch, Margarita Leib, and Shaul Shalvi" },
];
