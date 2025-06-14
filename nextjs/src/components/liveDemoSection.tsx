"use client";
import { useState } from "react";
import {
  Box,
  TextField,
  Button,
  Typography,
  Chip,
  CircularProgress,
  Alert,
} from "@mui/material";
import { Security, Warning } from "@mui/icons-material";

export default function LiveDemoSection() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState<null | {
    safe: boolean;
    riskScore: number;
    message?: string;
  }>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const checkUrl = async () => {
    if (!url) return;

    setLoading(true);
    setError("");

    try {
      // Normalize and validate URL
      let processedUrl = url.trim();

      // Add https:// if missing
      if (!/^https?:\/\//i.test(processedUrl)) {
        processedUrl = `https://${processedUrl}`;
      }

      // Validate URL format
      try {
        new URL(processedUrl); // Will throw if invalid
      } catch (e) {
        throw new Error(
          "Please enter a valid URL (e.g. facebook.com or https://facebook.com)"
        );
      }

      const response = await fetch("/api/detect", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url: processedUrl }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          errorData.message || `Request failed with status ${response.status}`
        );
      }

      const data = await response.json();
      setResult({
        safe: !data.isPhishing,
        riskScore: data.confidence ? Math.round(data.confidence * 100) : 0,
        message:
          data.message ||
          (data.isPhishing
            ? "Potential phishing detected"
            : "Legitimate website"),
      });
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to check URL. Please try again."
      );
      console.error("URL check error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ py: 8, bgcolor: "background.paper", borderRadius: 3 }}>
      <Typography
        variant="h3"
        textAlign="center"
        gutterBottom
        sx={{ fontWeight: 700 }}
      >
        Test Any Suspicious Link
      </Typography>

      <Box sx={{ maxWidth: 600, mx: "auto", p: 3 }}>
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <TextField
          fullWidth
          variant="outlined"
          placeholder="Enter URL (e.g. facebook.com or https://mybank-login.com)"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          sx={{ mb: 2 }}
          onKeyDown={(e) => e.key === "Enter" && checkUrl()}
          helperText="You can enter with or without https://"
        />

        <Button
          fullWidth
          size="large"
          variant="contained"
          onClick={checkUrl}
          disabled={!url || loading}
          startIcon={<Security />}
        >
          {loading ? <CircularProgress size={24} /> : "Scan Now"}
        </Button>

        {result && (
          <Box
            sx={{
              mt: 4,
              p: 3,
              border: "1px solid",
              borderColor: result.safe ? "success.main" : "error.main",
              borderRadius: 2,
            }}
          >
            <Typography
              variant="h5"
              sx={{ display: "flex", alignItems: "center", mb: 1 }}
            >
              {result.safe ? (
                <>
                  <Chip label="SAFE" color="success" sx={{ mr: 2 }} />
                  <span>This looks legitimate</span>
                </>
              ) : (
                <>
                  <Chip label="DANGEROUS" color="error" sx={{ mr: 2 }} />
                  <span>Potential phishing detected!</span>
                </>
              )}
            </Typography>
            <Typography>Risk score: {result.riskScore}/100</Typography>
            {!result.safe && (
              <Typography sx={{ mt: 1, display: "flex", alignItems: "center" }}>
                <Warning color="error" sx={{ mr: 1 }} />
                {result.message}
              </Typography>
            )}
          </Box>
        )}
      </Box>
    </Box>
  );
}
