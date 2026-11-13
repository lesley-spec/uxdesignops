(function () {
  var PAGE = 24;
  var SOURCES = { dovetail: "Dovetail", outset: "Outset", posthog: "PostHog", pendo: "Pendo" };
  var SIGNALS = {
    user_feedback: "User feedback",
    bug: "Bug report",
    friction: "Friction",
    quant: "Quant drop-off",
    research: "Research",
    support: "Support"
  };
  var data = [];
  var shown = PAGE;
  var form = document.getElementById("research-filters");
  var q = document.getElementById("q");
  if (!form || !q) return;
  var source = document.getElementById("source");
  var audience = document.getElementById("audience");
  var area = document.getElementById("area");
  var signal = document.getElementById("signal");
  var list = document.getElementById("nuggets");
  var count = document.getElementById("result-count");
  var empty = document.getElementById("empty");
  var more = document.getElementById("more");

  function matches(item) {
    if (source.value && item.source !== source.value) return false;
    if (audience.value && item.audience !== audience.value) return false;
    if (area.value && item.product_area !== area.value) return false;
    if (signal.value && item.signal !== signal.value) return false;
    var query = q.value.trim().toLowerCase();
    if (!query) return true;
    var blob = [item.text, item.theme, item.product_area, item.audience, SOURCES[item.source] || item.source]
      .join(" ")
      .toLowerCase();
    return blob.indexOf(query) !== -1;
  }

  function esc(value) {
    return String(value || "").replace(/[&<>"']/g, function (ch) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[ch];
    });
  }

  function render() {
    var hits = data.filter(matches);
    var slice = hits.slice(0, shown);
    list.innerHTML = slice.map(function (item) {
      var who = item.audience || "Audience not tagged";
      var sourceName = SOURCES[item.source] || item.source;
      var link = item.url
        ? '<a href="' + esc(item.url) + '" target="_blank" rel="noopener">Open in ' + esc(sourceName) + "</a>"
        : "";
      var bits = [
        esc(sourceName),
        esc(who),
        item.product_area ? esc(item.product_area) : "",
        item.theme ? esc(item.theme) : "",
        item.signal ? esc(SIGNALS[item.signal] || item.signal) : "",
        item.date ? esc(item.date) : ""
      ].filter(Boolean);
      return (
        '<article class="nugget"><p>' + esc(item.text) +
        '</p><p class="nugget-meta">' + bits.join(" · ") +
        (link ? " · " + link : "") + "</p></article>"
      );
    }).join("");
    count.textContent = hits.length ? "Showing " + slice.length + " of " + hits.length : "";
    empty.hidden = hits.length !== 0;
    empty.textContent = "No findings match that search.";
    more.hidden = slice.length >= hits.length;
  }

  function reset() {
    shown = PAGE;
    render();
  }

  form.addEventListener("submit", function (event) { event.preventDefault(); });
  [q, source, audience, area, signal].forEach(function (el) {
    el.addEventListener("input", reset);
    el.addEventListener("change", reset);
  });
  more.addEventListener("click", function () {
    shown += PAGE;
    render();
  });

  fetch("findings.json")
    .then(function (response) {
      if (!response.ok) throw new Error(String(response.status));
      return response.json();
    })
    .then(function (payload) {
      data = payload.findings || [];
      var areas = {};
      data.forEach(function (item) {
        if (item.product_area) areas[item.product_area] = true;
      });
      Object.keys(areas).sort().forEach(function (name) {
        var option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        area.appendChild(option);
      });
      render();
    })
    .catch(function () {
      count.textContent = "";
      empty.hidden = false;
      empty.textContent = "Could not load findings.";
    });
})();
