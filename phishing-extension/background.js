// Will handle background tasks like notifications
chrome.runtime.onInstalled.addListener(() => {
  console.log("Extension installed");
});
// Listens for page navigation completes
chrome.webNavigation.onCompleted.addListener((details) => {
  chrome.action.setIcon({
    path: details.url.includes("facebook")
      ? "icons/warning.png"
      : "icons/safe.png",
    tabId: details.tabId,
  });
});
