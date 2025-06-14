"use client";
import { Box, Typography, Grid } from "@mui/material";
import Image from "next/image";

const LOGOS = ["google", "microsoft", "slack", "dropbox", "salesforce", "zoom"];

export default function CompanyLogos() {
  return (
    <Box sx={{ py: 8, textAlign: "center" }}>
      <Typography variant="h6" gutterBottom color="text.secondary">
        PROTECTING EMPLOYEES AT:
      </Typography>
      <Grid container spacing={4} justifyContent="center" alignItems="center">
        {LOGOS.map((company) => (
          <Grid key={company}>
            <Image
              src={`/company-logos/${company}.svg`}
              alt={`${company} logo`}
              width={120}
              height={40}
              style={{ filter: "grayscale(100%)", opacity: 0.8 }}
            />
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}
