// app/page.tsx
"use client";
import { Container, Grid, Typography, Box } from "@mui/material";
import LiveDemoSection from "../components/liveDemoSection";
import TrustBadges from "../components/trustedBadges";
import CompanyLogos from "../components/companyLogos";
import FeatureGrid from "../components/featureGrid";
import ChromeButton from "../components/chromeButton";

export default function Home() {
  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* Hero Section */}
      <Grid container spacing={6} alignItems="center">
        <Grid>
          <Typography variant="h1">
            Protect Yourself From Phishing Attacks
          </Typography>
          <TrustBadges />
        </Grid>
        <Grid>
          <img
            src="/screenshot-hero.png"
            alt="Browser extension screenshot"
            style={{ width: "100%", height: "auto", borderRadius: "8px" }}
          />
        </Grid>
      </Grid>

      {/* Social Proof */}
      <CompanyLogos />

      {/* Features */}
      <FeatureGrid />

      {/* Live Demo */}
      <LiveDemoSection />

      {/* Final CTA */}
      <Box
        sx={{
          bgcolor: "primary.main",
          color: "white",
          p: 6,
          borderRadius: 2,
          textAlign: "center",
          mt: 4,
        }}
      >
        <Typography variant="h4" gutterBottom>
          Ready to browse safely?
        </Typography>
        <Typography variant="body1" sx={{ mb: 3 }}>
          Add our extension to your browser today
        </Typography>
        <ChromeButton />
      </Box>
    </Container>
  );
}
