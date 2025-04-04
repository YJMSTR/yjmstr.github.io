// Theme handling: respect saved choice, fall back to system preference.
(function () {
  const root = document.documentElement;
  const saved = localStorage.getItem("theme");
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  root.setAttribute("data-theme", saved || (prefersDark ? "dark" : "light"));

  const toggle = document.getElementById("theme-toggle");
  toggle.addEventListener("click", function () {
    const next =
      root.getAttribute("data-theme") === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", next);
    localStorage.setItem("theme", next);
  });

  const year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();

  // Reading progress bar (blog posts only)
  const bar = document.getElementById("progress-bar");
  if (bar) {
    const update = function () {
      const doc = document.documentElement;
      const total = doc.scrollHeight - doc.clientHeight;
      bar.style.width = (total > 0 ? (doc.scrollTop / total) * 100 : 0) + "%";
    };
    document.addEventListener("scroll", update, { passive: true });
    update();
  }
})();
