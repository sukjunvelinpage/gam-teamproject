"""
트윗 분류 사람 검수용 표본(100건)과 라벨링 엑셀을 만든다 (한국어판 / 베트남어판).

목적
    발표에 쓰인 기존 1,246건 트윗의 긍정/부정/소음 분류(LLM 1차 분류)를
    팀원이 직접 읽고 다시 분류해, 두 결과의 일치율을 계산하기 위한 준비 단계.

설계
    - 대상: data/trump_tweets_analysis_input.csv 중 legacy_signal_is_original_scope == 1 (1,246건)
    - 같은 문장의 중복 트윗은 하나만 남긴 뒤 추출 (19건 중복)
    - 가이드 문서에 예시로 쓴 트윗은 표본에서 제외 (정답을 미리 본 문제가 되지 않도록)
    - 기존 분류 비율에 맞춘 층화 추출: 긍정 29 / 부정 34 / 소음 37 = 100건, random_state=42
    - 추출 후 순서를 섞어서, 엑셀에는 기존 분류·판정 사유를 넣지 않는다 (블라인드 검수)
    - 한국어판과 베트남어판은 같은 100건·같은 순서·같은 열 배치. 안내 문구와 번역·맥락만 다르다.

출력
    docs/label_check/label_check_sample_100.xlsx     : 한국어판
    docs/label_check/label_check_sample_100_vi.xlsx  : 베트남어판

실행
    python scripts/build_label_check_sample.py          # 두 언어 모두 생성
    python scripts/build_label_check_sample.py ko       # 한국어판만
    python scripts/build_label_check_sample.py vi       # 베트남어판만
"""

import sys
from pathlib import Path

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = Path(__file__).resolve().parents[1]
TWEETS_PATH = ROOT / "data" / "trump_tweets_analysis_input.csv"
OUT_DIR = ROOT / "docs" / "label_check"

# 표본 100건의 번역·당시 맥락 (참고용, 평가 표현·주가 반응은 넣지 않음)
LANG_FILES = {
    "ko": {"xlsx": OUT_DIR / "label_check_sample_100.xlsx", "context": OUT_DIR / "sample_context_ko.csv"},
    "vi": {"xlsx": OUT_DIR / "label_check_sample_100_vi.xlsx", "context": OUT_DIR / "sample_context_vi.csv"},
}

SEED = 42
STRATA = {"Positive": 29, "Negative": 34, "Noise": 37}  # 1,246건의 28.7% / 33.8% / 37.6% 비율

# 드롭다운 값. score_label_check.py가 언어와 상관없이 같은 코드로 읽는다.
LABELS = {
    "ko": {"pos": "긍정", "neg": "부정", "noise": "소음", "sure": "확실", "unsure": "애매"},
    "vi": {"pos": "Tích cực", "neg": "Tiêu cực", "noise": "Nhiễu", "sure": "Chắc chắn", "unsure": "Phân vân"},
}

# 가이드 문서와 같은 예시. 표본에서 제외하기 위해 audit_key 대신 원문 일부로 찾는다.
# 근거는 팀원이 따라 할 수 있게 "어떤 단어/행동을 보고 판단했는지"로 적는다.
EXAMPLES = [
    # --- 긍정: 갈등 완화, 합의, 유예, 구매, 미국 투자·호황 ---
    ("I will be signing our very large and comprehensive Phase One Trade Deal with China on January 15", "pos",
     "1단계 무역합의 서명 날짜를 확정 발표. 합의 = 갈등 완화.",
     "Công bố ngày ký Thỏa thuận Thương mại Giai đoạn Một. Thỏa thuận = căng thẳng giảm."),
    ("China just announced that their economy is growing much slower", "pos",
     "앞부분은 중국 비난이지만 핵심 사실은 '중국이 관세 인상을 유예했다'와 '곧 합의 가능'. 결론이 완화 쪽.",
     "Phần đầu chỉ trích Trung Quốc, nhưng sự kiện chính là 'Trung Quốc đã tạm hoãn tăng thuế' và 'sắp có thỏa thuận'. Kết luận nghiêng về giảm căng thẳng."),
    ("CHINA HAS ALREADY BEGUN AGRICULTURAL PURCHASES", "pos",
     "중국의 미국산 농산물 구매 시작 = 합의 이행, 갈등 완화.",
     "Trung Quốc bắt đầu mua nông sản Mỹ = thực hiện thỏa thuận, căng thẳng giảm."),
    ("Having dinner tonight with Tim Cook of Apple", "pos",
     "애플의 미국 내 대규모 투자 언급. 미국 기업 투자·고용 호재.",
     "Nhắc đến khoản đầu tư lớn của Apple tại Mỹ. Doanh nghiệp đầu tư, tạo việc làm ở Mỹ."),
    ("Congrats to @U_S_Steel for investing", "pos",
     "'Tariffs are working'이 있지만 주인공은 US스틸의 10억 달러 미국 투자. 기업 투자 성과가 핵심이면 긍정.",
     "Có câu 'Tariffs are working' nhưng nhân vật chính là khoản đầu tư 1 tỷ USD của U.S. Steel tại Mỹ. Nếu trọng tâm là thành quả đầu tư của doanh nghiệp thì là Tích cực."),
    # --- 부정: 관세 부과·위협·지속 과시, 상대국 비난, 기업 압박, 연준 공격 ---
    ("The process has begun to place additional Tariffs at 25% on the remaining 325 Billion", "neg",
     "3,250억 달러에 25% 추가 관세 절차 개시. 구체적 세율·금액이 있는 신규 관세 = 가장 확실한 부정.",
     "Bắt đầu thủ tục áp thêm thuế 25% lên 325 tỷ USD hàng hóa. Thuế mới có thuế suất và số tiền cụ thể = Tiêu cực rõ ràng nhất."),
    ("I am a Tariff Man", "neg",
     "관세를 계속 쓰겠다는 의지 과시. 'wealth', 'billions' 같은 좋은 단어가 있어도 내용은 무역갈등 지속.",
     "Phô trương ý chí tiếp tục dùng thuế quan. Dù có từ ngữ tích cực như 'wealth', 'billions', nội dung vẫn là tiếp tục xung đột thương mại."),
    ("Tariffs are working far better than anyone ever anticipated", "neg",
     "관세 효과 자랑 + 중국 시장 폭락 언급. 관세를 거둘 생각이 없다는 신호 → 갈등 지속.",
     "Khoe hiệu quả của thuế quan và nhắc thị trường Trung Quốc lao dốc. Tín hiệu không có ý định gỡ thuế → xung đột tiếp diễn."),
    ("Our pathetic, slow moving Federal Reserve", "neg",
     "연준·파월을 공개 비난하며 금리 인하 압박. 대통령의 중앙은행 공격 = 정책 불확실성 증가로 본다.",
     "Công khai chỉ trích Fed và Powell, gây sức ép cắt lãi suất. Tổng thống tấn công ngân hàng trung ương = được xem là tăng bất định chính sách."),
    ("Early this year Harley-Davidson said they would move", "neg",
     "특정 기업(할리데이비슨)을 지목해 공개 비판. 개별 기업 압박.",
     "Chỉ đích danh và công khai chỉ trích một doanh nghiệp (Harley-Davidson). Gây sức ép lên doanh nghiệp cụ thể."),
    ("China is letting us down in that they have not been buying", "neg",
     "중국이 약속한 농산물 구매를 안 한다고 공개 불만. 합의 불이행 비난 = 갈등 고조.",
     "Công khai phàn nàn Trung Quốc không mua nông sản như đã hứa. Chỉ trích không thực hiện thỏa thuận = căng thẳng tăng."),
    # --- 소음: 경제 정책과 무관한 정치·코로나·동명이인·관용어 ---
    ("Sidney Powell and Lin Wood hit Georgia", "noise",
     "'Powell'은 연준 의장이 아니라 대선 소송 변호사 시드니 파월. 동명이인.",
     "'Powell' ở đây không phải Chủ tịch Fed mà là luật sư Sidney Powell trong các vụ kiện bầu cử. Trùng tên."),
    ("European Countries are sadly getting clobbered by the China Virus", "noise",
     "'China'가 있지만 코로나 상황 이야기. 무역·관세 조치 없음.",
     "Có từ 'China' nhưng là chuyện tình hình Covid. Không có biện pháp thương mại hay thuế quan."),
    ("There is no reason for these massive, deadly and costly forest fires", "noise",
     "'Fed payments'는 연준이 아니라 산불 연방 지원금. 키워드 오탐.",
     "'Fed payments' là tiền hỗ trợ của chính phủ liên bang cho cháy rừng, không phải Fed. Bắt nhầm từ khóa."),
    ("Somebody please wake up Mitt Romney", "noise",
     "우크라이나 통화·탄핵 관련 정치 공방. 'China'는 부패 조사 맥락.",
     "Tranh cãi chính trị về cuộc gọi với Ukraine và luận tội. 'China' xuất hiện trong bối cảnh điều tra tham nhũng."),
]

# 시트 안내 문구 (언어별)
TEXT = {
    "ko": {
        "sheets": ["1_작업방법", "2_분류기준", "3_예시", "4_라벨링"],
        "guide": [
            ["트윗 분류 검수 작업 방법"],
            [""],
            ["목적", "LLM이 1차로 나눈 긍정/부정/소음 분류가 사람이 읽어도 같은지 확인합니다. 정답 맞히기가 아니라 '독립적인 두 번째 판단'이 목적입니다."],
            ["분량", "트윗 100건. 1건당 30초~1분, 전체 1~1.5시간 정도 걸립니다."],
            ["순서", "① '2_분류기준'과 '3_예시'를 먼저 읽는다 → ② '4_라벨링' 시트의 노란 칸만 채운다 → ③ 파일 그대로 돌려준다"],
            ["입력 칸", "내 분류: 긍정/부정/소음 중 선택 (드롭다운)\n확신도: 확실/애매 중 선택\n한 줄 근거: 어떤 단어·행동을 보고 판단했는지 짧게 (애매한 경우는 꼭)"],
            ["지켜 주세요", "· 다른 팀원이나 AI에게 정답을 묻지 않습니다 (독립 판단이 깨집니다).\n· data/ 폴더의 기존 분류 결과를 보지 않습니다.\n· 영어가 어려우면 번역기(파파고, 구글 번역)는 써도 됩니다. 단, 판단은 직접.\n· 고민이 1분 넘게 길어지면 가장 가까운 쪽을 고르고 '애매'로 표시한 뒤 넘어갑니다."],
            ["번역·맥락 칸", "'4_라벨링'의 회색 칸(한국어 번역, 당시 맥락)은 이해를 돕는 참고 자료입니다.\n· AI로 작성했고 사실관계가 틀렸을 수 있습니다. 이상하면 원문을 기준으로 판단하고 메모해 주세요.\n· 일부러 '좋은 소식/나쁜 소식' 같은 평가와 그날 주가 움직임은 적지 않았습니다. 판단은 원문 내용으로 직접 합니다."],
            ["질문할 것", "기준 자체가 이해 안 되면 작업 전에 물어보세요. 개별 트윗 정답은 묻지 않습니다."],
        ],
        "rules": [
            ["단계", "질문", "답이 '예'이면"],
            ["핵심 질문", "이 트윗을 본 주식·채권·환율 투자자가 '미국 무역·경제 정책 불확실성이 줄었다'고 느낄까, '커졌다'고 느낄까, 아니면 '시장과 상관없는 말'로 넘길까?", ""],
            ["1단계", "무역·관세·중국 협상·연준 금리·특정 기업·미국 산업/경제 이야기가 실제로 있나?\n(키워드만 있고 내용은 선거·코로나·탄핵·동명이인이면 '아니오')", "아니오 → 소음"],
            ["2단계", "갈등이 풀리는 방향인가?\n합의·서명·타결, 관세 유예·연기·면제, 협상 순항, 상대국의 미국산 구매, 미국 내 기업 투자·공장·일자리, 미국 경제·증시 호황 자랑, 농가 지원금", "예 → 긍정"],
            ["3단계", "갈등이 커지는 방향인가?\n신규 관세 부과·세율 인상·위협, 관세 계속 쓰겠다는 과시, 상대국 무역적자·환율조작·약속 불이행 비난, 특정 기업 공개 압박·제재, 연준·파월 공격과 금리 인하 압박", "예 → 부정"],
            ["섞여 있을 때", "한 트윗에 좋은 말과 나쁜 말이 같이 있으면 '결론(마지막에 하겠다고 한 행동)'을 따른다.\n예: '협상 잘 되고 있다, 하지만 안 되면 25% 관세' → 부정", ""],
            ["리트윗(RT)", "리트윗한 글의 내용으로 똑같이 판단한다. 뉴스 제목만 있는 RT도 그 내용대로.", ""],
            ["잘린 트윗(...)", "보이는 부분만으로 판단. 판단할 내용이 거의 없으면 가장 가까운 쪽 + '애매'.", ""],
            [""],
            ["헷갈리기 쉬운 것", "판단", "이유"],
            ["'Tariffs are working', 'billions pouring in' 같은 좋은 단어", "부정", "단어가 아니라 내용을 본다. 관세를 거두지 않겠다는 뜻이므로 갈등 지속."],
            ["관세 언급 + 미국 기업 투자 성과가 주인공", "긍정", "주어가 '기업이 미국에 투자했다'면 긍정. 주어가 '관세가 옳다/계속한다'면 부정."],
            ["연준에 금리 인하를 요구", "부정", "금리 인하가 주가엔 좋을 수 있어도, 이 분류는 '대통령이 중앙은행을 공격한다 = 불확실성'으로 본다."],
            ["상대국이 약속을 안 지킨다는 불만", "부정", "새 관세가 없어도 합의 불이행 비난은 갈등 고조."],
            ["'China Virus', 바이든·헌터 공격, 선거·탄핵", "소음", "중국·무역 단어가 있어도 정책 조치가 없으면 시장 신호가 아니다."],
            ["Fed up / Sidney·Colin·Dina Powell / apple cart / Shawn Steel / man of steel", "소음", "연준·애플·철강과 무관한 관용어·동명이인."],
        ],
        "example_header": ["정답", "트윗 원문", "판단 근거"],
        "label_header": ["번호", "작성시각(뉴욕)", "RT", "트윗 원문", "한국어 번역(참고)", "당시 맥락(참고)",
                         "내 분류", "확신도", "한 줄 근거", "audit_key(수정 금지)"],
    },
    "vi": {
        "sheets": ["1_HuongDan", "2_TieuChi", "3_ViDu", "4_GanNhan"],
        "guide": [
            ["Hướng dẫn kiểm tra phân loại tweet"],
            [""],
            ["Mục đích", "Kiểm tra xem kết quả phân loại Tích cực / Tiêu cực / Nhiễu do AI (LLM) làm lần đầu có giống với đánh giá của con người hay không. Đây không phải bài kiểm tra đúng/sai, mà là 'đánh giá thứ hai một cách độc lập'."],
            ["Khối lượng", "100 tweet. Mỗi tweet khoảng 30 giây – 1 phút, tổng cộng khoảng 1 – 1,5 giờ."],
            ["Các bước", "① Đọc trước sheet '2_TieuChi' và '3_ViDu' → ② Chỉ điền vào các ô màu vàng ở sheet '4_GanNhan' → ③ Gửi lại nguyên file"],
            ["Ô cần điền", "Phân loại của tôi: chọn Tích cực / Tiêu cực / Nhiễu (danh sách thả xuống)\nMức chắc chắn: chọn Chắc chắn / Phân vân\nLý do ngắn: ghi ngắn gọn bạn dựa vào từ ngữ hay hành động nào để quyết định (bắt buộc với trường hợp Phân vân)"],
            ["Lưu ý", "· Không hỏi đáp án từng tweet với thành viên khác hoặc AI (sẽ mất tính độc lập).\n· Không mở kết quả phân loại có sẵn trong thư mục data/.\n· Có thể dùng công cụ dịch (Google Dịch, Papago). Nhưng việc phán đoán phải tự làm.\n· Nếu một tweet khiến bạn phân vân hơn 1 phút, hãy chọn phương án gần nhất, đánh dấu 'Phân vân' rồi chuyển sang tweet tiếp theo."],
            ["Ô dịch & bối cảnh", "Các ô màu xám ở sheet '4_GanNhan' (bản dịch tiếng Việt, bối cảnh lúc đó) chỉ để tham khảo.\n· Do AI viết nên có thể sai về sự kiện. Nếu thấy lạ, hãy phán đoán theo bản gốc tiếng Anh và ghi chú lại.\n· Chúng tôi cố ý không ghi các đánh giá kiểu 'tin tốt / tin xấu' và diễn biến giá cổ phiếu hôm đó. Hãy tự phán đoán dựa trên nội dung bản gốc."],
            ["Câu hỏi", "Nếu chưa hiểu tiêu chí, hãy hỏi trước khi bắt đầu. Đừng hỏi đáp án của từng tweet cụ thể."],
        ],
        "rules": [
            ["Bước", "Câu hỏi", "Nếu trả lời 'Có'"],
            ["Câu hỏi chính", "Một nhà đầu tư (cổ phiếu, trái phiếu, tỷ giá) đọc tweet này sẽ cảm thấy 'mức bất định của chính sách thương mại/kinh tế Mỹ đã GIẢM', 'đã TĂNG', hay coi đó là 'lời nói không liên quan đến thị trường'?", ""],
            ["Bước 1", "Tweet có THỰC SỰ nói về thương mại, thuế quan, đàm phán với Trung Quốc, lãi suất của Fed, một doanh nghiệp cụ thể, hoặc ngành công nghiệp/kinh tế Mỹ không?\n(Nếu chỉ có từ khóa nhưng nội dung là bầu cử, Covid, luận tội, trùng tên thì trả lời 'Không')", "Không → Nhiễu"],
            ["Bước 2", "Có theo hướng xung đột được tháo gỡ không?\nThỏa thuận, ký kết, đạt được đồng thuận; tạm hoãn, trì hoãn, miễn thuế; đàm phán thuận lợi; nước đối tác mua hàng Mỹ; doanh nghiệp đầu tư, xây nhà máy, tạo việc làm tại Mỹ; khoe kinh tế/chứng khoán Mỹ bùng nổ; tiền hỗ trợ nông dân", "Có → Tích cực"],
            ["Bước 3", "Có theo hướng xung đột gia tăng không?\nÁp thuế mới, tăng thuế suất, đe dọa áp thuế; khoe sẽ tiếp tục dùng thuế quan; chỉ trích nước đối tác về thâm hụt thương mại, thao túng tiền tệ, không giữ lời hứa; công khai gây sức ép/trừng phạt doanh nghiệp cụ thể; tấn công Fed/Powell và ép cắt lãi suất", "Có → Tiêu cực"],
            ["Khi lẫn lộn", "Nếu một tweet vừa có ý tốt vừa có ý xấu, hãy theo 'kết luận' (hành động cuối cùng được tuyên bố sẽ làm).\nVí dụ: 'Đàm phán đang rất tốt, NHƯNG nếu không đạt thì áp thuế 25%' → Tiêu cực", ""],
            ["Retweet (RT)", "Phán đoán theo nội dung của bài được retweet, giống như bình thường. RT chỉ có tiêu đề tin tức thì cũng theo nội dung tiêu đề đó.", ""],
            ["Tweet bị cắt (...)", "Chỉ phán đoán dựa trên phần nhìn thấy được. Nếu gần như không có nội dung để phán đoán thì chọn phương án gần nhất + 'Phân vân'.", ""],
            [""],
            ["Trường hợp dễ nhầm", "Phân loại", "Lý do"],
            ["Từ ngữ tích cực như 'Tariffs are working', 'billions pouring in'", "Tiêu cực", "Nhìn nội dung chứ không nhìn từ ngữ. Ý là không có ý định gỡ thuế nên xung đột tiếp diễn."],
            ["Có nhắc thuế quan nhưng nhân vật chính là thành quả đầu tư của doanh nghiệp tại Mỹ", "Tích cực", "Nếu chủ thể là 'doanh nghiệp đã đầu tư vào Mỹ' → Tích cực. Nếu chủ thể là 'thuế quan là đúng / sẽ tiếp tục' → Tiêu cực."],
            ["Yêu cầu Fed cắt lãi suất", "Tiêu cực", "Cắt lãi suất có thể tốt cho giá cổ phiếu, nhưng trong phân loại này 'Tổng thống tấn công ngân hàng trung ương' được xem là tăng bất định."],
            ["Phàn nàn nước đối tác không giữ lời hứa", "Tiêu cực", "Dù không có thuế mới, chỉ trích việc không thực hiện thỏa thuận vẫn làm căng thẳng tăng."],
            ["'China Virus', tấn công Biden/Hunter, bầu cử, luận tội", "Nhiễu", "Dù có từ 'Trung Quốc' hay 'thương mại', nếu không có biện pháp chính sách thì không phải tín hiệu thị trường."],
            ["Fed up / Sidney·Colin·Dina Powell / apple cart / Shawn Steel / man of steel", "Nhiễu", "Thành ngữ hoặc trùng tên, không liên quan đến Fed, Apple hay ngành thép."],
        ],
        "example_header": ["Đáp án", "Nguyên văn tweet", "Lý do phán đoán"],
        "label_header": ["STT", "Thời gian đăng (New York)", "RT", "Nguyên văn tweet", "Bản dịch tiếng Việt (tham khảo)",
                         "Bối cảnh lúc đó (tham khảo)", "Phân loại của tôi", "Mức chắc chắn", "Lý do ngắn",
                         "audit_key (không sửa)"],
    },
}


def load_existing_1246() -> pd.DataFrame:
    df = pd.read_csv(TWEETS_PATH, low_memory=False, dtype={"id": str})
    df = df[df["legacy_signal_is_original_scope"] == 1].copy()
    assert len(df) == 1246, f"기존 분류 대상은 1,246건이어야 합니다 (현재 {len(df)})"
    return df


def find_example_texts(df: pd.DataFrame) -> set:
    texts = set()
    for snippet, *_ in EXAMPLES:
        hit = df[df["text"].str.contains(snippet, regex=False, na=False)]
        assert len(hit) > 0, f"예시 트윗을 찾지 못했습니다: {snippet}"
        texts.update(hit["text"])
    return texts


def draw_sample(df: pd.DataFrame) -> pd.DataFrame:
    example_texts = find_example_texts(df)
    pool = df[~df["text"].isin(example_texts)].drop_duplicates("text")
    parts = [
        pool[pool["legacy_signal"] == label].sample(n=n, random_state=SEED)
        for label, n in STRATA.items()
    ]
    sample = pd.concat(parts).sample(frac=1, random_state=SEED).reset_index(drop=True)
    sample["번호"] = range(1, len(sample) + 1)
    ny = pd.to_datetime(sample["date_utc"], utc=True).dt.tz_convert("America/New_York")
    sample["작성시각_뉴욕"] = ny.dt.strftime("%Y-%m-%d %H:%M")
    sample["리트윗"] = sample["isRetweet"].map({"t": "RT", "f": ""}).fillna("")
    return sample


def attach_context(sample: pd.DataFrame, context_path: Path) -> pd.DataFrame:
    """표본 100건에 손으로 작성한 번역·당시 맥락을 audit_key로 붙인다."""
    ctx = pd.read_csv(context_path, encoding="utf-8-sig")
    out = sample.merge(ctx[["audit_key", "번역", "당시_맥락"]], on="audit_key", how="left", validate="one_to_one")
    missing = out["번역"].isna().sum()
    assert missing == 0, f"번역·맥락이 없는 표본 {missing}건 — 표본이 바뀌었다면 {context_path.name}도 다시 작성해야 합니다"
    return out


def find_example_rows(df: pd.DataFrame, lang: str) -> list:
    rows = []
    for snippet, code, reason_ko, reason_vi in EXAMPLES:
        r = df[df["text"].str.contains(snippet, regex=False, na=False)].iloc[0]
        rows.append((LABELS[lang][code], r["text"], reason_ko if lang == "ko" else reason_vi))
    return rows


HEADER_FILL = PatternFill("solid", fgColor="DDE7F0")
INPUT_FILL = PatternFill("solid", fgColor="FFF6D5")
REF_FILL = PatternFill("solid", fgColor="F2F2F2")
WRAP = Alignment(wrap_text=True, vertical="top")


def write_sheet_rows(ws, rows, widths):
    for row in rows:
        ws.append(row)
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[ws.cell(row=1, column=i).column_letter].width = w
    for row in ws.iter_rows():
        for c in row:
            c.alignment = WRAP


def build_workbook(sample: pd.DataFrame, example_rows: list, lang: str) -> Workbook:
    t = TEXT[lang]
    lab = LABELS[lang]
    s_guide, s_rules, s_examples, s_label = t["sheets"]
    wb = Workbook()

    # 1) 작업 방법
    ws = wb.active
    ws.title = s_guide
    write_sheet_rows(ws, t["guide"], [16, 100])
    ws["A1"].font = Font(bold=True, size=14)

    # 2) 분류 기준
    ws = wb.create_sheet(s_rules)
    write_sheet_rows(ws, t["rules"], [24, 80, 40])
    for c in ws[1] + ws[10]:
        c.font = Font(bold=True)
        c.fill = HEADER_FILL

    # 3) 예시
    ws = wb.create_sheet(s_examples)
    write_sheet_rows(ws, [t["example_header"]] + example_rows, [10, 90, 60])
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = HEADER_FILL

    # 4) 라벨링 (번역·맥락은 참고용 회색 칸, 노란 칸만 입력). 열 배치는 두 언어가 같다.
    ws = wb.create_sheet(s_label)
    ws.append(t["label_header"])
    for _, r in sample.iterrows():
        ws.append([r["번호"], r["작성시각_뉴욕"], r["리트윗"], r["text"], r["번역"], r["당시_맥락"],
                   None, None, None, r["audit_key"]])
    for i, w in enumerate([6, 17, 5, 60, 60, 45, 12, 11, 40, 12], start=1):
        ws.column_dimensions[ws.cell(row=1, column=i).column_letter].width = w
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = HEADER_FILL
        c.alignment = WRAP
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = WRAP
        for c in row[4:6]:
            c.fill = REF_FILL
        for c in row[6:9]:
            c.fill = INPUT_FILL
    last = len(sample) + 1
    dv_label = DataValidation(type="list", formula1=f'"{lab["pos"]},{lab["neg"]},{lab["noise"]}"', allow_blank=True)
    dv_conf = DataValidation(type="list", formula1=f'"{lab["sure"]},{lab["unsure"]}"', allow_blank=True)
    ws.add_data_validation(dv_label)
    ws.add_data_validation(dv_conf)
    dv_label.add(f"G2:G{last}")
    dv_conf.add(f"H2:H{last}")
    ws.freeze_panes = "E2"
    wb.active = 0
    return wb


def main(langs):
    df = load_existing_1246()
    sample = draw_sample(df)
    print("기존 분류 구성:", sample["legacy_signal"].value_counts().to_dict())
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for lang in langs:
        files = LANG_FILES[lang]
        wb = build_workbook(attach_context(sample, files["context"]), find_example_rows(df, lang), lang)
        wb.save(files["xlsx"])
        print(f"[{lang}] 표본 {len(sample)}건 저장: {files['xlsx']}")


if __name__ == "__main__":
    main(sys.argv[1:] or ["ko", "vi"])
