/*
 * DeckGen AI — Data Loader
 * ------------------------------------------------------------
 * Loads the mock "enterprise finance database" (per-quarter CSVs under
 * data/, e.g. data/q1.csv + data/q2.csv), parses them into structured
 * records, and exposes query helpers that the AI deck engine uses to build
 * data-driven slides.
 *
 * All amounts are USD. Variance = actual - budget (positive = overrun).
 */

(function (global) {
  "use strict";

  // Per-quarter source files. Add more quarters here as the data grows.
  const CSV_PATHS = ["data/q1.csv", "data/q2.csv"];

  // ----------------------------------------------------------
  // CSV parsing (tiny, dependency-free)
  // ----------------------------------------------------------
  function parseCSV(text) {
    const lines = text.trim().split(/\r?\n/);
    const headers = lines[0].split(",").map((h) => h.trim());
    return lines.slice(1).map((line) => {
      const cols = line.split(",");
      const row = {};
      headers.forEach((h, i) => {
        row[h] = (cols[i] || "").trim();
      });
      return row;
    });
  }

  // Convert a raw CSV row into a typed, enriched record.
  function enrich(row) {
    const budget = Number(row.budget_usd);
    const actual = Number(row.actual_usd);
    const variance = actual - budget;
    const variancePct = budget === 0 ? 0 : (variance / budget) * 100;
    return {
      quarter: row.quarter,
      department: row.department,
      category: row.category,
      budget,
      actual,
      variance,
      variancePct: Math.round(variancePct * 10) / 10,
    };
  }

  // ----------------------------------------------------------
  // DataStore — holds records + query API
  // ----------------------------------------------------------
  function createStore(records) {
    const api = {
      /** All enriched records. */
      all() {
        return records.slice();
      },

      /** Distinct quarters present in the data, e.g. ["Q1", "Q2"]. */
      quarters() {
        return [...new Set(records.map((r) => r.quarter))];
      },

      /** Distinct spend categories. */
      categories() {
        return [...new Set(records.map((r) => r.category))];
      },

      /** Filter records by quarter and/or category. */
      filter({ quarter, category, department } = {}) {
        return records.filter(
          (r) =>
            (!quarter || r.quarter === quarter) &&
            (!category || r.category === category) &&
            (!department || r.department === department)
        );
      },

      /**
       * Aggregate a quarter's spend by category.
       * Returns [{ category, budget, actual, variance, variancePct }] sorted
       * by variance descending (biggest overruns first).
       */
      aggregateByCategory(quarter) {
        const map = new Map();
        api.filter({ quarter }).forEach((r) => {
          const cur = map.get(r.category) || { budget: 0, actual: 0 };
          cur.budget += r.budget;
          cur.actual += r.actual;
          map.set(r.category, cur);
        });
        return [...map.entries()]
          .map(([category, v]) => {
            const variance = v.actual - v.budget;
            return {
              category,
              budget: v.budget,
              actual: v.actual,
              variance,
              variancePct: Math.round((variance / v.budget) * 1000) / 10,
            };
          })
          .sort((a, b) => b.variance - a.variance);
      },

      /** Totals for a quarter across every category. */
      quarterTotals(quarter) {
        const rows = api.filter({ quarter });
        const budget = rows.reduce((s, r) => s + r.budget, 0);
        const actual = rows.reduce((s, r) => s + r.actual, 0);
        const variance = actual - budget;
        return {
          quarter,
          budget,
          actual,
          variance,
          variancePct: budget === 0 ? 0 : Math.round((variance / budget) * 1000) / 10,
        };
      },

      /**
       * Detail for one category in one quarter, broken down by department.
       * Powers the "why did this overrun" drill-down slide.
       */
      categoryDetail(quarter, category) {
        const rows = api
          .filter({ quarter, category })
          .sort((a, b) => b.variance - a.variance);
        const budget = rows.reduce((s, r) => s + r.budget, 0);
        const actual = rows.reduce((s, r) => s + r.actual, 0);
        const variance = actual - budget;
        return {
          quarter,
          category,
          budget,
          actual,
          variance,
          variancePct: budget === 0 ? 0 : Math.round((variance / budget) * 1000) / 10,
          byDepartment: rows,
        };
      },

      /** The single biggest overrun category for a quarter. */
      topOverrun(quarter) {
        return api.aggregateByCategory(quarter)[0] || null;
      },

      /** Quarter-over-quarter change for a category (e.g. Q1 -> Q2 actuals). */
      quarterOverQuarter(category, fromQuarter, toQuarter) {
        const from = api
          .filter({ quarter: fromQuarter, category })
          .reduce((s, r) => s + r.actual, 0);
        const to = api
          .filter({ quarter: toQuarter, category })
          .reduce((s, r) => s + r.actual, 0);
        const change = to - from;
        return {
          category,
          from,
          to,
          change,
          changePct: from === 0 ? 0 : Math.round((change / from) * 1000) / 10,
        };
      },
    };
    return api;
  }

  // ----------------------------------------------------------
  // Public entrypoint
  // ----------------------------------------------------------
  async function fetchRecords(path) {
    const res = await fetch(path);
    if (!res.ok) {
      throw new Error(
        `DeckGen: could not load ${path} (${res.status}). ` +
          `Serve the folder over http (not file://).`
      );
    }
    const text = await res.text();
    return parseCSV(text).map(enrich);
  }

  const DataLoader = {
    /**
     * Loads and parses every per-quarter CSV, merges them, and returns a
     * single DataStore covering all quarters.
     * Usage: const store = await DataLoader.load();
     */
    async load(paths = CSV_PATHS) {
      const list = Array.isArray(paths) ? paths : [paths];
      const batches = await Promise.all(list.map(fetchRecords));
      const records = batches.flat();
      return createStore(records);
    },

    /** Build a store directly from CSV text (handy for tests / offline). */
    fromText(text) {
      return createStore(parseCSV(text).map(enrich));
    },
  };

  global.DataLoader = DataLoader;
})(typeof window !== "undefined" ? window : globalThis);
