import streamlit as st
import pandas as pd
from datetime import datetime
import json

# 頁面設定
st.set_page_config(page_title="紅酒貿易開單助手", layout="wide")

# ---------- 側邊欄：公司設定 ----------
st.sidebar.title("🏢 公司設定")
company_preset = st.sidebar.selectbox(
    "快速選擇公司",
    ["美酒國際貿易有限公司", "佳釀進口股份有限公司", "自訂公司"]
)

if company_preset == "美酒國際貿易有限公司":
    default_company = {
        "name": "美酒國際貿易有限公司",
        "address": "香港中環金融街8號國際金融中心二期",
        "phone": "+852 1234 5678",
        "tax_id": "12345678"
    }
elif company_preset == "佳釀進口股份有限公司":
    default_company = {
        "name": "佳釀進口股份有限公司",
        "address": "台北市信義區松仁路100號",
        "phone": "+886 2 8765 4321",
        "tax_id": "87654321"
    }
else:
    default_company = {
        "name": "",
        "address": "",
        "phone": "",
        "tax_id": ""
    }

company_name = st.sidebar.text_input("公司名稱", value=default_company["name"])
company_address = st.sidebar.text_area("公司地址", value=default_company["address"])
company_phone = st.sidebar.text_input("電話", value=default_company["phone"])
company_tax = st.sidebar.text_input("統一編號 / 稅號", value=default_company["tax_id"])

st.sidebar.markdown("---")
st.sidebar.info("📌 所有資料僅儲存於您目前的瀏覽器會話中，重整頁面會清除記錄。")

# ---------- 主畫面 ----------
st.title("🍷 紅酒貿易開單助手")

# 文件類型與基本資料欄位
col1, col2 = st.columns(2)
with col1:
    doc_type = st.radio("文件類型", ["🧾 發票 (Invoice)", "🚚 送貨單 (Delivery Note)"], horizontal=True)
with col2:
    doc_date = st.date_input("單據日期", value=datetime.today())

cust_name = st.text_input("客戶名稱", placeholder="請輸入客戶公司或個人名稱")
doc_number = st.text_input("單據編號", placeholder="例如：INV-2024001 / DN-2024001")

# ---------- 產品明細編輯器（自動計算小計與總額） ----------
st.subheader("📦 產品明細")

# 預設一筆空白範例
if "product_df" not in st.session_state:
    st.session_state.product_df = pd.DataFrame({
        "產品名稱": ["2018 Bordeaux 紅酒", "2019 Penfolds Bin 389"],
        "數量": [12, 6],
        "單價 (HKD)": [380, 720],
        "小計 (HKD)": [12*380, 6*720]
    })

# 使用 data_editor 讓使用者自由增刪修改
edited_df = st.data_editor(
    st.session_state.product_df,
    use_container_width=True,
    num_rows="dynamic",
    column_config={
        "產品名稱": st.column_config.TextColumn("產品名稱", required=True),
        "數量": st.column_config.NumberColumn("數量", step=1, min_value=1),
        "單價 (HKD)": st.column_config.NumberColumn("單價 (HKD)", step=10, min_value=0),
        "小計 (HKD)": st.column_config.NumberColumn("小計 (HKD)", disabled=True)
    },
    hide_index=True,
)

# 自動重新計算「小計」與「總金額」
if not edited_df.empty:
    edited_df["小計 (HKD)"] = edited_df["數量"] * edited_df["單價 (HKD)"]
    total_amount = edited_df["小計 (HKD)"].sum()
else:
    total_amount = 0

st.session_state.product_df = edited_df

# 顯示總金額（大字體）
st.markdown(f"### 💰 訂單總金額： **HKD {total_amount:,.2f}**")

# ---------- 輔助按鈕列 ----------
col_btn1, col_btn2, col_btn3 = st.columns(3)
with col_btn1:
    save_record = st.button("💾 儲存此單據至記錄", use_container_width=True)
with col_btn2:
    clear_form = st.button("🗑️ 清空表單", use_container_width=True)
with col_btn3:
    download_pdf_btn = st.button("📄 下載 PDF (打印版)", use_container_width=True)

# ---------- 清空表單邏輯 ----------
if clear_form:
    st.session_state.product_df = pd.DataFrame(columns=["產品名稱", "數量", "單價 (HKD)", "小計 (HKD)"])
    st.session_state.cust_name = ""
    st.session_state.doc_number = ""
    st.rerun()

# 保留使用者輸入到 session_state 以便載入記錄時還原
if "cust_name" not in st.session_state:
    st.session_state.cust_name = cust_name
if "doc_number" not in st.session_state:
    st.session_state.doc_number = doc_number

# 同步目前表單的值
st.session_state.cust_name = cust_name
st.session_state.doc_number = doc_number

# ---------- 儲存記錄至 session_state ----------
if save_record:
    if not cust_name.strip():
        st.error("請填寫客戶名稱")
    elif edited_df.empty:
        st.error("請至少輸入一項產品明細")
    else:
        new_record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "company": company_name,
            "doc_type": doc_type,
            "cust_name": cust_name,
            "doc_number": doc_number,
            "doc_date": doc_date.strftime("%Y-%m-%d"),
            "items": edited_df.to_dict(orient="records"),
            "total": total_amount
        }
        if "history" not in st.session_state:
            st.session_state.history = []
        st.session_state.history.insert(0, new_record)  # 最新在上方
        st.success("單據已儲存至記錄！")

# ---------- 顯示最近記錄 ----------
st.markdown("---")
st.subheader("📋 最近開單記錄")

if "history" not in st.session_state or len(st.session_state.history) == 0:
    st.info("尚無任何開單記錄，請先產生並儲存單據。")
else:
    for idx, record in enumerate(st.session_state.history[:10]):  # 顯示最近10筆
        with st.expander(f"{record['doc_type']} - {record['cust_name']} ({record['timestamp']})"):
            st.write(f"**單據編號**：{record['doc_number']}")
            st.write(f"**日期**：{record['doc_date']}")
            st.write(f"**總金額**：HKD {record['total']:,.2f}")
            if st.button(f"📂 載入此筆記錄", key=f"load_{idx}"):
                # 將記錄載回主表單
                st.session_state.cust_name = record['cust_name']
                st.session_state.doc_number = record['doc_number']
                st.session_state.product_df = pd.DataFrame(record['items'])
                st.rerun()

# ---------- PDF 下載功能（產生可打印的 HTML 單據） ----------
def generate_printable_html():
    """產生專業格式的 HTML 單據，供使用者下載後打印為 PDF"""
    # 判斷文件類型顯示文字
    if "發票" in doc_type:
        doc_title = "發票 INVOICE"
        en_title = "TAX INVOICE"
    else:
        doc_title = "送貨單 DELIVERY NOTE"
        en_title = "DELIVERY NOTE"

    # 產品明細表格 HTML 產生
    items_html = "<thead><tr><th>產品名稱</th><th>數量</th><th>單價 (HKD)</th><th>小計 (HKD)</th></tr></thead><tbody>"
    for _, row in edited_df.iterrows():
        items_html += f"<tr><td>{row['產品名稱']}</td><td>{row['數量']}</td><td>{row['單價 (HKD)']:,.2f}</td><td>{row['小計 (HKD)']:,.2f}</td></tr>"
    items_html += "</tbody>"

    html_content = f"""<!DOCTYPE html>
<html lang="zh-HK">
<head>
    <meta charset="UTF-8">
    <title>{doc_title} - {doc_number}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', 'Noto Sans CJK TC', 'Microsoft YaHei', sans-serif;
            background: #e9e7e4;
            padding: 40px 20px;
            display: flex;
            justify-content: center;
        }}
        .invoice-box {{
            max-width: 800px;
            width: 100%;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            padding: 30px 35px;
        }}
        h1 {{
            font-size: 28px;
            color: #9b2e2e;
            border-left: 6px solid #9b2e2e;
            padding-left: 16px;
            margin-bottom: 10px;
        }}
        .company-info {{
            margin-top: 20px;
            margin-bottom: 30px;
            padding: 15px 0;
            border-top: 2px solid #ddd;
            border-bottom: 2px solid #ddd;
            font-size: 14px;
            color: #333;
        }}
        .doc-details {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 30px;
            font-size: 14px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 25px 0;
        }}
        th, td {{
            border: 1px solid #ccc;
            padding: 10px 8px;
            text-align: left;
        }}
        th {{
            background: #f4f0eb;
            font-weight: 600;
        }}
        .total-row {{
            font-weight: bold;
            background: #f9f6f2;
            text-align: right;
        }}
        .total-amount {{
            font-size: 20px;
            color: #9b2e2e;
            font-weight: bold;
        }}
        .footer {{
            margin-top: 40px;
            font-size: 12px;
            color: #666;
            text-align: center;
            border-top: 1px solid #eee;
            padding-top: 20px;
        }}
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            .invoice-box {{
                box-shadow: none;
                padding: 0;
            }}
            .no-print {{
                display: none;
            }}
        }}
    </style>
</head>
<body>
<div class="invoice-box">
    <h1>{doc_title}<br><span style="font-size: 14px; color: #6b4c3b;">{en_title}</span></h1>
    
    <div class="company-info">
        <strong>{company_name}</strong><br>
        {company_address}<br>
        電話 {company_phone}　統編 {company_tax}
    </div>

    <div class="doc-details">
        <div><strong>客戶名稱：</strong> {cust_name}</div>
        <div><strong>單據編號：</strong> {doc_number}</div>
        <div><strong>開單日期：</strong> {doc_date.strftime('%Y-%m-%d')}</div>
    </div>

    <table>
        {items_html}
        <tr class="total-row">
            <td colspan="3" style="text-align: right;"><strong>總金額 HKD</strong></td>
            <td><strong class="total-amount">{total_amount:,.2f}</strong></td>
        </tr>
    </table>

    <div class="footer">
        此單據由紅酒貿易開單助手產生，請於收到貨品後核對明細。<br>
        感謝您的採購！
    </div>
</div>
</body>
</html>
"""
    return html_content

if download_pdf_btn:
    if not cust_name.strip():
        st.error("請先填寫客戶名稱再下載 PDF")
    elif edited_df.empty:
        st.error("請先新增產品明細再下載")
    else:
        html_str = generate_printable_html()
        st.download_button(
            label="⬇️ 點此下載 HTML 單據 (打開後按 Ctrl+P 或選擇「列印 > 另存為 PDF」)",
            data=html_str,
            file_name=f"{doc_type.split()[0]}_{doc_number}_{datetime.today().strftime('%Y%m%d')}.html",
            mime="text/html",
            key="pdf_download"
        )
        st.info("📌 下載後使用瀏覽器開啟該檔案，按「列印」或 Ctrl+P，選擇「另存為 PDF」即可獲得正式 PDF 單據。")
