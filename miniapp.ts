import { Router } from "express";
import fs from "fs";
import path from "path";

const router = Router();
const DATA_DIR = process.env.BOT_DATA_DIR || ".";

router.get("/miniapp", (_req, res) => {
  res.setHeader("Content-Type", "text/html; charset=utf-8");
  res.send(`<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8"/>
  <title>Xác Minh Thiết Bị</title>
</head>
<body>
  <h1>🔐 Xác Minh Thiết Bị</h1>
  <p>Đang kiểm tra thông tin thiết bị của bạn...</p>
  <button onclick="verify()">✅ Xác Minh</button>
  <script>
    async function verify() {
      alert('✅ Xác minh thành công!');
    }
  <\/script>
<\/body>
</html>`);
});

export default router;