// Dark theme only — the site is designed around the night-sky background.
(function () {
  const root = document.documentElement;
  root.setAttribute("data-theme", "dark");

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
