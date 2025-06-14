"use client";
import { Box, Typography, Grid, Card, CardContent } from "@mui/material";
import { Security, Lock, Warning, VisibilityOff } from "@mui/icons-material";

const FEATURES = [
  {
    icon: <Security fontSize="large" color="primary" />,
    title: "Real-time Protection",
    description:
      "Scans every link you click for phishing attempts in real-time",
  },
  {
    icon: <Lock fontSize="large" color="primary" />,
    title: "Banking Protection",
    description: "Extra security layer for financial websites and login pages",
  },
  {
    icon: <Warning fontSize="large" color="primary" />,
    title: "Warning System",
    description: "Clear visual warnings when visiting suspicious sites",
  },
  {
    icon: <VisibilityOff fontSize="large" color="primary" />,
    title: "Stealth Mode",
    description: "Prevents trackers from detecting your security extensions",
  },
];

export default function FeatureGrid() {
  return (
    <Box sx={{ py: 8 }}>
      <Typography
        variant="h3"
        textAlign="center"
        gutterBottom
        sx={{ fontWeight: 700 }}
      >
        How It Protects You
      </Typography>
      <Grid container spacing={4} sx={{ mt: 4 }}>
        {FEATURES.map((feature, index) => (
          <Grid key={index}>
            <Card sx={{ height: "100%", bgcolor: "background.paper" }}>
              <CardContent sx={{ p: 4, textAlign: "center" }}>
                <Box sx={{ mb: 2 }}>{feature.icon}</Box>
                <Typography variant="h5" gutterBottom>
                  {feature.title}
                </Typography>
                <Typography color="text.secondary">
                  {feature.description}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}
