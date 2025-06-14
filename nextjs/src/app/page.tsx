// app/page.tsx
"use client";
import {
  Box,
  Container,
  Typography,
  Button,
  Paper,
  Divider,
  Chip,
} from "@mui/material";
import Grid from "@mui/material/Grid";
import { motion } from "framer-motion";
import { Star, Security, Lock, Speed, VerifiedUser } from "@mui/icons-material";
import ChromeButton from "@/components/chromeButton";

export default function StorePage() {
  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* Hero Section with Trust Badges */}
      <Grid container spacing={6} alignItems="center" sx={{ mb: 8 }}>
        <Grid>
          <Chip
            label="Editors' Choice"
            color="primary"
            sx={{ mb: 2, fontWeight: 600 }}
            icon={<VerifiedUser />}
          />

          <Typography
            variant="h2"
            component="h1"
            gutterBottom
            sx={{ fontWeight: 700 }}
          >
            <Box component="span" color="primary.main">
              PhishGuard
            </Box>{" "}
            Blocks
            <br />
            Phishing Attacks Automatically
          </Typography>

          <Typography variant="h5" color="text.secondary" paragraph>
            Real-time AI protection that stops phishing scams before they reach
            you. Works silently as you browse.
          </Typography>

          <Box sx={{ display: "flex", alignItems: "center", gap: 3, mb: 3 }}>
            <Box sx={{ display: "flex", alignItems: "center" }}>
              {[1, 2, 3, 4, 5].map((star) => (
                <Star key={star} color="primary" />
              ))}
              <Typography variant="body1" sx={{ ml: 1 }}>
                4.8/5 (1,200+ reviews)
              </Typography>
            </Box>
          </Box>

          <Box
            sx={{
              display: "flex",
              gap: 2,
              alignItems: "center",
              flexWrap: "wrap",
            }}
          >
            <ChromeButton />
            <Button
              variant="outlined"
              size="large"
              sx={{ px: 4, py: 1.5, borderRadius: 2, fontWeight: 600 }}
              startIcon={<Security />}
            >
              How It Works
            </Button>
          </Box>

          {/* Trust Badges */}
          <Box
            sx={{
              display: "flex",
              gap: 3,
              mt: 3,
              alignItems: "center",
              flexWrap: "wrap",
            }}
          >
            <Typography
              variant="body2"
              sx={{ display: "flex", alignItems: "center" }}
            >
              <Lock color="success" sx={{ mr: 1 }} /> No data collection
            </Typography>
            <Typography
              variant="body2"
              sx={{ display: "flex", alignItems: "center" }}
            >
              <Speed color="success" sx={{ mr: 1 }} /> Zero latency
            </Typography>
          </Box>
        </Grid>

        <Grid>
          <Box
            component="img"
            src="/screenshot-hero.png"
            alt="PhishGuard blocking a phishing attempt"
            sx={{
              borderRadius: 2,
              boxShadow: 3,
              width: "100%",
              border: "1px solid",
              borderColor: "divider",
              transition: "transform 0.3s",
              "&:hover": {
                transform: "scale(1.02)",
              },
            }}
          />
        </Grid>
      </Grid>

      {/* Social Proof Section */}
      <Box sx={{ bgcolor: "background.paper", p: 4, borderRadius: 2, mb: 8 }}>
        <Typography variant="h5" textAlign="center" mb={4}>
          Trusted by security teams at
        </Typography>
        <Grid container spacing={4} justifyContent="center">
          {["Google", "Microsoft", "IBM", "Slack", "Shopify"].map((company) => (
            <Grid key={company}>
              <Typography variant="h6" color="text.secondary">
                {company}
              </Typography>
            </Grid>
          ))}
        </Grid>
      </Box>

      {/* Features Section with Animated Cards */}
      <Box sx={{ mb: 8 }}>
        <Typography
          variant="h3"
          textAlign="center"
          gutterBottom
          sx={{ fontWeight: 700 }}
        >
          How PhishGuard Protects You
        </Typography>
        <Grid container spacing={4}>
          {[
            {
              icon: <Security fontSize="large" color="primary" />,
              title: "Real-time scanning",
              text: "Checks every URL before you click using our constantly updated threat database",
            },
            {
              icon: <VerifiedUser fontSize="large" color="primary" />,
              title: "AI detection",
              text: "Identifies zero-day phishing attempts traditional tools miss",
            },
            {
              icon: <Speed fontSize="large" color="primary" />,
              title: "Lightning fast",
              text: "Adds no detectable latency to your browsing experience",
            },
          ].map((feature, index) => (
            <Grid key={index}>
              <motion.div whileHover={{ y: -5 }}>
                <Paper sx={{ p: 4, height: "100%", borderRadius: 3 }}>
                  <Box sx={{ mb: 2 }}>{feature.icon}</Box>
                  <Typography variant="h5" sx={{ fontWeight: 600, mb: 1.5 }}>
                    {feature.title}
                  </Typography>
                  <Typography color="text.secondary">{feature.text}</Typography>
                </Paper>
              </motion.div>
            </Grid>
          ))}
        </Grid>
      </Box>

      {/* Final CTA Section */}
      <Box
        sx={{
          bgcolor: "primary.main",
          color: "white",
          p: 6,
          borderRadius: 3,
          textAlign: "center",
          mb: 8,
        }}
      >
        <Typography variant="h3" gutterBottom sx={{ fontWeight: 700 }}>
          Ready to Browse Without Fear?
        </Typography>
        <Typography variant="h5" sx={{ mb: 4, opacity: 0.9 }}>
          Join 50,000+ protected users
        </Typography>
        <ChromeButton />
        <Typography variant="body2" sx={{ mt: 2, opacity: 0.8 }}>
          Free forever • No credit card required • 30-second install
        </Typography>
      </Box>
    </Container>
  );
}
