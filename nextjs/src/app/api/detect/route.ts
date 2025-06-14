// src/app/api/detect/route.ts
import { NextResponse } from "next/server";

export const runtime = "edge"; // Optional: for Vercel Edge Functions

export async function POST(request: Request) {
  try {
    const { url } = await request.json();

    if (!url) {
      return NextResponse.json({ error: "URL is required" }, { status: 400 });
    }

    const flaskResponse = await fetch("http://localhost:5000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Origin: "http://localhost:3000",
      },
      body: JSON.stringify({ url }),
    });

    if (!flaskResponse.ok) {
      const error = await flaskResponse.json();
      return NextResponse.json(
        { error: error.error || "Analysis failed" },
        { status: flaskResponse.status }
      );
    }

    const data = await flaskResponse.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error("API error:", error);
    return NextResponse.json(
      {
        error: "Failed to analyze URL",
        details: error instanceof Error ? error.message : String(error),
      },
      { status: 500 }
    );
  }
}
