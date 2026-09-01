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

  function siblingHref(nav, folder) {
    var feed = nav.querySelector('[data-nav="feed"]');
    if (feed && feed.getAttribute("href")) {
      return feed.getAttribute("href").replace(/feed\/?$/, folder + "/");
    }
    var personas = nav.querySelector('[data-nav="personas"]');
    if (personas && personas.getAttribute("href")) {
      return personas.getAttribute("href").replace(/personas\/?$/, folder + "/");
    }
    var listing = nav.querySelector('[data-nav="listing"]');
    if (listing && listing.getAttribute("href")) {
      return listing.getAttribute("href").replace(/research\/?$/, folder + "/");
    }
    var pipeline = nav.querySelector('[data-nav="pipeline"]');
    if (pipeline && pipeline.getAttribute("href")) {
      var base = pipeline.getAttribute("href");
      if (base.slice(-1) !== "/") base += "/";
      return base + folder + "/";
    }
    return "../" + folder + "/";
  }

  function ensureRequestsNav() {
    var nav = document.querySelector(".report-nav");
    if (!nav || nav.querySelector('[data-nav="requests"]')) return;

    var link = document.createElement("a");
    link.className = "nav-link";
    link.setAttribute("data-nav", "requests");
    link.href = siblingHref(nav, "requests");
    link.textContent = "Requests";
    var path = (location.pathname || "").replace(/\/+$/, "");
    if (path.slice(-9) === "/requests") link.classList.add("is-active");

    var feed = nav.querySelector('[data-nav="feed"]');
    var affinity = nav.querySelector('[data-nav="affinity"]');
    if (feed && feed.nextSibling) {
      nav.insertBefore(link, feed.nextSibling);
    } else if (affinity) {
      nav.insertBefore(link, affinity);
    } else {
      nav.appendChild(link);
    }
  }

  function init() {
    applyTheme(resolveTheme(localStorage.getItem(STORAGE_KEY)));
    ensureFeedNav();
    ensureRequestsNav();

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
