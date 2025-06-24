# Chứa luật nhận diện intent và mapping intent sang response
INTENT_RULES = [
    {"keywords": ["bánh", "gợi ý", "vị"], "intent": "suggest_cake"},
    {"keywords": ["giá", "bao nhiêu", "tiền"], "intent": "ask_price"},
    {"keywords": ["nhân viên", "kết nối", "liên hệ"], "intent": "connect_staff"},
    {"keywords": ["khuyến mãi", "ưu đãi", "giảm giá", "deal"], "intent": "ask_promotion"},
    {"keywords": ["đơn hàng", "kiểm tra đơn", "tình trạng đơn", "đơn của tôi"], "intent": "check_order"},
    {"keywords": ["đặt bánh", "theo yêu cầu", "custom", "cá nhân hóa"], "intent": "custom_cake"},
    {"keywords": ["giờ mở cửa", "giờ đóng cửa", "làm việc lúc nào", "mấy giờ mở"], "intent": "ask_opening_hours"},
    {"keywords": ["địa chỉ", "ở đâu", "cửa hàng ở đâu", "vị trí"], "intent": "ask_address"},
    {"keywords": ["thanh toán", "phương thức thanh toán", "trả tiền", "chuyển khoản"], "intent": "ask_payment"},
    {"keywords": ["giao hàng", "ship", "vận chuyển", "phí ship"], "intent": "ask_delivery"},
    {"keywords": ["feedback", "đánh giá", "nhận xét", "phản hồi"], "intent": "ask_feedback"},
    {"keywords": ["combo", "gói", "set bánh", "combo bánh"], "intent": "ask_combo"},
    {"keywords": ["thành phần", "nguyên liệu", "bánh làm từ gì", "chất liệu"], "intent": "ask_ingredient"},
    {"keywords": ["dịp đặc biệt", "ngày lễ", "bánh cho dịp", "bánh sự kiện"], "intent": "ask_special_event"},
    {"keywords": ["bảo quản", "giữ lạnh", "để được bao lâu", "hạn sử dụng"], "intent": "ask_preservation"},
    {"keywords": ["đổi trả", "bảo hành", "trả hàng", "đổi hàng"], "intent": "ask_return"},
    {"keywords": ["liên hệ", "số điện thoại", "hotline", "zalo"], "intent": "ask_contact"},
    {"keywords": ["đặt cọc", "cọc trước", "giữ bánh", "giữ chỗ"], "intent": "ask_deposit"},
    {"keywords": ["số lượng tối thiểu", "mua tối thiểu", "ít nhất bao nhiêu", "đặt tối thiểu"], "intent": "ask_minimum_order"},
    {"keywords": ["xuất hóa đơn", "hóa đơn đỏ", "vat", "invoice"], "intent": "ask_invoice"},
    {"keywords": ["khách hàng thân thiết", "tích điểm", "thẻ thành viên", "chương trình khách hàng"], "intent": "ask_loyalty"},
    {"keywords": ["lịch sử mua hàng", "đã mua gì", "mua trước đây", "đơn cũ"], "intent": "ask_purchase_history"},
    {"keywords": ["dinh dưỡng", "tư vấn dinh dưỡng", "calo", "chất béo"], "intent": "ask_nutrition"},
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
]

INTENT_RESPONSES = {
    "suggest_cake": [
        "Chúng tôi có nhiều loại bánh ngon. Bạn thích vị gì?",
        "Bạn muốn thử bánh vị nào? Socola, vani, trà xanh?"
    ],
    "ask_price": [
        "Bánh của chúng tôi có giá từ 200,000đ đến 2,000,000đ tùy loại.",
        "Bạn muốn hỏi giá loại bánh nào ạ?"
    ],
    "connect_staff": [
        "Bạn vui lòng đợi, nhân viên sẽ kết nối với bạn ngay.",
        "Chúng tôi sẽ chuyển bạn tới nhân viên hỗ trợ."
    ],
    "ask_promotion": [
        "Hiện tại shop đang có nhiều chương trình khuyến mãi hấp dẫn, bạn muốn biết về ưu đãi nào?",
        "Bạn quan tâm đến chương trình giảm giá nào? Mình gửi thông tin chi tiết nhé!"
    ],
    "check_order": [
        "Bạn vui lòng cung cấp mã đơn hàng để mình kiểm tra giúp nhé!",
        "Mình sẽ kiểm tra tình trạng đơn hàng cho bạn ngay, bạn cho mình xin thông tin đơn nhé."
    ],
    "custom_cake": [
        "Bạn muốn đặt bánh theo yêu cầu như thế nào? Mô tả chi tiết giúp shop nhé!",
        "Shop nhận làm bánh custom, bạn gửi ý tưởng hoặc hình mẫu cho mình nhé."
    ],
    "ask_opening_hours": [
        "Shop mở cửa từ 7h sáng đến 9h tối mỗi ngày.",
        "Giờ làm việc của shop là 7:00 - 21:00 tất cả các ngày trong tuần."
    ],
    "ask_address": [
        "Địa chỉ shop: 123 Đường Bánh Ngon, Quận 1, TP.HCM.",
        "Bạn muốn tìm cửa hàng gần nhất ở khu vực nào ạ?"
    ],
    "ask_payment": [
        "Shop hỗ trợ thanh toán tiền mặt, chuyển khoản và ví điện tử.",
        "Bạn muốn thanh toán bằng phương thức nào? Shop có Momo, ZaloPay, VNPay nhé!"
    ],
    "ask_delivery": [
        "Shop có giao hàng tận nơi toàn quốc, phí ship tùy khu vực bạn nhé!",
        "Bạn cần giao bánh đến đâu? Mình sẽ báo phí ship và thời gian giao dự kiến."
    ],
    "ask_feedback": [
        "Bạn có góp ý gì cho shop không? Mình rất mong nhận được phản hồi từ bạn!",
        "Cảm ơn bạn đã sử dụng dịch vụ, bạn có thể đánh giá trải nghiệm để shop phục vụ tốt hơn nhé!"
    ],
    "ask_combo": [
        "Shop có nhiều combo bánh tiết kiệm, bạn muốn tham khảo combo nào?",
        "Bạn cần combo cho bao nhiêu người? Mình sẽ gợi ý phù hợp nhé!"
    ],
    "ask_ingredient": [
        "Bạn muốn biết thành phần của loại bánh nào ạ? Shop luôn dùng nguyên liệu tươi mới!",
        "Bánh của shop làm từ nguyên liệu tự nhiên, không chất bảo quản. Bạn hỏi về loại bánh nào cụ thể nhé!"
    ],
    "ask_special_event": [
        "Bạn cần bánh cho dịp đặc biệt nào? Shop có nhiều mẫu bánh cho các sự kiện khác nhau!",
        "Bạn nói rõ dịp lễ/sự kiện để shop tư vấn mẫu bánh phù hợp nhé!"
    ],
    "ask_preservation": [
        "Bánh nên được bảo quản trong ngăn mát tủ lạnh và dùng trong 2-3 ngày.",
        "Bạn cần hướng dẫn bảo quản loại bánh nào? Shop sẽ tư vấn chi tiết nhé!"
    ],
    "ask_return": [
        "Shop hỗ trợ đổi trả nếu bánh có lỗi từ phía shop. Bạn vui lòng gửi hình ảnh và thông tin đơn hàng nhé!",
        "Bạn gặp vấn đề gì với sản phẩm? Shop sẽ hỗ trợ đổi trả nhanh nhất có thể."
    ],
    "ask_contact": [
        "Bạn có thể liên hệ shop qua số hotline 0123 456 789 hoặc Zalo cùng số nhé!",
        "Mọi thắc mắc bạn gọi trực tiếp 0123 456 789 hoặc inbox fanpage giúp shop nhé!"
    ],
    "ask_deposit": [
        "Một số đơn hàng cần đặt cọc trước, bạn muốn đặt loại bánh nào để shop báo phí cọc nhé!",
        "Bạn vui lòng chuyển khoản đặt cọc để shop giữ bánh cho bạn nhé!"
    ],
    "ask_minimum_order": [
        "Tùy loại bánh sẽ có số lượng tối thiểu khác nhau, bạn hỏi loại nào để shop tư vấn nhé!",
        "Bạn cần đặt tối thiểu bao nhiêu bánh? Shop sẽ kiểm tra và báo lại bạn nhé!"
    ],
    "ask_invoice": [
        "Shop có hỗ trợ xuất hóa đơn VAT cho doanh nghiệp, bạn cần xuất hóa đơn cho đơn hàng nào?",
        "Bạn vui lòng cung cấp thông tin công ty để shop xuất hóa đơn nhé!"
    ],
    "ask_loyalty": [
        "Shop có chương trình tích điểm cho khách hàng thân thiết, bạn đã đăng ký thành viên chưa?",
        "Bạn muốn biết quyền lợi thẻ thành viên? Shop sẽ gửi thông tin chi tiết nhé!"
    ],
    "ask_purchase_history": [
        "Bạn cần tra cứu lịch sử mua hàng, vui lòng cung cấp số điện thoại đã đặt bánh nhé!",
        "Shop sẽ kiểm tra đơn cũ cho bạn, bạn cho mình xin thông tin đặt hàng nhé!"
    ],
    "ask_nutrition": [
        "Bạn quan tâm đến thành phần dinh dưỡng của loại bánh nào? Shop sẽ gửi thông tin chi tiết nhé!",
        "Bạn cần tư vấn về calo, chất béo hay thành phần nào? Shop luôn sẵn sàng hỗ trợ!"
    ],
    "ask_for_kids": [
        "Shop có nhiều loại bánh phù hợp cho trẻ em, bạn muốn bánh vị gì cho bé?",
        "Bạn cần bánh cho bé dịp gì? Shop sẽ gợi ý mẫu phù hợp nhé!"
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
        "Shop có bánh phù hợp cho người lớn tuổi, ít ngọt, dễ tiêu hóa.",
        "Bạn muốn đặt bánh cho ông bà dịp gì? Shop sẽ gợi ý mẫu phù hợp nhé!"
    ],
    "ask_foreigner_cake": [
        "Shop có bánh kiểu Âu, bánh tây, phù hợp cho người nước ngoài.",
        "Bạn muốn đặt bánh cho khách nước ngoài dịp nào? Shop sẽ tư vấn nhé!"
    ],
    "ask_company_party_cake": [
        "Shop có nhiều mẫu bánh cho tiệc công ty, hội nghị, party.",
        "Bạn cần bánh cho bao nhiêu người? Shop sẽ gợi ý combo phù hợp nhé!"
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
        "Shop có bánh cho tiệc baby shower, bạn muốn trang trí theo chủ đề gì?",
        "Bạn cần bánh baby shower cho bao nhiêu người? Shop sẽ gợi ý size phù hợp nhé!"
    ],
    "ask_valentine_cake": [
        "Bạn muốn đặt bánh valentine tặng người yêu? Shop có nhiều mẫu lãng mạn!",
        "Bạn thích bánh valentine vị socola, dâu hay vị đặc biệt nào? Shop sẽ tư vấn nhé!"
    ],
    "ask_tet_cake": [
        "Shop có nhiều loại bánh cho dịp Tết, bạn muốn đặt loại nào?",
        "Bạn cần bánh tặng người thân hay đối tác dịp Tết? Shop sẽ gợi ý mẫu phù hợp nhé!"
    ],
    "ask_mid_autumn_cake": [
        "Shop có bánh trung thu truyền thống và hiện đại, bạn muốn thử loại nào?",
        "Bạn cần bánh trung thu cho gia đình hay làm quà tặng? Shop sẽ tư vấn nhé!"
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
        "Bạn muốn đặt bánh cho ngày 8/3 tặng mẹ, vợ hay đồng nghiệp? Shop có nhiều mẫu đẹp!",
        "Bạn cần bánh 8/3 trang trí hoa, trái cây hay kiểu nào? Shop sẽ gợi ý nhé!"
    ],
    "ask_vietnamese_womens_day_cake": [
        "Shop có bánh cho ngày 20/10, bạn muốn đặt loại nào?",
        "Bạn cần bánh 20/10 cho dịp gì? Shop sẽ tư vấn mẫu phù hợp nhé!"
    ],
    "ask_mothers_day_cake": [
        "Bạn muốn đặt bánh cho ngày của mẹ? Shop có nhiều mẫu ý nghĩa!",
        "Bạn cần bánh mother's day trang trí như thế nào? Shop sẽ gợi ý nhé!"
    ],
    "ask_fathers_day_cake": [
        "Shop có bánh cho ngày của cha, bạn muốn đặt loại nào?",
        "Bạn cần bánh father's day cho dịp gì? Shop sẽ tư vấn mẫu phù hợp nhé!"
    ],
    "ask_teachers_day_cake": [
        "Bạn muốn đặt bánh cho ngày nhà giáo Việt Nam? Shop có nhiều mẫu tri ân thầy cô!",
        "Bạn cần bánh 20/11 trang trí như thế nào? Shop sẽ gợi ý nhé!"
    ],
    "ask_childrens_day_cake": [
        "Shop có bánh cho ngày quốc tế thiếu nhi, bạn muốn đặt loại nào cho bé?",
        "Bạn cần bánh 1/6 cho bé trai hay bé gái? Shop sẽ tư vấn mẫu phù hợp nhé!"
    ],
    "ask_mens_day_cake": [
        "Bạn muốn đặt bánh cho ngày quốc tế đàn ông? Shop có nhiều mẫu độc đáo!",
        "Bạn cần bánh men's day cho dịp gì? Shop sẽ tư vấn mẫu phù hợp nhé!"
    ],
    "ask_happiness_day_cake": [
        "Bạn muốn đặt bánh cho ngày quốc tế hạnh phúc? Shop có nhiều mẫu ý nghĩa!",
        "Bạn cần bánh 20/3 trang trí như thế nào? Shop sẽ gợi ý nhé!"
    ],
    "ask_family_day_cake": [
        "Shop có bánh cho ngày quốc tế gia đình, bạn muốn đặt loại nào?",
        "Bạn cần bánh 28/6 cho dịp gì? Shop sẽ tư vấn mẫu phù hợp nhé!"
    ],
    "ask_friends_day_cake": [
        "Bạn muốn đặt bánh cho ngày quốc tế bạn bè? Shop có nhiều mẫu đẹp!",
        "Bạn cần bánh 30/7 cho dịp gì? Shop sẽ tư vấn mẫu phù hợp nhé!"
    ],
    "ask_love_day_cake": [
        "Bạn muốn đặt bánh cho ngày quốc tế tình yêu? Shop có nhiều mẫu lãng mạn!",
        "Bạn cần bánh 14/2 trang trí như thế nào? Shop sẽ gợi ý nhé!"
    ],
    "ask_peace_day_cake": [
        "Bạn muốn đặt bánh cho ngày quốc tế hòa bình? Shop có nhiều mẫu ý nghĩa!",
        "Bạn cần bánh 21/9 trang trí như thế nào? Shop sẽ gợi ý nhé!"
    ],
    "ask_labour_day_cake": [
        "Shop có bánh cho ngày quốc tế lao động, bạn muốn đặt loại nào?",
        "Bạn cần bánh 1/5 cho dịp gì? Shop sẽ tư vấn mẫu phù hợp nhé!"
    ],
}