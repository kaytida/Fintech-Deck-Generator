/*
 * DeckGen AI — App shell
 * Handles tab navigation between the Home and Demo pages.
 */

(function () {
  "use strict";

  const tabs = Array.from(document.querySelectorAll(".tab"));
  const pages = Array.from(document.querySelectorAll(".page"));

  function activate(tabName) {
    tabs.forEach((t) => t.classList.toggle("is-active", t.dataset.tab === tabName));
    pages.forEach((p) =>
      p.classList.toggle("is-active", p.id === `page-${tabName}`)
    );
    // keep the URL hash in sync so the tab is shareable / refresh-safe
    if (history.replaceState) {
      history.replaceState(null, "", `#${tabName}`);
    }
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  // Tab clicks
  tabs.forEach((tab) => {
    tab.addEventListener("click", () => activate(tab.dataset.tab));
  });

  // Any element with data-goto (e.g. the hero CTA) can switch tabs too
  document.querySelectorAll("[data-goto]").forEach((el) => {
    el.addEventListener("click", () => activate(el.dataset.goto));
  });

  // Restore tab from URL hash on load (#home / #demo)
  const initial = (location.hash || "#home").replace("#", "");
  activate(pages.some((p) => p.id === `page-${initial}`) ? initial : "home");
})();
