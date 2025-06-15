document.addEventListener("DOMContentLoaded", () => {
  const resultDiv = document.getElementById("result");
  const reportBtn = document.getElementById("report-btn");

  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const url = tabs[0]?.url;
    if (!url) {
      resultDiv.innerHTML = '<p class="error">No active tab found</p>';
      return;
    }

    fetch("http://localhost:5000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: url }),
    })
      .then((response) => {
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return response.json();
      })
      .then((data) => {
        const confidenceLevel = document.querySelector(".confidence-level");
        confidenceLevel.style.width = `${Math.round(data.confidence * 100)}%`;
        confidenceLevel.style.background = data.isPhishing
          ? "#ea4335"
          : "#34a853";

        resultDiv.innerHTML = `
          <h2>${data.isPhishing ? "⚠️ PHISHING" : "✅ SAFE"}</h2>
          <p>${Math.round(data.confidence * 100)}% confidence</p>
          <small>${new URL(url).hostname}</small>
        `;
      })
      .catch((error) => {
        resultDiv.innerHTML = `
          <p class="error">⚠️ Analysis Failed</p>
          <small>${error.message}</small>
        `;
      });
  });

  reportBtn.addEventListener("click", () => {
    chrome.tabs.create({ url: "https://example.com/report" });
  });
});
