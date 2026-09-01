(function () {
  "use strict";

  var STORAGE_KEY = "designops_auth_session";

  function config() {
    return window.DESIGNOPS_AUTH || {};
  }

  function allowedDomain() {
    return (config().allowedEmailDomain || "impact.com").toLowerCase();
  }

  function parseJwt(token) {
    try {
      var payload = token.split(".")[1];
      var json = atob(payload.replace(/-/g, "+").replace(/_/g, "/"));
      return JSON.parse(json);
    } catch (err) {
      return null;
    }
  }

  function emailAllowed(email, hostedDomain) {
    if (!email) return false;
    var domain = allowedDomain();
    var normalized = String(email).toLowerCase();
    if (hostedDomain && String(hostedDomain).toLowerCase() === domain) return true;
    return normalized.endsWith("@" + domain);
  }

  function readSession() {
    try {
      var raw = sessionStorage.getItem(STORAGE_KEY);
      if (!raw) return null;
      var session = JSON.parse(raw);
      if (!session || !session.email || !session.expiresAt) return null;
      if (Date.now() > session.expiresAt) {
        sessionStorage.removeItem(STORAGE_KEY);
        return null;
      }
      if (!emailAllowed(session.email, session.hd)) return null;
      return session;
    } catch (err) {
      return null;
    }
  }

  function writeSession(profile) {
    var hours = Number(config().sessionHours || 24);
    var session = {
      email: profile.email,
      hd: profile.hd || "",
      name: profile.name || "",
      givenName: profile.given_name || profile.givenName || "",
      familyName: profile.family_name || profile.familyName || "",
      picture: profile.picture || "",
      expiresAt: Date.now() + hours * 60 * 60 * 1000,
    };
    sessionStorage.setItem(STORAGE_KEY, JSON.stringify(session));
    return session;
  }

  function googlePictureUrl(session) {
    var url = String((session && session.picture) || "").trim();
    return url || null;
  }

  function initials(session) {
    var given = String((session && session.givenName) || "").trim();
    var family = String((session && session.familyName) || "").trim();
    if (given && family) {
      return (given[0] + family[0]).toUpperCase();
    }

    var parts = String((session && session.name) || "")
      .trim()
      .split(/\s+/)
      .filter(Boolean);
    if (parts.length >= 2) {
      return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
    }
    if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();

    var email = String((session && session.email) || "").trim();
    if (email) {
      var local = email.split("@")[0] || "";
      if (local.length >= 2) return local.slice(0, 2).toUpperCase();
      if (local.length === 1) return local.toUpperCase();
    }
    return "?";
  }

  function createInitialsAvatar(session) {
    var span = document.createElement("span");
    span.className = "designops-nav-avatar designops-nav-avatar-fallback";
    span.setAttribute("aria-hidden", "true");
    span.textContent = initials(session);
    return span;
  }

  function createNavAvatar(session) {
    var pictureUrl = googlePictureUrl(session);
    if (!pictureUrl) return createInitialsAvatar(session);

    var img = document.createElement("img");
    img.className = "designops-nav-avatar";
    img.src = pictureUrl;
    img.alt = "";
    img.referrerPolicy = "no-referrer";
    img.width = 32;
    img.height = 32;
    img.addEventListener("error", function onAvatarError() {
      img.removeEventListener("error", onAvatarError);
      img.replaceWith(createInitialsAvatar(session));
    });
    return img;
  }

  function ensureNavUserSlot() {
    var actions = document.querySelector(".top-nav-actions");
    if (!actions || document.getElementById("designops-nav-user")) return;
    var slot = document.createElement("div");
    slot.id = "designops-nav-user";
    slot.className = "designops-nav-user";
    slot.hidden = true;
    var toggle = document.getElementById("theme-toggle");
    if (toggle) actions.insertBefore(slot, toggle);
    else actions.appendChild(slot);
  }

  function renderNavUser(session) {
    if (!session) return;
    ensureNavUserSlot();
    var slot = document.getElementById("designops-nav-user");
    if (!slot) return;

    var label = session.name || session.email;
    slot.innerHTML = "";
    var inner = document.createElement("span");
    inner.className = "designops-nav-user-inner";
    inner.title = session.email || "";
    inner.appendChild(createNavAvatar(session));
    var nameEl = document.createElement("span");
    nameEl.className = "designops-nav-user-label";
    nameEl.textContent = label;
    inner.appendChild(nameEl);
    slot.appendChild(inner);
    slot.hidden = false;
  }

  function workflowAdminEmails() {
    var list = config().workflowAdminEmails;
    if (!Array.isArray(list) || !list.length) return ["lesley@impact.com"];
    return list.map(function (email) {
      return String(email || "").trim().toLowerCase();
    }).filter(Boolean);
  }

  function canRunWorkflow(session) {
    if (!session || !session.email) return false;
    var email = String(session.email).trim().toLowerCase();
    return workflowAdminEmails().indexOf(email) !== -1;
  }

  function updateWorkflowControls(session) {
    var visible = canRunWorkflow(session);
    document.querySelectorAll(".run-workflow-admin-only").forEach(function (el) {
      el.hidden = !visible;
    });
    document.dispatchEvent(new CustomEvent("designops-auth-change", { detail: { session: session || null } }));
  }

  window.DesignOpsAuth = {
    getSession: readSession,
    isAdmin: function () {
      return canRunWorkflow(readSession());
    },
  };

  function clearNavUser() {
    var slot = document.getElementById("designops-nav-user");
    if (!slot) return;
    slot.hidden = true;
    slot.innerHTML = "";
    updateWorkflowControls(null);
  }

  function els() {
    return {
      gate: document.getElementById("designops-auth-gate"),
      denied: document.getElementById("designops-auth-denied"),
      signIn: document.getElementById("designops-google-signin"),
      status: document.getElementById("designops-auth-status"),
    };
  }

  function setLocked(locked) {
    document.documentElement.classList.toggle("designops-auth-locked", locked);
  }

  function showGate() {
    var ui = els();
    setLocked(true);
    if (ui.gate) ui.gate.hidden = false;
    if (ui.denied) ui.denied.hidden = true;
  }

  function showDenied(email) {
    var ui = els();
    setLocked(true);
    clearNavUser();
    if (ui.gate) ui.gate.hidden = true;
    if (ui.denied) ui.denied.hidden = false;
    var deniedStatus = document.getElementById("designops-auth-status-denied");
    if (deniedStatus && email) {
      deniedStatus.textContent = "Signed in as " + email + ".";
    }
  }

  function unlock() {
    var ui = els();
    setLocked(false);
    if (ui.gate) ui.gate.hidden = true;
    if (ui.denied) ui.denied.hidden = true;
    var session = readSession();
    renderNavUser(session);
    updateWorkflowControls(session);
  }

  function showConfigError() {
    var ui = els();
    setLocked(true);
    if (ui.gate) ui.gate.hidden = false;
    if (ui.denied) ui.denied.hidden = true;
    if (ui.status) {
      ui.status.textContent =
        "Google sign-in is not configured yet. Add GOOGLE_OAUTH_CLIENT_ID to GitHub Actions secrets.";
    }
    if (ui.signIn) ui.signIn.innerHTML = "";
  }

  function handleCredentialResponse(response) {
    var credential = response && response.credential;
    if (!credential) {
      showGate();
      return;
    }
    var profile = parseJwt(credential);
    if (!profile || !profile.email) {
      showGate();
      return;
    }
    if (!emailAllowed(profile.email, profile.hd)) {
      showDenied(profile.email);
      sessionStorage.removeItem(STORAGE_KEY);
      return;
    }
    writeSession({
      email: profile.email,
      hd: profile.hd,
      name: profile.name,
      given_name: profile.given_name,
      family_name: profile.family_name,
      picture: profile.picture,
    });
    unlock();
  }

  function initGoogleSignIn(clientId) {
    var ui = els();
    if (!window.google || !window.google.accounts || !window.google.accounts.id) {
      if (ui.status) ui.status.textContent = "Loading Google sign-in…";
      window.setTimeout(function () {
        initGoogleSignIn(clientId);
      }, 120);
      return;
    }

    window.google.accounts.id.initialize({
      client_id: clientId,
      callback: handleCredentialResponse,
      hosted_domain: allowedDomain(),
      auto_select: false,
      cancel_on_tap_outside: true,
    });

    if (ui.signIn) {
      ui.signIn.innerHTML = "";
      window.google.accounts.id.renderButton(ui.signIn, {
        type: "standard",
        theme: "outline",
        size: "large",
        text: "signin_with",
        shape: "rectangular",
        logo_alignment: "left",
        width: 280,
      });
    }
    if (ui.status) ui.status.textContent = "";
  }

  function isLocalPreview() {
    var host = String(window.location.hostname || "");
    return host === "localhost" || host === "127.0.0.1" || host === "";
  }

  function boot() {
    var clientId = (config().googleClientId || "").trim();
    var session = readSession();

    if (isLocalPreview() || session) {
      unlock();
      return;
    }

    clearNavUser();
    showGate();

    if (!clientId) {
      showConfigError();
      return;
    }

    initGoogleSignIn(clientId);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
