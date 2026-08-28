(function () {
  var STORAGE_KEY = "theme";

  function systemPrefersDark() {
    return window.matchMedia("(prefers-color-scheme: dark)").matches;
  }

  function resolveTheme(stored) {
    if (stored === "dark") return "dark";
    if (stored === "light") return "light";
    return systemPrefersDark() ? "dark" : "light";
  }

  function applyTheme(resolved) {
    var root = document.documentElement;
    var isDark = resolved === "dark";
    root.classList.toggle("dark", isDark);
    root.style.colorScheme = isDark ? "dark" : "light";
  }

  function init() {
    applyTheme(resolveTheme(localStorage.getItem(STORAGE_KEY)));

    var btn = document.getElementById("theme-toggle");
    if (!btn) return;

    btn.addEventListener("click", function () {
      var next =
        resolveTheme(localStorage.getItem(STORAGE_KEY)) === "dark"
          ? "light"
          : "dark";
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
