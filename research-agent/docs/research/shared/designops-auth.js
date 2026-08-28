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
      expiresAt: Date.now() + hours * 60 * 60 * 1000,
    };
    sessionStorage.setItem(STORAGE_KEY, JSON.stringify(session));
    return session;
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

  function boot() {
    var clientId = (config().googleClientId || "").trim();
    var session = readSession();

    if (session) {
      unlock();
      return;
    }

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
