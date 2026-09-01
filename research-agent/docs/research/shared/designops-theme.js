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

  function ensureFeedNav() {
    var nav = document.querySelector(".report-nav");
    if (!nav || nav.querySelector('[data-nav="feed"]')) return;

    var personas = nav.querySelector('[data-nav="personas"]');
    var listing = nav.querySelector('[data-nav="listing"]');
    var href = "../feed/";
    if (personas && personas.getAttribute("href")) {
      href = personas.getAttribute("href").replace(/personas\/?$/, "feed/");
    } else if (listing && listing.getAttribute("href")) {
      href = listing.getAttribute("href").replace(/research\/?$/, "feed/");
    }

    var link = document.createElement("a");
    link.className = "nav-link";
    link.setAttribute("data-nav", "feed");
    link.href = href;
    link.textContent = "Competitors";
    var path = (location.pathname || "").replace(/\/+$/, "");
    if (path.slice(-5) === "/feed") link.classList.add("is-active");

    var affinity = nav.querySelector('[data-nav="affinity"]');
    if (personas && personas.nextSibling) {
      personas.parentNode.insertBefore(link, personas.nextSibling);
    } else if (affinity) {
      nav.insertBefore(link, affinity);
    } else {
      nav.appendChild(link);
    }
  }

  function init() {
    applyTheme(resolveTheme(localStorage.getItem(STORAGE_KEY)));
    ensureFeedNav();

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
