import streamlit as st
import requests
import json
import os
from datetime import datetime

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
            json={"model": "gpt-5", "max_tokens": 2048,
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

# ── 主布局 ────────────────────────────────────────────────────
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
                 "ops":  ("🎯","运营贴","互动引流为主，涨粉评论收藏转发")}
    cols = st.columns(3)
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
                "ops":   "写一篇小红书互动运营贴，标题用疑问句引发互动欲望，设置评论钩子，用「你们觉得…」「评论区聊聊…」等互动语句"
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
                        json={"model": "gpt-5", "max_tokens": 1024, "stream": True,
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
