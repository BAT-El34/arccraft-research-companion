export type Locale = "en" | "fr";
export const pages = [
  "home",
  "paper",
  "evidence",
  "figures",
  "lab",
  "failure-atlas",
  "data",
  "reproducibility",
  "limitations",
  "cite",
] as const;
export type Page = (typeof pages)[number];
export const routes: Record<Locale, Record<Page, string>> = {
  en: {
    home: "",
    paper: "paper",
    evidence: "evidence",
    figures: "figures",
    lab: "lab",
    "failure-atlas": "failure-atlas",
    data: "data",
    reproducibility: "reproducibility",
    limitations: "limitations",
    cite: "cite",
  },
  fr: {
    home: "",
    paper: "article",
    evidence: "preuves",
    figures: "figures",
    lab: "laboratoire",
    "failure-atlas": "failure-atlas",
    data: "donnees",
    reproducibility: "reproductibilite",
    limitations: "limites",
    cite: "citer",
  },
};
export const labels: Record<Locale, Record<Page, string>> = {
  en: {
    home: "Overview",
    paper: "Paper",
    evidence: "Evidence",
    figures: "Figures",
    lab: "Laboratory",
    "failure-atlas": "Failure Atlas",
    data: "Data & provenance",
    reproducibility: "Reproducibility",
    limitations: "Limitations",
    cite: "Cite this work",
  },
  fr: {
    home: "Vue d’ensemble",
    paper: "Article",
    evidence: "Preuves",
    figures: "Figures",
    lab: "Laboratoire",
    "failure-atlas": "Failure Atlas",
    data: "Données et provenance",
    reproducibility: "Reproductibilité",
    limitations: "Limites",
    cite: "Citer ce travail",
  },
};
export const href = (locale: Locale, page: Page) =>
  `/${locale}/${routes[locale][page]}${page === "home" ? "" : "/"}`;
export const tr = (locale: Locale, en: string, fr: string) =>
  locale === "fr" ? fr : en;
