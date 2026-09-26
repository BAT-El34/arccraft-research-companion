import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { pages, href, Locale } from "../../web/i18n";

for (const locale of ["en", "fr"] as Locale[]) {
  test(`${locale}: every route renders with language, one heading, and no runtime error`, async ({
    page,
  }) => {
    const errors: string[] = [];
    page.on("pageerror", (e) => errors.push(e.message));
    for (const p of pages) {
      const response = await page.goto(href(locale, p));
      expect(response?.status()).toBe(200);
      await expect(page.locator("html")).toHaveAttribute("lang", locale);
      await expect(page.locator("h1")).toHaveCount(1);
      await expect(page.locator('nav a[aria-current="page"]')).toHaveCount(1);
    }
    expect(errors).toEqual([]);
  });
}
test("language switch preserves semantic route; theme persists across navigation", async ({
  page,
}) => {
  await page.goto("/en/evidence/");
  await page.getByRole("link", { name: "FR", exact: true }).click();
  await expect(page).toHaveURL(/\/fr\/preuves\//);
  await page.getByRole("button", { name: /Thème/ }).click();
  const theme = await page.locator("html").getAttribute("data-theme");
  await page
    .getByRole("link", { name: /Laboratoire/, exact: false })
    .first()
    .click();
  await expect(page.locator("html")).toHaveAttribute("data-theme", theme!);
});
test("reference atlas includes five rejects with null metrics and filters export", async ({
  page,
}) => {
  await page.goto("/en/failure-atlas/");
  await page.getByLabel("Validation status").selectOption("REJECT");
  await expect(page.locator("tbody tr")).toHaveCount(5);
  await expect(page.locator("tbody tr").first()).toContainText("null");
  const downloaded = page.waitForEvent("download");
  await page.getByRole("button", { name: "JSON ↓", exact: true }).click();
  expect((await downloaded).suggestedFilename()).toBe(
    "arccraft-atlas-filtered.json",
  );
  await page.getByLabel("World ID").fill("9999");
  await expect(page.getByText("No event matches these filters.")).toBeVisible();
});
test("motor replay reports exact comparison; exploration is separate; network error clears prior success", async ({
  page,
}) => {
  await page.goto("/en/lab/");
  await page.getByLabel("Scientific model").selectOption("motor");
  const execution = page.waitForResponse(
    (r) =>
      r.url().endsWith("/api/v1/simulate/motor") &&
      r.request().method() === "POST",
  );
  await page.getByRole("button", { name: /Execute new run/ }).click();
  const receipt = await (await execution).json();
  expect(["VERIFIED", "DIVERGENT"]).toContain(receipt.proof_status);
  await expect(page.locator(".run-result h2")).toHaveText(receipt.proof_status);
  await page.getByLabel("Execution mode").selectOption("EXPLORATORY");
  await expect(page.locator(".run-result")).toHaveCount(0);
  await page.getByLabel("Severity multiplier").fill("1.25");
  await page.getByRole("button", { name: /Execute new run/ }).click();
  await expect(page.locator(".run-result h2")).toHaveText(
    "EXPLORATORY_NOT_VALIDATED",
  );
  await page.route("**/api/v1/simulate/motor", (route) =>
    route.abort("failed"),
  );
  await page.getByRole("button", { name: /Execute new run/ }).click();
  await expect(page.locator(".error[role=alert]")).toBeVisible();
  await expect(page.locator(".run-result")).toHaveCount(0);
});
test("candidate PDF download and figure assets exist", async ({
  page,
  request,
}) => {
  await page.goto("/en/paper/");
  const pdf = page.getByRole("link", { name: "PDF ↗", exact: true });
  await expect(pdf).toBeVisible();
  const response = await request.get((await pdf.getAttribute("href"))!);
  expect(response.headers()["content-type"]).toContain("application/pdf");
  await page.goto("/en/figures/");
  await expect(page.locator("figure")).toHaveCount(7);
  for (const img of await page.locator("figure img").all()) {
    expect((await request.get((await img.getAttribute("src"))!)).status()).toBe(
      200,
    );
  }
});
for (const theme of ["light", "dark"]) {
  test(`accessibility ${theme}: key routes and 320px reflow`, async ({
    page,
  }) => {
    await page.goto("/en/");
    await page.evaluate((value) => {
      localStorage.setItem("arccraft-theme", value);
      document.documentElement.dataset.theme = value;
    }, theme);
    for (const route of [
      "/en/",
      "/fr/preuves/",
      "/en/lab/",
      "/en/failure-atlas/",
    ]) {
      await page.goto(route);
      if (route.includes("atlas"))
        await expect(page.locator("tbody tr").first()).toBeVisible();
      const scan = await new AxeBuilder({ page })
        .withTags(["wcag2a", "wcag2aa", "wcag21aa"])
        .analyze();
      expect(scan.violations).toEqual([]);
      await page.setViewportSize({ width: 320, height: 800 });
      expect(
        await page.evaluate(
          () => document.documentElement.scrollWidth <= window.innerWidth,
        ),
      ).toBe(true);
      await page.setViewportSize({ width: 1440, height: 960 });
    }
    await page.goto("/en/");
    await page.screenshot({
      path: `test-results/home-${theme}.png`,
      fullPage: true,
    });
    await page.setViewportSize({ width: 390, height: 844 });
    await page.screenshot({
      path: `test-results/home-${theme}-mobile.png`,
      fullPage: true,
    });
  });
}

test("exploratory atlas retains its run and reference stays separate", async ({
  page,
}) => {
  await page.goto("/en/lab/");
  await page.getByLabel("Execution mode").selectOption("EXPLORATORY");
  await page.getByLabel("Worlds", { exact: true }).fill("100");
  await page.getByRole("button", { name: /Execute new run/ }).click();
  await expect(page.locator(".run-result h2")).toHaveText(
    "EXPLORATORY_NOT_VALIDATED",
  );
  await page.getByRole("button", { name: /Inspect this run/ }).click();
  await expect(page).toHaveURL(/source=live/);
  await expect(
    page.getByText("LIVE / EXPLORATORY", { exact: true }),
  ).toBeVisible();
  await expect(page.locator("tbody tr").first()).toBeVisible();
  await page
    .getByRole("link", { name: "Reference atlas", exact: true })
    .click();
  await expect(
    page.getByText("PRECOMPUTED REFERENCE / CANDIDATE", { exact: true }),
  ).toBeVisible();
  await page.getByLabel("Validation status").selectOption("REJECT");
  await expect(page.locator("tbody tr")).toHaveCount(5);
});

test("keyboard access, 200 percent zoom and cancellation announce a clean state", async ({
  page,
}) => {
  await page.goto("/en/lab/");
  await page.keyboard.press("Tab");
  await expect(
    page.getByRole("link", { name: "Skip to content" }),
  ).toBeFocused();
  await page.keyboard.press("Enter");
  await expect(page.locator("#main")).toBeFocused();
  await page.evaluate(() => {
    document.body.style.zoom = "2";
  });
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= window.innerWidth,
    ),
  ).toBe(true);
  await page.evaluate(() => {
    document.body.style.zoom = "1";
  });
  await page.route("**/api/v1/simulate/synthetic", async (route) => {
    await new Promise((r) => setTimeout(r, 3000));
    try {
      await route.abort();
    } catch {}
  });
  await page.getByRole("button", { name: /Execute new run/ }).click();
  await page.getByRole("button", { name: "Cancel", exact: true }).click();
  await expect(page.locator(".error[role=alert]")).toHaveText("Run cancelled.");
  await expect(page.locator(".run-result")).toHaveCount(0);
});
