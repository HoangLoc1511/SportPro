const express = require('express');
const bodyParser = require('body-parser');
const { WebhookClient, Payload } = require('dialogflow-fulfillment');
const sql = require('mssql');

const app = express();
app.use(bodyParser.json());

// Kết nối SQL Server (sửa lại user/pass nếu cần)
const dbConfig = {
  user: 'sa',
  password: 'MatKhauMoi123!',
  server: 'localhost', // dùng 'sql-xxxxx.database.windows.net' nếu dùng Azure SQL
  database: 'SportPro',
  options: {
    encrypt: false,
    trustServerCertificate: true
  }
};

// INTENT: Chào mừng
function handleWelcome(agent) {
  agent.add("🎉 Xin chào bạn đến với SportPro! Mình có thể giúp gì hôm nay?");
}

// INTENT: Tìm sản phẩm theo loại và giới tính
async function handleSearchProduct(agent) {
  const productType = agent.parameters.product_type;
  const gender = agent.parameters.gender;

  try {
    await sql.connect(dbConfig);
    const result = await sql.query`SELECT TOP 3 name, price FROM products WHERE type = ${productType} AND gender = ${gender}`;

    if (result.recordset.length > 0) {
      let response = `🛍 Một số ${productType} cho ${gender} bạn có thể tham khảo:\n`;
      result.recordset.forEach(p => {
        response += `• ${p.name} – ${p.price.toLocaleString()}đ\n`;
      });
      agent.add(response);
    } else {
      agent.add(`😅 Hiện chưa có ${productType} dành cho ${gender}. Bạn thử sản phẩm khác nhé!`);
    }
  } catch (err) {
    console.error(err);
    agent.add("🚨 Lỗi khi truy vấn sản phẩm.");
  }
}

// INTENT: Kiểm tra đơn hàng
async function handleOrderSupport(agent) {
  const orderId = agent.parameters.order_id;
  console.log("👉 order_id từ Dialogflow:", orderId);

  try {
    await sql.connect(dbConfig);
    console.log("✅ Kết nối SQL thành công");

    const result = await sql.query`SELECT * FROM orders WHERE order_id = ${orderId}`;
    console.log("📄 Kết quả truy vấn:", result.recordset);

    if (result.recordset.length > 0) {
      const order = result.recordset[0];
      agent.add(`📦 Đơn hàng **${order.order_id}** của **${order.customer_name}**:\n- Sản phẩm: ${order.product}\n- Trạng thái: ${order.status}`);
    } else {
      agent.add(`❌ Không tìm thấy đơn hàng **${orderId}**.`);
    }
  } catch (error) {
    console.error("❌ Lỗi SQL:", error);
    agent.add("😓 Có lỗi khi kiểm tra đơn hàng.");
  }
}

// INTENT: Tìm cửa hàng theo khu vực
async function handleStoreLocation(agent) {
  const location = agent.parameters.store_location?.toLowerCase().trim();

  try {
    await sql.connect(dbConfig);
    const result = await sql.query`SELECT * FROM stores WHERE location = ${location}`;

    if (result.recordset.length > 0) {
      const store = result.recordset[0];
      const message = `🏬 Cửa hàng tại ${location}:\n📍 ${store.address}\n📞 ${store.phone}\n👉 Fanpage: ${store.fanpage_link}`;
      agent.add(message);
    } else {
      agent.add("😅 Hiện chưa có cửa hàng ở khu vực đó. Bạn thử khu vực khác nhé!");
    }
  } catch (err) {
    console.error(err);
    agent.add("🚨 Lỗi khi lấy thông tin cửa hàng.");
  }
}

// INTENT: Hiển thị khuyến mãi
async function handlePromotion(agent) {
  try {
    await sql.connect(dbConfig);
    const result = await sql.query`SELECT TOP 2 * FROM promotions ORDER BY promo_id DESC`;

    if (result.recordset.length > 0) {
      let promoMsg = "🔥 Khuyến mãi hiện tại:\n";
      result.recordset.forEach(p => {
        promoMsg += `• ${p.title}\n${p.description}\n🔗 ${p.link}\n\n`;
      });
      agent.add(promoMsg.trim());
    } else {
      agent.add("😅 Hiện không có chương trình khuyến mãi nào.");
    }
  } catch (err) {
    console.error(err);
    agent.add("🚨 Lỗi khi truy vấn khuyến mãi.");
  }
}

// INTENT fallback
function handleFallback(agent) {
  agent.add("❓ Mình chưa hiểu bạn nói gì. Bạn có thể thử lại?");
}

// MAPPING intent với function xử lý
const intentMap = new Map();
intentMap.set('WelcomeIntent', handleWelcome);
intentMap.set('SearchProductIntent', handleSearchProduct);
intentMap.set('OrderSupportIntent', handleOrderSupport);
intentMap.set('StoreLocationIntent', handleStoreLocation);
intentMap.set('PromotionIntent', handlePromotion);
intentMap.set('Default Fallback Intent', handleFallback);

// ENDPOINT
app.post('/webhook', (req, res) => {
  const agent = new WebhookClient({ request: req, response: res });
  agent.handleRequest(intentMap);
});

// RUN SERVER
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`🚀 Webhook is running at http://localhost:${PORT}`);
});
