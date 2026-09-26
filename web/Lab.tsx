"use client";
import { useRef, useState } from "react";
import { Locale, href, tr } from "./i18n";
import RunResult, { RunRecord } from "./RunResult";
const modes = [
  "CANONICAL_REPLAY",
  "REGISTERED_VARIANT",
  "EXPLORATORY",
] as const;
export function download(
  value: unknown,
  name: string,
  type = "application/json",
) {
  const blob = new Blob(
    [typeof value === "string" ? value : JSON.stringify(value, null, 2)],
    { type },
  );
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = name;
  a.click();
  setTimeout(() => URL.revokeObjectURL(a.href), 1000);
}
export default function Lab({ locale }: { locale: Locale }) {
  const [mode, setMode] = useState<(typeof modes)[number]>("CANONICAL_REPLAY");
  const [engine, setEngine] = useState("synthetic");
  const [variant, setVariant] = useState("full");
  const [seed, setSeed] = useState(20260825);
  const [worlds, setWorlds] = useState(10000);
  const [simulations, setSimulations] = useState(50000);
  const [frequency, setFrequency] = useState(1);
  const [severity, setSeverity] = useState(1);
  const [expense, setExpense] = useState("");
  const [commission, setCommission] = useState("");
  const [run, setRun] = useState<RunRecord | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const controller = useRef<AbortController | null>(null);
  function invalidate() {
    controller.current?.abort();
    controller.current = null;
    setLoading(false);
    setRun(null);
    setError("");
  }
  async function execute(event: React.FormEvent) {
    event.preventDefault();
    invalidate();
    setLoading(true);
    const c = new AbortController();
    controller.current = c;
    let timeout = false;
    const timer = setTimeout(() => {
      timeout = true;
      c.abort();
    }, 55000);
    const payload =
      engine === "synthetic"
        ? {
            mode,
            variant: mode === "CANONICAL_REPLAY" ? "full" : variant,
            seed: mode === "CANONICAL_REPLAY" ? 20260825 : seed,
            worlds: mode === "EXPLORATORY" ? worlds : 10000,
          }
        : {
            mode,
            seed: mode === "CANONICAL_REPLAY" ? 42 : seed,
            n_simulations: mode === "CANONICAL_REPLAY" ? 50000 : simulations,
            frequency_multiplier: mode === "CANONICAL_REPLAY" ? 1 : frequency,
            severity_multiplier: mode === "CANONICAL_REPLAY" ? 1 : severity,
            expense_ratio:
              mode === "CANONICAL_REPLAY" || expense === ""
                ? null
                : Number(expense),
            commission_ratio:
              mode === "CANONICAL_REPLAY" || commission === ""
                ? null
                : Number(commission),
          };
    try {
      const res = await fetch(`/api/v1/simulate/${engine}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
        signal: c.signal,
      });
      const data = await res.json();
      if (!res.ok)
        throw Error(
          typeof data.detail === "string"
            ? data.detail
            : JSON.stringify(data.detail),
        );
      if (controller.current === c) setRun(data);
    } catch (e) {
      if (controller.current === c)
        setError(
          c.signal.aborted
            ? timeout
              ? tr(
                  locale,
                  "Time budget exceeded. No result was accepted.",
                  "Budget de temps dépassé. Aucun résultat accepté.",
                )
              : tr(locale, "Run cancelled.", "Run annulé.")
            : String(e),
        );
    } finally {
      clearTimeout(timer);
      if (controller.current === c) setLoading(false);
    }
  }
  return (
    <>
      <section className="section">
        <p className="eyebrow">
          {tr(locale, "REFERENCE / READ ONLY", "RÉFÉRENCE / LECTURE SEULE")}
        </p>
        <h2>
          {tr(
            locale,
            "Precomputed reference artifacts",
            "Artefacts de référence pré-calculés",
          )}
        </h2>
        <p>
          {tr(
            locale,
            "These downloads are frozen local reproductions. They are not the result of a new web execution.",
            "Ces téléchargements sont des reproductions locales figées. Ils ne résultent pas d’une nouvelle exécution web.",
          )}
        </p>
        <div className="actions">
          <a href="/downloads/artifacts/candidate/canonical-worlds.json">
            {tr(locale, "Synthetic worlds", "Mondes synthétiques")} ↓
          </a>
          <a href="/downloads/artifacts/candidate/motor-forecast.json">
            {tr(locale, "Motor forecast", "Projection automobile")} ↓
          </a>
          <a href="/data/registry.json">
            {tr(locale, "Source manifests", "Manifestes sources")} ↓
          </a>
        </div>
      </section>
      <section className="panel lab">
        <p className="eyebrow">
          {tr(locale, "NEW EXECUTION", "NOUVELLE EXÉCUTION")}
        </p>
        <h2>{tr(locale, "Reproduce or explore", "Reproduire ou explorer")}</h2>
        <form onSubmit={execute}>
          <div className="form-grid">
            <label>
              {tr(locale, "Execution mode", "Mode d’exécution")}
              <select
                value={mode}
                onChange={(e) => {
                  invalidate();
                  setMode(e.target.value as typeof mode);
                  if (e.target.value === "REGISTERED_VARIANT") {
                    setEngine("synthetic");
                    setSeed(20260825);
                  }
                }}
              >
                {modes.map((m) => (
                  <option key={m}>{m}</option>
                ))}
              </select>
            </label>
            <label>
              {tr(locale, "Scientific model", "Modèle scientifique")}
              <select
                disabled={mode === "REGISTERED_VARIANT"}
                value={engine}
                onChange={(e) => {
                  invalidate();
                  setEngine(e.target.value);
                  setSeed(e.target.value === "motor" ? 42 : 20260825);
                }}
              >
                <option value="synthetic">
                  {tr(locale, "Synthetic worlds", "Mondes synthétiques")}
                </option>
                <option value="motor">
                  {tr(
                    locale,
                    "External motor portfolio",
                    "Portefeuille automobile externe",
                  )}
                </option>
              </select>
            </label>
          </div>
          {mode === "CANONICAL_REPLAY" ? (
            <p className="locked">
              ▣{" "}
              {engine === "synthetic"
                ? tr(
                    locale,
                    "Locked: full configuration · seed 20260825 · 10,000 worlds · 12 periods.",
                    "Verrouillé : configuration complète · seed 20260825 · 10 000 mondes · 12 périodes.",
                  )
                : tr(
                    locale,
                    "Locked: seed 42 · 50,000 simulations · calibration 2022–2023 · evaluation 2024.",
                    "Verrouillé : seed 42 · 50 000 simulations · calibration 2022–2023 · évaluation 2024.",
                  )}
            </p>
          ) : (
            <div className="form-grid">
              <label>
                Seed{" "}
                {mode === "REGISTERED_VARIANT" ? (
                  <select
                    value={seed}
                    onChange={(e) => {
                      invalidate();
                      setSeed(Number(e.target.value));
                    }}
                  >
                    {[20260825, 20260826, 20260827].map((s) => (
                      <option key={s}>{s}</option>
                    ))}
                  </select>
                ) : (
                  <input
                    type="number"
                    required
                    min={0}
                    max={4294967295}
                    value={seed}
                    onChange={(e) => {
                      invalidate();
                      setSeed(Number(e.target.value));
                    }}
                  />
                )}
              </label>
              {engine === "synthetic" ? (
                <>
                  <label>
                    {tr(
                      locale,
                      "Registered configuration",
                      "Configuration enregistrée",
                    )}
                    <select
                      value={variant}
                      onChange={(e) => {
                        invalidate();
                        setVariant(e.target.value);
                      }}
                    >
                      {[
                        "full",
                        "no_validator",
                        "strict_reject",
                        "no_transitions",
                        "shared_stream",
                      ].map((v) => (
                        <option key={v}>{v}</option>
                      ))}
                    </select>
                  </label>
                  <label>
                    {tr(locale, "Worlds", "Mondes")}
                    <input
                      type="number"
                      min={100}
                      max={10000}
                      required
                      disabled={mode !== "EXPLORATORY"}
                      value={mode === "EXPLORATORY" ? worlds : 10000}
                      onChange={(e) => {
                        invalidate();
                        setWorlds(Number(e.target.value));
                      }}
                    />
                  </label>
                </>
              ) : (
                <>
                  <label>
                    Simulations
                    <input
                      type="number"
                      min={500}
                      max={50000}
                      required
                      value={simulations}
                      onChange={(e) => {
                        invalidate();
                        setSimulations(Number(e.target.value));
                      }}
                    />
                  </label>
                  <label>
                    {tr(
                      locale,
                      "Frequency multiplier",
                      "Multiplicateur de fréquence",
                    )}
                    <input
                      type="number"
                      min={0.5}
                      max={2}
                      step={0.05}
                      required
                      value={frequency}
                      onChange={(e) => {
                        invalidate();
                        setFrequency(Number(e.target.value));
                      }}
                    />
                  </label>
                  <label>
                    {tr(
                      locale,
                      "Severity multiplier",
                      "Multiplicateur de sévérité",
                    )}
                    <input
                      type="number"
                      min={0.5}
                      max={2}
                      step={0.05}
                      required
                      value={severity}
                      onChange={(e) => {
                        invalidate();
                        setSeverity(Number(e.target.value));
                      }}
                    />
                  </label>
                  <label>
                    {tr(
                      locale,
                      "Expense ratio assumption (optional)",
                      "Hypothèse de frais (facultatif)",
                    )}
                    <input
                      type="number"
                      min={0}
                      max={1}
                      step={0.01}
                      value={expense}
                      onChange={(e) => {
                        invalidate();
                        setExpense(e.target.value);
                      }}
                    />
                  </label>
                  <label>
                    {tr(
                      locale,
                      "Commission ratio assumption (optional)",
                      "Hypothèse de commissions (facultatif)",
                    )}
                    <input
                      type="number"
                      min={0}
                      max={1}
                      step={0.01}
                      value={commission}
                      onChange={(e) => {
                        invalidate();
                        setCommission(e.target.value);
                      }}
                    />
                  </label>
                </>
              )}
            </div>
          )}
          {engine === "motor" && (
            <p>
              {tr(
                locale,
                "Training periods remain fixed. Realized target claims evaluate the projection and never calibrate it. Supply both expense and commission assumptions or leave both blank.",
                "Les périodes de calibration restent fixes. Les sinistres réalisés de l’année cible évaluent la projection sans la calibrer. Renseigner frais et commissions ensemble ou laisser les deux champs vides.",
              )}
            </p>
          )}
          {mode === "EXPLORATORY" && (
            <p className="notice">
              {tr(
                locale,
                "EXPLORATORY — These assumptions are not independently validated.",
                "EXPLORATORY — Ces hypothèses ne sont pas validées indépendamment.",
              )}
            </p>
          )}
          <div className="actions">
            <button className="button primary" disabled={loading} type="submit">
              {loading
                ? tr(locale, "Computing…", "Calcul en cours…")
                : tr(locale, "Execute new run", "Exécuter un nouveau run")}{" "}
              →
            </button>
            {loading && (
              <button
                className="button"
                type="button"
                onClick={() => controller.current?.abort()}
              >
                {tr(locale, "Cancel", "Annuler")}
              </button>
            )}
          </div>
          <p className="muted">
            {tr(
              locale,
              "Public execution depends on the runtime health and shared rate-limit protection. A cancelled request may finish on the server but its response will not be accepted.",
              "L’exécution publique dépend de l’état du runtime et de la protection de débit partagée. Une requête annulée peut terminer côté serveur ; sa réponse ne sera pas acceptée.",
            )}
          </p>
        </form>
      </section>
      <section aria-live="polite" aria-busy={loading}>
        {error && (
          <p className="error" role="alert">
            {error}
          </p>
        )}
        {run && <RunResult run={run} locale={locale} />}
      </section>
    </>
  );
}
