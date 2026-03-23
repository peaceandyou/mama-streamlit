import streamlit as st
import anthropic

# ── 页面基础配置 ──────────────────────────────────────────────
st.set_page_config(
    page_title="嘛嘛公寓 · 小红书运营工具",
    page_icon="🏠",
    layout="wide"
)

# ── 自定义 CSS（小红书风格）────────────────────────────────────
st.markdown("""
<style>
  .stApp { background: #FDF6F7; }
  .main .block-container { background: #FDF6F7; }
  [data-testid="stAppViewContainer"] { background: #FDF6F7; }
  [data-testid="stHeader"] { background: #FFF0F2; border-bottom: 1px solid #F0D0D5; }
  section[data-testid="stSidebar"] { background: #fff0f2; }
  h1 { color: #FF2442 !important; }
  h2, h3 { color: #1A1A1A !important; }
  .stButton > button {
    background: linear-gradient(135deg, #FF2442, #FF6B7A) !important;
    color: white !important;
    border: none !important;
    border-radius: 24px !important;
    font-weight: 700 !important;
    padding: 10px 28px !important;
  }
  .stButton > button:hover { opacity: 0.9 !important; }
  .hot-tag {
    display: inline-block;
    background: #FFF0F2;
    color: #FF2442;
    border-radius: 12px;
    padding: 2px 10px;
    font-size: 12px;
    font-weight: 600;
    margin-right: 4px;
  }
  .related-chip {
    display: inline-block;
    background: #FF2442;
    color: white;
    border-radius: 10px;
    padding: 1px 8px;
    font-size: 11px;
    font-weight: 700;
  }
  .stTextArea textarea {
    font-size: 15px !important;
    line-height: 1.9 !important;
    border-radius: 14px !important;
  }
  div[data-testid="stExpander"] {
    border: 1.5px solid #F0E0E3 !important;
    border-radius: 12px !important;
    background: white !important;
    margin-bottom: 6px !important;
  }
</style>
""", unsafe_allow_html=True)

# ── 密码保护 ────────────────────────────────────────────────
CORRECT_PWD = st.secrets.get("password", "xiaohu2026")

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("## 🏠 嘛嘛公寓 · 小红书运营工具")
        st.markdown("**请输入访问密码**")
        pwd = st.text_input("", type="password", placeholder="请输入密码…", label_visibility="collapsed")
        if st.button("进 入", use_container_width=True):
            if pwd == CORRECT_PWD:
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("密码错误，请重新输入")
    st.stop()

# ── API 配置（从 secrets 读取）─────────────────────────────────
API_KEY = st.secrets.get("api_key", "")
API_URL = st.secrets.get("api_url", "https://code.newcli.com/claude")

# ── 热点数据 ────────────────────────────────────────────────
HOT_TOPICS = [
    {"id": 1,  "name": "毕业季租房避坑指南",       "heat": "982万",  "related": True,
     "reason": "毕业生是嘛嘛公寓的核心目标人群，零中介、月付模式正好戳中他们的痛点",
     "tip": "以「第一次租房的你」为角色切入，分享从踩坑到入住嘛嘛公寓的真实经历，重点突出「零中介省了多少钱」的数字对比",
     "url": "https://www.xiaohongshu.com/search_result?keyword=毕业季租房避坑"},
    {"id": 2,  "name": "重庆打工人生活vlog",        "heat": "756万",  "related": True,
     "reason": "重庆外来务工青年是嘛嘛公寓主要用户，日常居住类内容流量大且精准",
     "tip": "用「嘛嘛公寓一天」为主题，展示早起、通勤、公共空间等生活场景，配合「6分钟到单位」等具体描写",
     "url": "https://www.xiaohongshu.com/search_result?keyword=重庆打工人vlog"},
    {"id": 3,  "name": "月薪5000怎么在大城市生活",  "heat": "1243万", "related": True,
     "reason": "价格敏感型用户高度关注，999元/月的定价极具竞争力，是绝佳的种草切入点",
     "tip": "做一期「月薪5000在重庆的真实支出清单」，把租房项明确写出「嘛嘛公寓999/月」并与市场均价对比",
     "url": "https://www.xiaohongshu.com/search_result?keyword=月薪5000在大城市"},
    {"id": 4,  "name": "一个人住的小窝改造",        "heat": "892万",  "related": True,
     "reason": "20-30㎡的户型正好契合这类内容，展示小空间改造布置可获得大量收藏",
     "tip": "发一篇「25㎡精装单间改造前后对比」，展示入住的变化，附上布置tips，收藏率极高",
     "url": "https://www.xiaohongshu.com/search_result?keyword=一个人住小窝改造"},
    {"id": 5,  "name": "重庆旅游超级攻略",          "heat": "2100万", "related": False,
     "reason": "", "tip": "",
     "url": "https://www.xiaohongshu.com/search_result?keyword=重庆旅游攻略"},
    {"id": 6,  "name": "攒钱计划100天打卡",         "heat": "678万",  "related": True,
     "reason": "年轻人存钱意识强，灵活租期+月付模式减少大额押金压力，可与攒钱话题联动",
     "tip": "以「我的100天存钱计划」为题，把住在嘛嘛公寓「省下的中介费用来存钱」作为亮点植入",
     "url": "https://www.xiaohongshu.com/search_result?keyword=攒钱打卡"},
    {"id": 7,  "name": "新手租房一定要看",          "heat": "1560万", "related": True,
     "reason": "搜索量极大的通用租房话题，嘛嘛公寓零中介模式是很好的「正确示范」内容",
     "tip": "制作「租房新手避坑清单」，第4条自然引出「选保障性公寓如嘛嘛，省心又安全」",
     "url": "https://www.xiaohongshu.com/search_result?keyword=新手租房"},
    {"id": 8,  "name": "熙街商圈周边探店",          "heat": "234万",  "related": True,
     "reason": "精准地域话题，直接触达嘛嘛公寓周边潜在用户群体",
     "tip": "发一篇「住在熙街商圈的日常 | 周边吃喝玩乐全攻略」，带出嘛嘛公寓的位置优势",
     "url": "https://www.xiaohongshu.com/search_result?keyword=熙街商圈"},
    {"id": 9,  "name": "室内健身不花钱",            "heat": "445万",  "related": False,
     "reason": "", "tip": "",
     "url": "https://www.xiaohongshu.com/search_result?keyword=室内健身"},
    {"id": 10, "name": "年轻人的第一套「家」",       "heat": "893万",  "related": True,
     "reason": "情感共鸣话题，嘛嘛公寓的「家的感觉」定位与之高度匹配",
     "tip": "以情感叙事为主线，写「在重庆漂了两年，终于有了自己的窝」，引发强烈共鸣和转发",
     "url": "https://www.xiaohongshu.com/search_result?keyword=年轻人第一套家"},
]

# ── 顶部标题 ────────────────────────────────────────────────
st.markdown("# 🏠 嘛嘛公寓 · 小红书运营工具")
st.markdown("**重庆熙街商圈 · 保障性租赁住房 · AI帖子生成**")
st.divider()

# ── 主体两列布局 ────────────────────────────────────────────
left, right = st.columns([1, 1.2], gap="large")

# ╔══════════════════════════════╗
# ║         左列：热点            ║
# ╚══════════════════════════════╝
with left:

    # 公寓信息卡片
    with st.container(border=True):
        st.markdown("### 🏠 嘛嘛公寓")
        c1, c2 = st.columns(2)
        c1.metric("月租金", "999元起")
        c2.metric("总套数", "528套")
        c3, c4 = st.columns(2)
        c3.metric("户型", "20-30㎡")
        c4.metric("中介费", "零中介")
        st.caption("📍 重庆熙街商圈地铁站旁 · 灵活租期 · 月付 · 拎包入住")

    st.markdown("### 🔥 小红书热点话题")

    related_topics = [t for t in HOT_TOPICS if t["related"]]
    other_topics   = [t for t in HOT_TOPICS if not t["related"]]

    st.markdown(f"<span class='related-chip'>相关 {len(related_topics)} 个</span>　筛选出与嘛嘛公寓最相关的热点", unsafe_allow_html=True)
    st.markdown("")

    for i, t in enumerate(HOT_TOPICS):
        rank_emoji = ["🥇","🥈","🥉"][i] if i < 3 else f"**{i+1}**"
        label = f"{rank_emoji} #{t['name']}　🔥{t['heat']}"
        if t["related"]:
            label += "　✅相关"

        with st.expander(label):
            if t["related"]:
                st.markdown(f"**为何相关：** {t['reason']}")
                st.markdown(f"**运营建议：** {t['tip']}")
                col_a, col_b = st.columns([1, 1])
                with col_a:
                    st.link_button("🔗 在小红书查看", t["url"], use_container_width=True)
                with col_b:
                    if st.button("✨ 用这个生成帖子", key=f"use_{t['id']}", use_container_width=True):
                        st.session_state.selected_topic = t["name"]
                        st.rerun()
            else:
                st.caption("本话题与嘛嘛公寓关联度较低，可作为辅助参考。")
                st.link_button("🔗 在小红书查看", t["url"])

# ╔══════════════════════════════╗
# ║        右列：生成器           ║
# ╚══════════════════════════════╝
with right:

    st.markdown("### ✍️ 帖子生成器")

    # 已选热点显示
    if "selected_topic" not in st.session_state:
        st.session_state.selected_topic = ""

    selected = st.text_input(
        "当前热点（可手动填写，或点左侧「用这个生成帖子」自动填入）",
        value=st.session_state.selected_topic,
        placeholder="例如：毕业季租房避坑指南",
        key="topic_input"
    )
    st.session_state.selected_topic = selected

    # 帖子类型
    st.markdown("**选择帖子类型**")
    post_type = st.radio(
        "",
        ["🌱 种草帖 · 真实体验分享，吸引用户了解",
         "📢 商广帖 · 突出卖点，强调性价比和行动引导",
         "🎯 运营贴 · 互动引流为主，涨粉评论收藏转发"],
        label_visibility="collapsed"
    )
    type_key = {"🌱": "grass", "📢": "ad", "🎯": "ops"}[post_type[0]]

    # 写作风格
    st.markdown("**写作风格**")
    tone = st.select_slider(
        "",
        options=["轻松日常", "干货专业", "故事叙述", "搞笑幽默"],
        label_visibility="collapsed"
    )

    # 关键词
    st.markdown("**关键词（多选）**")
    default_kws = ["月租999", "零中介", "熙街商圈", "拎包入住", "地铁房", "重庆租房"]
    selected_kws = st.multiselect("", default_kws, default=["月租999", "零中介", "熙街商圈"], label_visibility="collapsed")
    custom_kw = st.text_input("补充自定义关键词（逗号分隔）", placeholder="例如：青年公寓,保障房", label_visibility="visible")
    if custom_kw:
        selected_kws += [k.strip() for k in custom_kw.split(",") if k.strip()]

    st.divider()

    # 生成按钮
    gen_btn = st.button("✨ 一键生成帖子", use_container_width=True, type="primary")

    # 生成逻辑
    if gen_btn:
        if not API_KEY:
            st.error("API Key 未配置，请联系管理员")
        else:
            topic_part = f"围绕小红书热点话题「#{selected}」" if selected else "围绕重庆租房/青年住房话题"

            type_guide = {
                "grass": """写一篇小红书种草帖：
- 标题用「emoji+感叹号+数字/对比」公式
- 正文第一人称真实分享，描写找房→入住的故事
- 自然植入嘛嘛公寓优势（不要硬广感）
- 结尾带3-5个话题标签（#格式）""",
                "ad": """写一篇小红书商业广告帖：
- 标题直接点出最大卖点，加强紧迫感
- 列出3-5个核心优势，配emoji分隔
- 重点突出价格优势（999起）和零中介
- 有明确引导行动，结尾带话题标签""",
                "ops": """写一篇小红书互动运营贴：
- 标题用疑问句或投票句引发互动欲望
- 设置互动钩子（投票/问卷/晒图话题）
- 用「你们觉得…」「评论区聊聊…」等互动语句
- 结尾带话题标签"""
            }

            prompt = f"""你是专业的小红书文案运营，正在为「重庆嘛嘛公寓」创作一篇帖子。

公寓信息：
- 位置：重庆市熙街商圈地铁站旁
- 定价：月租999元起（精装20-30㎡单间/复式）
- 特色：零中介费、灵活租期、租金月付、家具家电全配
- 目标用户：在渝工作的外来青年、应届毕业生
- 配套：休闲书屋、多功能活动大厅

任务：{topic_part}，{type_guide[type_key]}

写作风格：{tone}
关键词：{' '.join(selected_kws)}

要求：直接输出帖子内容，不加说明语，200-350字，有小红书「闺蜜推荐」的真实感。"""

            with st.spinner("AI 正在创作中，请稍候…"):
                try:
                    client = anthropic.Anthropic(
                        api_key=API_KEY,
                        base_url=API_URL
                    )
                    message = client.messages.create(
                        model="claude-opus-4-6",
                        max_tokens=1024,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    result = message.content[0].text
                    st.session_state.generated_post = result
                except Exception as e:
                    st.error(f"生成失败：{e}")

    # 结果展示
    if "generated_post" in st.session_state and st.session_state.generated_post:
        st.markdown("### 📋 帖子预览")
        post_text = st.text_area(
            "",
            value=st.session_state.generated_post,
            height=320,
            label_visibility="collapsed"
        )
        st.caption(f"共 {len(st.session_state.generated_post)} 字")

        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "📥 下载帖子文本",
                data=post_text,
                file_name="小红书帖子.txt",
                mime="text/plain",
                use_container_width=True
            )
        with col2:
            st.button("🔄 重新生成", on_click=lambda: st.session_state.pop("generated_post", None), use_container_width=True)

        st.info("💡 复制方法：点击上方文本框，全选（Ctrl+A / Command+A），复制（Ctrl+C / Command+C）", icon="📋")
