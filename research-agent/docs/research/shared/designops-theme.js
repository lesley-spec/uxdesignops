(function () {
  var STORAGE_KEY = "ux-designops-theme";

  function systemPrefersDark() {
    return window.matchMedia("(prefers-color-scheme: dark)").matches;
  }

  function resolveTheme(stored) {
    if (stored === "dark" || stored === "light") return stored;
    return systemPrefersDark() ? "dark" : "light";
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    var btn = document.getElementById("theme-toggle");
    if (!btn) return;
    var isDark = theme === "dark";
    btn.setAttribute("aria-pressed", isDark ? "true" : "false");
    btn.setAttribute(
      "aria-label",
      isDark ? "Switch to light theme" : "Switch to dark theme"
    );
    btn.textContent = isDark ? "Light" : "Dark";
  }

  function currentTheme() {
    return document.documentElement.getAttribute("data-theme") || "light";
  }

  function init() {
    applyTheme(resolveTheme(localStorage.getItem(STORAGE_KEY)));
    var btn = document.getElementById("theme-toggle");
    if (!btn) return;
    btn.addEventListener("click", function () {
      var next = currentTheme() === "dark" ? "light" : "dark";
      localStorage.setItem(STORAGE_KEY, next);
      applyTheme(next);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
