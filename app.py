import streamlit as st

# ページの設定（タイトルとレイアウト）
st.set_page_config(page_title="老後資金必要額算出シミュレーター", layout="centered")

# タイトル・導入
st.title("「わが家の老後資金の必要額」算出シミュレーター")
st.caption("※本ツールは、書籍『50歳から備える「老後資金」と投資の終わり方』第２章④節に対応しています。")

st.markdown("""
書籍付録の**「ワークシートA」**に対応した自動計算ツールです。
書籍をお手元にご用意いただき、各項目を入力してください。
""")

st.write("---")

# -------------------------------------------------------------------------
# 【ステップ１ & ２】年金受給見込額と手取り額の自動算出
# -------------------------------------------------------------------------
st.header("【ステップ１・２】年金受給見込額（額面）の入力と手取り額の算出")
st.markdown("将来の「確実な収入」のベースを把握します。「ねんきん定期便」やシミュレーター等の数字（額面・年額）を記入してください。金額を入力すると、手取り額が自動計算されます。")

col1, col2 = st.columns(2)

with col1:
    st.subheader("ご本人")
    a1 = st.number_input(
        "ご本人の年金受給見込額（年額・額面）: [A1]", 
        min_value=0.0, 
        value=180.0, 
        step=10.0, 
        format="%.1f",
        help="単位：万円"
    )
    
    # 手取り率の自動判定ロジック
    if a1 < 180.0:
        rate_1 = 0.95
    elif 180.0 <= a1 <= 280.0:
        rate_1 = 0.90
    else:
        rate_1 = 0.85
        
    b1 = a1 * rate_1
    st.info(f"自動判定された手取り率: {rate_1*100:.0f}％ (×{rate_1:.2f})")
    st.metric(label="ご本人の手取り額 [B1]", value=f"{b1:.1f} 万円")

with col2:
    st.subheader("配偶者")
    a2 = st.number_input(
        "配偶者の年金受給見込額（年額・額面）: [A2]", 
        min_value=0.0, 
        value=70.0, 
        step=10.0, 
        format="%.1f",
        help="単位：万円（※単身の方は 0 を入力してください）"
    )
    
    # 手取り率の自動判定ロジック（0の場合は一律0円・手取り率なし）
    if a2 == 0.0:
        rate_2 = 0.0
        b2 = 0.0
        st.info("単身（または未入力）設定")
    else:
        if a2 < 180.0:
            rate_2 = 0.95
        elif 180.0 <= a2 <= 280.0:
            rate_2 = 0.90
        else:
            rate_2 = 0.85
        b2 = a2 * rate_2
        st.info(f"自動判定された手取り率: {rate_2*100:.0f}％ (×{rate_2:.2f})")
        
    st.metric(label="配偶者の手取り額 [B2]", value=f"{b2:.1f} 万円")

# 世帯合計
st.write(" ")
b_total = b1 + b2
st.subheader(f"③ 世帯合計の手取り額 [B]： **{b_total:,.1f} 万円**")

st.write("---")

# -------------------------------------------------------------------------
# 【ステップ３・４】老後の不足資金を算出する
# -------------------------------------------------------------------------
st.header("【ステップ３・４】老後の不足資金を算出する")
st.markdown("老後20年間（または想定する期間）でいくら不足するかを計算します。")

c = st.number_input(
    "① 1年間に必要と予想される支出： [C]", 
    min_value=0.0, 
    value=360.0, 
    step=10.0, 
    format="%.1f",
    help="単位：万円（目安：夫婦平均は年約308万円、単身平均は年約179万円）"
)

# 1年間の不足額 [D]
d = c - b_total

st.write(" ")
st.markdown(f"**② 1年間の不足額 [D]：**")
if d > 0:
    st.markdown(f"[C] {c:.1f}万円 － [B] {b_total:.1f}万円 ＝ <span style='color:red; font-size:20px; font-weight:bold;'>{d:.1f} 万円（不足）</span>", unsafe_allow_html=True)
else:
    st.markdown(f"[C] {c:.1f}万円 － [B] {b_total:.1f}万円 ＝ <span style='color:green; font-size:20px; font-weight:bold;'>{abs(d):.1f} 万円（黒字・準備完了）</span>", unsafe_allow_html=True)

st.write(" ")
years = st.number_input(
    "取り崩し期間（年）", 
    min_value=1, 
    max_value=50, 
    value=20, 
    step=1
)

# 「老後の不足資金」の総額 [E]
e = d * years

st.write(" ")
st.subheader(f"③「老後の不足資金」の総額 [E]：")
if e > 0:
    st.subheader(f"**{e:,.1f} 万円** （{d:.1f}万円 × {years}年）")
else:
    st.subheader(f"**0 万円** （現在の年金収入の範囲で賄えています）")
    e = 0.0 # マイナスの場合は次のステップ用に0にリセット

st.write("---")

# -------------------------------------------------------------------------
# 【ステップ５】自分で準備する目標額を決定する
# -------------------------------------------------------------------------
st.header("【ステップ５】自分で準備する目標額を決定する")
st.markdown("退職金などの臨時収入を差し引いて、最終結果を出します。")

f = st.number_input(
    "① 退職金やその他の臨時収入： [F]", 
    min_value=0.0, 
    value=500.0, 
    step=10.0, 
    format="%.1f",
    help="単位：万円"
)

# 【最終結果】自分（達）で準備する目標額： [G]
g = e - f

st.write(" ")
st.markdown("### 【最終結果】自分（達）で準備する目標額 【G】")

if g > 0:
    st.success(f"必要な目標額は **{g:,.1f} 万円** です。")
    st.info("この金額を目標に、資産形成や投資の出口戦略を考えていきましょう。")
else:
    st.success(f"目標額は **0 万円（現在の準備で充足しています）** です！")
    st.balloons() # お祝いのエフェクト