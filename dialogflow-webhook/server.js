const express = require('express');
const bodyParser = require('body-parser');
const { WebhookClient, Payload } = require('dialogflow-fulfillment');

const app = express();
app.use(bodyParser.json());

// ===== DỮ LIỆU MẪU =====
const sampleProducts = {
  'giày thể thao': {
    'nam': ["Giày Nike Air Max - 1.200.000đ", "Giày Adidas Ultraboost - 1.500.000đ"],
    'nữ': ["Giày Puma nữ - 980.000đ", "Giày Skechers nữ - 1.050.000đ"]
  },
  'áo thể thao': {
    'nam': ["Áo Nike Dri-FIT - 450.000đ", "Áo Adidas nam - 500.000đ"],
    'nữ': ["Áo tanktop nữ - 400.000đ", "Áo thể thao Zumba - 430.000đ"]
  }
};

const sampleOrders = {
  'HD001': { customer_name: 'Nguyễn Văn A', product: 'Giày Nike Air Max', status: 'Đang giao' },
  'HD002': { customer_name: 'Trần Thị B', product: 'Áo Adidas Run', status: 'Đã giao' }
};

const sampleStores = {
  'nha trang': {
    address: '01 Nguyễn Thị Minh Khai, Nha Trang',
    phone: '0888 862426',
    fanpage_link: 'https://www.facebook.com/SportproNhaTrang1'
  },
  'vũng tàu': {
    address: '170 Nguyễn Văn Trỗi, Vũng Tàu',
    phone: '0911 054356',
    fanpage_link: 'https://www.facebook.com/SportproVungTau'
  },
  'vinh': {
    address: '34 Nguyễn Văn Cừ, Vinh',
    phone: '0254 3500 098',
    fanpage_link: 'https://www.facebook.com/sportprovinh.vn'
  }
};

const promotions = [
  {
    title: 'Giảm 50% giày Adidas',
    description: 'Áp dụng toàn bộ mẫu Ultraboost đến hết 30/6.',
    link: 'https://sportpro.vn/collections/adidas-sale-50'
  },
  {
    title: 'Mua 2 tặng 1 áo thể thao',
    description: 'Khuyến mãi đặc biệt cho thành viên từ 1/6–15/6.',
    link: 'https://sportpro.vn/collections/ao-the-thao-khuyen-mai'
  }
];

function normalizeInput(text) {
  const lower = text.toLowerCase();
  const gender = lower.includes('nam') ? 'nam' : lower.includes('nữ') ? 'nữ' : null;
  let product_type = null;
  if (lower.includes('giày')) product_type = 'giày thể thao';
  else if (lower.includes('áo')) product_type = 'áo thể thao';
  return { product_type, gender };
}

// ===== WELCOME INTENT =====
function handleWelcome(agent) {
  const welcomeMessage = {
    richContent: [[
      {
        type: "info",
        title: "🎉 Chào mừng bạn đến với SportPro!",
        subtitle: "Mình có thể giúp gì hôm nay?"
      },
      {
        type: "chips",
        options: [
          { text: "🛍 Tìm sản phẩm" },
          { text: "📦 Kiểm tra đơn hàng" },
          { text: "🏬 Tìm cửa hàng" },
          { text: "🔥 Xem khuyến mãi" }
        ]
      }
    ]]
  };
  agent.add(new Payload(agent.UNSPECIFIED, welcomeMessage, { rawPayload: true, sendAsMessage: true }));
}

// ===== TÌM SẢN PHẨM =====
function handleSearchProduct(agent) {
  const rawQuery = agent.query;
  let productType = agent.parameters.product_type;
  let gender = agent.parameters.gender;

  // Chuẩn hóa từ văn bản nếu thiếu entity
  if (!productType || !gender) {
    const normalized = normalizeInput(rawQuery);
    productType = productType || normalized.product_type;
    gender = gender || normalized.gender;
  }

  if (!productType && !gender) {
    agent.add("🛍 Bạn muốn tìm sản phẩm gì (giày thể thao, áo thể thao)? Cho nam hay nữ?");
    return;
  }
  if (!productType) {
    agent.add("📌 Bạn muốn tìm sản phẩm nào? Ví dụ: giày thể thao, áo thể thao?");
    return;
  }
  if (!gender) {
    agent.add("📌 Sản phẩm bạn cần dành cho nam hay nữ?");
    return;
  }

  const typeKey = productType.toLowerCase();
  const genderKey = gender.toLowerCase();
  const matched = sampleProducts[typeKey]?.[genderKey];

  if (matched) {
    let response = `🛍 Một số ${productType} cho ${gender} bạn có thể tham khảo:\n`;
    matched.forEach(item => response += `• ${item}\n`);
    agent.add(response);
  } else {
    agent.add(`❗ Loại sản phẩm bạn nhập chưa có. Bạn có thể chọn: giày thể thao hoặc áo thể thao.`);
  }
}

// ===== KIỂM TRA ĐƠN HÀNG =====
function handleOrderSupport(agent) {
  const orderId = agent.parameters.order_id;
  if (!orderId) {
    agent.add("⚠️ Bạn chưa cung cấp mã đơn hàng.");
    return;
  }
  const order = sampleOrders[orderId.toUpperCase()];
  if (order) {
    agent.add(`📦 Đơn hàng **${orderId.toUpperCase()}** của **${order.customer_name}**:\n- Sản phẩm: ${order.product}\n- Trạng thái: ${order.status}`);
  } else {
    agent.add(`❌ Không tìm thấy đơn hàng **${orderId.toUpperCase()}**.`);
  }
}

// ===== TÌM CỬA HÀNG =====
function handleStoreLocation(agent) {
  let location = agent.parameters.store_location;
  if (!location || location.length < 3) {
    agent.add("📍 Bạn vui lòng nhập tên khu vực cụ thể như: Nha Trang, Vũng Tàu, Vinh...");
    return;
  }
  location = location.toLowerCase().trim();
  const store = sampleStores[location];
  if (store) {
    const message = `🏬 Cửa hàng tại ${location}:\n📍 Địa chỉ: ${store.address}\n📞 Hotline: ${store.phone}\n🌐 Fanpage: ${store.fanpage_link}`;
    agent.add(message);
  } else {
    agent.add(`❌ Hiện tại chưa có cửa hàng nào ở khu vực \"${location}\". Bạn vui lòng thử khu vực khác nhé!`);
  }
}

// ===== KHUYẾN MÃI =====
function handlePromotion(agent) {
  let promoMsg = "🔥 Khuyến mãi hiện tại:\n";
  promotions.forEach(p => {
    promoMsg += `• ${p.title}\n${p.description}\n🔗 ${p.link}\n\n`;
  });
  agent.add(promoMsg.trim());
}

// ===== FALLBACK =====
function handleFallback(agent) {
  agent.add("❓ Mình chưa hiểu ý bạn lắm. Bạn có thể chọn từ menu hoặc nói rõ hơn?");
}

// ===== INTENT MAPPING =====
const intentMap = new Map();
intentMap.set('WelcomeIntent', handleWelcome);
intentMap.set('SearchProductIntent', handleSearchProduct);
intentMap.set('OrderSupportIntent', handleOrderSupport);
intentMap.set('StoreLocationIntent', handleStoreLocation);
intentMap.set('PromotionIntent', handlePromotion);
intentMap.set('Default Fallback Intent', handleFallback);

// ===== WEBHOOK ROUTE =====
app.post('/webhook', (req, res) => {
  const agent = new WebhookClient({ request: req, response: res });
  agent.handleRequest(intentMap);
});

// ===== SERVER START =====
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`🚀 Webhook server is running at http://localhost:${PORT}`);
});
