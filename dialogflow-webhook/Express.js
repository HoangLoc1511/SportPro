const express = require('express');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());

// Dữ liệu ví dụ cho các sản phẩm và cửa hàng
const products = {
  "giày thể thao": "Nike, Adidas, Puma...",
  "áo thể thao": "Nike, Adidas, Under Armour..."
};

const stores = {
  "nha trang": "01 Nguyễn Thị Minh Khai, Phường Lộc Thọ, TP. Nha Trang, Khánh Hoà",
  "vung tau": "170 Nguyễn Văn Trỗi, phường 4, TP. Vũng Tàu",
  "vinh": "34 Nguyễn Văn Cừ, TP Vinh, Nghệ An"
};

// API để nhận yêu cầu từ người dùng
app.post('/webhook', (req, res) => {
  const userMessage = req.body.queryResult.queryText.toLowerCase(); // Lấy câu hỏi từ người dùng

  // Phản hồi ban đầu
  let response = "Xin lỗi, tôi không hiểu câu hỏi của bạn.";

  // Kiểm tra intent từ câu hỏi
  if (userMessage.includes("giày thể thao")) {
    response = `Chúng tôi có các giày thể thao từ Nike, Adidas, Puma...`;
  } else if (userMessage.includes("áo thể thao")) {
    response = `Chúng tôi có áo thể thao từ Nike, Adidas, Under Armour...`;
  } else if (userMessage.includes("cửa hàng nha trang")) {
    response = `🏪 Cửa hàng SportPro tại Nha Trang: ${stores["nha trang"]}`;
  } else if (userMessage.includes("cửa hàng vũng tàu")) {
    response = `🏪 Cửa hàng SportPro tại Vũng Tàu: ${stores["vung tau"]}`;
  } else if (userMessage.includes("cửa hàng vinh")) {
    response = `🏪 Cửa hàng SportPro tại Vinh: ${stores["vinh"]}`;
  } else if (userMessage.includes("kiểm tra đơn hàng")) {
    response = `Vui lòng cung cấp mã đơn hàng để kiểm tra.`;
  } else if (userMessage.includes("tư vấn sản phẩm")) {
    response = "Bạn muốn tư vấn về sản phẩm nào? Giày thể thao, áo thể thao?";
  }

  // Trả lời phản hồi lại cho người dùng
  res.json({
    fulfillmentText: response
  });
});

// Lắng nghe trên cổng
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Webhook server is running on port ${PORT}`);
});
