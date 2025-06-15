// blocked.js
document.addEventListener("DOMContentLoaded", () => {
  // Check Chrome API availability
  if (!chrome?.runtime?.sendMessage) {
    document.body.innerHTML = `
      <div style="color: white; text-align: center; padding: 20px;">
        <h1>Extension Error</h1>
        <p>Please reload this page after installing PhishGuard</p>
        <button onclick="window.location.href='https://www.google.com'">Go to Safety</button>
      </div>
    `;
    return;
  }

  // Extract URL parameters
  const params = new URLSearchParams(window.location.search);
  const originalUrl = params.get("originalUrl") || "unknown";
  const confidence = params.get("confidence") || 0;
  const domain = params.get("domain") || "unknown";

  // Update UI
  document.getElementById("domain").textContent =
    new URL(decodeURIComponent(originalUrl)).hostname || "unknown";
  document.getElementById("confidence").textContent =
    confidence === "unknown"
      ? "unknown"
      : Math.round(parseFloat(confidence) * 100) + "%";

  // Button handlers
  document.getElementById("continue").addEventListener("click", () => {
    const url = decodeURIComponent(originalUrl);
    console.log("[BLOCKED] Attempting to proceed to:", url);

    chrome.runtime.sendMessage(
      {
        action: "proceed",
        url: url,
      },
      (response) => {
        if (!response?.success) {
          console.warn("[BLOCKED] Falling back to direct navigation");
          window.location.href = url;
        }
      }
    );
  });

  document.getElementById("back").addEventListener("click", () => {
    chrome.runtime.sendMessage({ action: "goBack" }, (response) => {
      if (!response?.success) {
        console.error("Error:", chrome.runtime.lastError);
        // Multi-level fallbacks
        if (window.history.length > 0) {
          window.history.back();
        } else {
          window.location.href = "https://www.google.com";
        }
      }
    });

    // Additional fallback in case the message doesn't get through
    setTimeout(() => {
      if (window.location.href.includes("blocked.html")) {
        if (window.history.length > 1) {
          window.history.back();
        } else {
          window.location.href = "https://www.google.com";
        }
      }
    }, 500);
  });
});
