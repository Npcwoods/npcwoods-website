export type Chapter = {
  number: number;
  title: string;
  body: string;
};

export type Review = {
  initials: string;
  quote: string;
};

export type Faq = {
  question: string;
  answer: string;
};

export const smsHref = "sms:4806394722";
export const smsMessage = "Hi Chris, I’d like to start a $59 visit.";
export const smsVisitHref = `${smsHref}?&body=${encodeURIComponent(smsMessage)}`;

export const chapters = [
  {
    number: 1,
    title: "I feel awful.",
    body: "You need a clear next step, without turning your whole day upside down.",
  },
  {
    number: 2,
    title: "I don’t have time for the runaround.",
    body: "Getting help should not mean rearranging work, family, and everything else.",
  },
  {
    number: 3,
    title: "A real person can help me.",
    body: "Chris Woods, NP, personally reviews your message and helps you understand the safest next step.",
  },
  {
    number: 4,
    title: "This is actually simple.",
    body: "Tell Chris what’s going on. He’ll review it and reply with clear next steps.",
  },
  {
    number: 5,
    title: "I know exactly what to do next.",
    body: "One text starts a straightforward conversation about the care that fits your situation.",
  },
] as const satisfies readonly [Chapter, Chapter, Chapter, Chapter, Chapter];

export const reviews: readonly Review[] = [
  {
    initials: "A.H.",
    quote: "Fast and convenient—I reached out at 10:08 and was taken care of by 10:52 the same day.",
  },
  {
    initials: "J.R.",
    quote: "Simple and easy. My prescription was sent in without any hassle.",
  },
  {
    initials: "T.P.",
    quote: "Timely, professional, and easy to talk to.",
  },
] as const;

export const states = [
  "Arizona",
  "Colorado",
  "Georgia",
  "Idaho",
  "Iowa",
  "Montana",
  "Nevada",
  "New Mexico",
  "North Carolina",
  "Oregon",
  "Utah",
] as const;

export const faqs: readonly Faq[] = [
  {
    question: "What happens when I text Chris?",
    answer: "Chris reviews what you share and explains the safest next step for your situation.",
  },
  {
    question: "What does a visit cost?",
    answer: "Each visit is a $59 flat fee, with no hidden fees.",
  },
  {
    question: "What if text-based care is not the safe fit?",
    answer: "Chris will plainly direct you to in-person or emergency care when that is the safest next step.",
  },
] as const;
