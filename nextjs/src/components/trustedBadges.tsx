"use client";
import { Box, Typography, Stack } from "@mui/material";
import Image from "next/image";

export default function TrustBadges() {
  return (
    <Box sx={{ mt: 4 }}>
      <Typography variant="body2" color="text.secondary" gutterBottom>
        TRUSTED BY SECURITY EXPERTS AT:
      </Typography>
      <Stack direction="row" spacing={2} alignItems="center">
        {["norton", "mcafee", "avast", "bitdefender"].map((brand) => (
          <Image
            key={brand}
            src={`/trust-badges/${brand}.svg`}
            alt={`${brand} trusted badge`}
            width={80}
            height={40}
            style={{ objectFit: "contain" }}
          />
        ))}
      </Stack>
    </Box>
  );
}
