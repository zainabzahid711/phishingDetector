// nextjs-popup/src/app/api/phishing-check/route.js
import { NextResponse } from "next/server";

export async function POST(request) {
  try {
    const { url } = await request.json();

    // Call your Python server
    const pythonResponse = await fetch("http://localhost:5000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    });

    if (!pythonResponse.ok) {
      throw new Error("Python server error");
    }

    const data = await pythonResponse.json();
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json(
      { error: error.message || "Prediction failed" },
      { status: 500 }
    );
  }
}
