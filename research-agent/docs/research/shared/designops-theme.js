(function () {
  var STORAGE_KEY = "theme";
  var SUBNAV_ITEMS = [
    {
      key: "frame",
      label: "The Frame",
      external: "https://claude.ai/artifact/FHc7oAPoyohgxo87VdxCGw",
    },
    {
      key: "personas-v2",
      label: "Personas V2",
      external: "https://claude.ai/artifact/FaBjbFu7hiM5LYBfALemAQ",
    },
    { key: "listing", label: "Insight Monitor", path: "research/" },
    { key: "personas", label: "Personas (V1)", path: "personas/" },
    { key: "affinity", label: "Affinity", path: "reports/2026-08-24-affinity.html" },
    { key: "feed", label: "Competitor News", path: "feed/" },
  ];

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

  function currentPath() {
    return (location.pathname || "").replace(/\/+$/, "");
  }

  function researchSection() {
    var path = currentPath();
    if (/\/personas(\/|$)/.test(path) || path.slice(-8) === "personas") return "personas";
    if (/\/frame(\/|$)/.test(path) || path.slice(-5) === "frame") return "frame";
    if (/\/feed(\/|$)/.test(path) || path.slice(-4) === "feed") return "feed";
    if (/affinity\.html$/.test(path)) return "affinity";
    if (/\/research(\/|$)/.test(path) && path.indexOf("/skills/") === -1) return "listing";
    if (/\/reports\//.test(path)) return "listing";
    return null;
  }

  function siteRootFromListing(nav) {
    var listing = nav && nav.querySelector('[data-nav="listing"]');
    var href = listing && listing.getAttribute("href");
    if (!href) {
      var dropdown = nav && nav.querySelector(".nav-dropdown[data-nav='listing']");
      href = dropdown && dropdown.getAttribute("data-listing-href");
    }
    if (!href) return "../";
    if (href === "./" || href === "./index.html") return "../";
    return href.replace(/research\/?$/, "");
  }

  function siblingHref(nav, folder) {
    var root = siteRootFromListing(nav);
    return root + folder + "/";
  }

  function ensureRequestsNav() {
    var nav = document.querySelector(".report-nav");
    if (!nav || nav.querySelector('[data-nav="requests"]')) return;

    var link = document.createElement("a");
    link.className = "nav-link";
    link.setAttribute("data-nav", "requests");
    link.href = siblingHref(nav, "requests");
    link.textContent = "Requests";
    var path = currentPath();
    if (path.slice(-9) === "/requests") link.classList.add("is-active");

    var listing = nav.querySelector('[data-nav="listing"], .nav-dropdown[data-nav="listing"]');
    var report = nav.querySelector('[data-nav="report"]');
    if (report) {
      if (report.nextSibling) nav.insertBefore(link, report.nextSibling);
      else nav.appendChild(link);
    } else if (listing) {
      if (listing.nextSibling) nav.insertBefore(link, listing.nextSibling);
      else nav.appendChild(link);
    } else {
      nav.appendChild(link);
    }
  }

  function placeExamplesAfterPipeline(nav) {
    if (!nav) return;
    var pipeline = nav.querySelector('[data-nav="pipeline"]');
    var examples = nav.querySelector('[data-nav="walkthrough"]');
    if (!pipeline || !examples) return;
    if (pipeline.nextElementSibling === examples) return;
    if (pipeline.nextSibling) {
      nav.insertBefore(examples, pipeline.nextSibling);
    } else {
      nav.appendChild(examples);
    }
  }

  function normalizeTopNav() {
    var nav = document.querySelector(".report-nav");
    if (!nav) return null;
    placeExamplesAfterPipeline(nav);

    ["personas", "feed", "affinity"].forEach(function (key) {
      nav.querySelectorAll('a[data-nav="' + key + '"]').forEach(function (el) {
        el.parentNode.removeChild(el);
      });
    });

    return nav;
  }

  function removeSecondaryBar() {
    var existing = document.getElementById("research-subnav");
    if (existing) existing.parentNode.removeChild(existing);
  }

  function hrefFor(nav, item) {
    if (item.external) return item.external;
    var listing = nav.querySelector("a[data-nav='listing']");
    var listingHref =
      (listing && listing.getAttribute("href")) ||
      (nav.querySelector(".nav-dropdown[data-nav='listing']") &&
        nav.querySelector(".nav-dropdown[data-nav='listing']").getAttribute("data-listing-href"));
    var root = siteRootFromListing(nav);
    if (item.key === "listing") return listingHref || root + item.path;
    return root + item.path;
  }

  function fillResearchPanel(panel, nav) {
    panel.innerHTML = "";
    SUBNAV_ITEMS.forEach(function (item) {
      var link = document.createElement("a");
      link.className = "nav-dropdown-item";
      link.setAttribute("data-subnav", item.key);
      link.setAttribute("role", "menuitem");
      link.href = hrefFor(nav, item);
      link.textContent = item.label;
      if (item.external) {
        link.target = "_blank";
        link.rel = "noopener noreferrer";
        link.setAttribute("data-external", "true");
      }
      panel.appendChild(link);
    });
  }

  function setDropdownOpen(dropdown, open) {
    var toggle = dropdown.querySelector(".nav-dropdown-toggle");
    var panel = dropdown.querySelector(".nav-dropdown-panel");
    if (!toggle || !panel) return;
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    panel.hidden = !open;
  }

  function ensureResearchDropdown(nav) {
    if (!nav) return;

    var section = researchSection();
    var existing = nav.querySelector(".nav-dropdown[data-nav='listing']");
    var listingLink = nav.querySelector("a[data-nav='listing']");

    if (!existing && !listingLink) return;

    var listingHref = existing
      ? existing.getAttribute("data-listing-href")
      : listingLink.getAttribute("href");

    if (!existing) {
      existing = document.createElement("div");
      existing.className = "nav-dropdown";
      existing.setAttribute("data-nav", "listing");
      existing.setAttribute("data-listing-href", listingHref);

      var toggle = document.createElement("button");
      toggle.type = "button";
      toggle.className = "nav-link nav-dropdown-toggle";
      toggle.setAttribute("aria-expanded", "false");
      toggle.setAttribute("aria-haspopup", "true");
      toggle.setAttribute("aria-controls", "research-dropdown");
      toggle.id = "research-dropdown-toggle";
      toggle.textContent = "Research";

      var panel = document.createElement("div");
      panel.className = "nav-dropdown-panel";
      panel.id = "research-dropdown";
      panel.hidden = true;
      panel.setAttribute("role", "menu");
      panel.setAttribute("aria-labelledby", "research-dropdown-toggle");

      fillResearchPanel(panel, nav);

      existing.appendChild(toggle);
      existing.appendChild(panel);
      listingLink.parentNode.replaceChild(existing, listingLink);

      toggle.addEventListener("click", function (event) {
        event.stopPropagation();
        setDropdownOpen(existing, panel.hidden);
      });

      document.addEventListener("click", function (event) {
        if (!existing.contains(event.target)) setDropdownOpen(existing, false);
      });

      document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") setDropdownOpen(existing, false);
      });
    } else {
      var panel = existing.querySelector(".nav-dropdown-panel");
      if (panel) fillResearchPanel(panel, nav);
    }

    var toggle = existing.querySelector(".nav-dropdown-toggle");
    if (toggle) toggle.classList.toggle("is-active", !!section);
    existing.querySelectorAll("[data-subnav]").forEach(function (link) {
      link.classList.toggle("is-active", link.getAttribute("data-subnav") === section);
    });
  }

  function syncStickyOffset() {
    var header = document.querySelector(".top-nav");
    if (!header) return;
    document.documentElement.style.setProperty(
      "--top-nav-height",
      header.offsetHeight + "px"
    );
  }

  function ensureDropdownStyles() {
    if (document.getElementById("designops-nav-dropdown-css")) return;
    var style = document.createElement("style");
    style.id = "designops-nav-dropdown-css";
    style.textContent =
      ".report-nav .nav-dropdown{position:relative;display:inline-flex;}" +
      ".report-nav .nav-dropdown-panel{position:absolute;z-index:1300;top:calc(100% + 6px);left:0;min-width:15rem;margin:0;padding:6px;border-radius:8px;border:1px solid var(--border-default);background:var(--card);box-shadow:var(--fab-shadow);display:flex;flex-direction:column;gap:2px;}" +
      ".report-nav .nav-dropdown-panel[hidden]{display:none!important;}" +
      ".report-nav .nav-dropdown-item{display:block;width:100%;box-sizing:border-box;padding:8px 12px;border-radius:6px;text-decoration:none!important;white-space:nowrap;font-size:.88rem;font-weight:600;color:var(--text-default);background:transparent;}" +
      ".report-nav .nav-dropdown-item:hover{background:var(--background-hover);color:var(--text-default);}" +
      ".report-nav .nav-dropdown-item.is-active{color:var(--interactive-default);background:var(--info-bg);}" +
      ".report-nav .nav-dropdown-item[data-external='true']::after{content:' \\2197';font-size:.85em;opacity:.75;}";
    document.head.appendChild(style);
  }

  function init() {
    applyTheme(resolveTheme(localStorage.getItem(STORAGE_KEY)));
    ensureDropdownStyles();
    var nav = normalizeTopNav();
    ensureRequestsNav();
    removeSecondaryBar();
    ensureResearchDropdown(nav);
    syncStickyOffset();
    window.addEventListener("resize", syncStickyOffset);

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
