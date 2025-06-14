// app/api/detect/route.ts
import { NextResponse } from "next/server";

export const runtime = "edge"; // Optional: for Vercel Edge Functions

export async function POST() {
  if (req.method !== "POST") {
    return NextResponse.json({ error: "Method not allowed" }, { status: 405 });
  }

  try {
    const { url } = await req.json();

    const flaskResponse = await fetch("http://localhost:5000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    });

    if (!flaskResponse.ok) {
      throw new Error(`API responded with ${flaskResponse.status}`);
    }

    return NextResponse.json(await flaskResponse.json());
  } catch (error) {
    return NextResponse.json({ error: "API request failed" }, { status: 500 });
  }
}
