/**
 * Theme manager: system (default) | light | dark
 */
(function () {
  const STORAGE_KEY = "theme";

  function getStored() {
    const v = localStorage.getItem(STORAGE_KEY);
    if (v === "light" || v === "dark" || v === "system") return v;
    return "system";
  }

  function resolveDark(mode) {
    if (mode === "dark") return true;
    if (mode === "light") return false;
    return window.matchMedia("(prefers-color-scheme: dark)").matches;
  }

  function apply(mode) {
    const resolved = resolveDark(mode);
    document.documentElement.classList.toggle("dark", resolved);
    document.documentElement.dataset.theme = mode;
    window.dispatchEvent(
      new CustomEvent("theme-change", { detail: { mode, resolved } })
    );
  }

  window.themeManager = {
    getMode() {
      return getStored();
    },
    setMode(mode) {
      if (!["system", "light", "dark"].includes(mode)) return;
      localStorage.setItem(STORAGE_KEY, mode);
      apply(mode);
    },
    apply() {
      apply(getStored());
    },
    init() {
      apply(getStored());
      window
        .matchMedia("(prefers-color-scheme: dark)")
        .addEventListener("change", () => {
          if (getStored() === "system") apply("system");
        });
    },
  };

  window.themeManager.init();
})();
