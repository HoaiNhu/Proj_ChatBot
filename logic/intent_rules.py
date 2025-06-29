# Chứa luật nhận diện intent và mapping intent sang response
INTENT_RULES = [
    {"keywords": ["xin chào", "chào", "hello", "hi", "shop ơi", "có ai không"], "intent": "greeting"},
    {"keywords": ["cảm ơn", "thanks", "thank you", "cảm ơn shop", "cảm ơn bạn"], "intent": "thank_you"},
    {"keywords": ["tạm biệt", "bye", "hẹn gặp lại", "bye bye"], "intent": "goodbye"},
    {"keywords": ["bánh", "gợi ý", "vị", "ngon", "thử"], "intent": "suggest_cake"},
    {"keywords": ["giá", "bao nhiêu", "tiền", "giá bao nhiêu", "bao nhiêu tiền", "bao nhiêu đ", "bao nhiêu vnd", "giá cả", "chi phí"], "intent": "ask_price"},
    {"keywords": ["nhân viên", "kết nối", "liên hệ", "tư vấn viên"], "intent": "connect_staff"},
    {"keywords": ["khuyến mãi", "ưu đãi", "giảm giá", "deal", "sale", "promo"], "intent": "ask_promotion"},
    {"keywords": ["đơn hàng", "kiểm tra đơn", "tình trạng đơn", "đơn của tôi", "order"], "intent": "check_order"},
    {"keywords": ["đặt bánh", "theo yêu cầu", "custom", "cá nhân hóa", "làm theo ý"], "intent": "custom_cake"},
    {"keywords": ["giờ mở cửa", "giờ đóng cửa", "làm việc lúc nào", "mấy giờ mở", "mở cửa", "đóng cửa"], "intent": "ask_opening_hours"},
    {"keywords": ["địa chỉ", "ở đâu", "cửa hàng ở đâu", "vị trí", "chỗ nào"], "intent": "ask_address"},
    {"keywords": ["thanh toán", "phương thức thanh toán", "trả tiền", "chuyển khoản", "payment"], "intent": "ask_payment"},
    {"keywords": ["giao hàng", "ship", "vận chuyển", "phí ship", "delivery", "giao"], "intent": "ask_delivery"},
    {"keywords": ["feedback", "đánh giá", "nhận xét", "phản hồi", "review"], "intent": "ask_feedback"},
    {"keywords": ["combo", "gói", "set bánh", "combo bánh", "bộ"], "intent": "ask_combo"},
    {"keywords": ["thành phần", "nguyên liệu", "bánh làm từ gì", "chất liệu", "ingredient", "làm từ gì"], "intent": "ask_ingredient"},
    {"keywords": ["dịp đặc biệt", "ngày lễ", "bánh cho dịp", "bánh sự kiện"], "intent": "ask_special_event"},
    {"keywords": ["bảo quản", "giữ lạnh", "để được bao lâu", "hạn sử dụng", "shelf life"], "intent": "ask_preservation"},
    {"keywords": ["đổi trả", "bảo hành", "trả hàng", "đổi hàng", "warranty"], "intent": "ask_return"},
    {"keywords": ["liên hệ", "số điện thoại", "hotline", "zalo", "phone", "call"], "intent": "ask_contact"},
    {"keywords": ["số lượng tối thiểu", "mua tối thiểu", "ít nhất bao nhiêu", "đặt tối thiểu"], "intent": "ask_minimum_order"},
    {"keywords": ["xuất hóa đơn", "hóa đơn đỏ", "vat", "invoice"], "intent": "ask_invoice"},
    {"keywords": ["khách hàng thân thiết", "tích điểm", "thẻ thành viên", "chương trình khách hàng"], "intent": "ask_loyalty"},
    {"keywords": ["lịch sử mua hàng", "đã mua gì", "mua trước đây", "đơn cũ"], "intent": "ask_purchase_history"},
    {"keywords": ["dinh dưỡng", "tư vấn dinh dưỡng", "calo", "chất béo", "nutrition"], "intent": "ask_nutrition"},
    {"keywords": ["bánh cho trẻ em", "bánh cho bé", "bánh cho con nít", "bánh cho trẻ nhỏ"], "intent": "ask_for_kids"},
    {"keywords": ["bánh ăn kiêng", "bánh ít đường", "bánh giảm cân", "bánh healthy"], "intent": "ask_diet_cake"},
    {"keywords": ["bánh chay", "bánh không trứng", "bánh không sữa", "bánh vegan"], "intent": "ask_vegan_cake"},
    {"keywords": ["bánh mới", "bánh vừa ra", "bánh hot", "bánh mới nhất"], "intent": "ask_new_cake"},
    {"keywords": ["bánh best seller", "bánh bán chạy", "bánh nổi bật", "bánh được yêu thích"], "intent": "ask_best_seller"},
    {"keywords": ["bánh theo mùa", "bánh mùa hè", "bánh mùa đông", "bánh mùa thu", "bánh mùa xuân"], "intent": "ask_seasonal_cake"},
    {"keywords": ["bánh cho dịp lễ", "bánh lễ tết", "bánh sự kiện", "bánh ngày lễ"], "intent": "ask_festival_cake"},
    {"keywords": ["bánh mini", "bánh nhỏ", "bánh cá nhân", "bánh size nhỏ"], "intent": "ask_mini_cake"},
    {"keywords": ["bánh ship xa", "giao tỉnh", "giao xa", "bánh gửi đi xa"], "intent": "ask_long_distance_delivery"},
    {"keywords": ["bánh trang trí", "bánh đẹp", "bánh decor", "bánh nghệ thuật"], "intent": "ask_decor_cake"},
    {"keywords": ["bánh in hình", "bánh in ảnh", "bánh in chữ", "bánh in logo"], "intent": "ask_printed_cake"},
    {"keywords": ["bánh màu sắc", "bánh nhiều màu", "bánh theo màu", "bánh phối màu"], "intent": "ask_color_cake"},
    {"keywords": ["bánh không đường", "bánh sugar free", "bánh cho người tiểu đường", "bánh ăn kiêng đường"], "intent": "ask_sugar_free_cake"},
    {"keywords": ["bánh ít béo", "bánh low fat", "bánh giảm béo", "bánh healthy"], "intent": "ask_low_fat_cake"},
    {"keywords": ["bánh không gluten", "bánh gluten free", "bánh cho người dị ứng gluten", "bánh không bột mì"], "intent": "ask_gluten_free_cake"},
    {"keywords": ["bánh cho người tiểu đường", "bánh sugar free", "bánh không đường", "bánh dành cho tiểu đường"], "intent": "ask_diabetes_cake"},
    {"keywords": ["bánh cho người lớn tuổi", "bánh cho ông bà", "bánh cho người già", "bánh cho người cao tuổi"], "intent": "ask_elderly_cake"},
    {"keywords": ["bánh cho người nước ngoài", "bánh tây", "bánh kiểu âu", "bánh ngoại quốc"], "intent": "ask_foreigner_cake"},
    {"keywords": ["bánh cho tiệc công ty", "bánh cho sự kiện", "bánh cho hội nghị", "bánh cho party"], "intent": "ask_company_party_cake"},
    {"keywords": ["bánh sinh nhật", "bánh birthday", "bánh mừng tuổi mới", "bánh happy birthday"], "intent": "ask_birthday_cake"},
    {"keywords": ["bánh cưới", "bánh wedding", "bánh đám cưới", "bánh tiệc cưới"], "intent": "ask_wedding_cake"},
    {"keywords": ["bánh thôi nôi", "bánh đầy tháng", "bánh mừng thôi nôi", "bánh tiệc thôi nôi"], "intent": "ask_baby_cake"},
    {"keywords": ["bánh baby shower", "bánh cho baby shower", "bánh tiệc baby shower", "bánh mừng baby shower"], "intent": "ask_baby_shower_cake"},
    {"keywords": ["bánh valentine", "bánh cho valentine", "bánh tình yêu", "bánh ngày lễ tình nhân"], "intent": "ask_valentine_cake"},
    {"keywords": ["bánh tết", "bánh cho tết", "bánh ngày tết", "bánh tết nguyên đán"], "intent": "ask_tet_cake"},
    {"keywords": ["bánh trung thu", "bánh cho trung thu", "bánh ngày trung thu", "bánh trung thu đặc biệt"], "intent": "ask_mid_autumn_cake"},
    {"keywords": ["bánh giáng sinh", "bánh noel", "bánh christmas", "bánh ngày giáng sinh"], "intent": "ask_christmas_cake"},
    {"keywords": ["bánh halloween", "bánh cho halloween", "bánh ngày halloween", "bánh halloween đặc biệt"], "intent": "ask_halloween_cake"},
    {"keywords": ["bánh 8/3", "bánh quốc tế phụ nữ", "bánh ngày 8/3", "bánh mùng 8 tháng 3"], "intent": "ask_womens_day_cake"},
    {"keywords": ["bánh 20/10", "bánh phụ nữ việt nam", "bánh ngày 20/10", "bánh mùng 20 tháng 10"], "intent": "ask_vietnamese_womens_day_cake"},
    {"keywords": ["bánh ngày của mẹ", "bánh mother's day", "bánh cho mẹ", "bánh mừng mẹ"], "intent": "ask_mothers_day_cake"},
    {"keywords": ["bánh ngày của cha", "bánh father's day", "bánh cho cha", "bánh mừng cha"], "intent": "ask_fathers_day_cake"},
    {"keywords": ["bánh ngày nhà giáo", "bánh 20/11", "bánh cho thầy cô", "bánh mừng thầy cô"], "intent": "ask_teachers_day_cake"},
    {"keywords": ["bánh quốc tế thiếu nhi", "bánh 1/6", "bánh cho trẻ em", "bánh thiếu nhi"], "intent": "ask_childrens_day_cake"},
    {"keywords": ["bánh quốc tế đàn ông", "bánh men's day", "bánh cho nam", "bánh mừng đàn ông"], "intent": "ask_mens_day_cake"},
    {"keywords": ["bánh quốc tế hạnh phúc", "bánh ngày hạnh phúc", "bánh mừng hạnh phúc", "bánh 20/3"], "intent": "ask_happiness_day_cake"},
    {"keywords": ["bánh quốc tế gia đình", "bánh ngày gia đình", "bánh mừng gia đình", "bánh 28/6"], "intent": "ask_family_day_cake"},
    {"keywords": ["bánh quốc tế bạn bè", "bánh ngày bạn bè", "bánh mừng bạn bè", "bánh 30/7"], "intent": "ask_friends_day_cake"},
    {"keywords": ["bánh quốc tế tình yêu", "bánh ngày tình yêu", "bánh mừng tình yêu", "bánh 14/2"], "intent": "ask_love_day_cake"},
    {"keywords": ["bánh quốc tế hòa bình", "bánh ngày hòa bình", "bánh mừng hòa bình", "bánh 21/9"], "intent": "ask_peace_day_cake"},
    {"keywords": ["bánh quốc tế lao động", "bánh 1/5", "bánh ngày lao động", "bánh mừng lao động"], "intent": "ask_labour_day_cake"},
    {"keywords": ["ăn kiêng", "ít đường", "giảm cân"], "intent": "ask_diet_cake"},
    {"keywords": ["bánh chay", "vegan", "không trứng", "không sữa"], "intent": "ask_vegan_cake"},
    {"keywords": ["bánh mini", "bánh nhỏ", "mini cake"], "intent": "ask_mini_cake"},
    {"keywords": ["halloween", "bánh halloween"], "intent": "ask_halloween_cake"},
    {"keywords": ["bánh màu", "bánh xanh", "bánh đỏ", "bánh vàng"], "intent": "ask_color_cake"},
    {"keywords": ["bánh sinh nhật"], "intent": "ask_birthday_cake"},
    {"keywords": ["bánh cưới"], "intent": "ask_wedding_cake"},
    {"keywords": ["bánh thôi nôi"], "intent": "ask_baby_cake"},
    {"keywords": ["giáng sinh"], "intent": "ask_christmas_cake"},
    {"keywords": ["bánh tết"], "intent": "ask_tet_cake"},
    {"keywords": ["bánh cho người lớn tuổi", "bánh cho ông bà", "bánh cho người già", "bánh cho người cao tuổi"], "intent": "ask_elderly_cake"},
    {"keywords": ["bánh cho tiệc công ty", "bánh cho sự kiện", "bánh cho hội nghị", "bánh cho party"], "intent": "ask_company_party_cake"},
    {"keywords": ["bánh baby shower", "bánh cho baby shower", "bánh tiệc baby shower", "bánh mừng baby shower"], "intent": "ask_baby_shower_cake"},
    {"keywords": ["bánh valentine", "bánh cho valentine", "bánh tình yêu", "bánh ngày lễ tình nhân"], "intent": "ask_valentine_cake"},
    {"keywords": ["bánh trung thu", "bánh cho trung thu", "bánh ngày trung thu", "bánh trung thu đặc biệt"], "intent": "ask_mid_autumn_cake"},
    {"keywords": ["bánh 8/3", "bánh quốc tế phụ nữ", "bánh ngày 8/3", "bánh mùng 8 tháng 3"], "intent": "ask_womens_day_cake"},
    {"keywords": ["bánh 20/10", "bánh phụ nữ việt nam", "bánh ngày 20/10", "bánh mùng 20 tháng 10"], "intent": "ask_vietnamese_womens_day_cake"},
    {"keywords": ["bánh ngày của mẹ", "bánh mother's day", "bánh cho mẹ", "bánh mừng mẹ"], "intent": "ask_mothers_day_cake"},
    {"keywords": ["bánh ngày của cha", "bánh father's day", "bánh cho cha", "bánh mừng cha"], "intent": "ask_fathers_day_cake"},
    {"keywords": ["bánh ngày nhà giáo", "bánh 20/11", "bánh cho thầy cô", "bánh mừng thầy cô"], "intent": "ask_teachers_day_cake"},
    {"keywords": ["bánh quốc tế thiếu nhi", "bánh 1/6", "bánh cho trẻ em", "bánh thiếu nhi"], "intent": "ask_childrens_day_cake"},
    {"keywords": ["bánh quốc tế đàn ông", "bánh men's day", "bánh cho nam", "bánh mừng đàn ông"], "intent": "ask_mens_day_cake"},
    {"keywords": ["bánh quốc tế hạnh phúc", "bánh ngày hạnh phúc", "bánh mừng hạnh phúc", "bánh 20/3"], "intent": "ask_happiness_day_cake"},
    {"keywords": ["bánh quốc tế gia đình", "bánh ngày gia đình", "bánh mừng gia đình", "bánh 28/6"], "intent": "ask_family_day_cake"},
    {"keywords": ["bánh quốc tế bạn bè", "bánh ngày bạn bè", "bánh mừng bạn bè", "bánh 30/7"], "intent": "ask_friends_day_cake"},
    {"keywords": ["bánh quốc tế tình yêu", "bánh ngày tình yêu", "bánh mừng tình yêu", "bánh 14/2"], "intent": "ask_love_day_cake"},
    {"keywords": ["bánh quốc tế hòa bình", "bánh ngày hòa bình", "bánh mừng hòa bình", "bánh 21/9"], "intent": "ask_peace_day_cake"},
    {"keywords": ["bánh quốc tế lao động", "bánh 1/5", "bánh ngày lao động", "bánh mừng lao động"], "intent": "ask_labour_day_cake"}
]

INTENT_RESPONSES = {
    "greeting": [
        "Xin chào bạn! Shop có thể giúp gì cho bạn?",
        "Chào bạn, bạn muốn tìm loại bánh nào hôm nay?",
        "Shop xin chào! Bạn cần tư vấn về bánh không ạ?",
        "Rất vui được gặp bạn, bạn muốn đặt bánh gì?",
        "Chào mừng bạn đến với Avocado Cake!"
    ],
    "thank_you": [
        "Cảm ơn bạn đã tin tưởng và ủng hộ shop!",
        "Shop rất vui khi được phục vụ bạn!",
        "Cảm ơn bạn, chúc bạn một ngày tốt lành!",
        "Cảm ơn bạn đã liên hệ với shop!",
        "Shop luôn sẵn sàng hỗ trợ bạn bất cứ lúc nào!"
    ],
    "goodbye": [
        "Tạm biệt bạn, hẹn gặp lại lần sau!",
        "Chúc bạn một ngày vui vẻ và nhiều năng lượng!",
        "Shop mong sớm gặp lại bạn!",
        "Cảm ơn bạn, chúc bạn luôn hạnh phúc!",
        "Nếu cần hỗ trợ gì thêm, bạn cứ nhắn cho shop nhé!"
    ],
    "suggest_cake": [
        "Shop có nhiều loại bánh ngon như Red Velvet, Tiramisu, Mousse, bạn muốn thử loại nào?",
        "Bạn thích vị socola, trà xanh hay phô mai? Shop sẽ gợi ý bánh phù hợp!",
        "Bạn muốn bánh kem, bánh bông lan hay bánh mousse?",
        "Shop có bánh sinh nhật, bánh tiệc, bánh mini, bạn cần loại nào?",
        "Bạn muốn shop gợi ý bánh theo dịp hay theo sở thích?"
    ],
    "ask_price": [
        "Bánh của shop có giá từ 200.000đ đến 2.000.000đ tuỳ loại và kích cỡ.",
        "Bạn muốn hỏi giá loại bánh nào để shop báo chi tiết nhé!",
        "Shop có nhiều mức giá, bạn cần bánh cho bao nhiêu người?",
        "Bạn vui lòng cho shop biết tên bánh để báo giá chính xác!",
        "Bạn muốn tham khảo bảng giá bánh sinh nhật, bánh tiệc hay bánh mini?"
    ],
    "connect_staff": [
        "Shop sẽ kết nối bạn với nhân viên tư vấn ngay!",
        "Bạn vui lòng chờ một chút, nhân viên sẽ hỗ trợ bạn ngay lập tức!",
        "Shop đã chuyển thông tin của bạn cho nhân viên, bạn đợi chút nhé!",
        "Bạn cần hỗ trợ gì thêm, nhân viên sẽ liên hệ ngay!",
        "Nhân viên tư vấn sẽ gọi lại cho bạn trong ít phút nữa!"
    ],
    "ask_promotion": [
        "Hiện tại shop có nhiều chương trình khuyến mãi hấp dẫn, bạn muốn biết về ưu đãi nào?",
        "Bạn quan tâm đến chương trình giảm giá nào? Shop gửi thông tin chi tiết nhé!",
        "Shop đang có ưu đãi cho khách hàng mới, bạn muốn nhận mã giảm giá không?",
        "Bạn muốn biết về combo tiết kiệm hay giảm giá theo dịp lễ?",
        "Shop thường xuyên có khuyến mãi, bạn theo dõi fanpage để cập nhật nhé!"
    ],
    "check_order": [
        "Bạn vui lòng cung cấp mã đơn hàng để shop kiểm tra giúp nhé!",
        "Shop sẽ kiểm tra tình trạng đơn hàng cho bạn ngay, bạn cho mình xin thông tin đơn nhé!",
        "Bạn đặt hàng qua kênh nào để shop tra cứu nhanh hơn?",
        "Bạn cần kiểm tra đơn hàng nào, vui lòng gửi mã hoặc số điện thoại đặt hàng!",
        "Shop sẽ báo lại tình trạng đơn hàng trong ít phút nữa!"
    ],
    "custom_cake": [
        "Bạn muốn đặt bánh theo yêu cầu như thế nào? Mô tả chi tiết giúp shop nhé!",
        "Shop nhận làm bánh custom, bạn gửi ý tưởng hoặc hình mẫu cho mình nhé!",
        "Bạn muốn bánh trang trí theo chủ đề gì? Shop sẽ tư vấn mẫu phù hợp!",
        "Bạn cần bánh kích thước, màu sắc, vị gì? Shop sẽ làm theo ý bạn!",
        "Bạn gửi hình mẫu hoặc mô tả chi tiết để shop báo giá nhé!"
    ],
    "ask_opening_hours": [
        "Shop mở cửa từ 7h sáng đến 9h tối mỗi ngày.",
        "Giờ làm việc của shop là 7:00 - 21:00 tất cả các ngày trong tuần.",
        "Bạn muốn đến shop vào khung giờ nào để shop phục vụ tốt nhất?",
        "Shop luôn sẵn sàng phục vụ bạn từ sáng đến tối!",
        "Bạn cần đặt bánh ngoài giờ, shop vẫn hỗ trợ giao tận nơi nhé!"
    ],
    "ask_address": [
        "Địa chỉ shop: 123 Đường Bánh Ngon, Quận 1, TP.HCM.",
        "Bạn muốn tìm cửa hàng gần nhất ở khu vực nào ạ?",
        "Shop có nhiều chi nhánh, bạn cần địa chỉ ở quận nào?",
        "Bạn cần chỉ đường đến shop không? Shop gửi bản đồ nhé!",
        "Bạn muốn nhận bánh tại shop hay giao tận nơi?"
    ],
    "ask_payment": [
        "Shop hỗ trợ thanh toán tiền mặt, chuyển khoản và ví điện tử.",
        "Bạn muốn thanh toán bằng phương thức nào? Shop có Momo, ZaloPay, VNPay nhé!",
        "Bạn cần xuất hoá đơn VAT, shop sẽ hỗ trợ khi thanh toán.",
        "Bạn muốn thanh toán trước hay khi nhận bánh?",
        "Shop có hỗ trợ trả góp cho đơn hàng lớn, bạn muốn tìm hiểu không?"
    ],
    "ask_delivery": [
        "Shop có giao hàng tận nơi toàn quốc, phí ship tuỳ khu vực bạn nhé!",
        "Bạn cần giao bánh đến đâu? Shop sẽ báo phí ship và thời gian giao dự kiến.",
        "Shop hỗ trợ giao nhanh trong nội thành, bạn cần nhận bánh trong bao lâu?",
        "Bạn muốn nhận bánh trong ngày hay đặt trước?",
        "Shop có đối tác giao hàng uy tín, đảm bảo bánh đến tay bạn an toàn!"
    ],
    "ask_feedback": [
        "Bạn có góp ý gì cho shop không? Shop rất mong nhận được phản hồi từ bạn!",
        "Cảm ơn bạn đã sử dụng dịch vụ, bạn có thể đánh giá trải nghiệm để shop phục vụ tốt hơn nhé!",
        "Bạn muốn gửi feedback về sản phẩm hay dịch vụ? Shop luôn lắng nghe!",
        "Shop rất trân trọng mọi ý kiến đóng góp của bạn!",
        "Bạn có thể để lại nhận xét trên fanpage hoặc Google Review giúp shop nhé!"
    ],
    "ask_combo": [
        "Shop có nhiều combo bánh tiết kiệm, bạn muốn tham khảo combo nào?",
        "Bạn cần combo cho bao nhiêu người? Shop sẽ gợi ý phù hợp nhé!",
        "Bạn muốn combo bánh sinh nhật, tiệc hay quà tặng?",
        "Shop có combo theo mùa, bạn muốn thử combo nào?",
        "Bạn muốn biết giá combo hay thành phần combo?"
    ],
    "ask_ingredient": [
        "Bạn muốn biết thành phần của loại bánh nào ạ? Shop luôn dùng nguyên liệu tươi mới!",
        "Bánh của shop làm từ nguyên liệu tự nhiên, không chất bảo quản. Bạn hỏi về loại bánh nào cụ thể nhé!",
        "Bạn quan tâm đến thành phần nào trong bánh?",
        "Shop có thể gửi bảng thành phần chi tiết nếu bạn cần!",
        "Bạn muốn biết bánh có chứa trứng, sữa, gluten hay không? Shop sẽ kiểm tra giúp bạn!"
    ],
    "ask_special_event": [
        "Bạn cần bánh cho dịp đặc biệt nào? Shop có nhiều mẫu bánh cho các sự kiện khác nhau!",
        "Bạn nói rõ dịp lễ/sự kiện để shop tư vấn mẫu bánh phù hợp nhé!",
        "Shop có bánh cho sinh nhật, cưới hỏi, thôi nôi, bạn cần dịp nào?",
        "Bạn muốn đặt bánh cho sự kiện công ty, gia đình hay cá nhân?",
        "Shop có thể trang trí bánh theo chủ đề sự kiện bạn muốn!"
    ],
    "ask_preservation": [
        "Bánh nên được bảo quản trong ngăn mát tủ lạnh và dùng trong 2-3 ngày.",
        "Bạn cần hướng dẫn bảo quản loại bánh nào? Shop sẽ tư vấn chi tiết nhé!",
        "Shop có hướng dẫn bảo quản riêng cho từng loại bánh, bạn hỏi loại nào?",
        "Bạn muốn biết cách bảo quản khi vận chuyển xa không?",
        "Shop khuyên dùng bánh trong ngày để đảm bảo vị ngon nhất!"
    ],
    "ask_return": [
        "Shop hỗ trợ đổi trả nếu bánh có lỗi từ phía shop. Bạn vui lòng gửi hình ảnh và thông tin đơn hàng nhé!",
        "Bạn gặp vấn đề gì với sản phẩm? Shop sẽ hỗ trợ đổi trả nhanh nhất có thể.",
        "Bạn muốn đổi trả trong bao lâu sau khi nhận bánh? Shop sẽ kiểm tra chính sách cho bạn!",
        "Shop cam kết hoàn tiền nếu sản phẩm không đúng cam kết!",
        "Bạn cần hỗ trợ đổi trả, vui lòng liên hệ hotline hoặc inbox fanpage nhé!"
    ],
    "ask_contact": [
        "Bạn có thể liên hệ shop qua số hotline 0123 456 789 hoặc Zalo cùng số nhé!",
        "Mọi thắc mắc bạn gọi trực tiếp 0123 456 789 hoặc inbox fanpage giúp shop nhé!",
        "Shop luôn sẵn sàng hỗ trợ bạn qua điện thoại, Zalo, Facebook!",
        "Bạn muốn nhận tư vấn qua kênh nào? Shop sẽ liên hệ lại ngay!",
        "Bạn có thể gửi email cho shop qua info@avocadocake.vn nếu cần hỗ trợ chi tiết!"
    ],
    "ask_invoice": [
        "Shop có hỗ trợ xuất hóa đơn VAT cho doanh nghiệp, bạn cần xuất hóa đơn cho đơn hàng nào?",
        "Bạn vui lòng cung cấp thông tin công ty để shop xuất hóa đơn nhé!",
        "Bạn muốn xuất hóa đơn điện tử hay giấy? Shop sẽ hỗ trợ theo yêu cầu!",
        "Shop sẽ gửi hóa đơn qua email hoặc giao tận nơi cho bạn!",
        "Bạn cần xuất hóa đơn cho đơn hàng cá nhân hay công ty?"
    ],
    "ask_loyalty": [
        "Shop có chương trình tích điểm cho khách hàng thân thiết, bạn đã đăng ký thành viên chưa?",
        "Bạn muốn biết quyền lợi thẻ thành viên? Shop sẽ gửi thông tin chi tiết nhé!",
        "Bạn có thể kiểm tra điểm tích lũy qua số điện thoại đăng ký!",
        "Shop có ưu đãi riêng cho khách hàng thân thiết mỗi tháng!",
        "Bạn muốn biết cách đổi điểm lấy quà tặng không?"
    ],
    "ask_purchase_history": [
        "Bạn cần tra cứu lịch sử mua hàng, vui lòng cung cấp số điện thoại đã đặt bánh nhé!",
        "Shop sẽ kiểm tra đơn cũ cho bạn, bạn cho mình xin thông tin đặt hàng nhé!",
        "Bạn muốn biết các đơn hàng đã mua trong tháng này hay trước đó?",
        "Shop có thể gửi danh sách đơn hàng qua email hoặc Zalo cho bạn!",
        "Bạn cần hỗ trợ về đơn hàng nào cụ thể không?"
    ],
    "ask_nutrition": [
        "Bạn quan tâm đến thành phần dinh dưỡng của loại bánh nào? Shop sẽ gửi thông tin chi tiết nhé!",
        "Bạn cần tư vấn về calo, chất béo hay thành phần nào? Shop luôn sẵn sàng hỗ trợ!",
        "Shop có bảng dinh dưỡng cho từng loại bánh, bạn hỏi loại nào nhé!",
        "Bạn muốn biết bánh có phù hợp cho người ăn kiêng không?",
        "Bạn cần tư vấn về bánh cho trẻ em, người lớn tuổi hay người tiểu đường?"
    ],
    "ask_for_kids": [
        "Shop có nhiều loại bánh phù hợp cho trẻ em, bạn muốn bánh vị gì cho bé?",
        "Bạn cần bánh cho bé dịp gì? Shop sẽ gợi ý mẫu phù hợp nhé!",
        "Bạn muốn bánh ít ngọt, nhiều màu sắc hay hình thú cho bé?",
        "Shop có bánh sinh nhật, bánh mini cho bé, bạn muốn tham khảo không?",
        "Bạn cần tư vấn về thành phần an toàn cho trẻ nhỏ không?"
    ],
    "ask_diet_cake": [
        "Shop có bánh ăn kiêng, ít đường, ít béo, bạn muốn thử loại nào?",
        "Bạn quan tâm bánh healthy vị gì? Shop sẽ tư vấn loại phù hợp nhé!"
    ],
    "ask_vegan_cake": [
        "Shop có bánh chay, không trứng, không sữa, bạn muốn đặt loại nào?",
        "Bạn cần bánh vegan cho dịp nào? Shop sẽ gợi ý mẫu phù hợp nhé!"
    ],
    "ask_new_cake": [
        "Shop vừa ra mắt nhiều loại bánh mới, bạn muốn thử loại nào?",
        "Bạn muốn xem danh sách bánh mới nhất không? Shop gửi menu nhé!"
    ],
    "ask_best_seller": [
        "Bánh bán chạy nhất hiện nay là Red Velvet và Tiramisu, bạn muốn thử không?",
        "Bạn muốn biết top 3 bánh được yêu thích nhất không? Shop gửi thông tin nhé!"
    ],
    "ask_seasonal_cake": [
        "Shop có nhiều loại bánh theo mùa, bạn quan tâm mùa nào?",
        "Bạn muốn thử bánh đặc trưng mùa hè, mùa đông hay mùa nào?"
    ],
    "ask_festival_cake": [
        "Bạn cần bánh cho dịp lễ nào? Shop có nhiều mẫu cho các sự kiện đặc biệt!",
        "Bạn nói rõ dịp lễ để shop tư vấn mẫu bánh phù hợp nhé!"
    ],
    "ask_mini_cake": [
        "Shop có bánh mini, nhỏ xinh, phù hợp làm quà tặng hoặc tiệc nhỏ.",
        "Bạn muốn đặt bánh mini vị gì? Shop sẽ gửi mẫu cho bạn tham khảo nhé!"
    ],
    "ask_long_distance_delivery": [
        "Shop hỗ trợ giao bánh đi tỉnh xa, bạn cần gửi bánh đến đâu?",
        "Bạn muốn biết phí ship đi xa? Shop sẽ báo giá và thời gian giao dự kiến nhé!"
    ],
    "ask_decor_cake": [
        "Shop nhận trang trí bánh theo yêu cầu, bạn muốn decor kiểu gì?",
        "Bạn gửi ý tưởng hoặc hình mẫu trang trí cho shop nhé!"
    ],
    "ask_printed_cake": [
        "Shop có bánh in hình, in chữ, in logo theo yêu cầu, bạn muốn in gì lên bánh?",
        "Bạn gửi file hình hoặc nội dung muốn in lên bánh cho shop nhé!"
    ],
    "ask_color_cake": [
        "Bạn thích bánh màu gì? Shop có thể phối màu theo ý bạn!",
        "Bạn muốn bánh phối nhiều màu hay một màu chủ đạo? Shop sẽ tư vấn nhé!"
    ],
    "ask_sugar_free_cake": [
        "Shop có bánh không đường, phù hợp cho người ăn kiêng hoặc tiểu đường.",
        "Bạn muốn thử bánh sugar free vị gì? Shop sẽ gửi mẫu nhé!"
    ],
    "ask_low_fat_cake": [
        "Shop có bánh ít béo, tốt cho sức khỏe, bạn muốn thử loại nào?",
        "Bạn quan tâm bánh low fat vị gì? Shop sẽ tư vấn nhé!"
    ],
    "ask_gluten_free_cake": [
        "Shop có bánh không gluten, phù hợp cho người dị ứng bột mì.",
        "Bạn muốn đặt bánh gluten free loại nào? Shop sẽ gửi menu nhé!"
    ],
    "ask_diabetes_cake": [
        "Shop có bánh dành riêng cho người tiểu đường, bạn muốn thử loại nào?",
        "Bạn cần tư vấn bánh phù hợp cho người tiểu đường? Shop sẽ hỗ trợ nhé!"
    ],
    "ask_elderly_cake": [
        "Shop có bánh đặc biệt cho người lớn tuổi, ít đường và dễ ăn!",
        "Bánh cho ông bà thường ít ngọt và mềm, bạn muốn thử loại nào?",
        "Shop có bánh healthy phù hợp với người cao tuổi!",
        "Bánh cho người già thường ít béo và ít đường, bạn quan tâm không?",
        "Shop có thể làm bánh theo yêu cầu đặc biệt cho người lớn tuổi!"
    ],
    "ask_foreigner_cake": [
        "Shop có bánh kiểu Âu, bánh tây, phù hợp cho người nước ngoài.",
        "Bạn muốn đặt bánh cho khách nước ngoài dịp nào? Shop sẽ tư vấn nhé!"
    ],
    "ask_company_party_cake": [
        "Shop có nhiều mẫu bánh cho tiệc công ty, bạn cần cho bao nhiêu người?",
        "Bánh cho sự kiện công ty thường có logo hoặc chủ đề đặc biệt!",
        "Shop có combo bánh cho hội nghị với giá ưu đãi!",
        "Bánh cho party công ty có thể in logo công ty theo yêu cầu!",
        "Shop có bánh mini phù hợp cho tiệc công ty!"
    ],
    "ask_birthday_cake": [
        "Bạn cần bánh sinh nhật cho bé, người lớn hay công ty? Shop có nhiều mẫu đẹp lắm!",
        "Bạn muốn đặt bánh sinh nhật kiểu truyền thống hay hiện đại? Shop sẽ tư vấn nhé!"
    ],
    "ask_wedding_cake": [
        "Shop nhận làm bánh cưới nhiều tầng, trang trí theo yêu cầu.",
        "Bạn muốn đặt bánh cưới phong cách nào? Shop sẽ gửi mẫu cho bạn tham khảo nhé!"
    ],
    "ask_baby_cake": [
        "Bạn cần bánh thôi nôi, đầy tháng cho bé trai hay bé gái? Shop có nhiều mẫu dễ thương!",
        "Bạn muốn đặt bánh thôi nôi trang trí hình gì? Shop sẽ tư vấn nhé!"
    ],
    "ask_baby_shower_cake": [
        "Shop có bánh dễ thương cho baby shower, bạn muốn xem mẫu nào?",
        "Bánh baby shower thường có chủ đề em bé, bạn thích màu gì?",
        "Shop có thể làm bánh theo chủ đề baby shower theo yêu cầu!",
        "Bánh cho tiệc baby shower thường nhỏ nhắn và dễ thương!",
        "Shop có combo bánh mini cho baby shower!"
    ],
    "ask_valentine_cake": [
        "Shop có bánh lãng mạn cho Valentine, bạn muốn thử loại nào?",
        "Bánh Valentine thường có màu hồng đỏ và hình trái tim!",
        "Shop có bánh chocolate đặc biệt cho ngày lễ tình nhân!",
        "Bánh cho Valentine có thể in tên hoặc lời nhắn theo yêu cầu!",
        "Shop có combo bánh Valentine với giá ưu đãi!"
    ],
    "ask_tet_cake": [
        "Shop có nhiều loại bánh cho dịp Tết, bạn muốn đặt loại nào?",
        "Bạn cần bánh tặng người thân hay đối tác dịp Tết? Shop sẽ gợi ý mẫu phù hợp nhé!"
    ],
    "ask_mid_autumn_cake": [
        "Shop có bánh trung thu truyền thống và hiện đại!",
        "Bánh trung thu của shop có nhiều vị khác nhau, bạn thích vị gì?",
        "Shop có bánh trung thu đặc biệt cho dịp này!",
        "Bánh trung thu có thể làm theo yêu cầu với nhân đặc biệt!",
        "Shop có set bánh trung thu tặng quà!"
    ],
    "ask_christmas_cake": [
        "Shop có bánh giáng sinh trang trí đẹp mắt, bạn muốn đặt loại nào?",
        "Bạn cần bánh giáng sinh cho tiệc gia đình hay công ty? Shop sẽ gợi ý mẫu phù hợp nhé!"
    ],
    "ask_halloween_cake": [
        "Shop có bánh halloween trang trí độc đáo, bạn muốn thử không?",
        "Bạn cần bánh halloween cho tiệc nhỏ hay sự kiện lớn? Shop sẽ tư vấn nhé!"
    ],
    "ask_womens_day_cake": [
        "Shop có bánh đặc biệt cho ngày Quốc tế Phụ nữ 8/3!",
        "Bánh 8/3 thường có màu hồng và trang trí hoa!",
        "Shop có bánh chocolate đặc biệt cho phụ nữ!",
        "Bánh cho ngày 8/3 có thể in lời chúc theo yêu cầu!",
        "Shop có combo bánh tặng mẹ và chị em!"
    ],
    "ask_vietnamese_womens_day_cake": [
        "Shop có bánh đặc biệt cho ngày Phụ nữ Việt Nam 20/10!",
        "Bánh 20/10 thường có chủ đề Việt Nam và hoa sen!",
        "Shop có bánh truyền thống cho ngày phụ nữ Việt Nam!",
        "Bánh cho 20/10 có thể làm theo phong cách Việt Nam!",
        "Shop có combo bánh tặng phụ nữ Việt Nam!"
    ],
    "ask_mothers_day_cake": [
        "Shop có bánh đặc biệt cho ngày của Mẹ!",
        "Bánh cho mẹ thường có màu hồng và hoa hồng!",
        "Shop có bánh chocolate đặc biệt tặng mẹ!",
        "Bánh cho ngày của Mẹ có thể in lời yêu thương!",
        "Shop có combo bánh tặng mẹ với giá ưu đãi!"
    ],
    "ask_fathers_day_cake": [
        "Shop có bánh đặc biệt cho ngày của Cha!",
        "Bánh cho cha thường có màu xanh và chủ đề nam tính!",
        "Shop có bánh chocolate đặc biệt tặng cha!",
        "Bánh cho ngày của Cha có thể in lời tri ân!",
        "Shop có combo bánh tặng cha với giá ưu đãi!"
    ],
    "ask_teachers_day_cake": [
        "Shop có bánh đặc biệt cho ngày Nhà giáo Việt Nam 20/11!",
        "Bánh cho thầy cô thường có chủ đề giáo dục!",
        "Shop có bánh chocolate đặc biệt tặng thầy cô!",
        "Bánh cho 20/11 có thể in lời tri ân thầy cô!",
        "Shop có combo bánh tặng thầy cô!"
    ],
    "ask_childrens_day_cake": [
        "Shop có bánh đặc biệt cho ngày Quốc tế Thiếu nhi 1/6!",
        "Bánh cho trẻ em thường có màu sắc vui nhộn!",
        "Shop có bánh hình thú ngộ nghĩnh cho thiếu nhi!",
        "Bánh cho 1/6 có thể làm theo chủ đề hoạt hình!",
        "Shop có combo bánh mini cho trẻ em!"
    ],
    "ask_mens_day_cake": [
        "Shop có bánh đặc biệt cho ngày Quốc tế Đàn ông!",
        "Bánh cho nam giới thường có chủ đề thể thao hoặc xe hơi!",
        "Shop có bánh chocolate đặc biệt cho đàn ông!",
        "Bánh cho ngày đàn ông có thể in logo thể thao!",
        "Shop có combo bánh tặng đàn ông!"
    ],
    "ask_happiness_day_cake": [
        "Shop có bánh đặc biệt cho ngày Quốc tế Hạnh phúc 20/3!",
        "Bánh cho ngày hạnh phúc thường có màu vàng và nụ cười!",
        "Shop có bánh chocolate đặc biệt cho ngày hạnh phúc!",
        "Bánh cho 20/3 có thể in biểu tượng hạnh phúc!",
        "Shop có combo bánh chia sẻ hạnh phúc!"
    ],
    "ask_family_day_cake": [
        "Shop có bánh đặc biệt cho ngày Quốc tế Gia đình 28/6!",
        "Bánh cho gia đình thường có chủ đề sum vầy!",
        "Shop có bánh chocolate đặc biệt cho gia đình!",
        "Bánh cho ngày gia đình có thể in hình gia đình!",
        "Shop có combo bánh cho cả gia đình!"
    ],
    "ask_friends_day_cake": [
        "Shop có bánh đặc biệt cho ngày Quốc tế Bạn bè 30/7!",
        "Bánh cho bạn bè thường có chủ đề tình bạn!",
        "Shop có bánh chocolate đặc biệt tặng bạn!",
        "Bánh cho ngày bạn bè có thể in lời chúc!",
        "Shop có combo bánh chia sẻ với bạn bè!"
    ],
    "ask_love_day_cake": [
        "Shop có bánh đặc biệt cho ngày Quốc tế Tình yêu!",
        "Bánh cho ngày tình yêu thường có màu đỏ và trái tim!",
        "Shop có bánh chocolate đặc biệt cho tình yêu!",
        "Bánh cho ngày tình yêu có thể in lời yêu thương!",
        "Shop có combo bánh lãng mạn cho đôi lứa!"
    ],
    "ask_peace_day_cake": [
        "Shop có bánh đặc biệt cho ngày Quốc tế Hòa bình 21/9!",
        "Bánh cho ngày hòa bình thường có màu trắng và chim bồ câu!",
        "Shop có bánh chocolate đặc biệt cho hòa bình!",
        "Bánh cho 21/9 có thể in biểu tượng hòa bình!",
        "Shop có combo bánh chia sẻ hòa bình!"
    ],
    "ask_labour_day_cake": [
        "Shop có bánh đặc biệt cho ngày Quốc tế Lao động 1/5, bạn muốn tham khảo mẫu nào?",
        "Bánh cho ngày Lao động thường có chủ đề công việc, bạn quan tâm không?",
        "Shop có thể làm bánh theo chủ đề ngày Lao động theo yêu cầu của bạn!",
        "Bánh cho ngày 1/5 thường được trang trí đặc biệt, bạn muốn xem mẫu không?",
        "Shop có combo bánh cho ngày Lao động với giá ưu đãi!"
    ]
}