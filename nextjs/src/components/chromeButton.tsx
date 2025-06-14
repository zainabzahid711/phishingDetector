"use client";

export default function ChromeButton() {
  const EXTENSION_ID = "hbklihhbjochkplkbobpllcjiandcmdh";
  const STORE_URL = `https://chrome.google.com/webstore/detail/${EXTENSION_ID}`;

  return (
    <a
      href={STORE_URL}
      target="_blank"
      rel="noopener noreferrer"
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: "12px",
        backgroundColor: "#4285F4",
        color: "white",
        padding: "12px 24px",
        borderRadius: "8px",
        border: "none",
        fontSize: "16px",
        fontWeight: "500",
        cursor: "pointer",
        textDecoration: "none",
        transition: "background-color 0.3s",
      }}
      onMouseOver={(e) => (e.currentTarget.style.backgroundColor = "#3367D6")}
      onMouseOut={(e) => (e.currentTarget.style.backgroundColor = "#4285F4")}
    >
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
        <path
          d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"
          fill="#fff"
        />
        <path
          d="M12 6c-3.31 0-6 2.69-6 6s2.69 6 6 6 6-2.69 6-6-2.69-6-6-6zm0 10c-2.21 0-4-1.79-4-4s1.79-4 4-4 4 1.79 4 4-1.79 4-4 4z"
          fill="#fff"
        />
      </svg>
      Add to Chrome
    </a>
  );
}
