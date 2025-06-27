# Template động cho từng intent, dùng để fill slot từ dữ liệu MongoDB

SUGGEST_CAKE_TEMPLATES = [
    "Shop gợi ý bạn thử bánh {cake_name}, vị rất được khách yêu thích!",
    "Bạn có thể tham khảo bánh {cake_name}, hiện đang bán chạy tại shop.",
    "Nếu thích vị {flavor}, bạn nên thử bánh {cake_name} nhé!",
    "Bánh {cake_name} phù hợp cho dịp {occasion}, bạn quan tâm không?",
    "Shop có bánh {cake_name} mới ra mắt, bạn muốn thử không?",
    "Bạn thích bánh mềm hay giòn? Shop có {cake_name} rất ngon!",
    "Bánh {cake_name} đang có ưu đãi, bạn muốn biết thêm không?",
    "Bạn cần bánh cho tiệc {occasion}? Shop gợi ý {cake_name} nhé!",
    "Khách hàng thường chọn {cake_name} cho dịp {occasion}, bạn muốn xem mẫu không?",
    "Bạn muốn bánh ít ngọt? Shop có {cake_name} rất hợp!",
    "Shop có nhiều loại bánh như {cake_name}, bạn muốn xem hình không?",
    "Bạn thích vị gì? Shop có thể gợi ý bánh phù hợp như {cake_name} cho bạn!"
]

ASK_PRICE_TEMPLATES = [
    "Bánh {cake_name} hiện có giá {price}đ.",
    "Giá của {cake_name} là {price}đ bạn nhé!",
    "Bạn quan tâm bánh {cake_name}? Giá là {price}đ.",
    "Bánh {cake_name} đang được bán với giá {price}đ.",
    "Shop báo giá bánh {cake_name}: {price}đ.",
    "Giá bánh {cake_name} có thể thay đổi theo size, hiện tại là {price}đ.",
    "Bạn muốn biết giá bánh {cake_name}? Shop báo là {price}đ.",
    "Bánh {cake_name} đang có giá ưu đãi {price}đ.",
    "Giá bánh {cake_name} hôm nay là {price}đ.",
    "Bạn cần báo giá bánh {cake_name}? Shop gửi bạn: {price}đ.",
    "Bánh {cake_name} có nhiều mức giá, bạn muốn chọn size nào?",
    "Shop có thể tư vấn thêm về giá nếu bạn cần!"
]

ASK_PROMO_TEMPLATES = [
    "Hiện tại shop có chương trình: {promo_name} giảm {promo_value}%.",
    "Shop đang có ưu đãi: {promo_name}, giảm giá lên đến {promo_value}%.",
    "Bạn có thể nhận mã giảm giá {promo_name} khi đặt bánh hôm nay.",
    "Khuyến mãi mới nhất: {promo_name} - giảm {promo_value}%.",
    "Shop thường xuyên có ưu đãi, hiện tại là {promo_name} giảm {promo_value}%.",
    "Đừng bỏ lỡ chương trình {promo_name} với mức giảm {promo_value}% nhé!",
    "Shop có nhiều ưu đãi hấp dẫn, nổi bật là {promo_name} giảm {promo_value}%.",
    "Bạn muốn biết thêm về ưu đãi {promo_name}? Shop hỗ trợ ngay!",
    "Khách hàng mới sẽ được nhận ưu đãi {promo_name} giảm {promo_value}%.",
    "Shop có chương trình tích điểm đổi quà, bạn muốn tham gia không?"
]

ASK_INGREDIENT_TEMPLATES = [
    "Bánh {cake_name} gồm các thành phần: {ingredient}.",
    "Thành phần chính của {cake_name} là: {ingredient}.",
    "Bạn quan tâm thành phần bánh {cake_name}? Shop gửi bạn: {ingredient}.",
    "Bánh {cake_name} được làm từ: {ingredient}.",
    "Shop luôn dùng nguyên liệu tươi mới cho {cake_name}: {ingredient}.",
    "{cake_name} có các nguyên liệu: {ingredient}.",
    "Bạn muốn biết bánh {cake_name} có gì đặc biệt? Thành phần: {ingredient}.",
    "Thành phần của {cake_name} đảm bảo an toàn: {ingredient}.",
    "Bánh {cake_name} không dùng chất bảo quản, thành phần: {ingredient}.",
    "Nếu bạn dị ứng gì, shop sẽ kiểm tra thành phần {cake_name} giúp bạn!"
]

ASK_ADDRESS_TEMPLATES = [
    "Địa chỉ shop: {address}.",
    "Bạn có thể ghé shop tại: {address}.",
    "Shop ở địa chỉ: {address}, rất mong được đón bạn!",
    "Bạn muốn đến cửa hàng? Địa chỉ: {address}.",
    "Shop có chi nhánh tại: {address}.",
    "Bạn cần chỉ đường đến shop? Địa chỉ: {address}.",
    "Shop luôn sẵn sàng phục vụ bạn tại: {address}.",
    "Bạn muốn nhận bánh tại shop hay giao tận nơi? Địa chỉ: {address}.",
    "Shop có nhiều chi nhánh, bạn cần địa chỉ ở khu vực nào?",
    "Bạn cần chỉ đường Google Maps không? Shop gửi link nhé!"
]

ASK_OPENING_TEMPLATES = [
    "Shop mở cửa từ {open_hour}.",
    "Giờ làm việc của shop: {open_hour}.",
    "Bạn có thể ghé shop trong khung giờ: {open_hour}.",
    "Shop phục vụ khách từ {open_hour}.",
    "Giờ mở cửa: {open_hour}.",
    "Shop hoạt động từ {open_hour} mỗi ngày.",
    "Bạn cần đặt bánh ngoài giờ, shop vẫn hỗ trợ giao tận nơi nhé!",
    "Shop mở cửa tất cả các ngày trong tuần từ {open_hour}.",
    "Bạn muốn đặt bánh ngoài giờ, shop sẽ hỗ trợ nếu báo trước!",
    "Shop luôn sẵn sàng phục vụ bạn trong giờ làm việc: {open_hour}."
]

ASK_CONTACT_TEMPLATES = [
    "Bạn có thể liên hệ shop qua số: {phone} hoặc Zalo cùng số nhé!",
    "Mọi thắc mắc bạn gọi trực tiếp {phone} hoặc inbox fanpage giúp shop nhé!",
    "Shop luôn sẵn sàng hỗ trợ bạn qua điện thoại, Zalo, Facebook!",
    "Bạn muốn nhận tư vấn qua kênh nào? Shop sẽ liên hệ lại ngay!",
    "Bạn có thể gửi email cho shop qua {email} nếu cần hỗ trợ chi tiết!",
    "Shop hỗ trợ khách qua hotline: {phone} và Zalo: {phone}.",
    "Bạn cần hỗ trợ gấp? Gọi {phone} nhé!",
    "Shop có fanpage, Zalo, hotline: {phone}, bạn muốn liên hệ kênh nào?",
    "Bạn cần tư vấn đặt bánh, gọi {phone} hoặc nhắn Zalo nhé!",
    "Shop luôn lắng nghe ý kiến khách hàng qua {phone} hoặc {email}."
]

ASK_FEEDBACK_TEMPLATES = [
    "Bạn có góp ý gì cho shop không? Shop rất mong nhận được phản hồi từ bạn!",
    "Cảm ơn bạn đã sử dụng dịch vụ, bạn có thể đánh giá trải nghiệm để shop phục vụ tốt hơn nhé!",
    "Bạn muốn gửi feedback về sản phẩm hay dịch vụ? Shop luôn lắng nghe!",
    "Shop rất trân trọng mọi ý kiến đóng góp của bạn!",
    "Bạn có thể để lại nhận xét trên fanpage hoặc Google Review giúp shop nhé!",
    "Shop luôn mong nhận được phản hồi để cải thiện chất lượng!",
    "Bạn có thể gửi feedback trực tiếp qua Zalo hoặc hotline {phone}.",
    "Cảm ơn bạn đã tin tưởng, mọi góp ý đều giúp shop phát triển hơn!",
    "Bạn muốn đánh giá sản phẩm hay dịch vụ? Shop sẽ ghi nhận ngay!",
    "Shop có form góp ý online, bạn muốn nhận link không?"
]

ASK_COMBO_TEMPLATES = [
    "Shop có nhiều combo bánh tiết kiệm, bạn muốn tham khảo combo nào?",
    "Bạn cần combo cho bao nhiêu người? Shop sẽ gợi ý phù hợp nhé!",
    "Bạn muốn combo bánh sinh nhật, tiệc hay quà tặng?",
    "Shop có combo theo mùa, bạn muốn thử combo nào?",
    "Bạn muốn biết giá combo hay thành phần combo?",
    "Combo {combo_name} đang có ưu đãi, bạn muốn biết chi tiết không?",
    "Shop có combo cho nhóm nhỏ và nhóm lớn, bạn cần loại nào?",
    "Bạn muốn đặt combo bánh kèm nước uống không?",
    "Combo bánh {combo_name} phù hợp cho dịp {occasion}.",
    "Bạn cần tư vấn combo tiết kiệm nhất? Shop hỗ trợ ngay!"
]

ASK_DELIVERY_TEMPLATES = [
    "Shop có giao hàng tận nơi toàn quốc, phí ship tuỳ khu vực bạn nhé!",
    "Bạn cần giao bánh đến đâu? Shop sẽ báo phí ship và thời gian giao dự kiến.",
    "Shop hỗ trợ giao nhanh trong nội thành, bạn cần nhận bánh trong bao lâu?",
    "Bạn muốn nhận bánh trong ngày hay đặt trước?",
    "Shop có đối tác giao hàng uy tín, đảm bảo bánh đến tay bạn an toàn!",
    "Phí ship đến {address} là {ship_fee}đ, bạn xác nhận giúp shop nhé!",
    "Bạn muốn giao hàng ngoài giờ hành chính? Shop sẽ hỗ trợ nếu báo trước!",
    "Shop có thể giao bánh hẹn giờ, bạn muốn nhận lúc nào?",
    "Bạn cần giao bánh cho sự kiện? Shop sẽ sắp xếp ship đúng giờ!",
    "Shop có freeship cho đơn trên {free_ship_limit}đ, bạn muốn tham khảo không?"
]

ASK_NUTRITION_TEMPLATES = [
    "Bạn quan tâm đến thành phần dinh dưỡng của loại bánh nào? Shop sẽ gửi thông tin chi tiết nhé!",
    "Bạn cần tư vấn về calo, chất béo hay thành phần nào? Shop luôn sẵn sàng hỗ trợ!",
    "Shop có bảng dinh dưỡng cho từng loại bánh, bạn hỏi loại nào nhé!",
    "Bạn muốn biết bánh có phù hợp cho người ăn kiêng không?",
    "Bạn cần tư vấn về bánh cho trẻ em, người lớn tuổi hay người tiểu đường?",
    "Bánh {cake_name} có {calo} calo, phù hợp cho chế độ ăn lành mạnh.",
    "Shop có thể gửi bảng dinh dưỡng chi tiết qua Zalo nếu bạn cần!",
    "Bạn muốn biết bánh có chứa gluten, sữa, trứng không? Shop kiểm tra giúp bạn!",
    "Bánh {cake_name} có thành phần dinh dưỡng: {nutrition}.",
    "Bạn cần tư vấn về bánh healthy, shop sẽ hỗ trợ ngay!"
]

ASK_FOR_KIDS_TEMPLATES = [
    "Shop có nhiều loại bánh phù hợp cho trẻ em, bạn muốn bánh vị gì cho bé?",
    "Bạn cần bánh cho bé dịp gì? Shop sẽ gợi ý mẫu phù hợp nhé!",
    "Bạn muốn bánh ít ngọt, nhiều màu sắc hay hình thú cho bé?",
    "Shop có bánh sinh nhật, bánh mini cho bé, bạn muốn tham khảo không?",
    "Bạn cần tư vấn về thành phần an toàn cho trẻ nhỏ không?",
    "Bánh {cake_name} được nhiều bé yêu thích, bạn muốn xem hình không?",
    "Shop có bánh cho bé dị ứng sữa, trứng, bạn cần loại nào?",
    "Bạn muốn đặt bánh cho bé trai hay bé gái? Shop sẽ gợi ý mẫu phù hợp!",
    "Bánh cho bé có thể trang trí theo chủ đề hoạt hình, bạn muốn thử không?",
    "Bạn cần bánh cho tiệc sinh nhật, thôi nôi hay dịp đặc biệt nào cho bé?"
]

CUSTOM_CAKE_TEMPLATES = [
    "Bạn muốn đặt bánh theo yêu cầu như thế nào? Mô tả chi tiết giúp shop nhé!",
    "Shop nhận làm bánh custom, bạn gửi ý tưởng hoặc hình mẫu cho mình nhé!",
    "Bạn muốn bánh trang trí theo chủ đề gì? Shop sẽ tư vấn mẫu phù hợp!",
    "Bạn cần bánh kích thước, màu sắc, vị gì? Shop sẽ làm theo ý bạn!",
    "Bạn gửi hình mẫu hoặc mô tả chi tiết để shop báo giá nhé!",
    "Shop có thể in hình, chữ, logo lên bánh theo yêu cầu của bạn!",
    "Bạn muốn bánh cho dịp gì? Shop sẽ gợi ý mẫu custom phù hợp!",
    "Bánh custom có thể chọn vị, màu, trang trí theo ý bạn!",
    "Bạn cần bánh gấp, shop sẽ ưu tiên làm nhanh nhất có thể!",
    "Bạn muốn đặt bánh cá nhân hóa cho ai? Shop sẽ tư vấn mẫu độc đáo!"
]

CONNECT_STAFF_TEMPLATES = [
    "Shop sẽ kết nối bạn với nhân viên tư vấn ngay!",
    "Bạn vui lòng chờ một chút, nhân viên sẽ hỗ trợ bạn ngay lập tức!",
    "Shop đã chuyển thông tin của bạn cho nhân viên, bạn đợi chút nhé!",
    "Bạn cần hỗ trợ gì thêm, nhân viên sẽ liên hệ ngay!",
    "Nhân viên tư vấn sẽ gọi lại cho bạn trong ít phút nữa!",
    "Bạn muốn trao đổi qua Zalo hay điện thoại? Shop sẽ kết nối ngay!",
    "Bạn cần tư vấn chi tiết, nhân viên sẽ hỗ trợ tận tình!",
    "Shop luôn sẵn sàng hỗ trợ khách hàng qua hotline và Zalo!",
    "Bạn muốn gặp quản lý hay nhân viên tư vấn? Shop sẽ sắp xếp!",
    "Bạn cần hỗ trợ gấp, shop sẽ ưu tiên kết nối nhanh nhất!"
]

CHECK_ORDER_TEMPLATES = [
    "Bạn vui lòng cung cấp mã đơn hàng để shop kiểm tra giúp nhé!",
    "Shop sẽ kiểm tra tình trạng đơn hàng cho bạn ngay, bạn cho mình xin thông tin đơn nhé!",
    "Bạn đặt hàng qua kênh nào để shop tra cứu nhanh hơn?",
    "Bạn cần kiểm tra đơn hàng nào, vui lòng gửi mã hoặc số điện thoại đặt hàng!",
    "Shop sẽ báo lại tình trạng đơn hàng trong ít phút nữa!",
    "Bạn muốn biết đơn đã giao hay chưa? Shop kiểm tra ngay!",
    "Shop có thể gửi thông tin đơn hàng qua Zalo nếu bạn cần!",
    "Bạn cần hỗ trợ về đơn hàng nào cụ thể không?",
    "Shop sẽ ưu tiên kiểm tra đơn hàng gấp cho bạn!",
    "Bạn muốn đổi/trả đơn hàng này không? Shop sẽ hỗ trợ luôn!"
]

ASK_PAYMENT_TEMPLATES = [
    "Shop hỗ trợ thanh toán tiền mặt, chuyển khoản và ví điện tử.",
    "Bạn muốn thanh toán bằng phương thức nào? Shop có Momo, ZaloPay, VNPay nhé!",
    "Bạn cần xuất hoá đơn VAT, shop sẽ hỗ trợ khi thanh toán.",
    "Bạn muốn thanh toán trước hay khi nhận bánh?",
    "Shop có hỗ trợ trả góp cho đơn hàng lớn, bạn muốn tìm hiểu không?",
    "Bạn có thể thanh toán qua thẻ tín dụng, chuyển khoản hoặc tiền mặt.",
    "Shop nhận thanh toán qua nhiều kênh, bạn chọn kênh nào tiện nhất nhé!",
    "Bạn cần hướng dẫn thanh toán online không? Shop sẽ gửi chi tiết!",
    "Shop có thể gửi mã QR để bạn thanh toán nhanh chóng!",
    "Bạn muốn thanh toán qua app nào? Shop hỗ trợ Momo, ZaloPay, VNPay."
]

ASK_PRESERVATION_TEMPLATES = [
    "Bánh nên được bảo quản trong ngăn mát tủ lạnh và dùng trong 2-3 ngày.",
    "Bạn cần hướng dẫn bảo quản loại bánh nào? Shop sẽ tư vấn chi tiết nhé!",
    "Shop có hướng dẫn bảo quản riêng cho từng loại bánh, bạn hỏi loại nào?",
    "Bạn muốn biết cách bảo quản khi vận chuyển xa không?",
    "Shop khuyên dùng bánh trong ngày để đảm bảo vị ngon nhất!",
    "Bánh có thể để ngoài tủ lạnh tối đa 4 tiếng, sau đó nên bảo quản lạnh.",
    "Bạn cần bảo quản bánh khi đi xa? Shop sẽ hướng dẫn đóng gói kỹ!",
    "Bánh kem nên để ngăn mát, tránh ánh nắng trực tiếp.",
    "Shop có thể gửi hướng dẫn bảo quản chi tiết qua Zalo nếu bạn cần!",
    "Bạn muốn biết hạn sử dụng từng loại bánh không? Shop sẽ kiểm tra!"
]

ASK_RETURN_TEMPLATES = [
    "Shop hỗ trợ đổi trả nếu bánh có lỗi từ phía shop. Bạn vui lòng gửi hình ảnh và thông tin đơn hàng nhé!",
    "Bạn gặp vấn đề gì với sản phẩm? Shop sẽ hỗ trợ đổi trả nhanh nhất có thể.",
    "Bạn muốn đổi trả trong bao lâu sau khi nhận bánh? Shop sẽ kiểm tra chính sách cho bạn!",
    "Shop cam kết hoàn tiền nếu sản phẩm không đúng cam kết!",
    "Bạn cần hỗ trợ đổi trả, vui lòng liên hệ hotline hoặc inbox fanpage nhé!",
    "Shop có chính sách đổi trả rõ ràng, bạn muốn biết chi tiết không?",
    "Bạn muốn đổi bánh vì lý do gì? Shop sẽ hỗ trợ tận tình!",
    "Shop sẽ ưu tiên xử lý đổi trả cho khách hàng thân thiết!",
    "Bạn cần đổi trả gấp, shop sẽ hỗ trợ nhanh nhất có thể!",
    "Bạn muốn biết quy trình đổi trả? Shop sẽ gửi hướng dẫn chi tiết!"
]

ASK_SPECIAL_EVENT_TEMPLATES = [
    "Bạn cần bánh cho dịp đặc biệt nào? Shop có nhiều mẫu bánh cho các sự kiện khác nhau!",
    "Bạn nói rõ dịp lễ/sự kiện để shop tư vấn mẫu bánh phù hợp nhé!",
    "Shop có bánh cho sinh nhật, cưới hỏi, thôi nôi, bạn cần dịp nào?",
    "Bạn muốn đặt bánh cho sự kiện công ty, gia đình hay cá nhân?",
    "Shop có thể trang trí bánh theo chủ đề sự kiện bạn muốn!",
    "Bạn cần bánh cho ngày lễ nào? Shop sẽ gợi ý mẫu phù hợp!",
    "Shop có nhiều mẫu bánh cho các dịp lễ lớn, bạn muốn xem hình không?",
    "Bạn muốn đặt bánh cho dịp gì? Shop sẽ tư vấn mẫu độc đáo!",
    "Bánh cho sự kiện có thể in logo, hình ảnh, bạn muốn thử không?",
    "Shop có ưu đãi cho đơn đặt bánh sự kiện lớn, bạn muốn biết chi tiết không?"
]

ASK_LOYALTY_TEMPLATES = [
    "Shop có chương trình tích điểm cho khách hàng thân thiết, bạn đã đăng ký thành viên chưa?",
    "Bạn muốn biết quyền lợi thẻ thành viên? Shop sẽ gửi thông tin chi tiết nhé!",
    "Bạn có thể kiểm tra điểm tích lũy qua số điện thoại đăng ký!",
    "Shop có ưu đãi riêng cho khách hàng thân thiết mỗi tháng!",
    "Bạn muốn biết cách đổi điểm lấy quà tặng không?",
    "Khách hàng thân thiết sẽ được ưu đãi giảm giá, tặng quà sinh nhật!",
    "Bạn muốn đăng ký thành viên? Shop sẽ hướng dẫn ngay!",
    "Shop có chương trình tích điểm đổi bánh miễn phí, bạn muốn tham gia không?",
    "Bạn cần kiểm tra điểm thưởng hiện tại? Shop sẽ hỗ trợ ngay!",
    "Shop có ưu đãi đặc biệt cho khách hàng VIP, bạn muốn biết thêm không?"
]

ASK_INVOICE_TEMPLATES = [
    "Shop có hỗ trợ xuất hóa đơn VAT cho doanh nghiệp, bạn cần xuất hóa đơn cho đơn hàng nào?",
    "Bạn vui lòng cung cấp thông tin công ty để shop xuất hóa đơn nhé!",
    "Bạn muốn xuất hóa đơn điện tử hay giấy? Shop sẽ hỗ trợ theo yêu cầu!",
    "Shop sẽ gửi hóa đơn qua email hoặc giao tận nơi cho bạn!",
    "Bạn cần xuất hóa đơn cho đơn hàng cá nhân hay công ty?",
    "Shop có thể xuất hóa đơn đỏ cho mọi đơn hàng, bạn cần hỗ trợ gì thêm?",
    "Bạn muốn nhận hóa đơn qua email hay nhận trực tiếp?",
    "Shop sẽ hỗ trợ xuất hóa đơn nhanh nhất có thể!",
    "Bạn cần xuất hóa đơn cho nhiều đơn hàng cùng lúc không?",
    "Shop có thể gửi bản scan hóa đơn qua Zalo nếu bạn cần!"
]

ASK_PURCHASE_HISTORY_TEMPLATES = [
    "Bạn cần tra cứu lịch sử mua hàng, vui lòng cung cấp số điện thoại đã đặt bánh nhé!",
    "Shop sẽ kiểm tra đơn cũ cho bạn, bạn cho mình xin thông tin đặt hàng nhé!",
    "Bạn muốn biết các đơn hàng đã mua trong tháng này hay trước đó?",
    "Shop có thể gửi danh sách đơn hàng qua email hoặc Zalo cho bạn!",
    "Bạn cần hỗ trợ về đơn hàng nào cụ thể không?",
    "Shop sẽ ưu tiên kiểm tra lịch sử mua hàng cho bạn!",
    "Bạn muốn biết tổng số đơn đã mua trong năm nay không?",
    "Shop có thể gửi chi tiết từng đơn hàng nếu bạn cần!",
    "Bạn muốn biết đơn hàng nào được tặng ưu đãi không?",
    "Shop sẽ hỗ trợ kiểm tra lịch sử mua hàng nhanh nhất!"
]
