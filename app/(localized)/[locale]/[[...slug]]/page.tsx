import { notFound } from "next/navigation";
import { pages, routes, labels, Locale, href } from "@/i18n";
import Companion from "@/Companion";
export const dynamicParams = false;
export function generateStaticParams() {
  return (["en", "fr"] as Locale[]).flatMap((locale) =>
    pages.map((page) => ({
      locale,
      slug: routes[locale][page] ? [routes[locale][page]] : [],
    })),
  );
}
function resolve(locale: string, slug: string[] = []) {
  return locale === "en" || locale === "fr"
    ? pages.find((page) => routes[locale][page] === slug.join("/"))
    : undefined;
}
export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string; slug?: string[] }>;
}) {
  const { locale, slug } = await params;
  const page = resolve(locale, slug);
  if (!page) return {};
  return {
    title: `${labels[locale as Locale][page]} — ARCCRAFT`,
    description:
      "Procedural stress testing of actuarial models. Scientific evidence, limitations and reproducible experiments.",
    alternates: { languages: { en: href("en", page), fr: href("fr", page) } },
  };
}
export default async function Page({
  params,
}: {
  params: Promise<{ locale: string; slug?: string[] }>;
}) {
  const { locale, slug } = await params;
  const page = resolve(locale, slug);
  if (!page) notFound();
  return <Companion locale={locale as Locale} page={page} />;
}
