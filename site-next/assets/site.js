(function () {
  var root = document.documentElement;
  var key = "theme";
  var toggle = document.getElementById("theme-toggle");
  var menu = document.getElementById("menu-btn");
  var sidebar = document.getElementById("sidebar");
  var scrim = document.getElementById("scrim");

  function apply(dark) {
    root.classList.toggle("dark", dark);
    root.style.colorScheme = dark ? "dark" : "light";
    if (toggle) toggle.setAttribute("aria-pressed", dark ? "true" : "false");
  }

  if (toggle) {
    toggle.addEventListener("click", function () {
      var dark = !root.classList.contains("dark");
      localStorage.setItem(key, dark ? "dark" : "light");
      apply(dark);
    });
  }

  function setMenu(open) {
    if (!sidebar) return;
    sidebar.classList.toggle("is-open", open);
    if (scrim) scrim.classList.toggle("is-open", open);
    if (menu) menu.setAttribute("aria-expanded", open ? "true" : "false");
  }

  if (menu) menu.addEventListener("click", function () { setMenu(!sidebar.classList.contains("is-open")); });
  if (scrim) scrim.addEventListener("click", function () { setMenu(false); });
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") setMenu(false);
  });

  document.querySelectorAll(".copy, [data-copy]").forEach(function (button) {
    button.addEventListener("click", function () {
      var specBlock = button.closest(".spec");
      var pre = specBlock ? specBlock.querySelector("pre") : null;
      var text = pre ? pre.textContent : (button.getAttribute("data-copy") || "");
      navigator.clipboard.writeText(text).then(function () {
        var previous = button.textContent;
        button.textContent = "Copied";
        window.setTimeout(function () { button.textContent = previous; }, 1600);
      });
    });
  });

  var finder = document.getElementById("token-finder");
  if (finder) {
    var rows = Array.prototype.slice.call(document.querySelectorAll("[data-token]"));
    var sections = Array.prototype.slice.call(document.querySelectorAll(".token-section, .token-group"));
    var empty = document.getElementById("finder-empty");
    function applyFinder() {
      var query = finder.value.trim().toLowerCase();
      rows.forEach(function (row) {
        var hay = (row.getAttribute("data-token") || "").toLowerCase();
        row.classList.toggle("is-hidden", query.length > 0 && hay.indexOf(query) === -1);
      });
      sections.forEach(function (section) {
        var visible = section.querySelector("[data-token]:not(.is-hidden)");
        section.classList.toggle("is-hidden", !visible);
      });
      if (empty) empty.classList.toggle("is-hidden", !query || rows.some(function (row) { return !row.classList.contains("is-hidden"); }));
    }
    finder.addEventListener("input", applyFinder);
  }

  var links = Array.prototype.slice.call(document.querySelectorAll(".toc a"));
  if (!links.length || !("IntersectionObserver" in window)) return;
  var byId = {};
  links.forEach(function (link) {
    var id = (link.getAttribute("href") || "").slice(1);
    if (id) byId[id] = link;
  });
  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      var link = byId[entry.target.id];
      if (!link) return;
      if (entry.isIntersecting) {
        links.forEach(function (item) { item.classList.remove("is-active"); });
        link.classList.add("is-active");
      }
    });
  }, { rootMargin: "-20% 0px -70% 0px", threshold: 0 });
  Object.keys(byId).forEach(function (id) {
    var node = document.getElementById(id);
    if (node) observer.observe(node);
  });
})();
