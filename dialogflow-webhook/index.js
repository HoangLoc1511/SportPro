const functions = require('firebase-functions');
const { WebhookClient } = require('dialogflow-fulfillment');

exports.dialogflowFirebaseFulfillment = functions.https.onRequest((req, res) => {
  const agent = new WebhookClient({ request: req, response: res });

  // Xử lý intent StoreLocationIntent
  function handleStoreLocation(agent) {
    const loc = agent.parameters.store_location?.toLowerCase() || '';

    const storeData = {
      'nha trang': {
        title: '🏪 SportPro.vn Nha Trang',
        subtitle: '01 Nguyễn Thị Minh Khai, Phường Lộc Thọ, TP. Nha Trang, Khánh Hoà\n🕘 8:00 - 22:00 (Thứ 2 – CN)\n📞 0888 862426',
        button: { text: 'Fanpage Nha Trang', link: 'https://www.facebook.com/SportproNhaTrang1' }
      },
      'vinpearl harbour nha trang': {
        title: '🏪 SportPro Vinpearl Harbour Nha Trang',
        subtitle: 'Lô L-05, Vinpearl Harbour Nha Trang\n🕘 8:00 - 22:00 (Thứ 2 – CN)\n📞 0911 054356'
      },
      'vũng tàu': {
        title: '🏪 SportPro.vn Vũng Tàu',
        subtitle: '170 Nguyễn Văn Trỗi, P.4, TP. Vũng Tàu, Bà Rịa - Vũng Tàu\n🕘 8:00 - 22:00 (Thứ 2 – CN)\n📞 0254 3500 098',
        button: { text: 'Fanpage Vũng Tàu', link: 'https://www.facebook.com/SportproVungTau' }
      },
      'buôn ma thuột': {
        title: '🏪 SportPro.vn Buôn Ma Thuột',
        subtitle: '08 Hai Bà Trưng, P. Thắng Lợi, TP. Buôn Ma Thuột, Đắk Lắk\n🕘 8:00 - 22:00 (Thứ 2 – CN)\n📞 0822 24 29 29',
        button: { text: 'Fanpage Buôn Ma Thuột', link: 'https://www.facebook.com/SportproBuonMaThuot' }
      },
      'vinh': {
        title: '🏪 SportPro.vn Vinh',
        subtitle: '34 Nguyễn Văn Cừ, TP. Vinh, Nghệ An\n🕘 8:00 - 22:00 (Thứ 2 – CN)\n📞 0931 622 633',
        button: { text: 'Fanpage Vinh', link: 'https://www.facebook.com/sportprovinh.vn' }
      }
    };

    const data = storeData[loc];

    if (data) {
      // Tạo richContent response
      const richResponse = [
        [
          {
            type: 'info',
            title: data.title,
            subtitle: data.subtitle
          }
        ]
      ];

      if (data.button) {
        richResponse[0].push({
          type: 'button',
          icon: { type: 'chevron_right', color: '#FF5722' },
          text: data.button.text,
          link: data.button.link
        });
      }

      agent.add(new Payload(agent.UNSPECIFIED, { richContent: richResponse }, { rawPayload: true, sendAsMessage: true }));
    } else {
      // Trả lời nếu không tìm thấy
      agent.add('🏬 SportPro hiện có nhiều cửa hàng trên toàn quốc. Bạn cần tìm cửa hàng ở khu vực nào ạ?\n👉 Ví dụ: Nha Trang, Vinpearl Harbour Nha Trang, Vũng Tàu, Buôn Ma Thuột, Vinh.');
    }
  }

  // Map intent name với hàm xử lý
  let intentMap = new Map();
  intentMap.set('StoreLocationIntent', handleStoreLocation);

  // Nếu bạn có thêm intent khác, map thêm ở đây:
  // intentMap.set('WelcomeIntent', handleWelcomeIntent);
  // intentMap.set('SearchProductIntent', handleSearchProductIntent);
  // ...

  agent.handleRequest(intentMap);
});