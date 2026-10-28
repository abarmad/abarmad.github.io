export interface EventLink {
  label: string;
  href: string;
}

export interface EventItem {
  date: string;        // start date, YYYY-MM-DD
  endDate?: string;    // optional, for multi-day events
  title: string;       // event or talk title
  type?: string;       // e.g. "Talk", "Conference", "Seminar"
  location?: string;
  details?: string;    // e.g. the title of the paper being presented
}

// Add upcoming events anywhere in the list. The home page shows the soonest
// ones first, and an event disappears after its last day.
// If nothing here is upcoming, the box is hidden.
export const events: EventItem[] = [
  {
    date: "2026-10-31", // REPLACE this sample with a real event
    title: "ESA North America",
    type: "Paper",
    location: "Charlottesville, Virginia, USA",
    details: "Presenting: Order Bias in Performance Evaluation: An Experiment with Sequential Contributors",
  },
  {
    date: "2026-11-02", // REPLACE this sample with a real event
    title: "Universidad Francisco Marroquín",
    type: "Paper",
    location: "Ciudad de Guatemala, Guatemala",
    details: "Presenting: Order Bias in Performance Evaluation: An Experiment with Sequential Contributors",
  },
  {
    date: "2026-11-12", // REPLACE this sample with a real event
    title: "American University of Sharjah",
    type: "Talk",
    location: "Sharjah, UAE",
    details: "Guest Talk: More Than a Research Space: The Experimental Lab as a Catalyst for Academic Excellence",
  },
  {
    date: "2027-01-04", // REPLACE this sample with a real event
    title: "ASSA ESA Session on Experiments on Bounded Rationality and Communication",
    type: "Talk",
    location: "Washington DC, USA",
    details: "Guest Talk: Are teams more rational than individuals? A meta-study and new experiments",
  },
];
