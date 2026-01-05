import express from "express";
import cors from "cors";

const app = express();

app.use(cors());
app.use(express.json());

// ✅ route test bắt buộc phải có
app.get("/", (req, res) => {
  res.send("Backend is running on port 5000");
});

export default app;
