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
  document.getElementById("domain").textContent = decodeURIComponent(domain);
  document.getElementById("confidence").textContent =
    confidence === "unknown"
      ? "unknown"
      : Math.round(parseFloat(confidence) * 100) + "%";

  // Button handlers
  document.getElementById("continue").addEventListener("click", () => {
    console.log("[DEBUG] Proceed button clicked - start");

    // Double-decode the URL in case it's encoded twice
    const decodedUrl = decodeURIComponent(decodeURIComponent(originalUrl));
    console.log("[DEBUG] Decoded URL:", decodedUrl);

    // Add validation
    if (!decodedUrl.startsWith("http")) {
      console.error("Invalid URL format:", decodedUrl);
      return;
    }

    chrome.runtime.sendMessage(
      {
        action: "proceed",
        url: decodedUrl,
      },
      (response) => {
        // Add more detailed error handling
        if (chrome.runtime.lastError) {
          console.error("Runtime error:", chrome.runtime.lastError.message);
        }

        if (!response?.success) {
          console.error("[FALLBACK] Using direct navigation");
          window.location.href = decodedUrl;
        } else {
          console.log("[DEBUG] Proceed successful via extension");
        }
      }
    );

    // Add immediate feedback
    document.getElementById("continue").textContent = "Processing...";
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
