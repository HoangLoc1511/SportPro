const express = require('express');
const bodyParser = require('body-parser');
const { WebhookClient } = require('dialogflow-fulfillment');
const sql = require('mssql');

const app = express();
app.use(bodyParser.json());

// ===== CẤU HÌNH SQL SERVER =====
const dbConfig = {
  user: 'sa',
  password: 'MatKhauMoi123!',
  server: 'localhost',
  database: 'SportPro',
  options: {
    encrypt: false,
    trustServerCertificate: true
  }
};

// ===== INTENT: CHÀO MỪNG =====
function handleWelcome(agent) {
  agent.add("🎉 Xin chào bạn đến với SportPro! Mình có thể giúp gì hôm nay?");
}

// ===== INTENT: TÌM SẢN PHẨM =====
async function handleSearchProduct(agent) {
  const productType = agent.parameters.product_type;
  const gender = agent.parameters.gender;

  if (!productType || !gender) {
    agent.add("❓ Bạn vui lòng cung cấp loại sản phẩm và giới tính cụ thể hơn nhé.");
    return;
  }

  try {
    const pool = await sql.connect(dbConfig);
    const result = await pool.request()
      .input('type', sql.NVarChar(50), productType.toLowerCase())
      .input('gender', sql.NVarChar(20), gender.toLowerCase())
      .query('SELECT TOP 3 name, price FROM products WHERE LOWER(type) = @type AND LOWER(gender) = @gender');

    if (result.recordset.length > 0) {
      let response = `🛍 Một số ${productType} cho ${gender} bạn có thể tham khảo:\n`;
      result.recordset.forEach(p => {
        response += `• ${p.name} – ${p.price.toLocaleString()}đ\n`;
      });
      agent.add(response);
    } else {
      agent.add(`😅 Hiện chưa có ${productType} dành cho ${gender}. Bạn thử sản phẩm khác nhé!`);
    }
  } catch (error) {
    console.error("❌ Lỗi truy vấn sản phẩm:", error);
    agent.add("🚨 Có lỗi xảy ra khi tìm sản phẩm.");
  }
}

// ===== INTENT: KIỂM TRA ĐƠN HÀNG =====
async function handleOrderSupport(agent) {
  const orderId = agent.parameters.order_id;
  if (!orderId) {
    agent.add("⚠️ Bạn chưa cung cấp mã đơn hàng.");
    return;
  }

  const upperOrderId = orderId.toUpperCase();
  console.log("👉 orderId nhận từ người dùng:", orderId);

  try {
    const pool = await sql.connect(dbConfig);
    const result = await pool.request()
      .input('orderId', sql.VarChar(20), upperOrderId)
      .query('SELECT * FROM orders WHERE UPPER(order_id) = @orderId');

    console.log("📄 Kết quả truy vấn:", result.recordset);

    if (result.recordset.length > 0) {
      const order = result.recordset[0];
      agent.add(`📦 Đơn hàng **${order.order_id}** của **${order.customer_name}**:\n- Sản phẩm: ${order.product}\n- Trạng thái: ${order.status}`);
    } else {
      agent.add(`❌ Không tìm thấy đơn hàng **${upperOrderId}**.`);
    }
  } catch (error) {
    console.error("❌ Lỗi khi kiểm tra đơn hàng:", error);
    agent.add("😓 Có lỗi khi kiểm tra đơn hàng.");
  }
}

// ===== INTENT: THÔNG TIN CỬA HÀNG =====
async function handleStoreLocation(agent) {
  const location = agent.parameters.store_location?.toLowerCase().trim();
  if (!location) {
    agent.add("❓ Bạn vui lòng cung cấp tên khu vực cần tìm cửa hàng.");
    return;
  }

  try {
    const pool = await sql.connect(dbConfig);
    const result = await pool.request()
      .input('loc', sql.NVarChar(50), location)
      .query('SELECT * FROM stores WHERE LOWER(location) = @loc');

    if (result.recordset.length > 0) {
      const store = result.recordset[0];
      const message = `🏬 Cửa hàng tại ${location}:\n📍 ${store.address}\n📞 ${store.phone}\n👉 Fanpage: ${store.fanpage_link}`;
      agent.add(message);
    } else {
      agent.add(`😅 Chưa có cửa hàng tại khu vực **${location}**.`);
    }
  } catch (error) {
    console.error("❌ Lỗi khi lấy thông tin cửa hàng:", error);
    agent.add("🚨 Có lỗi xảy ra khi tìm cửa hàng.");
  }
}

// ===== INTENT: KHUYẾN MÃI =====
async function handlePromotion(agent) {
  try {
    const pool = await sql.connect(dbConfig);
    const result = await pool.request()
      .query('SELECT TOP 2 * FROM promotions ORDER BY promo_id DESC');

    if (result.recordset.length > 0) {
      let promoMsg = "🔥 Khuyến mãi hiện tại:\n";
      result.recordset.forEach(p => {
        promoMsg += `• ${p.title}\n${p.description}\n🔗 ${p.link}\n\n`;
      });
      agent.add(promoMsg.trim());
    } else {
      agent.add("😅 Hiện không có chương trình khuyến mãi nào.");
    }
  } catch (error) {
    console.error("❌ Lỗi khi truy vấn khuyến mãi:", error);
    agent.add("🚨 Có lỗi khi lấy thông tin khuyến mãi.");
  }
}

// ===== INTENT: FALLBACK =====
function handleFallback(agent) {
  agent.add("❓ Mình chưa hiểu ý bạn lắm. Bạn có thể nói rõ hơn không?");
}

// ===== MAPPING INTENTS =====
const intentMap = new Map();
intentMap.set('WelcomeIntent', handleWelcome);
intentMap.set('SearchProductIntent', handleSearchProduct);
intentMap.set('OrderSupportIntent', handleOrderSupport);
intentMap.set('StoreLocationIntent', handleStoreLocation);
intentMap.set('PromotionIntent', handlePromotion);
intentMap.set('Default Fallback Intent', handleFallback);

// ===== ROUTE =====
app.post('/webhook', (req, res) => {
  const agent = new WebhookClient({ request: req, response: res });
  agent.handleRequest(intentMap);
});

// ===== START SERVER =====
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`🚀 Webhook server is running at http://localhost:${PORT}`);
});
