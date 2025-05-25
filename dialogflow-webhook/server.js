const express = require('express');
const bodyParser = require('body-parser');
const { WebhookClient } = require('dialogflow-fulfillment');

const app = express();
app.use(bodyParser.json());

// ===== INTENT: CHÀO MỪNG =====
function handleWelcome(agent) {
  agent.add("🎉 Xin chào bạn đến với SportPro! Mình có thể giúp gì hôm nay?");
}

// ===== INTENT: TÌM SẢN PHẨM =====
function handleSearchProduct(agent) {
  const productType = agent.parameters.product_type;
  const gender = agent.parameters.gender;

  if (!productType || !gender) {
    agent.add("❓ Bạn vui lòng cung cấp loại sản phẩm và giới tính cụ thể hơn nhé.");
    return;
  }

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

  const matched = sampleProducts[productType?.toLowerCase()]?.[gender?.toLowerCase()];

  if (matched) {
    let response = `🛍 Một số ${productType} cho ${gender} bạn có thể tham khảo:\n`;
    matched.forEach(item => response += `• ${item}\n`);
    agent.add(response);
  } else {
    agent.add(`😅 Hiện chưa có dữ liệu mẫu cho ${productType} dành cho ${gender}.`);
  }
}

// ===== INTENT: KIỂM TRA ĐƠN HÀNG =====
function handleOrderSupport(agent) {
  const orderId = agent.parameters.order_id;

  if (!orderId) {
    agent.add("⚠️ Bạn chưa cung cấp mã đơn hàng.");
    return;
  }

  // Dữ liệu mẫu
  const sampleOrders = {
    'HD001': {
      customer_name: 'Nguyễn Văn A',
      product: 'Giày Nike Air Max',
      status: 'Đang giao'
    },
    'HD002': {
      customer_name: 'Trần Thị B',
      product: 'Áo Adidas Run',
      status: 'Đã giao'
    }
  };

  const order = sampleOrders[orderId.toUpperCase()];

  if (order) {
    agent.add(`📦 Đơn hàng **${orderId.toUpperCase()}** của **${order.customer_name}**:\n- Sản phẩm: ${order.product}\n- Trạng thái: ${order.status}`);
  } else {
    agent.add(`❌ Không tìm thấy đơn hàng **${orderId.toUpperCase()}**.`);
  }
}

// ===== INTENT: THÔNG TIN CỬA HÀNG =====
function handleStoreLocation(agent) {
  let location = agent.parameters.store_location;

  if (!location) {
    agent.add("❓ Bạn vui lòng nhập lại tên khu vực bạn cần tìm cửa hàng, ví dụ: Nha Trang, Vũng Tàu, Vinh...");
    return;
  }

  location = location.toLowerCase().trim();

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

  const store = sampleStores[location];

  if (store) {
    const message = `🏬 Cửa hàng tại ${location}:\n📍 Địa chỉ: ${store.address}\n📞 Hotline: ${store.phone}\n🌐 Fanpage: ${store.fanpage_link}`;
    agent.add(message);
  } else {
    agent.add(`❌ Hiện tại chưa có cửa hàng nào ở khu vực "${location}". Bạn vui lòng thử khu vực khác nhé!`);
  }
}

// ===== INTENT: KHUYẾN MÃI =====
function handlePromotion(agent) {
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

  let promoMsg = "🔥 Khuyến mãi hiện tại:\n";
  promotions.forEach(p => {
    promoMsg += `• ${p.title}\n${p.description}\n🔗 ${p.link}\n\n`;
  });

  agent.add(promoMsg.trim());
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
