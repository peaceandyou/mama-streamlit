import streamlit as st
import anthropic

# ── 页面配置 ──────────────────────────────────────────────────
st.set_page_config(
    page_title="嘛嘛公寓 · 小红书运营工具",
    page_icon="🏠",
    layout="wide"
)

# ── 全局样式注入 ──────────────────────────────────────────────
st.markdown("""
<style>
/* 隐藏 Streamlit 默认元素 */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="stToolbar"] {display: none !important;}
[data-testid="stDecoration"] {display: none !important;}
.stDeployButton {display: none !important;}
[data-testid="stStatusWidget"] {display: none !important;}

/* 背景色 */
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main { background: #FDF6F7 !important; }
.main .block-container {
    padding-top: 0 !important;
    padding-bottom: 40px !important;
    max-width: 1280px !important;
}

/* 顶部导航栏 */
.navbar {
    background: white;
    border-bottom: 1px solid #F0E0E3;
    padding: 0 28px;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 2px 12px rgba(255,36,66,0.06);
    margin: 0 -28px 28px -28px;
    position: sticky;
    top: 0;
    z-index: 999;
}
.nav-left { display: flex; align-items: center; gap: 10px; }
.nav-logo {
    width: 36px; height: 36px;
    background: #FF2442;
    border-radius: 10px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 18px; color: white; font-weight: 900;
}
.nav-title { font-size: 17px; font-weight: 700; color: #1A1A1A; }
.nav-sub { font-size: 12px; color: #999; margin-top: 1px; }

/* 卡片 */
.card {
    background: white;
    border-radius: 16px;
    padding: 20px;
    border: 1px solid #F0E0E3;
    box-shadow: 0 4px 20px rgba(255,36,66,0.07);
    margin-bottom: 16px;
}
.card-title {
    font-size: 16px; font-weight: 700;
    color: #1A1A1A; margin-bottom: 14px;
    display: flex; align-items: center; gap: 6px;
}

/* 公寓信息网格 */
.apt-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.apt-chip {
    display: flex; align-items: center; gap: 6px;
    padding: 8px 10px;
    background: #FFF0F2;
    border-radius: 10px;
    font-size: 12px; color: #555;
}
.apt-chip strong { color: #1A1A1A; }

/* 热点列表 */
.hot-item {
    border: 1.5px solid #F0E0E3;
    border-radius: 10px;
    margin-bottom: 6px;
    background: white;
    overflow: hidden;
    cursor: pointer;
    transition: border-color 0.2s;
}
.hot-header {
    display: flex; align-items: center;
    gap: 10px; padding: 10px 12px;
}
.hot-rank {
    width: 22px; height: 22px;
    border-radius: 6px;
    font-size: 12px; font-weight: 800;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0; color: white;
}
.rank-1 { background: #FF2442; }
.rank-2 { background: #FF6B35; }
.rank-3 { background: #FFB800; color: #333; }
.rank-n { background: #F0F0F0; color: #999; }
.hot-name { flex: 1; font-size: 13px; font-weight: 600; color: #1A1A1A; }
.hot-heat { font-size: 11px; color: #999; }
.related-badge {
    font-size: 10px; padding: 2px 7px;
    border-radius: 10px;
    background: #FFF0F2; color: #FF2442; font-weight: 700;
}
.hot-detail {
    padding: 0 12px 12px 44px;
    font-size: 12px; color: #555; line-height: 1.7;
    border-top: 1px solid #F8F0F1;
    display: none;
}

/* 分析建议 */
.analysis-item {
    background: #FFF0F2;
    border: 1px solid #FFD0D8;
    border-radius: 10px;
    padding: 12px;
    margin-bottom: 10px;
}
.analysis-topic { font-size: 13px; font-weight: 700; color: #FF2442; margin-bottom: 4px; }
.analysis-text { font-size: 12px; color: #555; line-height: 1.6; }

/* 类型选择卡片 */
.type-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 4px; }
.type-card {
    border: 2px solid #F0E0E3; border-radius: 10px;
    padding: 14px; background: white; cursor: pointer;
    transition: all 0.2s;
}
.type-card:hover, .type-card.active {
    border-color: #FF2442; background: #FFF0F2;
}
.type-card.active .tc-name { color: #FF2442; }
.tc-icon { font-size: 24px; margin-bottom: 6px; }
.tc-name { font-size: 14px; font-weight: 700; color: #1A1A1A; margin-bottom: 3px; }
.tc-desc { font-size: 11px; color: #999; line-height: 1.4; }

/* 关键词标签 */
.kw-wrap { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 8px; }
.kw-tag {
    padding: 5px 13px; border-radius: 16px;
    font-size: 12px; font-weight: 600;
    border: 1.5px solid #E0E0E0;
    background: white; color: #555; cursor: pointer;
    transition: all 0.15s;
}
.kw-tag.on { background: #FFF0F2; color: #FF2442; border-color: #FF2442; }

/* 生成按钮 */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #FF2442 0%, #FF6B7A 100%) !important;
    color: white !important; border: none !important;
    border-radius: 14px !important;
    font-size: 16px !important; font-weight: 700 !important;
    padding: 14px 0 !important;
    width: 100% !important;
    box-shadow: 0 4px 16px rgba(255,36,66,0.25) !important;
    transition: all 0.2s !important;
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(255,36,66,0.35) !important;
}

/* 预览区 */
.preview-wrap {
    background: white;
    border-radius: 16px;
    border: 1.5px solid #F0E0E3;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(255,36,66,0.07);
}
.preview-bar {
    background: #F8F8F8;
    padding: 8px 16px;
    display: flex; align-items: center; gap: 6px;
    border-bottom: 1px solid #F0E0E3;
}
.dot { width:10px; height:10px; border-radius:50%; display:inline-block; }

/* 段落标签 */
.sec-label {
    font-size: 11px; font-weight: 700; color: #bbb;
    letter-spacing: 0.06em; text-transform: uppercase;
    margin-bottom: 8px;
}

/* topic bar */
.topic-bar {
    display: flex; align-items: center; gap: 10px;
    padding: 11px 16px;
    background: #FFF0F2;
    border-radius: 10px;
    border: 1.5px dashed #FF8899;
    margin-bottom: 14px;
}
.topic-bar-label { font-size: 12px; color: #bbb; white-space: nowrap; }
.topic-bar-val { font-size: 13px; font-weight: 700; color: #FF2442; flex: 1; }

/* expander 覆盖 */
div[data-testid="stExpander"] {
    border: 1.5px solid #F0E0E3 !important;
    border-radius: 10px !important;
    background: white !important;
    margin-bottom: 6px !important;
}
div[data-testid="stExpander"] summary {
    font-weight: 600 !important;
}

/* metric */
[data-testid="stMetric"] {
    background: #FFF8F9; border-radius: 10px; padding: 8px 12px;
}
[data-testid="stMetricValue"] { color: #FF2442 !important; font-size: 22px !important; }
[data-testid="stMetricLabel"] { color: #999 !important; font-size: 12px !important; }

/* 输入框 */
.stTextInput > div > div > input, .stTextArea > div > textarea {
    border-radius: 12px !important;
    border-color: #F0E0E3 !important;
    font-size: 14px !important;
}
.stTextInput > div > div > input:focus, .stTextArea > div > textarea:focus {
    border-color: #FF2442 !important;
    box-shadow: 0 0 0 2px rgba(255,36,66,0.1) !important;
}

/* multiselect */
[data-testid="stMultiSelect"] span[data-baseweb="tag"] {
    background: #FFF0F2 !important;
    color: #FF2442 !important;
    border-radius: 12px !important;
}

/* radio */
[data-testid="stRadio"] label { font-size: 13px !important; }
</style>
""", unsafe_allow_html=True)

# ── 密码保护 ──────────────────────────────────────────────────
CORRECT_PWD = st.secrets.get("password", "xiaohu2026")
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("""
    <div style="min-height:100vh;background:linear-gradient(145deg,#FF2442,#FF6B7A,#FFB0BB);
    display:flex;align-items:center;justify-content:center;">
    </div>""", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.1, 1])
    with col:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background:white;border-radius:24px;padding:36px 32px;
        box-shadow:0 24px 60px rgba(255,36,66,0.2);text-align:center;">
          <div style="width:64px;height:64px;background:linear-gradient(135deg,#FF2442,#FF6B7A);
          border-radius:20px;display:flex;align-items:center;justify-content:center;
          font-size:32px;font-weight:900;color:white;margin:0 auto 16px;">嘛</div>
          <div style="font-size:20px;font-weight:800;margin-bottom:4px;">嘛嘛公寓运营工具</div>
          <div style="font-size:13px;color:#999;margin-bottom:24px;">请输入访问密码以继续使用</div>
        </div>
        """, unsafe_allow_html=True)
        pwd = st.text_input("", type="password", placeholder="请输入密码…", label_visibility="collapsed")
        if st.button("进 入", use_container_width=True):
            if pwd == CORRECT_PWD:
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("密码错误，请重新输入")
    st.stop()

# ── 配置 ──────────────────────────────────────────────────────
API_KEY = st.secrets.get("api_key", "")
API_URL = st.secrets.get("api_url", "https://code.newcli.com/claude")

# ── 热点数据 ──────────────────────────────────────────────────
HOT_TOPICS = [
    {"id":1,  "name":"毕业季租房避坑指南",      "heat":"982万",  "related":True,
     "reason":"毕业生是嘛嘛公寓的核心目标人群，零中介、月付模式正好戳中他们的痛点",
     "tip":"以「第一次租房的你」为角色切入，分享从踩坑到入住嘛嘛公寓的真实经历，重点突出「零中介省了多少钱」的数字对比",
     "url":"https://www.xiaohongshu.com/search_result?keyword=毕业季租房避坑"},
    {"id":2,  "name":"重庆打工人生活vlog",       "heat":"756万",  "related":True,
     "reason":"重庆外来务工青年是嘛嘛公寓主要用户，日常居住类内容流量大且精准",
     "tip":"用「嘛嘛公寓一天」为主题，展示早起、通勤、公共空间等生活场景，配合「6分钟到单位」等具体描写",
     "url":"https://www.xiaohongshu.com/search_result?keyword=重庆打工人vlog"},
    {"id":3,  "name":"月薪5000怎么在大城市生活", "heat":"1243万", "related":True,
     "reason":"价格敏感型用户高度关注，999元/月的定价极具竞争力，是绝佳的种草切入点",
     "tip":"做一期「月薪5000在重庆的真实支出清单」，把租房项明确写出「嘛嘛公寓999/月」并与市场均价对比",
     "url":"https://www.xiaohongshu.com/search_result?keyword=月薪5000在大城市"},
    {"id":4,  "name":"一个人住的小窝改造",       "heat":"892万",  "related":True,
     "reason":"20-30㎡的户型正好契合这类内容，展示小空间改造布置可获得大量收藏",
     "tip":"发一篇「25㎡精装单间改造前后对比」，展示入住的变化，附上布置tips，收藏率极高",
     "url":"https://www.xiaohongshu.com/search_result?keyword=一个人住小窝改造"},
    {"id":5,  "name":"重庆旅游超级攻略",         "heat":"2100万", "related":False,
     "reason":"","tip":"",
     "url":"https://www.xiaohongshu.com/search_result?keyword=重庆旅游攻略"},
    {"id":6,  "name":"攒钱计划100天打卡",        "heat":"678万",  "related":True,
     "reason":"年轻人存钱意识强，灵活租期+月付模式减少大额押金压力，可与攒钱话题联动",
     "tip":"以「我的100天存钱计划」为题，把住在嘛嘛公寓「省下的中介费用来存钱」作为亮点植入",
     "url":"https://www.xiaohongshu.com/search_result?keyword=攒钱打卡"},
    {"id":7,  "name":"新手租房一定要看",         "heat":"1560万", "related":True,
     "reason":"搜索量极大的通用租房话题，嘛嘛公寓零中介模式是很好的「正确示范」内容",
     "tip":"制作「租房新手避坑清单」，第4条自然引出「选保障性公寓如嘛嘛，省心又安全」",
     "url":"https://www.xiaohongshu.com/search_result?keyword=新手租房"},
    {"id":8,  "name":"熙街商圈周边探店",         "heat":"234万",  "related":True,
     "reason":"精准地域话题，直接触达嘛嘛公寓周边潜在用户群体",
     "tip":"发一篇「住在熙街商圈的日常 | 周边吃喝玩乐全攻略」，带出嘛嘛公寓的位置优势",
     "url":"https://www.xiaohongshu.com/search_result?keyword=熙街商圈"},
    {"id":9,  "name":"室内健身不花钱",           "heat":"445万",  "related":False,
     "reason":"","tip":"",
     "url":"https://www.xiaohongshu.com/search_result?keyword=室内健身"},
    {"id":10, "name":"年轻人的第一套「家」",      "heat":"893万",  "related":True,
     "reason":"情感共鸣话题，嘛嘛公寓的「家的感觉」定位与之高度匹配",
     "tip":"以情感叙事为主线，写「在重庆漂了两年，终于有了自己的窝」，引发强烈共鸣和转发",
     "url":"https://www.xiaohongshu.com/search_result?keyword=年轻人第一套家"},
]

# ── 自定义导航栏 ──────────────────────────────────────────────
st.markdown("""
<div class="navbar">
  <div class="nav-left">
    <div class="nav-logo">嘛</div>
    <div>
      <div class="nav-title">嘛嘛公寓 · 小红书运营工具</div>
      <div class="nav-sub">重庆熙街商圈 · AI帖子生成</div>
    </div>
  </div>
  <div style="background:#FFF0F2;border:1.5px solid #FF2442;color:#FF2442;
  padding:6px 16px;border-radius:20px;font-size:13px;font-weight:600;">
    ✅ 已就绪
  </div>
</div>
""", unsafe_allow_html=True)

# ── Session State 初始化 ──────────────────────────────────────
if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = ""
if "post_type" not in st.session_state:
    st.session_state.post_type = "grass"
if "generated_post" not in st.session_state:
    st.session_state.generated_post = ""
if "active_kws" not in st.session_state:
    st.session_state.active_kws = {"月租999", "零中介", "熙街商圈"}

# ── 主布局 ────────────────────────────────────────────────────
left, right = st.columns([1, 1.3], gap="large")

# ╔══════════════════════╗
# ║       左列            ║
# ╚══════════════════════╝
with left:

    # 公寓信息卡片
    st.markdown("""
    <div class="card">
      <div class="card-title">🏠 嘛嘛公寓
        <span style="margin-left:auto;background:#F0FDF4;color:#16a34a;
        font-size:11px;padding:3px 10px;border-radius:20px;font-weight:600;">重庆·熙街商圈</span>
      </div>
      <div class="apt-grid">
        <div class="apt-chip">💰 月租 <strong>999元起</strong></div>
        <div class="apt-chip">🚇 <strong>地铁站旁</strong></div>
        <div class="apt-chip">🏗️ <strong>528套</strong> 精装公寓</div>
        <div class="apt-chip">✅ <strong>零中介费</strong></div>
        <div class="apt-chip">📐 20-30㎡ <strong>单间/复式</strong></div>
        <div class="apt-chip">🎯 面向 <strong>青年群体</strong></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # 热点话题
    related_count = sum(1 for t in HOT_TOPICS if t["related"])
    st.markdown(f"""
    <div class="card-title" style="margin-bottom:10px;">
      🔥 小红书热点话题
      <span style="margin-left:auto;background:#FFF0F2;color:#FF2442;
      font-size:11px;padding:3px 10px;border-radius:20px;font-weight:600;">{related_count} 个相关</span>
    </div>
    """, unsafe_allow_html=True)

    rank_colors = ["rank-1","rank-2","rank-3"] + ["rank-n"]*7

    for i, t in enumerate(HOT_TOPICS):
        related_html = '<span class="related-badge">相关</span>' if t["related"] else ""
        label = f"{'🥇' if i==0 else '🥈' if i==1 else '🥉' if i==2 else f'{i+1}'} #{t['name']}  🔥{t['heat']}  {'✅' if t['related'] else ''}"

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
                st.caption("本话题与嘛嘛公寓关联度较低，可作辅助参考。")
                st.link_button("🔗 小红书查看", t["url"])

    # 分析建议
    st.markdown("""
    <div class="card-title" style="margin-top:8px;margin-bottom:10px;">
      💡 相关热点分析建议
    </div>
    """, unsafe_allow_html=True)

    for t in HOT_TOPICS:
        if t["related"]:
            st.markdown(f"""
            <div class="analysis-item">
              <div class="analysis-topic"># {t['name']} <span style="font-size:11px;font-weight:400;color:#FF8899">🔥{t['heat']}</span></div>
              <div class="analysis-text">{t['tip']}</div>
            </div>
            """, unsafe_allow_html=True)

# ╔══════════════════════╗
# ║       右列            ║
# ╚══════════════════════╝
with right:

    st.markdown('<div class="card-title">✍️ 帖子生成器</div>', unsafe_allow_html=True)

    # 已选热点显示
    topic_val = st.session_state.selected_topic or "未选择，请从左侧点击「用此热点」自动填入"
    topic_color = "#FF2442" if st.session_state.selected_topic else "#bbb"
    st.markdown(f"""
    <div class="topic-bar">
      <span class="topic-bar-label">当前热点：</span>
      <span class="topic-bar-val" style="color:{topic_color}">
        {'#' + st.session_state.selected_topic if st.session_state.selected_topic else topic_val}
      </span>
    </div>
    """, unsafe_allow_html=True)

    custom_topic = st.text_input("或手动输入热点关键词", value=st.session_state.selected_topic,
                                  placeholder="例如：毕业季租房避坑指南", label_visibility="visible")
    if custom_topic != st.session_state.selected_topic:
        st.session_state.selected_topic = custom_topic

    st.markdown("<hr style='border-color:#F0E0E3;margin:14px 0'>", unsafe_allow_html=True)

    # 帖子类型
    st.markdown('<div class="sec-label">选择帖子类型</div>', unsafe_allow_html=True)
    type_labels = {
        "grass": ("🌱", "种草帖", "真实体验分享，吸引用户主动了解"),
        "ad":    ("📢", "商广帖", "突出卖点，强调性价比和行动引导"),
        "ops":   ("🎯", "运营贴", "互动引流为主，涨粉评论收藏转发"),
    }
    tc1, tc2, tc3 = st.columns(3)
    for col, (key, (icon, name, desc)) in zip([tc1, tc2, tc3], type_labels.items()):
        is_active = st.session_state.post_type == key
        active_cls = "active" if is_active else ""
        with col:
            st.markdown(f"""
            <div class="type-card {active_cls}" onclick="">
              <div class="tc-icon">{icon}</div>
              <div class="tc-name">{name}</div>
              <div class="tc-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"选择{name}", key=f"type_{key}", use_container_width=True,
                         type="primary" if is_active else "secondary"):
                st.session_state.post_type = key
                st.rerun()

    st.markdown("<hr style='border-color:#F0E0E3;margin:14px 0'>", unsafe_allow_html=True)

    # 写作风格
    st.markdown('<div class="sec-label">写作风格</div>', unsafe_allow_html=True)
    tones = ["轻松日常", "干货专业", "故事叙述", "搞笑幽默"]
    if "tone" not in st.session_state:
        st.session_state.tone = "轻松日常"
    tone_cols = st.columns(4)
    for col, t in zip(tone_cols, tones):
        is_on = st.session_state.tone == t
        with col:
            if st.button(t, key=f"tone_{t}", use_container_width=True,
                         type="primary" if is_on else "secondary"):
                st.session_state.tone = t
                st.rerun()

    st.markdown("<hr style='border-color:#F0E0E3;margin:14px 0'>", unsafe_allow_html=True)

    # 关键词
    st.markdown('<div class="sec-label">补充关键词</div>', unsafe_allow_html=True)
    default_kws = ["月租999", "零中介", "熙街商圈", "拎包入住", "地铁房", "重庆租房"]
    kw_cols = st.columns(6)
    for col, kw in zip(kw_cols, default_kws):
        is_on = kw in st.session_state.active_kws
        with col:
            if st.button(kw, key=f"kw_{kw}", use_container_width=True,
                         type="primary" if is_on else "secondary"):
                if is_on:
                    st.session_state.active_kws.discard(kw)
                else:
                    st.session_state.active_kws.add(kw)
                st.rerun()

    custom_kw = st.text_input("自定义关键词（逗号分隔）", placeholder="例如：青年公寓,保障房",
                               label_visibility="visible")
    all_kws = list(st.session_state.active_kws)
    if custom_kw:
        all_kws += [k.strip() for k in custom_kw.split(",") if k.strip()]

    st.markdown("<hr style='border-color:#F0E0E3;margin:14px 0'>", unsafe_allow_html=True)

    # 生成按钮
    gen = st.button("✨ 一键生成帖子", use_container_width=True, type="primary")

    if gen:
        if not API_KEY:
            st.error("API Key 未配置，请联系管理员")
        else:
            topic_part = f"围绕小红书热点话题「#{st.session_state.selected_topic}」" \
                         if st.session_state.selected_topic else "围绕重庆租房/青年住房话题"
            type_guide = {
                "grass": "写一篇小红书种草帖，第一人称真实分享，标题用emoji+感叹号+数字公式，自然植入嘛嘛公寓优势，结尾带3-5个话题标签",
                "ad":    "写一篇小红书商业广告帖，直接点出最大卖点，列3-5个核心优势配emoji，重点突出999元起和零中介，有明确引导行动",
                "ops":   "写一篇小红书互动运营贴，标题用疑问句引发互动，设置评论钩子，用「你们觉得…」等互动语句"
            }
            prompt = f"""你是专业的小红书文案运营，为「重庆嘛嘛公寓」创作帖子。

公寓信息：月租999元起，熙街商圈地铁站旁，20-30㎡精装单间/复式，零中介费，灵活租期，月付，家具家电全配，配套休闲书屋和多功能活动大厅，面向外来青年和应届毕业生。

任务：{topic_part}，{type_guide[st.session_state.post_type]}

风格：{st.session_state.tone}
关键词：{' '.join(all_kws)}

直接输出帖子，不加说明，200-350字，有小红书「闺蜜推荐」的真实感。"""

            with st.spinner("✨ AI 正在创作中…"):
                try:
                    client = anthropic.Anthropic(api_key=API_KEY, base_url=API_URL)
                    msg = client.messages.create(
                        model="claude-opus-4-6",
                        max_tokens=1024,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    st.session_state.generated_post = msg.content[0].text
                except Exception as e:
                    st.error(f"生成失败：{e}")

    # 结果预览
    if st.session_state.generated_post:
        st.markdown("""
        <div class="preview-wrap">
          <div class="preview-bar">
            <span class="dot" style="background:#FF5F5F"></span>
            <span class="dot" style="background:#FFB800"></span>
            <span class="dot" style="background:#22c55e"></span>
            <span style="font-size:11px;color:#999;margin-left:auto">小红书 · 帖子预览</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        post_text = st.text_area("", value=st.session_state.generated_post,
                                  height=300, label_visibility="collapsed")
        st.caption(f"共 {len(st.session_state.generated_post)} 字　·　复制方法：点击文本框 → Command+A 全选 → Command+C 复制")

        c1, c2 = st.columns(2)
        c1.download_button("📥 下载为 txt 文件", data=post_text,
                           file_name="小红书帖子.txt", mime="text/plain",
                           use_container_width=True)
        if c2.button("🔄 重新生成", use_container_width=True):
            st.session_state.generated_post = ""
            st.rerun()
