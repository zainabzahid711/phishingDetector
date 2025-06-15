// Configuration
const TEST_MODE = false; // Set to false in production
const API_ENDPOINT = "http://localhost:5000/predict";
const CONFIDENCE_THRESHOLD = 0.7;
const WHITELIST = [
  /\.pdf(\?|$)/i, // All PDF files
  /google(\.com|adservices\.com)/i,
  /microsoft\.com/i,
  // Add other trusted domains here
];

// Mock response for testing
const getMockResponse = (url) => ({
  isPhishing: url.includes("fake") || url.includes("phishing"),
  confidence: 0.85,
  domain: new URL(url).hostname,
});

// Main detection logic
chrome.webNavigation.onBeforeNavigate.addListener(async (details) => {
  console.log("Navigation detected:", details.url);

  if (WHITELIST.some((pattern) => pattern.test(details.url))) {
    console.log("[DEBUG] Whitelisted URL skipped:", details.url);
    return;
  }

  if (!details.url.startsWith("http")) {
    console.log("Non-HTTP URL skipped");
    return;
  }

  try {
    let detectionResult;

    if (TEST_MODE) {
      detectionResult = getMockResponse(details.url);
    } else {
      const response = await fetch(API_ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: details.url }),
      });
      detectionResult = await response.json();
    }

    if (
      detectionResult.isPhishing &&
      detectionResult.confidence > CONFIDENCE_THRESHOLD
    ) {
      const blockedUrl = new URL(chrome.runtime.getURL("blocked.html"));
      blockedUrl.searchParams.set("originalUrl", details.url);
      blockedUrl.searchParams.set("confidence", detectionResult.confidence);
      blockedUrl.searchParams.set("domain", detectionResult.domain);

      chrome.tabs.update(details.tabId, { url: blockedUrl.href });
    }
  } catch (error) {
    console.error("detection failed:", error);
    // Optionally log to analytics or show subtle warning
  }
});
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log("[BACKGROUND] Message received:", request.action);

  if (request.action === "proceed") {
    console.log("[BACKGROUND] Processing proceed to:", request.url);

    if (!sender.tab || !sender.tab.id) {
      console.error("No tab ID available");
      sendResponse({ success: false });
      return true;
    }

    // Add URL validation
    try {
      // Fix URL decoding (only decode once)
      const urlToLoad = request.url.startsWith("http")
        ? request.url
        : decodeURIComponent(request.url);

      console.log("[BACKGROUND] Processed URL:", urlToLoad);

      chrome.tabs.update(sender.tab.id, { url: urlToLoad }, () => {
        if (chrome.runtime.lastError) {
          console.error("Tab update error:", chrome.runtime.lastError);
          // Emergency fallback
          chrome.tabs.executeScript(sender.tab.id, {
            code: `window.location.href = "${urlToLoad.replace(/"/g, '\\"')}";`,
          });
        }
        sendResponse({ success: true });
      });
    } catch (e) {
      console.error("[BACKGROUND] Critical error:", e);
      sendResponse({ success: false, error: e.message });
    }
    return true; // Keep message channel open
  } else if (request.action === "goBack") {
    chrome.tabs.goBack(sender.tab.id, () => {
      if (chrome.runtime.lastError) {
        chrome.tabs.update(sender.tab.id, { url: "https://www.google.com" });
      }
      sendResponse({ success: true });
    });
    return true; // Needed for async response
  }
});
