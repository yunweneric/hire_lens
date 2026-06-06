/**
 * Job description editor: write / preview toggle with server-side Markdown render.
 */
(function () {
  function getCsrfToken() {
    const input = document.querySelector("[name=csrfmiddlewaretoken]");
    if (input) return input.value;
    const match = document.cookie.match(/csrftoken=([^;]+)/);
    return match ? decodeURIComponent(match[1]) : "";
  }

  function initEditor(root) {
    const previewUrl = root.dataset.previewUrl;
    const textarea = root.querySelector("[data-job-editor='description']");
    const previewEl = root.querySelector("[data-job-editor-preview]");
    const writePane = root.querySelector("[data-job-editor-write]");
    const previewPane = root.querySelector("[data-job-editor-preview-pane]");
    const writeBtn = root.querySelector("[data-job-editor-mode='write']");
    const previewBtn = root.querySelector("[data-job-editor-mode='preview']");

    if (!textarea || !previewEl || !previewUrl) return;

    let mode = "write";
    let previewHtml = "";
    let loading = false;

    function setMode(next) {
      mode = next;
      const isWrite = mode === "write";
      writePane.classList.toggle("hidden", !isWrite);
      previewPane.classList.toggle("hidden", isWrite);
      writeBtn.classList.toggle("is-active", isWrite);
      writeBtn.setAttribute("aria-pressed", isWrite ? "true" : "false");
      previewBtn.classList.toggle("is-active", !isWrite);
      previewBtn.setAttribute("aria-pressed", !isWrite ? "true" : "false");
      textarea.toggleAttribute("required", isWrite);
    }

    async function loadPreview() {
      const markdown = textarea.value;
      if (!markdown.trim()) {
        previewHtml = "";
        previewEl.innerHTML =
          '<p class="text-sm text-muted-foreground">Nothing to preview yet. Switch to Write and add a description.</p>';
        return;
      }
      loading = true;
      previewEl.innerHTML =
        '<div class="job-editor-preview-loading">Rendering preview…</div>';
      try {
        const res = await fetch(previewUrl, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCsrfToken(),
          },
          body: JSON.stringify({ markdown }),
        });
        if (!res.ok) throw new Error("Preview failed");
        const data = await res.json();
        previewHtml = data.html || "";
        previewEl.innerHTML = previewHtml;
      } catch {
        previewEl.innerHTML =
          '<p class="text-sm text-destructive">Could not load preview. Try again.</p>';
      } finally {
        loading = false;
      }
    }

    writeBtn.addEventListener("click", () => setMode("write"));
    previewBtn.addEventListener("click", async () => {
      setMode("preview");
      await loadPreview();
    });

    root.closest("form")?.addEventListener("submit", () => {
      if (mode === "preview") setMode("write");
    });

    setMode("write");
  }

  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("[data-job-editor-root]").forEach(initEditor);
  });
})();
