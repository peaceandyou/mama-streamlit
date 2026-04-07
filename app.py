import streamlit as st
import requests
import json
import os
import base64
import io
from datetime import datetime
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont

st.set_page_config(
    page_title="嘛嘛公寓 · 小红书运营工具",
    page_icon="🏠",
    layout="wide"
)

st.markdown("""
<style>
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
.stDeployButton,
[data-testid="stStatusWidget"] { display: none !important; visibility: hidden !important; }

[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main { background: #FDF6F7 !important; }

.main .block-container {
    padding-top: 0 !important;
    padding-bottom: 40px !important;
    max-width: 1280px !important;
}

/* 导航栏 */
.navbar {
    background: white;
    border-bottom: 1px solid #F0E0E3;
    padding: 0 28px;
    height: 60px;
    display: flex; align-items: center; justify-content: space-between;
    box-shadow: 0 2px 12px rgba(255,36,66,0.06);
    margin: 0 -28px 24px -28px;
}
.nav-logo {
    width: 36px; height: 36px; background: #FF2442;
    border-radius: 10px; display: inline-flex;
    align-items: center; justify-content: center;
    font-size: 18px; color: white; font-weight: 900; margin-right: 10px;
}
.nav-title { font-size: 17px; font-weight: 700; color: #1A1A1A; }
.nav-sub   { font-size: 12px; color: #999; margin-top: 1px; }

/* 通用卡片 */
.card {
    background: white; border-radius: 16px; padding: 20px;
    border: 1px solid #F0E0E3;
    box-shadow: 0 4px 20px rgba(255,36,66,0.07);
    margin-bottom: 16px;
}
.card-title {
    font-size: 16px; font-weight: 700; color: #1A1A1A;
    margin-bottom: 14px; display: flex; align-items: center; gap: 6px;
}

/* 公寓芯片 */
.apt-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.apt-chip {
    display: flex; align-items: center; gap: 6px;
    padding: 8px 10px; background: #FFF0F2;
    border-radius: 10px; font-size: 12px; color: #555;
}
.apt-chip strong { color: #1A1A1A; }

/* 分析建议 */
.analysis-item {
    background: #FFF0F2; border: 1px solid #FFD0D8;
    border-radius: 10px; padding: 12px; margin-bottom: 10px;
}
.analysis-topic { font-size: 13px; font-weight: 700; color: #FF2442; margin-bottom: 4px; }
.analysis-text  { font-size: 12px; color: #555; line-height: 1.6; }

/* topic bar */
.topic-bar {
    display: flex; align-items: center; gap: 10px;
    padding: 11px 16px; background: #FFF0F2;
    border-radius: 10px; border: 1.5px dashed #FF8899; margin-bottom: 14px;
}
.topic-bar-label { font-size: 12px; color: #bbb; white-space: nowrap; }
.topic-bar-val   { font-size: 13px; font-weight: 700; color: #FF2442; flex: 1; }

/* sec label */
.sec-label {
    font-size: 11px; font-weight: 700; color: #bbb;
    letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 8px;
}

/* 帖子类型卡片 */
.type-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; }
.type-card {
    border: 2px solid #F0E0E3; border-radius: 10px;
    padding: 14px; background: white; text-align: center;
}
.type-card.active { border-color: #FF2442; background: #FFF0F2; }
.type-card.active .tc-name { color: #FF2442; }
.tc-icon { font-size: 24px; margin-bottom: 6px; }
.tc-name { font-size: 14px; font-weight: 700; color: #1A1A1A; margin-bottom: 3px; }
.tc-desc { font-size: 11px; color: #999; line-height: 1.4; }

/* 只让生成按钮是红色 */
button[kind="primary"] {
    background: linear-gradient(135deg, #FF2442, #FF6B7A) !important;
    color: white !important; border: none !important;
    border-radius: 14px !important;
    font-size: 16px !important; font-weight: 700 !important;
}
button[kind="secondary"] {
    background: white !important;
    color: #555 !important;
    border: 1.5px solid #E0E0E0 !important;
    border-radius: 20px !important;
}

/* 预览区 */
.preview-bar {
    background: #F8F8F8; padding: 8px 16px;
    display: flex; align-items: center; gap: 6px;
    border-bottom: 1px solid #F0E0E3;
    border-radius: 14px 14px 0 0;
}
.dot { width:10px; height:10px; border-radius:50%; display:inline-block; }

/* radio 横排 */
div[data-testid="stRadio"] > div { flex-direction: row !important; gap: 12px !important; flex-wrap: wrap; }
div[data-testid="stRadio"] label { font-size: 13px !important; }

/* expander */
div[data-testid="stExpander"] {
    border: 1.5px solid #F0E0E3 !important;
    border-radius: 10px !important;
    background: white !important;
    margin-bottom: 6px !important;
}

/* 输入框 */
.stTextInput input, .stTextArea textarea {
    border-radius: 12px !important;
    border-color: #F0E0E3 !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #FF2442 !important;
    box-shadow: 0 0 0 2px rgba(255,36,66,0.1) !important;
}

/* multiselect tag */
[data-baseweb="tag"] {
    background: #FFF0F2 !important;
    color: #FF2442 !important;
    border-radius: 12px !important;
}

/* 更新中提示 */
.updating-badge {
    background: #FFF7E6; border: 1.5px solid #FFB800;
    color: #B45309; border-radius: 20px;
    padding: 4px 14px; font-size: 12px; font-weight: 600;
    display: inline-flex; align-items: center; gap: 5px;
}
</style>
""", unsafe_allow_html=True)

# ── 密码保护（简洁居中）────────────────────────────────────────
CORRECT_PWD = st.secrets.get("password", "xiaohu2026")
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background:white;border-radius:24px;padding:36px 32px;
        box-shadow:0 12px 40px rgba(255,36,66,0.15);text-align:center;
        border:1px solid #FFE0E5;">
          <div style="width:64px;height:64px;
          background:linear-gradient(135deg,#FF2442,#FF6B7A);
          border-radius:20px;font-size:32px;font-weight:900;color:white;
          display:flex;align-items:center;justify-content:center;
          margin:0 auto 16px;box-shadow:0 8px 20px rgba(255,36,66,0.3);">嘛</div>
          <div style="font-size:20px;font-weight:800;margin-bottom:6px;">嘛嘛公寓运营工具</div>
          <div style="font-size:13px;color:#999;margin-bottom:24px;">请输入访问密码以继续使用</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        pwd = st.text_input("", type="password", placeholder="请输入密码…", label_visibility="collapsed")
        if st.button("进 入", use_container_width=True, type="primary"):
            if pwd == CORRECT_PWD:
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("密码错误，请重新输入")
    st.stop()

# ── 配置 ──────────────────────────────────────────────────────
API_KEY = st.secrets.get("api_key", "")
API_URL = st.secrets.get("api_url", "https://code.newcli.com/claude")
REPLICATE_API_TOKEN = st.secrets.get("replicate_api_token", "")
VOLCENGINE_API_KEY = st.secrets.get("volcengine_api_key", "")

# ── 默认热点数据 ──────────────────────────────────────────────
DEFAULT_HOT_TOPICS = [
    {"id":1,  "name":"毕业季租房避坑指南",      "heat":"982万",  "related":True,
     "reason":"毕业生是嘛嘛公寓的核心目标人群，零中介、月付模式正好戳中他们的痛点",
     "tip":"以「第一次租房的你」为角色切入，重点突出「零中介省了多少钱」的数字对比",
     "url":"https://www.xiaohongshu.com/search_result?keyword=毕业季租房避坑"},
    {"id":2,  "name":"重庆打工人生活vlog",       "heat":"756万",  "related":True,
     "reason":"重庆外来务工青年是嘛嘛公寓主要用户，日常居住类内容流量大且精准",
     "tip":"用「嘛嘛公寓一天」为主题，配合「6分钟到单位」「楼下就是地铁」等具体描写",
     "url":"https://www.xiaohongshu.com/search_result?keyword=重庆打工人vlog"},
    {"id":3,  "name":"月薪5000怎么在大城市生活", "heat":"1243万", "related":True,
     "reason":"价格敏感型用户高度关注，999元/月的定价极具竞争力",
     "tip":"做「月薪5000在重庆的真实支出清单」，把「嘛嘛公寓999/月」与市场均价对比",
     "url":"https://www.xiaohongshu.com/search_result?keyword=月薪5000在大城市"},
    {"id":4,  "name":"一个人住的小窝改造",       "heat":"892万",  "related":True,
     "reason":"20-30㎡户型正好契合这类内容，展示小空间改造布置可获大量收藏",
     "tip":"发「25㎡精装单间改造前后对比」，附布置tips，收藏率极高",
     "url":"https://www.xiaohongshu.com/search_result?keyword=一个人住小窝改造"},
    {"id":5,  "name":"重庆旅游超级攻略",         "heat":"2100万", "related":False,
     "reason":"","tip":"",
     "url":"https://www.xiaohongshu.com/search_result?keyword=重庆旅游攻略"},
    {"id":6,  "name":"攒钱计划100天打卡",        "heat":"678万",  "related":True,
     "reason":"年轻人存钱意识强，灵活租期+月付减少大额押金压力",
     "tip":"以「100天存钱计划」为题，把「省下的中介费用来存钱」自然植入",
     "url":"https://www.xiaohongshu.com/search_result?keyword=攒钱打卡"},
    {"id":7,  "name":"新手租房一定要看",         "heat":"1560万", "related":True,
     "reason":"搜索量极大的通用租房话题，零中介模式是很好的「正确示范」",
     "tip":"制作「租房新手避坑清单」，第4条引出「选保障性公寓如嘛嘛，省心安全」",
     "url":"https://www.xiaohongshu.com/search_result?keyword=新手租房"},
    {"id":8,  "name":"熙街商圈周边探店",         "heat":"234万",  "related":True,
     "reason":"精准地域话题，直接触达嘛嘛公寓周边潜在用户",
     "tip":"发「住在熙街商圈的日常 | 周边吃喝玩乐全攻略」，带出位置优势",
     "url":"https://www.xiaohongshu.com/search_result?keyword=熙街商圈"},
    {"id":9,  "name":"室内健身不花钱",           "heat":"445万",  "related":False,
     "reason":"","tip":"",
     "url":"https://www.xiaohongshu.com/search_result?keyword=室内健身"},
    {"id":10, "name":"年轻人的第一套「家」",      "heat":"893万",  "related":True,
     "reason":"情感共鸣话题，嘛嘛公寓「家的感觉」定位与之高度匹配",
     "tip":"写「在重庆漂了两年，终于有了自己的窝」，引发强烈共鸣和转发",
     "url":"https://www.xiaohongshu.com/search_result?keyword=年轻人第一套家"},
]

# ── 热点持久化：读写本地文件 ──────────────────────────────────
TOPICS_FILE = os.path.join(os.path.dirname(__file__), "hot_topics_saved.json")

def load_saved_topics():
    """从文件加载热点，失败则返回默认数据"""
    try:
        if os.path.exists(TOPICS_FILE):
            with open(TOPICS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("topics", DEFAULT_HOT_TOPICS), data.get("updated_at", "")
    except Exception:
        pass
    return DEFAULT_HOT_TOPICS, ""

def save_topics(topics, updated_at):
    """保存热点到文件"""
    try:
        with open(TOPICS_FILE, "w", encoding="utf-8") as f:
            json.dump({"topics": topics, "updated_at": updated_at}, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

# ── Session State ─────────────────────────────────────────────
for k, v in [("selected_topic",""), ("post_type","grass"),
             ("tone","轻松日常"), ("generated_post",""),
             ("hot_topics", None), ("hot_topics_updated_at", None)]:
    if k not in st.session_state:
        st.session_state[k] = v

if st.session_state.hot_topics is None:
    saved_topics, saved_at = load_saved_topics()
    st.session_state.hot_topics = saved_topics
    st.session_state.hot_topics_updated_at = saved_at

# ── 热点更新函数 ──────────────────────────────────────────────
def update_hot_topics():
    if not API_KEY:
        st.error("API Key 未配置，无法更新热点")
        return

    prompt = """你是小红书运营专家。请根据当前小红书平台的流行趋势，为「重庆嘛嘛公寓」生成10个热点话题。

公寓信息：月租999元起，熙街商圈地铁站旁，20-30㎡精装单间/复式，零中介费，灵活租期，月付，面向外来青年和应届毕业生。

要求：
- 10个话题，其中7-8个与嘛嘛公寓高度相关，2-3个热门但关联度低
- 热度数据用真实感的数字（如「xxx万」）
- 对相关话题给出具体运营建议

请严格按以下JSON格式返回，不要加任何说明文字，只返回JSON数组：
[
  {
    "name": "话题名称",
    "heat": "xxx万",
    "related": true,
    "reason": "为何与嘛嘛公寓相关的分析（相关时填写）",
    "tip": "具体的运营建议（相关时填写）"
  }
]
不相关的话题 reason 和 tip 填空字符串 ""。"""

    try:
        resp = requests.post(
            f"{API_URL}/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}", "content-type": "application/json"},
            json={"model": "claude-sonnet-4-6", "max_tokens": 2048,
                  "messages": [{"role": "user", "content": prompt}]},
            timeout=60,
        )
        if resp.status_code != 200:
            st.error(f"更新失败：{resp.status_code}")
            return

        content = resp.json()["choices"][0]["message"]["content"]
        # 提取JSON部分
        start = content.find("[")
        end = content.rfind("]") + 1
        if start == -1 or end == 0:
            st.error("更新失败：AI返回格式有误，请重试")
            return

        new_topics_raw = json.loads(content[start:end])
        new_topics = []
        for i, t in enumerate(new_topics_raw):
            new_topics.append({
                "id": i + 1,
                "name": t.get("name", ""),
                "heat": t.get("heat", ""),
                "related": t.get("related", False),
                "reason": t.get("reason", ""),
                "tip": t.get("tip", ""),
                "url": f"https://www.xiaohongshu.com/search_result?keyword={t.get('name','')}",
            })
        now_str = datetime.now().strftime("%Y年%m月%d日 %H:%M")
        st.session_state.hot_topics = new_topics
        st.session_state.hot_topics_updated_at = now_str
        save_topics(new_topics, now_str)

    except Exception as e:
        st.error(f"更新失败：{e}")

# ── 导航栏 ────────────────────────────────────────────────────
st.markdown("""
<div class="navbar">
  <div style="display:flex;align-items:center;gap:10px;">
    <div class="nav-logo">嘛</div>
    <div>
      <div class="nav-title">嘛嘛公寓 · 小红书运营工具</div>
      <div class="nav-sub">重庆熙街商圈 · AI帖子生成</div>
    </div>
  </div>
  <div style="background:#F0FDF4;border:1.5px solid #22c55e;color:#16a34a;
  padding:6px 16px;border-radius:20px;font-size:13px;font-weight:600;">
    ● 已就绪
  </div>
</div>
""", unsafe_allow_html=True)

# ── 图片美化函数 ──────────────────────────────────────────────
def beautify_image(img: Image.Image, style: str) -> Image.Image:
    img = img.convert("RGB")
    if style == "小清新":
        img = ImageEnhance.Brightness(img).enhance(1.15)
        img = ImageEnhance.Contrast(img).enhance(1.1)
        img = ImageEnhance.Color(img).enhance(0.9)
        img = ImageEnhance.Sharpness(img).enhance(1.3)
    elif style == "温暖橙":
        img = ImageEnhance.Brightness(img).enhance(1.1)
        img = ImageEnhance.Color(img).enhance(1.3)
        img = ImageEnhance.Contrast(img).enhance(1.05)
        r, g, b = img.split()
        r = ImageEnhance.Brightness(r).enhance(1.12)
        b = ImageEnhance.Brightness(b).enhance(0.88)
        img = Image.merge("RGB", (r, g, b))
    elif style == "复古胶片":
        img = ImageEnhance.Color(img).enhance(0.6)
        img = ImageEnhance.Brightness(img).enhance(1.05)
        img = ImageEnhance.Contrast(img).enhance(0.9)
        r, g, b = img.split()
        r = ImageEnhance.Brightness(r).enhance(1.08)
        b = ImageEnhance.Brightness(b).enhance(0.85)
        img = Image.merge("RGB", (r, g, b))
    elif style == "明亮通透":
        img = ImageEnhance.Brightness(img).enhance(1.25)
        img = ImageEnhance.Contrast(img).enhance(1.15)
        img = ImageEnhance.Color(img).enhance(1.1)
        img = ImageEnhance.Sharpness(img).enhance(1.4)
    return img

def add_polaroid_frame(img: Image.Image) -> Image.Image:
    """宝丽来白边框 + 日期戳"""
    w, h = img.size
    border = int(w * 0.05)
    bottom_border = int(w * 0.12)

    new_img = Image.new("RGB", (w + border * 2, h + border + bottom_border), "white")
    new_img.paste(img, (border, border))

    draw = ImageDraw.Draw(new_img)
    date_text = datetime.now().strftime("%Y.%m.%d")
    try:
        font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", int(w * 0.04))
    except:
        font = ImageFont.load_default()

    text_bbox = draw.textbbox((0, 0), date_text, font=font)
    text_w = text_bbox[2] - text_bbox[0]
    text_x = (new_img.width - text_w) // 2
    text_y = h + border + int(bottom_border * 0.3)
    draw.text((text_x, text_y), date_text, fill="#888888", font=font)

    return new_img

def add_info_stickers(img: Image.Image) -> Image.Image:
    """彩色信息贴纸"""
    img = img.copy()
    draw = ImageDraw.Draw(img)
    w, h = img.size

    stickers = [
        {"text": "💰 月租999起", "color": "#FFE5E5", "pos": (int(w*0.05), int(h*0.05))},
        {"text": "📍 熙街商圈", "color": "#E5F5FF", "pos": (int(w*0.05), int(h*0.12))},
        {"text": "✅ 零中介", "color": "#E5FFE5", "pos": (int(w*0.05), int(h*0.19))},
    ]

    try:
        font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", int(w * 0.035))
    except:
        font = ImageFont.load_default()

    for sticker in stickers:
        text = sticker["text"]
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]

        x, y = sticker["pos"]
        padding = int(w * 0.015)
        draw.rounded_rectangle(
            [x, y, x + text_w + padding * 2, y + text_h + padding * 2],
            radius=int(w * 0.015),
            fill=sticker["color"]
        )
        draw.text((x + padding, y + padding), text, fill="#333333", font=font)

    return img

def add_hand_drawn_doodles(img: Image.Image) -> Image.Image:
    """手绘涂鸦：圆圈、箭头、星星"""
    img = img.copy()
    draw = ImageDraw.Draw(img)
    w, h = img.size
    line_width = max(2, int(w * 0.005))

    # 右上角圆圈
    circle_x, circle_y = int(w * 0.75), int(h * 0.15)
    circle_r = int(w * 0.08)
    draw.ellipse(
        [circle_x - circle_r, circle_y - circle_r, circle_x + circle_r, circle_y + circle_r],
        outline="#FF6B7A", width=line_width
    )

    # 左下角箭头
    arrow_start = (int(w * 0.15), int(h * 0.85))
    arrow_end = (int(w * 0.25), int(h * 0.75))
    draw.line([arrow_start, arrow_end], fill="#FFB800", width=line_width)
    draw.polygon([
        arrow_end,
        (arrow_end[0] - int(w * 0.02), arrow_end[1] + int(w * 0.015)),
        (arrow_end[0] + int(w * 0.015), arrow_end[1] + int(w * 0.02))
    ], fill="#FFB800")

    # 右下角星星
    star_x, star_y = int(w * 0.85), int(h * 0.88)
    star_size = int(w * 0.025)
    draw.text((star_x, star_y), "⭐", fill="#FFD700", font=None)

    return img

def add_magazine_bar(img: Image.Image) -> Image.Image:
    """杂志风底部信息栏"""
    w, h = img.size
    bar_height = int(h * 0.15)

    new_img = Image.new("RGB", (w, h + bar_height), "white")
    new_img.paste(img, (0, 0))

    draw = ImageDraw.Draw(new_img)
    draw.rectangle([0, h, w, h + bar_height], fill="#FFF0F2")

    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", int(w * 0.05))
        font_sub = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", int(w * 0.03))
    except:
        font_title = font_sub = ImageFont.load_default()

    title = "嘛嘛公寓 · 重庆熙街商圈"
    subtitle = "月租999起 | 零中介 | 地铁房"

    title_bbox = draw.textbbox((0, 0), title, font=font_title)
    title_w = title_bbox[2] - title_bbox[0]
    draw.text(((w - title_w) // 2, h + int(bar_height * 0.2)), title, fill="#FF2442", font=font_title)

    sub_bbox = draw.textbbox((0, 0), subtitle, font=font_sub)
    sub_w = sub_bbox[2] - sub_bbox[0]
    draw.text(((w - sub_w) // 2, h + int(bar_height * 0.6)), subtitle, fill="#888888", font=font_sub)

    return new_img

def image_to_base64(img: Image.Image) -> str:
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return base64.b64encode(buf.getvalue()).decode("utf-8")

def image_to_bytes(img: Image.Image) -> bytes:
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return buf.getvalue()

def generate_image_caption(img: Image.Image, style: str, api_key: str, api_url: str) -> str:
    b64 = image_to_base64(img)
    prompt = f"""你是专业的小红书图文运营，请根据这张图片，为「重庆嘛嘛公寓」写一篇小红书帖子。

公寓信息：月租999元起，熙街商圈地铁站旁，20-30㎡精装单间/复式，零中介费，灵活租期，面向外来青年和应届毕业生。

图片美化风格：{style}
要求：第一人称，真实自然，200-300字，结尾带3-5个话题标签，有「闺蜜推荐」的亲切感，自然融入公寓优势。
直接输出帖子内容，不加任何说明语。"""

    resp = requests.post(
        f"{api_url}/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "content-type": "application/json"},
        json={
            "model": "gpt-4o",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
                {"type": "text", "text": prompt}
            ]}]
        },
        timeout=60,
    )
    if resp.status_code != 200:
        raise Exception(f"API错误：{resp.status_code}")
    return resp.json()["choices"][0]["message"]["content"]

# ── 提示词优化函数 ────────────────────────────────────────────
def optimize_image_prompt(user_input: str, scene_type: str, api_key: str, api_url: str) -> str:
    """用 Claude 把用户简单描述优化成专业图片生成提示词"""
    prompt = f"""你是专业的AI图片生成提示词工程师，专注于室内设计和公寓摄影风格。

用户想生成一张图片，场景类型：{scene_type}
用户的简单描述：{user_input}

请将用户描述扩写成高质量的图片生成提示词，要求：
1. 保留用户的核心意图
2. 补充专业摄影参数（光线、角度、色调等）
3. 加入小红书爆款风格描述
4. 适合公寓/室内场景
5. 只输出优化后的提示词，不加任何解释，不超过100字"""

    try:
        resp = requests.post(
            f"{api_url}/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "content-type": "application/json"},
            json={"model": "claude-sonnet-4-6", "max_tokens": 256,
                  "messages": [{"role": "user", "content": prompt}]},
            timeout=30,
        )
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"].strip()
    except Exception:
        pass
    return user_input  # 失败时返回原始输入

# ── AI 图片生成函数（火山引擎）──────────────────────────────
def volcengine_generate_from_text(description: str, api_key: str) -> str:
    """火山引擎 AI 文字生成图片"""
    if not api_key:
        raise Exception("火山引擎 API Key 未配置")

    url = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "doubao-seedream-5-0-260128",
        "prompt": description,
        "response_format": "url",
        "size": "2K"
    }

    resp = requests.post(url, headers=headers, json=data, timeout=60)
    if resp.status_code != 200:
        raise Exception(f"API错误：{resp.status_code} {resp.text}")

    result = resp.json()
    if "data" in result and len(result["data"]) > 0:
        return result["data"][0]["url"]
    else:
        raise Exception("生成失败：返回数据格式错误")

def volcengine_enhance_image(img: Image.Image, requirements: str, api_key: str) -> str:
    """火山引擎 AI 图片优化"""
    if not api_key:
        raise Exception("火山引擎 API Key 未配置")

    # 将图片转换为base64
    img_buffer = io.BytesIO()
    img.save(img_buffer, format="JPEG")
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
    img_data_url = f"data:image/jpeg;base64,{img_base64}"

    url = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "doubao-seedream-5-0-260128",
        "prompt": requirements,
        "image": img_data_url,
        "response_format": "url",
        "size": "2K"
    }

    resp = requests.post(url, headers=headers, json=data, timeout=60)
    if resp.status_code != 200:
        raise Exception(f"API错误：{resp.status_code} {resp.text}")

    result = resp.json()
    if "data" in result and len(result["data"]) > 0:
        return result["data"][0]["url"]
    else:
        raise Exception("生成失败：返回数据格式错误")

def volcengine_style_transfer(source_img: Image.Image, reference_img: Image.Image, api_key: str) -> str:
    """火山引擎 AI 风格模仿"""
    if not api_key:
        raise Exception("火山引擎 API Key 未配置")

    # 将两张图片都转换为base64
    source_buffer = io.BytesIO()
    source_img.save(source_buffer, format="JPEG")
    source_base64 = base64.b64encode(source_buffer.getvalue()).decode()
    source_data_url = f"data:image/jpeg;base64,{source_base64}"

    ref_buffer = io.BytesIO()
    reference_img.save(ref_buffer, format="JPEG")
    ref_base64 = base64.b64encode(ref_buffer.getvalue()).decode()
    ref_data_url = f"data:image/jpeg;base64,{ref_base64}"

    url = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "doubao-seedream-5-0-260128",
        "image": [source_data_url, ref_data_url],
        "sequential_image_generation": "disabled",
        "response_format": "url",
        "size": "2K"
    }

    resp = requests.post(url, headers=headers, json=data, timeout=60)
    if resp.status_code != 200:
        raise Exception(f"API错误：{resp.status_code} {resp.text}")

    result = resp.json()
    if "data" in result and len(result["data"]) > 0:
        return result["data"][0]["url"]
    else:
        raise Exception("生成失败：返回数据格式错误")

# ── 主布局（标签页切换）────────────────────────────────────────
tab_copy, tab_image = st.tabs(["✍️ 文案工具", "🎨 图片美化"])

# ══ 文案工具 ══════════════════════════════════════════════════
with tab_copy:
    left, right = st.columns([1, 1.3], gap="large")

# ══ 左列 ══════════════════════════════════════════════════════
with left:

    # 公寓信息
    st.markdown("""
    <div class="card">
      <div class="card-title">🏠 嘛嘛公寓
        <span style="margin-left:auto;background:#F0FDF4;color:#16a34a;
        font-size:11px;padding:3px 10px;border-radius:20px;font-weight:600;">重庆·熙街商圈</span>
      </div>
      <div class="apt-grid">
        <div class="apt-chip">💰 月租 <strong>999元起</strong></div>
        <div class="apt-chip">🚇 <strong>地铁站旁</strong></div>
        <div class="apt-chip">🏗️ <strong>528套</strong>精装公寓</div>
        <div class="apt-chip">✅ <strong>零中介费</strong></div>
        <div class="apt-chip">📐 20-30㎡ <strong>单/复式</strong></div>
        <div class="apt-chip">🎯 面向<strong>青年群体</strong></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # 热点话题标题行：标题 + 更新按钮 + 相关数量
    HOT_TOPICS = st.session_state.hot_topics
    related_count = sum(1 for t in HOT_TOPICS if t["related"])

    title_col, btn_col, badge_col = st.columns([2.2, 1.2, 1])
    with title_col:
        updated_at = st.session_state.hot_topics_updated_at or ""
        date_hint = f'<span style="font-size:11px;color:#bbb;font-weight:400;margin-left:8px;">更新于 {updated_at}</span>' if updated_at else '<span style="font-size:11px;color:#bbb;font-weight:400;margin-left:8px;">默认数据</span>'
        st.markdown(f'<div style="font-size:16px;font-weight:700;color:#1A1A1A;padding-top:6px;">🔥 小红书热点话题{date_hint}</div>',
                    unsafe_allow_html=True)
    with btn_col:
        if st.button("🔄 更新热点", key="update_topics", use_container_width=True):
            with st.spinner("热点更新中…"):
                update_hot_topics()
            st.rerun()
    with badge_col:
        st.markdown(f'<div style="background:#FFF0F2;color:#FF2442;font-size:11px;padding:6px 10px;border-radius:20px;font-weight:600;text-align:center;margin-top:2px;">{related_count} 个相关</div>',
                    unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom:8px'></div>", unsafe_allow_html=True)

    for i, t in enumerate(HOT_TOPICS):
        label = f"{'🥇' if i==0 else '🥈' if i==1 else '🥉' if i==2 else f'{i+1}.'} #{t['name']}  🔥{t['heat']}{'  ✅' if t['related'] else ''}"
        with st.expander(label):
            if t["related"]:
                st.markdown(f"**为何相关：** {t['reason']}")
                st.markdown(f"**运营建议：** {t['tip']}")
                c1, c2 = st.columns(2)
                c1.link_button("🔗 小红书查看", t["url"], use_container_width=True)
                if c2.button("✨ 用此热点", key=f"sel_{t['id']}", use_container_width=True):
                    st.session_state.selected_topic = t["name"]
                    st.rerun()
            else:
                st.caption("与嘛嘛公寓关联度较低，可作辅助参考。")
                st.link_button("🔗 小红书查看", t["url"])

    # 分析建议
    st.markdown('<div class="card-title" style="margin-top:8px;">💡 相关热点分析建议</div>',
                unsafe_allow_html=True)
    for t in HOT_TOPICS:
        if t["related"] and t["tip"]:
            st.markdown(f"""
            <div class="analysis-item">
              <div class="analysis-topic"># {t['name']} <span style="font-size:11px;font-weight:400;color:#FF8899">🔥{t['heat']}</span></div>
              <div class="analysis-text">{t['tip']}</div>
            </div>""", unsafe_allow_html=True)

# ══ 右列 ══════════════════════════════════════════════════════
with right:

    st.markdown('<div class="card-title">✍️ 帖子生成器</div>', unsafe_allow_html=True)

    # 已选热点
    tv = st.session_state.selected_topic
    st.markdown(f"""
    <div class="topic-bar">
      <span class="topic-bar-label">当前热点：</span>
      <span class="topic-bar-val" style="color:{'#FF2442' if tv else '#bbb'}">
        {'#'+tv if tv else '未选择，请从左侧点击「用此热点」'}
      </span>
    </div>""", unsafe_allow_html=True)

    new_topic = st.text_input("或手动输入热点关键词",
                               value=st.session_state.selected_topic,
                               placeholder="例如：毕业季租房避坑指南")
    if new_topic != st.session_state.selected_topic:
        st.session_state.selected_topic = new_topic

    st.markdown("<hr style='border-color:#F0E0E3;margin:14px 0'>", unsafe_allow_html=True)

    # 帖子类型
    st.markdown('<div class="sec-label">选择帖子类型</div>', unsafe_allow_html=True)
    type_info = {"grass":("🌱","种草帖","真实体验分享，吸引用户主动了解"),
                 "ad":   ("📢","商广帖","突出卖点，强调性价比和行动引导"),
                 "ops":  ("🎯","运营贴","互动引流为主，涨粉评论收藏转发"),
                 "official":("🏢","官号贴","官方视角发布，品牌形象展示")}
    cols = st.columns(4)
    for col, (key,(icon,name,desc)) in zip(cols, type_info.items()):
        is_on = st.session_state.post_type == key
        col.markdown(f"""
        <div class="type-card {'active' if is_on else ''}">
          <div class="tc-icon">{icon}</div>
          <div class="tc-name">{name}</div>
          <div class="tc-desc">{desc}</div>
        </div>""", unsafe_allow_html=True)
        if col.button(f"{'✓ ' if is_on else ''}选{name}", key=f"type_{key}",
                      use_container_width=True):
            st.session_state.post_type = key
            st.rerun()

    st.markdown("<hr style='border-color:#F0E0E3;margin:14px 0'>", unsafe_allow_html=True)

    # 写作风格
    st.markdown('<div class="sec-label">写作风格</div>', unsafe_allow_html=True)
    tone = st.radio("", ["轻松日常","干货专业","故事叙述","搞笑幽默"],
                    index=["轻松日常","干货专业","故事叙述","搞笑幽默"].index(st.session_state.tone),
                    horizontal=True, label_visibility="collapsed")
    st.session_state.tone = tone

    st.markdown("<hr style='border-color:#F0E0E3;margin:14px 0'>", unsafe_allow_html=True)

    # 关键词
    st.markdown('<div class="sec-label">补充关键词（多选）</div>', unsafe_allow_html=True)
    default_kws = ["月租999","零中介","熙街商圈","拎包入住","地铁房","重庆租房"]
    selected_kws = st.multiselect("", default_kws,
                                   default=["月租999","零中介","熙街商圈"],
                                   label_visibility="collapsed")
    custom_kw = st.text_input("自定义关键词（逗号分隔）",
                               placeholder="例如：青年公寓,保障房")
    if custom_kw:
        selected_kws += [k.strip() for k in custom_kw.split(",") if k.strip()]

    st.markdown("<hr style='border-color:#F0E0E3;margin:14px 0'>", unsafe_allow_html=True)

    # ── 新增：我的想法 ────────────────────────────────────────
    st.markdown('<div class="sec-label">💬 我的想法（选填）</div>', unsafe_allow_html=True)
    user_idea = st.text_area(
        "",
        placeholder="例如：想写一篇温暖的故事，讲第一次来重庆打工租到嘛嘛公寓的感受……",
        height=90,
        label_visibility="collapsed",
        key="user_idea"
    )

    st.markdown("<div style='margin-bottom:4px'></div>", unsafe_allow_html=True)

    # ── 新增：参考模板 ────────────────────────────────────────
    st.markdown('<div class="sec-label">📋 参考模板（选填，粘贴你喜欢的帖子风格）</div>', unsafe_allow_html=True)
    user_template = st.text_area(
        "",
        placeholder="把你喜欢的小红书帖子粘贴到这里，AI会参考它的风格和结构来写……",
        height=110,
        label_visibility="collapsed",
        key="user_template"
    )

    st.markdown("<hr style='border-color:#F0E0E3;margin:14px 0'>", unsafe_allow_html=True)

    # 生成按钮
    if st.button("✨ 一键生成帖子", use_container_width=True, type="primary"):
        if not API_KEY:
            st.error("API Key 未配置，请联系管理员")
        else:
            topic_part = f"围绕小红书热点话题「#{st.session_state.selected_topic}」" \
                         if st.session_state.selected_topic else "围绕重庆租房/青年住房话题"
            type_guide = {
                "grass": "写一篇小红书种草帖，第一人称真实分享视角，标题用emoji+感叹号+数字公式，自然植入嘛嘛公寓优势（不要硬广感），结尾带3-5个话题标签",
                "ad":    "写一篇小红书商业广告帖，标题直接点出最大卖点，列3-5个核心优势配emoji分隔，重点突出999元起和零中介，有明确引导行动",
                "ops":   "写一篇小红书互动运营贴，标题用疑问句引发互动欲望，设置评论钩子，用「你们觉得…」「评论区聊聊…」等互动语句",
                "official": "写一篇嘛嘛公寓官方账号发布的帖子，以品牌官方视角，语气亲切专业，可以是公寓动态、租客故事、生活理念分享等，展现品牌温度和价值观，结尾带官方话题标签"
            }

            # 拼接额外指令
            extra = ""
            if user_idea.strip():
                extra += f"\n\n运营者的想法和方向：{user_idea.strip()}"
            if user_template.strip():
                extra += f"\n\n请参考以下帖子的风格、语气和结构（不要抄内容，只学风格）：\n{user_template.strip()}"

            prompt = f"""你是专业的小红书文案运营，为「重庆嘛嘛公寓」创作一篇帖子。

公寓信息：月租999元起，熙街商圈地铁站旁，20-30㎡精装单间/复式，零中介费，灵活租期，月付，家具家电全配，配套休闲书屋和多功能活动大厅，面向外来青年和应届毕业生。

任务：{topic_part}，{type_guide[st.session_state.post_type]}

风格：{st.session_state.tone}
关键词：{' '.join(selected_kws)}{extra}

直接输出帖子内容，不加任何说明语，200-350字，有小红书「闺蜜推荐」的真实感。"""

            with st.spinner("✨ AI 正在创作中，请稍候…"):
                try:
                    resp = requests.post(
                        f"{API_URL}/v1/chat/completions",
                        headers={"Authorization": f"Bearer {API_KEY}", "content-type": "application/json"},
                        json={"model": "claude-sonnet-4-6", "max_tokens": 1024, "stream": True,
                              "messages": [{"role": "user", "content": prompt}]},
                        stream=True, timeout=120,
                    )
                    if resp.status_code != 200:
                        st.error(f"生成失败：{resp.status_code} {resp.text[:200]}")
                    else:
                        full_text = ""
                        for line in resp.iter_lines():
                            if not line:
                                continue
                            line = line.decode("utf-8") if isinstance(line, bytes) else line
                            if line.startswith("data: "):
                                data = line[6:]
                                if data.strip() == "[DONE]":
                                    break
                                try:
                                    c = json.loads(data).get("choices", [{}])[0].get("delta", {}).get("content", "")
                                    if c:
                                        full_text += c
                                except Exception:
                                    continue
                        if full_text:
                            st.session_state.generated_post = full_text
                        else:
                            st.error("生成失败：返回内容为空，请检查 API Key")
                except Exception as e:
                    st.error(f"生成失败：{e}")

    # ── 结果预览 ──────────────────────────────────────────────
    if st.session_state.generated_post:
        st.markdown("""
        <div class="preview-bar">
          <span class="dot" style="background:#FF5F5F"></span>
          <span class="dot" style="background:#FFB800"></span>
          <span class="dot" style="background:#22c55e"></span>
          <span style="font-size:11px;color:#999;margin-left:auto">小红书 · 帖子预览</span>
        </div>""", unsafe_allow_html=True)

        post_text = st.text_area(
            "", value=st.session_state.generated_post,
            height=300, label_visibility="collapsed",
            key="post_output"
        )
        char_count = len(st.session_state.generated_post)
        st.caption(f"共 **{char_count}** 字　·　复制：点击文本框 → Command+A 全选 → Command+C 复制")

        c1, c2 = st.columns(2)
        c1.download_button(
            "📥 下载为 txt 文件",
            data=post_text, file_name="小红书帖子.txt",
            mime="text/plain", use_container_width=True
        )
        if c2.button("🔄 重新生成", use_container_width=True):
            st.session_state.generated_post = ""
            st.rerun()

# ══ 图片美化 ══════════════════════════════════════════════════
with tab_image:
    st.markdown('<div class="card-title" style="margin-top:8px;">🎨 小红书图片美化</div>',
                unsafe_allow_html=True)
    st.markdown('<div style="font-size:13px;color:#888;margin-bottom:16px;">上传公寓或生活照片，一键美化成小红书风格，并自动生成配套文案。</div>',
                unsafe_allow_html=True)

    # 模式选择
    st.markdown('<div class="sec-label">选择美化模式</div>', unsafe_allow_html=True)
    mode = st.radio(
        "",
        ["🎨 传统美化（滤镜+装饰）", "🤖 AI 图片优化", "✨ AI 文字生成图片", "🎭 AI 风格模仿"],
        horizontal=True,
        label_visibility="collapsed",
        key="beautify_mode"
    )

    st.markdown("<hr style='border-color:#F0E0E3;margin:14px 0'>", unsafe_allow_html=True)

    img_left, img_right = st.columns([1, 1.2], gap="large")

    with img_left:
        # ═══ 传统美化模式 ═══
        if mode == "🎨 传统美化（滤镜+装饰）":
            st.markdown('<div class="sec-label">📷 上传照片</div>', unsafe_allow_html=True)
            uploaded_file = st.file_uploader(
                "", type=["jpg", "jpeg", "png"],
                label_visibility="collapsed",
                key="img_upload"
            )

            if uploaded_file:
                original_img = Image.open(uploaded_file)
                st.image(original_img, caption="原图", use_container_width=True)

                st.markdown("<hr style='border-color:#F0E0E3;margin:14px 0'>", unsafe_allow_html=True)
                st.markdown('<div class="sec-label">🎨 选择美化风格</div>', unsafe_allow_html=True)

                style_info = {
                    "小清新": "清透自然，色彩淡雅，适合室内/生活场景",
                    "温暖橙": "暖色调，温馨舒适，适合居家/傍晚场景",
                    "复古胶片": "低饱和，复古质感，适合文艺风格",
                    "明亮通透": "高亮高对比，清晰锐利，适合空间展示",
                }

                style_cols = st.columns(2)
                for i, (s, desc) in enumerate(style_info.items()):
                    with style_cols[i % 2]:
                        st.markdown(f"""
                        <div style="background:#FFF0F2;border:1.5px solid #FFD0D8;border-radius:10px;
                        padding:10px 12px;margin-bottom:8px;">
                          <div style="font-size:13px;font-weight:700;color:#FF2442;">{s}</div>
                          <div style="font-size:11px;color:#888;margin-top:3px;">{desc}</div>
                        </div>""", unsafe_allow_html=True)

                img_style = st.radio(
                    "选择风格",
                    list(style_info.keys()),
                    horizontal=True,
                    label_visibility="collapsed",
                    key="img_style"
                )

                st.markdown("<hr style='border-color:#F0E0E3;margin:14px 0'>", unsafe_allow_html=True)
                st.markdown('<div class="sec-label">✨ 装饰效果（可多选）</div>', unsafe_allow_html=True)

                deco_options = st.multiselect(
                    "",
                    ["📸 宝丽来边框", "🏷️ 信息贴纸", "✏️ 手绘涂鸦", "📰 杂志排版"],
                    default=[],
                    label_visibility="collapsed",
                    key="deco_options"
                )

                st.markdown("<hr style='border-color:#F0E0E3;margin:14px 0'>", unsafe_allow_html=True)

                gen_caption = st.checkbox("✍️ 同时生成配套文案", value=True, key="gen_caption")

                if st.button("✨ 一键美化", use_container_width=True, type="primary"):
                    with st.spinner("🎨 图片美化中，请稍候…"):
                        beautified = beautify_image(original_img, img_style)

                        # 应用装饰效果
                        if "📸 宝丽来边框" in deco_options:
                            beautified = add_polaroid_frame(beautified)
                        if "🏷️ 信息贴纸" in deco_options:
                            beautified = add_info_stickers(beautified)
                        if "✏️ 手绘涂鸦" in deco_options:
                            beautified = add_hand_drawn_doodles(beautified)
                        if "📰 杂志排版" in deco_options:
                            beautified = add_magazine_bar(beautified)

                        st.session_state["beautified_img"] = beautified
                        st.session_state["beautified_style"] = img_style

                    if gen_caption and API_KEY:
                        with st.spinner("✍️ AI 生成文案中…"):
                            try:
                                caption = generate_image_caption(beautified, img_style, API_KEY, API_URL)
                                st.session_state["img_caption"] = caption
                            except Exception as e:
                                st.session_state["img_caption"] = ""
                                st.warning(f"文案生成失败：{e}")
                    elif gen_caption and not API_KEY:
                        st.warning("API Key 未配置，跳过文案生成")

                    st.rerun()

        # ═══ AI 图片优化模式 ═══
        elif mode == "🤖 AI 图片优化":
            st.markdown('<div class="sec-label">📷 上传照片</div>', unsafe_allow_html=True)
            uploaded_file = st.file_uploader(
                "", type=["jpg", "jpeg", "png"],
                label_visibility="collapsed",
                key="ai_opt_upload"
            )

            if uploaded_file:
                original_img = Image.open(uploaded_file)
                st.image(original_img, caption="原图", use_container_width=True)

                st.markdown("<hr style='border-color:#F0E0E3;margin:14px 0'>", unsafe_allow_html=True)
                st.markdown('<div class="sec-label">✍️ 优化要求</div>', unsafe_allow_html=True)

                requirements = st.text_area(
                    "",
                    placeholder="例如：让房间更明亮温馨，增强阳光感，突出空间感...",
                    height=100,
                    label_visibility="collapsed",
                    key="ai_requirements"
                )

                if st.button("🤖 AI 优化图片", use_container_width=True, type="primary"):
                    if not VOLCENGINE_API_KEY:
                        st.error("火山引擎 API Key 未配置")
                    elif not requirements.strip():
                        st.warning("请填写优化要求")
                    else:
                        with st.spinner("🤖 AI 正在优化图片，请稍候（约10-30秒）..."):
                            try:
                                if API_KEY:
                                    optimized_req = optimize_image_prompt(requirements, "公寓图片优化", API_KEY, API_URL)
                                else:
                                    optimized_req = requirements
                                img_url = volcengine_enhance_image(original_img, optimized_req, VOLCENGINE_API_KEY)
                                if img_url:
                                    st.session_state["ai_result_url"] = img_url
                                    st.session_state["ai_mode"] = "优化"
                                    st.rerun()
                                else:
                                    st.error("AI 生成失败，请重试")
                            except Exception as e:
                                st.error(f"AI 生成失败：{e}")

        # ═══ AI 文字生成图片模式 ═══
        elif mode == "✨ AI 文字生成图片":
            st.markdown('<div class="sec-label">✍️ 描述你想要的图片</div>', unsafe_allow_html=True)

            description = st.text_area(
                "",
                placeholder="例如：一个温馨的单间公寓，阳光从窗户洒进来，现代简约风格，有床、书桌和小沙发...",
                height=150,
                label_visibility="collapsed",
                key="ai_description"
            )

            st.markdown("<hr style='border-color:#F0E0E3;margin:14px 0'>", unsafe_allow_html=True)
            st.markdown('<div style="font-size:12px;color:#888;line-height:1.6;">💡 提示：描述越详细，生成效果越好。可以包含：房间类型、光线、色调、家具、氛围等。</div>', unsafe_allow_html=True)

            if st.button("✨ AI 生成图片", use_container_width=True, type="primary"):
                if not VOLCENGINE_API_KEY:
                    st.error("火山引擎 API Key 未配置")
                elif not description.strip():
                    st.warning("请填写图片描述")
                else:
                    with st.spinner("✨ AI 正在生成图片，请稍候（约10-30秒）..."):
                        try:
                            if API_KEY:
                                optimized = optimize_image_prompt(description, "文字生成公寓图片", API_KEY, API_URL)
                            else:
                                optimized = description
                            img_url = volcengine_generate_from_text(optimized, VOLCENGINE_API_KEY)
                            if img_url:
                                st.session_state["ai_result_url"] = img_url
                                st.session_state["ai_mode"] = "生成"
                                st.rerun()
                            else:
                                st.error("AI 生成失败，请重试")
                        except Exception as e:
                            st.error(f"AI 生成失败：{e}")

        # ═══ AI 风格模仿模式 ═══
        elif mode == "🎭 AI 风格模仿":
            st.markdown('<div class="sec-label">📷 上传原图</div>', unsafe_allow_html=True)
            source_file = st.file_uploader(
                "", type=["jpg", "jpeg", "png"],
                label_visibility="collapsed",
                key="ai_source_upload"
            )

            if source_file:
                source_img = Image.open(source_file)
                st.image(source_img, caption="原图", use_container_width=True)

            st.markdown("<hr style='border-color:#F0E0E3;margin:14px 0'>", unsafe_allow_html=True)
            st.markdown('<div class="sec-label">🎨 上传参考风格图</div>', unsafe_allow_html=True)

            reference_file = st.file_uploader(
                "", type=["jpg", "jpeg", "png"],
                label_visibility="collapsed",
                key="ai_reference_upload"
            )

            if reference_file:
                reference_img = Image.open(reference_file)
                st.image(reference_img, caption="参考风格", use_container_width=True)

            st.markdown("<hr style='border-color:#F0E0E3;margin:14px 0'>", unsafe_allow_html=True)
            st.markdown('<div style="font-size:12px;color:#888;line-height:1.6;">💡 提示：AI 会模仿参考图的色调、光线和氛围，应用到原图上。</div>', unsafe_allow_html=True)

            if st.button("🎭 AI 风格转换", use_container_width=True, type="primary"):
                if not VOLCENGINE_API_KEY:
                    st.error("火山引擎 API Key 未配置")
                elif not source_file:
                    st.warning("请上传原图")
                elif not reference_file:
                    st.warning("请上传参考风格图")
                else:
                    with st.spinner("🎭 AI 正在转换风格，请稍候（约10-30秒）..."):
                        try:
                            img_url = volcengine_style_transfer(source_img, reference_img, VOLCENGINE_API_KEY)
                            if img_url:
                                st.session_state["ai_result_url"] = img_url
                                st.session_state["ai_mode"] = "风格转换"
                                st.rerun()
                            else:
                                st.error("AI 生成失败，请重试")
                        except Exception as e:
                            st.error(f"AI 生成失败：{e}")

    with img_right:
        # 显示 AI 生成结果
        if "ai_result_url" in st.session_state and st.session_state["ai_result_url"]:
            ai_mode = st.session_state.get("ai_mode", "AI")
            st.markdown(f'<div class="sec-label">✅ {ai_mode}结果</div>', unsafe_allow_html=True)

            try:
                import requests
                response = requests.get(st.session_state["ai_result_url"])
                ai_img = Image.open(io.BytesIO(response.content))
                st.image(ai_img, use_container_width=True)

                img_bytes = image_to_bytes(ai_img)
                c1, c2 = st.columns(2)
                c1.download_button(
                    "📥 下载图片",
                    data=img_bytes,
                    file_name=f"嘛嘛公寓_AI{ai_mode}.jpg",
                    mime="image/jpeg",
                    use_container_width=True
                )
                if c2.button("🔄 重新生成", use_container_width=True, key="regen_ai"):
                    st.session_state["ai_result_url"] = None
                    st.rerun()
            except Exception as e:
                st.error(f"图片加载失败：{e}")

        # 显示传统美化结果
        elif "beautified_img" in st.session_state and st.session_state["beautified_img"] is not None:
            st.markdown(f'<div class="sec-label">✅ 美化结果 · {st.session_state.get("beautified_style","")}</div>',
                        unsafe_allow_html=True)
            st.image(st.session_state["beautified_img"], use_container_width=True)

            img_bytes = image_to_bytes(st.session_state["beautified_img"])
            st.download_button(
                "📥 下载美化图片",
                data=img_bytes,
                file_name=f"嘛嘛公寓_{st.session_state.get('beautified_style','')}.jpg",
                mime="image/jpeg",
                use_container_width=True
            )

            if st.session_state.get("img_caption"):
                st.markdown("<hr style='border-color:#F0E0E3;margin:14px 0'>", unsafe_allow_html=True)
                st.markdown('<div class="sec-label">✍️ AI 配套文案</div>', unsafe_allow_html=True)
                st.markdown("""
                <div class="preview-bar">
                  <span class="dot" style="background:#FF5F5F"></span>
                  <span class="dot" style="background:#FFB800"></span>
                  <span class="dot" style="background:#22c55e"></span>
                  <span style="font-size:11px;color:#999;margin-left:auto">小红书 · 图文文案</span>
                </div>""", unsafe_allow_html=True)

                caption_text = st.text_area(
                    "", value=st.session_state["img_caption"],
                    height=260, label_visibility="collapsed",
                    key="caption_output"
                )
                c1, c2 = st.columns(2)
                c1.download_button(
                    "📥 下载文案",
                    data=caption_text,
                    file_name="小红书图文文案.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                if c2.button("🔄 重新生成文案", use_container_width=True, key="regen_caption"):
                    st.session_state["img_caption"] = ""
                    st.rerun()
        else:
            st.markdown("""
            <div style="height:300px;display:flex;align-items:center;justify-content:center;
            flex-direction:column;gap:12px;background:#FFF8F9;border-radius:16px;
            border:2px dashed #FFD0D8;">
              <div style="font-size:40px;">🖼️</div>
              <div style="font-size:14px;color:#bbb;">上传图片后，美化结果会显示在这里</div>
            </div>""", unsafe_allow_html=True)
