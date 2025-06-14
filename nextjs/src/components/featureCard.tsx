// components/featureCard.tsx
import { Card, Typography } from "@mui/material";

export default function FeatureCard({
  icon,
  title,
  text,
}: {
  icon: string;
  title: string;
  text: string;
}) {
  return (
    <Card
      elevation={3}
      sx={{
        height: "100%",
        display: "flex",
        flexDirection: "column",
        alignItems: "flex-start",
        p: 3,
        border: "1px solid",
        borderColor: "divider",
        "&:hover": {
          borderColor: "primary.light",
        },
      }}
    >
      <Typography
        variant="h3"
        component="div"
        sx={{ fontSize: "2.5rem", mb: 2 }}
      >
        {icon}
      </Typography>
      <Typography variant="h5" component="h3" gutterBottom>
        {title}
      </Typography>
      <Typography variant="body1" color="text.secondary">
        {text}
      </Typography>
    </Card>
  );
}
