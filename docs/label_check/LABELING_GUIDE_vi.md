# Hướng dẫn kiểm tra phân loại tweet (dành cho thành viên nhóm)

## 1. Tại sao cần làm việc này?

Nhóm dùng 1.246 tweet về thương mại trong bài thuyết trình. Các tweet này được AI (LLM) phân loại trước thành **Tích cực / Tiêu cực / Nhiễu**.
Khi thuyết trình, nếu bị hỏi "Làm sao tin được kết quả phân loại của AI?", nhóm muốn trả lời: "Con người đã đọc riêng 100 tweet và kết quả giống AI ○○%".

Vì vậy, điều quan trọng nhất là **bạn tự phán đoán mà không xem kết quả của AI**. Đây không phải bài kiểm tra đúng/sai. Những tweet bạn phân loại khác AI cũng là một kết quả có ý nghĩa.

## 2. Cách làm

- **File:** `label_check_sample_100_vi.xlsx`
- **Khối lượng:** 100 tweet, khoảng 1–1,5 giờ
- **Các bước**
  1. Đọc trước tài liệu này (hoặc sheet `2_TieuChi` và `3_ViDu` trong file Excel).
  2. Ở sheet `4_GanNhan`, **chỉ điền 3 ô màu vàng**:
     - **Phân loại của tôi:** Tích cực / Tiêu cực / Nhiễu (danh sách thả xuống)
     - **Mức chắc chắn:** Chắc chắn / Phân vân
     - **Lý do ngắn:** ghi ngắn gọn bạn dựa vào từ ngữ hay hành động nào. Bắt buộc với trường hợp Phân vân.
  3. Gửi lại nguyên file. Không sửa cột `audit_key`.
- **Ô màu xám (bản dịch tiếng Việt, bối cảnh lúc đó) chỉ để tham khảo.**
  - Do AI viết nên có thể sai về sự kiện. Nếu thấy lạ, hãy phán đoán theo bản gốc tiếng Anh và ghi chú lại.
  - Chúng tôi cố ý không ghi các đánh giá kiểu "tin tốt / tin xấu" và diễn biến giá cổ phiếu hôm đó. Nhóm dùng kết quả phân loại để kiểm định phản ứng của giá cổ phiếu. Nếu nhìn giá cổ phiếu rồi mới phân loại, kết luận sẽ thành lập luận vòng tròn.
- **Lưu ý**
  - Không hỏi đáp án từng tweet với thành viên khác hoặc AI.
  - Không mở kết quả phân loại có sẵn trong thư mục `data/`.
  - Có thể dùng công cụ dịch (Google Dịch, Papago). Nhưng việc phán đoán phải tự làm.
  - Nếu một tweet khiến bạn phân vân hơn 1 phút, hãy chọn phương án gần nhất, đánh dấu "Phân vân" rồi chuyển sang tweet tiếp theo.

## 3. Tiêu chí phân loại

**Chỉ một câu hỏi chính:**
> Một nhà đầu tư (cổ phiếu, trái phiếu, tỷ giá) đọc tweet này sẽ cảm thấy "mức bất định của chính sách thương mại/kinh tế Mỹ đã **GIẢM**", "đã **TĂNG**", hay coi đó là "**lời nói không liên quan đến thị trường**"?

| Bước | Điều cần kiểm tra | Kết quả |
|---|---|---|
| 1 | Tweet có **thực sự** nói về thương mại, thuế quan, đàm phán với Trung Quốc, lãi suất của Fed, một doanh nghiệp cụ thể, hoặc ngành công nghiệp và kinh tế Mỹ không? Nếu chỉ có từ khóa nhưng nội dung là bầu cử, Covid, luận tội hay trùng tên thì xem như "không có". | Không → **Nhiễu** |
| 2 | Có theo hướng xung đột được tháo gỡ không? Ví dụ: thỏa thuận, ký kết, đạt đồng thuận; tạm hoãn, trì hoãn, miễn thuế; đàm phán thuận lợi; nước đối tác mua hàng Mỹ; doanh nghiệp đầu tư, xây nhà máy, tạo việc làm tại Mỹ; khoe kinh tế và chứng khoán Mỹ bùng nổ; tiền hỗ trợ nông dân. | **Tích cực** |
| 3 | Có theo hướng xung đột gia tăng không? Ví dụ: áp thuế mới, tăng thuế suất, đe dọa áp thuế; khoe sẽ tiếp tục dùng thuế quan; chỉ trích nước đối tác về thâm hụt thương mại, thao túng tiền tệ, không giữ lời hứa; công khai gây sức ép hoặc trừng phạt doanh nghiệp cụ thể; tấn công Fed/Powell và ép cắt lãi suất. | **Tiêu cực** |

**Quy tắc bổ sung**
- **Khi vừa có ý tốt vừa có ý xấu:** theo kết luận, tức là hành động cuối cùng được tuyên bố sẽ làm.
  Ví dụ: "Đàm phán đang rất tốt. NHƯNG nếu không đạt thì áp thuế 25%" → **Tiêu cực**
- **Retweet (RT):** phán đoán theo nội dung của bài được retweet, giống như bình thường.
- **Tweet bị cắt (kết thúc bằng `...`):** chỉ phán đoán dựa trên phần nhìn thấy. Nếu gần như không có nội dung thì chọn phương án gần nhất và đánh dấu "Phân vân".

### Các trường hợp dễ nhầm

| Trường hợp | Phân loại | Lý do |
|---|---|---|
| Từ ngữ tích cực như "Tariffs are working", "billions pouring in" | Tiêu cực | Nhìn nội dung chứ không nhìn từ ngữ. Ý là không có ý định gỡ thuế nên xung đột tiếp diễn. |
| Có nhắc thuế quan nhưng nhân vật chính là thành quả đầu tư của doanh nghiệp tại Mỹ | Tích cực | Nếu chủ thể là "doanh nghiệp đã đầu tư vào Mỹ" thì Tích cực. Nếu chủ thể là "thuế quan là đúng / sẽ tiếp tục" thì Tiêu cực. |
| Yêu cầu Fed cắt lãi suất | Tiêu cực | Cắt lãi suất có thể tốt cho giá cổ phiếu. Nhưng trong phân loại này, việc "Tổng thống tấn công ngân hàng trung ương" được xem là tăng bất định. |
| Phàn nàn nước đối tác không giữ lời hứa | Tiêu cực | Dù không có thuế mới, chỉ trích việc không thực hiện thỏa thuận vẫn làm căng thẳng tăng. |
| "China Virus", tấn công Biden/Hunter, bầu cử, luận tội | Nhiễu | Dù có từ "Trung Quốc" hay "thương mại", nếu không có biện pháp chính sách thì không phải tín hiệu thị trường. |
| fed up / Sidney·Colin·Dina Powell / apple cart / Shawn Steel / man of steel | Nhiễu | Đây là thành ngữ hoặc trùng tên, không liên quan đến Fed, Apple hay ngành thép. |

## 4. Ví dụ rõ ràng và lý do

Các ví dụ dưới đây không nằm trong 100 tweet cần kiểm tra.

### Tích cực

| Tweet (tóm tắt) | Lý do phán đoán |
|---|---|
| *"I will be signing our very large and comprehensive Phase One Trade Deal with China on January 15..."* | Công bố ngày ký Thỏa thuận Thương mại Giai đoạn Một. Thỏa thuận là giảm căng thẳng. |
| *"China just announced that their economy is growing much slower... They have just suspended U.S. Tariff Hikes... It could happen, and rather soon!"* | Phần đầu chỉ trích Trung Quốc. Nhưng sự kiện chính là "Trung Quốc đã tạm hoãn tăng thuế" và "sắp có thỏa thuận", nên kết luận nghiêng về giảm căng thẳng. |
| *"CHINA HAS ALREADY BEGUN AGRICULTURAL PURCHASES FROM OUR GREAT PATRIOT FARMERS"* | Trung Quốc bắt đầu mua nông sản Mỹ là thực hiện thỏa thuận. |
| *"Having dinner tonight with Tim Cook of Apple. They will be spending vast sums of money in the U.S."* | Nhắc đến khoản đầu tư lớn của Apple tại Mỹ. Doanh nghiệp đầu tư vào Mỹ. |
| *"Congrats to @U_S_Steel for investing $1+ BILLION... Tariffs are working..."* | Có câu "Tariffs are working" nhưng nhân vật chính là khoản đầu tư của U.S. Steel tại Mỹ. Nếu trọng tâm là thành quả đầu tư của doanh nghiệp thì là Tích cực. |

### Tiêu cực

| Tweet (tóm tắt) | Lý do phán đoán |
|---|---|
| *"The process has begun to place additional Tariffs at 25% on the remaining 325 Billion Dollars..."* | Bắt đầu thủ tục áp thêm thuế 25% lên 325 tỷ USD hàng hóa. Thuế mới có thuế suất và số tiền cụ thể là Tiêu cực rõ ràng nhất. |
| *"I am a Tariff Man... We are right now taking in $billions in Tariffs."* | Phô trương ý chí tiếp tục dùng thuế quan. Dù có từ tích cực như wealth, billions, nội dung vẫn là tiếp tục xung đột thương mại. |
| *"Tariffs are working far better than anyone ever anticipated. China market has dropped 27%..."* | Khoe hiệu quả của thuế quan và nhắc thị trường Trung Quốc lao dốc. Đây là tín hiệu không có ý định gỡ thuế. |
| *"Our pathetic, slow moving Federal Reserve, headed by Jay Powell..."* | Công khai chỉ trích Fed và Powell, gây sức ép cắt lãi suất. Tấn công ngân hàng trung ương được xem là tăng bất định. |
| *"Early this year Harley-Davidson said they would move much of their plant operations... to Thailand..."* | Chỉ đích danh và công khai chỉ trích Harley-Davidson. Đây là gây sức ép lên doanh nghiệp cụ thể. |
| *"...China is letting us down in that they have not been buying the agricultural products..."* | Công khai phàn nàn Trung Quốc không mua nông sản như đã hứa. Chỉ trích không thực hiện thỏa thuận là căng thẳng tăng. |

### Nhiễu

| Tweet (tóm tắt) | Lý do phán đoán |
|---|---|
| *"RT: Sidney Powell and Lin Wood hit Georgia with 104-page lawsuit."* | Powell ở đây không phải Chủ tịch Fed mà là luật sư Sidney Powell trong các vụ kiện bầu cử. Trùng tên. |
| *"European Countries are sadly getting clobbered by the China Virus."* | Có từ China nhưng là chuyện tình hình Covid. Không có biện pháp thương mại hay thuế quan. |
| *"...forest fires in California... Remedy now, or no more Fed payments!"* | Fed payments ở đây là tiền hỗ trợ của chính phủ liên bang cho cháy rừng, không phải Fed. Bắt nhầm từ khóa. |
| *"Somebody please wake up Mitt Romney... my statement on China pertained to corruption, not politics."* | Tranh cãi chính trị về cuộc gọi với Ukraine và luận tội. China xuất hiện trong bối cảnh điều tra tham nhũng. |

---

Nếu chưa hiểu tiêu chí, hãy hỏi trước khi bắt đầu. Cảm ơn bạn!
