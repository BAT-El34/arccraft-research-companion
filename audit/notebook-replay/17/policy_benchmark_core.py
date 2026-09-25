from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy import sparse
from scipy.optimize import minimize


MODEL_COLUMNS = [
    "insured_id", "year", "policy_type", "policy_status", "business_type", "payment_frequency",
    "bonus_score", "driver_age", "vehicle_age", "age_driving_licence",
    "fuel_type", "vehicle_value", "seats", "power_to_weight_ratio",
    "vehicle_brand", "municipality_type", "circulation_area", "total_premium",
    "total_claims", "total_incurred", "total_exposure",
]

CATEGORICAL_FEATURES = [
    "policy_type", "business_type", "payment_frequency", "bonus_score",
    "fuel_type", "vehicle_brand", "municipality_type", "circulation_area",
]

NUMERIC_FEATURES = [
    "driver_age", "vehicle_age", "age_driving_licence", "vehicle_value",
    "seats", "power_to_weight_ratio",
]


def load_model_data(db_path: Path) -> pd.DataFrame:
    import sqlite3

    with sqlite3.connect(db_path) as con:
        return pd.read_sql_query(
            f"SELECT {', '.join(MODEL_COLUMNS)} FROM motor_portfolio ORDER BY year, insured_id",
            con,
        )


@dataclass
class SparseFeatureEncoder:
    include_calendar_trend: bool = False
    rare_brand_min_count: int = 500

    def fit(self, frame: pd.DataFrame) -> "SparseFeatureEncoder":
        self.numeric_parameters_: dict[str, dict[str, float]] = {}
        transformed = self._numeric_raw(frame)
        for column in transformed.columns:
            values = transformed[column].to_numpy(dtype=float)
            finite = np.isfinite(values)
            median = float(np.nanmedian(values[finite])) if finite.any() else 0.0
            filled = np.where(finite, values, median)
            low, high = np.quantile(filled, [0.005, 0.995])
            clipped = np.clip(filled, low, high)
            mean = float(np.mean(clipped))
            std = float(np.std(clipped)) or 1.0
            self.numeric_parameters_[column] = {
                "median": median, "low": float(low), "high": float(high),
                "mean": mean, "std": std,
            }

        self.category_parameters_: dict[str, dict[str, Any]] = {}
        for column in CATEGORICAL_FEATURES:
            values = frame[column].fillna("__MISSING__").astype(str).str.strip()
            counts = values.value_counts(dropna=False)
            if column == "vehicle_brand":
                kept = counts[counts >= self.rare_brand_min_count].index.tolist()
            else:
                kept = counts.index.tolist()
            reference = str(counts.index[0])
            levels = sorted({str(x) for x in kept if str(x) != reference})
            if "__OTHER__" not in levels:
                levels.append("__OTHER__")
            self.category_parameters_[column] = {
                "kept": set(map(str, kept)), "reference": reference, "levels": levels,
            }

        names = ["intercept"]
        names.extend(transformed.columns.tolist())
        names.extend(f"{column}={level}" for column in CATEGORICAL_FEATURES
                     for level in self.category_parameters_[column]["levels"])
        self.feature_names_ = names
        return self

    def _numeric_raw(self, frame: pd.DataFrame) -> pd.DataFrame:
        raw = pd.DataFrame(index=frame.index)
        raw["driver_age"] = pd.to_numeric(frame["driver_age"], errors="coerce")
        raw["vehicle_age"] = pd.to_numeric(frame["vehicle_age"], errors="coerce")
        # The dictionary says calendar year, but observed values 0-80 contradict it.
        # Use only as an unidentified tenure-like proxy and preserve the ambiguity.
        raw["licence_value_proxy"] = pd.to_numeric(frame["age_driving_licence"], errors="coerce")
        raw["log_vehicle_value"] = np.log1p(pd.to_numeric(frame["vehicle_value"], errors="coerce"))
        raw["seats"] = pd.to_numeric(frame["seats"], errors="coerce")
        raw["log_power_to_weight"] = np.log1p(pd.to_numeric(frame["power_to_weight_ratio"], errors="coerce"))
        for base in ["driver_age", "vehicle_age", "licence_value_proxy", "log_vehicle_value"]:
            raw[f"{base}_squared"] = raw[base] ** 2
        if self.include_calendar_trend:
            raw["calendar_index"] = pd.to_numeric(frame["year"], errors="coerce") - 2022.0
        return raw

    def transform(self, frame: pd.DataFrame) -> sparse.csr_matrix:
        n = len(frame)
        blocks: list[sparse.csr_matrix] = [sparse.csr_matrix(np.ones((n, 1), dtype=float))]
        transformed = self._numeric_raw(frame)
        numeric_columns = []
        for column, params in self.numeric_parameters_.items():
            values = transformed[column].to_numpy(dtype=float)
            values = np.where(np.isfinite(values), values, params["median"])
            values = np.clip(values, params["low"], params["high"])
            numeric_columns.append((values - params["mean"]) / params["std"])
        blocks.append(sparse.csr_matrix(np.column_stack(numeric_columns)))

        rows = np.arange(n)
        for column in CATEGORICAL_FEATURES:
            params = self.category_parameters_[column]
            values = frame[column].fillna("__MISSING__").astype(str).str.strip().to_numpy()
            mapped = np.array([v if v in params["kept"] else "__OTHER__" for v in values], dtype=object)
            level_to_col = {level: j for j, level in enumerate(params["levels"])}
            cols = np.array([level_to_col.get(v, -1) if v != params["reference"] else -1 for v in mapped])
            mask = cols >= 0
            block = sparse.csr_matrix(
                (np.ones(mask.sum()), (rows[mask], cols[mask])),
                shape=(n, len(params["levels"])),
            )
            blocks.append(block)
        return sparse.hstack(blocks, format="csr")


@dataclass
class PenalizedPPML:
    alpha: float = 1e-4
    max_iterations: int = 500

    def fit(self, X: sparse.csr_matrix, y: np.ndarray, exposure: np.ndarray) -> "PenalizedPPML":
        y = np.asarray(y, dtype=float)
        exposure = np.asarray(exposure, dtype=float)
        if np.any(exposure <= 0) or np.any(y < 0):
            raise ValueError("PPML requires positive exposure and non-negative response")
        offset = np.log(exposure)
        n = len(y)
        beta0 = np.zeros(X.shape[1], dtype=float)
        beta0[0] = np.log(max(y.sum() / exposure.sum(), 1e-12))
        penalty_mask = np.ones(X.shape[1], dtype=float)
        penalty_mask[0] = 0.0

        def objective(beta: np.ndarray) -> tuple[float, np.ndarray]:
            eta = np.clip(X @ beta + offset, -30.0, 30.0)
            mu = np.exp(eta)
            loss = float(np.mean(mu - y * eta) + 0.5 * self.alpha * np.sum((penalty_mask * beta) ** 2))
            gradient = np.asarray(X.T @ (mu - y)).ravel() / n + self.alpha * penalty_mask * beta
            return loss, gradient

        result = minimize(
            fun=lambda b: objective(b)[0], x0=beta0,
            jac=lambda b: objective(b)[1], method="L-BFGS-B",
            options={"maxiter": self.max_iterations, "ftol": 1e-11, "gtol": 1e-7, "maxls": 40},
        )
        self.coef_ = result.x
        self.converged_ = bool(result.success)
        self.message_ = str(result.message)
        self.iterations_ = int(result.nit)
        self.training_total_observed_ = float(y.sum())
        self.training_total_predicted_ = float(self.predict_mean(X, exposure).sum())
        return self

    def predict_rate(self, X: sparse.csr_matrix) -> np.ndarray:
        return np.exp(np.clip(X @ self.coef_, -30.0, 30.0))

    def predict_mean(self, X: sparse.csr_matrix, exposure: np.ndarray) -> np.ndarray:
        return np.asarray(exposure, dtype=float) * self.predict_rate(X)


def poisson_deviance(y: np.ndarray, mu: np.ndarray) -> float:
    y = np.asarray(y, dtype=float)
    mu = np.clip(np.asarray(mu, dtype=float), 1e-12, None)
    terms = mu.copy()
    positive = y > 0
    terms[positive] = y[positive] * np.log(y[positive] / mu[positive]) - (y[positive] - mu[positive])
    return float(2.0 * np.mean(terms))


def aggregate_interval(mean_count: np.ndarray, mean_severity: np.ndarray, sigma_log: float) -> dict[str, float]:
    mean_count = np.asarray(mean_count, dtype=float)
    mean_severity = np.asarray(mean_severity, dtype=float)
    count_mean = float(mean_count.sum())
    count_sd = float(np.sqrt(count_mean))
    incurred_mean = float(np.sum(mean_count * mean_severity))
    incurred_var = float(np.sum(mean_count * (mean_severity ** 2) * np.exp(sigma_log ** 2)))
    incurred_sd = float(np.sqrt(max(incurred_var, 0.0)))
    return {
        "claim_q025": max(count_mean - 1.96 * count_sd, 0.0),
        "claim_q975": count_mean + 1.96 * count_sd,
        "incurred_q025": max(incurred_mean - 1.96 * incurred_sd, 0.0),
        "incurred_q975": incurred_mean + 1.96 * incurred_sd,
    }


def calibration_by_decile(observed: np.ndarray, predicted: np.ndarray, label: str) -> pd.DataFrame:
    work = pd.DataFrame({"observed": observed, "predicted": predicted})
    work["decile"] = pd.qcut(work["predicted"].rank(method="first"), 10, labels=False) + 1
    out = work.groupby("decile", as_index=False).agg(
        rows=("observed", "size"), observed=("observed", "sum"), predicted=("predicted", "sum")
    )
    out["observed_to_predicted"] = out["observed"] / out["predicted"].replace(0, np.nan)
    out["metric"] = label
    return out


def fit_policy_models(
    frame: pd.DataFrame, calibration_years: list[int], target_year: int,
    sigma_log: float, include_calendar_trend: bool = False,
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    train = frame[frame["year"].isin(calibration_years)].copy()
    target = frame[frame["year"] == target_year].copy()
    encoder = SparseFeatureEncoder(include_calendar_trend=include_calendar_trend).fit(train)
    X_train = encoder.transform(train)
    X_target = encoder.transform(target)

    positive_exposure = train["total_exposure"].to_numpy(float) > 0
    frequency_model = PenalizedPPML().fit(
        X_train[positive_exposure],
        train.loc[positive_exposure, "total_claims"].to_numpy(float),
        train.loc[positive_exposure, "total_exposure"].to_numpy(float),
    )
    target_count_mean = frequency_model.predict_mean(X_target, target["total_exposure"].to_numpy(float))

    claim_bearing = train["total_claims"].to_numpy(float) > 0
    severity_model = PenalizedPPML().fit(
        X_train[claim_bearing],
        train.loc[claim_bearing, "total_incurred"].to_numpy(float),
        train.loc[claim_bearing, "total_claims"].to_numpy(float),
    )
    target_severity_mean = severity_model.predict_rate(X_target)

    pooled_frequency = float(train["total_claims"].sum() / train["total_exposure"].sum())
    pooled_severity = float(train["total_incurred"].sum() / train["total_claims"].sum())
    pooled_count_mean = target["total_exposure"].to_numpy(float) * pooled_frequency
    pooled_severity_vector = np.full(len(target), pooled_severity)

    variants = [
        ("aggregate_pooled", pooled_count_mean, pooled_severity_vector),
        ("policy_frequency_pooled_severity", target_count_mean, pooled_severity_vector),
        ("policy_frequency_policy_severity", target_count_mean, target_severity_mean),
    ]
    rows = []
    for name, count_mean, severity_mean in variants:
        incurred_mean = count_mean * severity_mean
        intervals = aggregate_interval(count_mean, severity_mean, sigma_log)
        observed_claims = float(target["total_claims"].sum())
        observed_incurred = float(target["total_incurred"].sum())
        predicted_claims = float(count_mean.sum())
        predicted_incurred = float(incurred_mean.sum())
        rows.append({
            "calibration": f"{min(calibration_years)}-{max(calibration_years)}",
            "target": target_year,
            "model": name + ("_calendar_trend" if include_calendar_trend else ""),
            "observed_claims": observed_claims,
            "predicted_claims": predicted_claims,
            "claim_error_pct": 100.0 * (predicted_claims - observed_claims) / observed_claims,
            "claim_poisson_deviance": poisson_deviance(target["total_claims"], count_mean),
            "claims_in_process_95_interval": intervals["claim_q025"] <= observed_claims <= intervals["claim_q975"],
            "observed_incurred": observed_incurred,
            "predicted_incurred": predicted_incurred,
            "incurred_error_pct": 100.0 * (predicted_incurred - observed_incurred) / observed_incurred,
            "incurred_poisson_deviance": poisson_deviance(target["total_incurred"], incurred_mean),
            "incurred_in_process_95_interval": intervals["incurred_q025"] <= observed_incurred <= intervals["incurred_q975"],
            **intervals,
        })

    calibration = pd.concat([
        calibration_by_decile(target["total_claims"].to_numpy(float), target_count_mean, "claim_count"),
        calibration_by_decile(target["total_incurred"].to_numpy(float), target_count_mean * target_severity_mean, "incurred"),
    ], ignore_index=True)
    calibration.insert(0, "target", target_year)

    diagnostics = {
        "frequency_converged": frequency_model.converged_,
        "frequency_message": frequency_model.message_,
        "frequency_iterations": frequency_model.iterations_,
        "frequency_training_observed": frequency_model.training_total_observed_,
        "frequency_training_predicted": frequency_model.training_total_predicted_,
        "severity_converged": severity_model.converged_,
        "severity_message": severity_model.message_,
        "severity_iterations": severity_model.iterations_,
        "severity_training_observed": severity_model.training_total_observed_,
        "severity_training_predicted": severity_model.training_total_predicted_,
        "n_features": len(encoder.feature_names_),
        "feature_names": encoder.feature_names_,
        "target_count_mean": target_count_mean,
        "target_severity_mean": target_severity_mean,
    }
    return pd.DataFrame(rows), calibration, diagnostics
