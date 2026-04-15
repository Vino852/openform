以下是您所需的红酒贸易公司专用开单Web App的代码.它支持在手机端创建和管理发票、送货单等单据，并将数据保存在浏览器中.
```html
<!DOCTYPE html>
<html lang="zh-HK">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes, viewport-fit=cover">
    <title>紅酒貿易開單助手 | 發票·送貨單·借項·貸項</title>
    <style>
        * {
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }

        body {
            font-family: system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Helvetica, sans-serif;
            background: #f4f2ef;
            margin: 0;
            padding: 16px 12px 32px;
            color: #2c2418;
        }

        /* 主容器 */
        .app-container {
            max-width: 580px;
            margin: 0 auto;
        }

        /* 卡片通用樣式 */
        .card {
            background: white;
            border-radius: 28px;
            box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04), 0 1px 2px rgba(0, 0, 0, 0.03);
            padding: 20px 18px;
            margin-bottom: 20px;
            transition: all 0.2s ease;
        }

        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            flex-wrap: wrap;
            margin-bottom: 18px;
            border-left: 4px solid #9b2e2e;
            padding-left: 12px;
        }

        .card-header h2 {
            font-size: 1.45rem;
            font-weight: 600;
            margin: 0;
            color: #2c2418;
        }

        .badge-doc {
            background: #f0ede8;
            border-radius: 40px;
            padding: 6px 12px;
            font-size: 0.7rem;
            font-weight: 500;
            color: #6b4c3b;
        }

        /* 表單 */
        .form-row {
            margin-bottom: 18px;
            display: flex;
            flex-direction: column;
        }

        label {
            font-weight: 500;
            font-size: 0.8rem;
            margin-bottom: 6px;
            color: #5f4c3b;
            letter-spacing: 0.3px;
        }

        input, select, textarea {
            background: #fefcf9;
            border: 1px solid #e2dbd2;
            border-radius: 20px;
            padding: 12px 16px;
            font-size: 0.95rem;
            font-family: inherit;
            transition: 0.2s;
            width: 100%;
            outline: none;
            color: #1e1914;
        }

        input:focus, select:focus, textarea:focus {
            border-color: #b85c3a;
            box-shadow: 0 0 0 3px rgba(184, 92, 58, 0.1);
        }

        textarea {
            border-radius: 24px;
            resize: vertical;
        }

        .double-group {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
        }
        .double-group .form-row {
            flex: 1;
        }

        /* 明細行 (items) */
        .items-section {
            margin: 20px 0 12px;
            background: #faf8f5;
            border-radius: 24px;
            padding: 12px 10px;
        }

        .item-row {
            background: white;
            border-radius: 20px;
            padding: 12px;
            margin-bottom: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            align-items: center;
        }
        .item-row input {
            flex: 2;
            min-width: 120px;
        }
        .item-row input.item-qty {
            flex: 0.8;
            min-width: 70px;
        }
        .item-row input.item-price {
            flex: 1;
            min-width: 100px;
        }
        .item-row .remove-item {
            background: #fce4e0;
            border: none;
            border-radius: 40px;
            padding: 8px 14px;
            font-weight: 600;
            color: #b13e2c;
            cursor: pointer;
            font-size: 0.8rem;
        }

        .add-item-btn {
            background: #ece6df;
            border: none;
            border-radius: 40px;
            padding: 10px 18px;
            font-weight: 500;
            font-size: 0.85rem;
            color: #4f3a2b;
            width: 100%;
            cursor: pointer;
            margin-top: 8px;
        }

        /* 動作按鈕 */
        .actions {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin-top: 24px;
            margin-bottom: 8px;
        }
        button.primary {
            background: #9b2e2e;
            border: none;
            border-radius: 40px;
            padding: 12px 20px;
            font-weight: 600;
            color: white;
            flex: 1;
            cursor: pointer;
            font-size: 0.9rem;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }
        button.secondary {
            background: #e7dfd7;
            border: none;
            border-radius: 40px;
            padding: 12px 20px;
            font-weight: 500;
            color: #3b2c21;
            flex: 1;
            cursor: pointer;
        }
        button.danger {
            background: #fff1ed;
            color: #b1533c;
            border: 1px solid #f0cfc4;
        }

        /* 歷史列表 */
        .history-item {
            background: #fefaf5;
            border-radius: 20px;
            padding: 14px;
            margin-bottom: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 8px;
            border: 1px solid #ece2d8;
        }
        .history-info {
            font-size: 0.85rem;
        }
        .history-number {
            font-weight: 700;
            color: #9b2e2e;
        }
        .history-btns {
            display: flex;
            gap: 8px;
        }
        .small-btn {
            background: transparent;
            border: 1px solid #ddd2c6;
            border-radius: 30px;
            padding: 6px 14px;
            font-size: 0.7rem;
            cursor: pointer;
        }
        .preview-area {
            background: #fefaf5;
            border-radius: 24px;
            padding: 16px;
            font-size: 0.8rem;
            white-space: pre-wrap;
            font-family: monospace;
            max-height: 260px;
            overflow: auto;
            border: 1px solid #ece0d4;
        }
        hr {
            margin: 18px 0;
            border-color: #ede3d9;
        }
        .doc-type-selector {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        .type-chip {
            background: #f0ede8;
            padding: 8px 18px;
            border-radius: 40px;
            font-weight: 500;
            cursor: pointer;
            font-size: 0.85rem;
            transition: all 0.1s;
        }
        .type-chip.active {
            background: #9b2e2e;
            color: white;
        }
        .footer-note {
            text-align: center;
            font-size: 0.7rem;
            color: #8b765f;
            margin-top: 24px;
        }
        @media (max-width: 480px) {
            .card {
                padding: 16px;
            }
            .item-row {
                flex-direction: column;
                align-items: stretch;
            }
            .item-row .remove-item {
                align-self: flex-end;
            }
        }
    </style>
</head>
<body>
<div class="app-container">
    <!-- 主要開單卡片 -->
    <div class="card">
        <div class="card-header">
            <h2>🍷 紅酒開單助手</h2>
            <span class="badge-doc">離線儲存 · 本地資料庫</span>
        </div>

        <!-- 單據類型快速切換 -->
        <div class="doc-type-selector" id="docTypeSelector">
            <div data-type="invoice" class="type-chip active">🧾 發票 (Invoice)</div>
            <div data-type="delivery_note" class="type-chip">🚚 送貨單 (DN)</div>
            <div data-type="debit_note" class="type-chip">📉 借項通知單 (Debit)</div>
            <div data-type="credit_note" class="type-chip">📈 貸項通知單 (Credit)</div>
        </div>

        <!-- 表單欄位 -->
        <div>
            <div class="double-group">
                <div class="form-row">
                    <label>單據編號 *</label>
                    <input type="text" id="docNumber" placeholder="例如 INV-24001 / DN-101" autocomplete="off">
                </div>
                <div class="form-row">
                    <label>日期</label>
                    <input type="date" id="docDate">
                </div>
            </div>
            <div class="double-group">
                <div class="form-row">
                    <label>客戶名稱</label>
                    <input type="text" id="customerName" placeholder="客戶 / 酒莊名稱">
                </div>
                <div class="form-row">
                    <label>客戶編號(選填)</label>
                    <input type="text" id="customerCode" placeholder="客戶代碼">
                </div>
            </div>

            <!-- 產品明細區塊 -->
            <div class="items-section">
                <label>🍾 紅酒品項明細</label>
                <div id="itemsContainer"></div>
                <button type="button" class="add-item-btn" id="addItemBtn">+ 新增紅酒品項</button>
            </div>

            <div class="form-row">
                <label>備註 / 條款</label>
                <textarea rows="2" id="remarks" placeholder="付款方式、運送條件、酒款備註..."></textarea>
            </div>

            <div class="actions">
                <button class="primary" id="createDocBtn">✅ 建立單據</button>
                <button class="secondary" id="resetFormBtn">🗑️ 清空表單</button>
            </div>
        </div>
    </div>

    <!-- 預覽區塊：即時顯示產生的單據內容 -->
    <div class="card">
        <div class="card-header">
            <h2>📄 即時預覽</h2>
            <span class="badge-doc">當前選擇類型預覽</span>
        </div>
        <div id="previewContent" class="preview-area">
            填寫資料後將顯示單據樣式...
        </div>
    </div>

    <!-- 歷史記錄區塊: 顯示已儲存的所有單據 -->
    <div class="card">
        <div class="card-header">
            <h2>📚 單據記錄</h2>
            <button id="clearHistoryBtn" class="small-btn" style="background:#f0e5dc;">清除全部記錄</button>
        </div>
        <div id="historyList">
            <div style="text-align:center; color:#b1947a;">暫無單據，建立後會自動保存</div>
        </div>
    </div>
    <div class="footer-note">
        ✨ 所有單據皆儲存於瀏覽器 (localStorage) · 可離線使用
    </div>
</div>

<script>
    // ---------- 儲存 KEY ----------
    const STORAGE_KEY = "WineTrade_Documents";

    // 文件類型對應中文標題
    const docTypeMap = {
        invoice: { title: "發票 INVOICE", short: "INV" },
        delivery_note: { title: "送貨單 DELIVERY NOTE", short: "DN" },
        debit_note: { title: "借項通知單 DEBIT NOTE", short: "DN" },
        credit_note: { title: "貸項通知單 CREDIT NOTE", short: "CN" }
    };

    // 當前編輯中的資料
    let currentDocType = "invoice";   // invoice, delivery_note, debit_note, credit_note
    let items = [];                   // 每個item: { description, quantity, unitPrice }

    // DOM 元素
    const docNumberInput = document.getElementById("docNumber");
    const docDateInput = document.getElementById("docDate");
    const customerNameInput = document.getElementById("customerName");
    const customerCodeInput = document.getElementById("customerCode");
    const remarksInput = document.getElementById("remarks");
    const itemsContainer = document.getElementById("itemsContainer");
    const previewDiv = document.getElementById("previewContent");
    const historyListDiv = document.getElementById("historyList");

    // 設定今日日期為預設
    function setDefaultDate() {
        if (!docDateInput.value) {
            const today = new Date().toISOString().slice(0,10);
            docDateInput.value = today;
        }
    }

    // 渲染品項輸入行
    function renderItems() {
        if (!itemsContainer) return;
        itemsContainer.innerHTML = "";
        if (items.length === 0) {
            // 預設一筆空品項讓使用者好填
            items.push({ description: "", quantity: 1, unitPrice: 0 });
        }
        items.forEach((item, idx) => {
            const row = document.createElement("div");
            row.className = "item-row";
            row.innerHTML = `
                <input type="text" class="item-desc" placeholder="紅酒名稱 (例: Château Margaux 2018)" value="${escapeHtml(item.description)}">
                <input type="number" class="item-qty" placeholder="數量" value="${item.quantity}" step="any" min="0">
                <input type="number" class="item-price" placeholder="單價 (HKD)" value="${item.unitPrice}" step="any" min="0">
                <button class="remove-item" data-index="${idx}">刪除</button>
            `;
            const descInput = row.querySelector(".item-desc");
            const qtyInput = row.querySelector(".item-qty");
            const priceInput = row.querySelector(".item-price");
            const removeBtn = row.querySelector(".remove-item");

            descInput.addEventListener("input", (e) => { items[idx].description = e.target.value; updatePreview(); });
            qtyInput.addEventListener("input", (e) => { items[idx].quantity = parseFloat(e.target.value) || 0; updatePreview(); });
            priceInput.addEventListener("input", (e) => { items[idx].unitPrice = parseFloat(e.target.value) || 0; updatePreview(); });
            removeBtn.addEventListener("click", () => { 
                items.splice(idx, 1);
                if(items.length === 0) items.push({ description: "", quantity: 1, unitPrice: 0 });
                renderItems();
                updatePreview();
            });
            itemsContainer.appendChild(row);
        });
        updatePreview();
    }

    // 新增品項
    function addNewItem() {
        items.push({ description: "", quantity: 1, unitPrice: 0 });
        renderItems();
    }

    // 計算總額
    function calculateTotal() {
        let total = 0;
        for(let it of items) {
            const qty = parseFloat(it.quantity) || 0;
            const price = parseFloat(it.unitPrice) || 0;
            total += qty * price;
        }
        return total;
    }

    // 從表單取得當前完整 document 物件
    function getCurrentDocumentObject() {
        const docNumberRaw = docNumberInput.value.trim();
        const finalDocNumber = docNumberRaw === "" ? `${docTypeMap[currentDocType].short}-${Math.floor(Math.random()*10000)}` : docNumberRaw;
        const date = docDateInput.value || new Date().toISOString().slice(0,10);
        const customer = customerNameInput.value.trim() || "(客戶名稱未填)";
        const customerCode = customerCodeInput.value.trim();
        const remarks = remarksInput.value.trim() || "";
        const filteredItems = items.filter(it => it.description.trim() !== "" || (it.quantity > 0 && it.unitPrice > 0));
        const finalItems = filteredItems.length ? filteredItems : [{ description: "未填寫品項", quantity: 0, unitPrice: 0 }];
        const totalAmount = calculateTotal();

        return {
            id: Date.now() + Math.random() * 10000,
            docType: currentDocType,
            docTypeTitle: docTypeMap[currentDocType].title,
            docNumber: finalDocNumber,
            date: date,
            customerName: customer,
            customerCode: customerCode,
            items: finalItems.map(it => ({ ...it, quantity: parseFloat(it.quantity) || 0, unitPrice: parseFloat(it.unitPrice) || 0 })),
            remarks: remarks,
            total: totalAmount,
            createdAt: new Date().toISOString()
        };
    }

    // 產生單據預覽文字 (漂亮排版)
    function generatePreview(doc) {
        const typeTitle = doc.docTypeTitle;
        const lines = [];
        lines.push(`═══════════════════════════════`);
        lines.push(`        ${typeTitle}`);
        lines.push(`═══════════════════════════════`);
        lines.push(`編號：${doc.docNumber}`);
        lines.push(`日期：${doc.date}`);
        lines.push(`客戶：${doc.customerName}${doc.customerCode ? ` (${doc.customerCode})` : ''}`);
        lines.push(`-----------------------------------`);
        lines.push(`品項                        數量   單價(HKD)   小計`);
        for(let it of doc.items) {
            const desc = it.description.length > 18 ? it.description.slice(0,15)+"..." : it.description.padEnd(18);
            const qtyStr = String(it.quantity).padEnd(6);
            const priceStr = String(it.unitPrice.toFixed(2)).padEnd(10);
            const subtotal = (it.quantity * it.unitPrice).toFixed(2);
            lines.push(`${desc}  ${qtyStr}  ${priceStr}  ${subtotal}`);
        }
        lines.push(`-----------------------------------`);
        lines.push(`總額 (HKD):        ${doc.total.toFixed(2)}`);
        if(doc.remarks) {
            lines.push(`備註：${doc.remarks}`);
        }
        lines.push(`═══════════════════════════════`);
        if(doc.docType === "credit_note") lines.push(`※ 此為貸項通知單，抵扣金額`);
        if(doc.docType === "debit_note") lines.push(`※ 此為借項通知單，應付金額增加`);
        if(doc.docType === "delivery_note") lines.push(`※ 此為送貨單，僅供交貨確認`);
        lines.push(`系統產生時間: ${new Date().toLocaleString()}`);
        return lines.join("\n");
    }

    // 更新即時預覽
    function updatePreview() {
        const draft = getCurrentDocumentObject();
        const previewText = generatePreview(draft);
        previewDiv.innerText = previewText;
    }

    // 儲存單據到 localStorage
    function saveDocument(doc) {
        const stored = localStorage.getItem(STORAGE_KEY);
        let documents = stored ? JSON.parse(stored) : [];
        documents.unshift(doc); // 最新在最前
        localStorage.setItem(STORAGE_KEY, JSON.stringify(documents));
        renderHistory();
        return doc;
    }

    // 渲染歷史記錄
    function renderHistory() {
        const stored = localStorage.getItem(STORAGE_KEY);
        let docs = stored ? JSON.parse(stored) : [];
        if(!docs.length) {
            historyListDiv.innerHTML = `<div style="text-align:center; color:#b1947a;">暫無單據，建立後會自動保存</div>`;
            return;
        }
        historyListDiv.innerHTML = "";
        docs.forEach(doc => {
            const typeLabel = doc.docType === "invoice" ? "🧾發票" : (doc.docType === "delivery_note" ? "🚚送貨單" : (doc.docType === "debit_note" ? "📉借項單" : "📈貸項單"));
            const div = document.createElement("div");
            div.className = "history-item";
            div.innerHTML = `
                <div class="history-info">
                    <span class="history-number">${typeLabel} ${doc.docNumber}</span><br>
                    ${doc.date} | ${doc.customerName} | 總額 HK$ ${doc.total.toFixed(2)}
                </div>
                <div class="history-btns">
                    <button class="small-btn view-doc" data-id="${doc.id}">👁️ 預覽</button>
                    <button class="small-btn delete-doc" data-id="${doc.id}">🗑️ 刪除</button>
                </div>
            `;
            const viewBtn = div.querySelector(".view-doc");
            const delBtn = div.querySelector(".delete-doc");
            viewBtn.addEventListener("click", (e) => {
                e.stopPropagation();
                showDocumentPreview(doc);
            });
            delBtn.addEventListener("click", (e) => {
                e.stopPropagation();
                deleteDocumentById(doc.id);
            });
            historyListDiv.appendChild(div);
        });
    }

    // 刪除單據
    function deleteDocumentById(id) {
        let docs = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
        const newDocs = docs.filter(d => d.id != id);
        localStorage.setItem(STORAGE_KEY, JSON.stringify(newDocs));
        renderHistory();
        // 如果正在編輯的預覽不用特別處理，但可提示
    }

    // 展示單據詳細預覽 (彈出或覆蓋預覽區)
    function showDocumentPreview(doc) {
        const previewHtml = generatePreview(doc);
        // 可直接把右側預覽區切換顯示
        previewDiv.innerText = previewHtml;
        // 可同時提示使用者已載入查看模式，但不覆蓋編輯表單內容，但為了方便，可以詢問載入編輯? 
        if(confirm("要將此單據載入表單進行編輯/另存嗎？\n點擊確定會載入內容")) {
            loadDocumentToForm(doc);
        }
    }

    // 載入歷史單據至表單 (方便修改/重印)
    function loadDocumentToForm(doc) {
        currentDocType = doc.docType;
        // 更新 tab active 樣式
        document.querySelectorAll(".type-chip").forEach(chip => {
            if(chip.dataset.type === currentDocType) chip.classList.add("active");
            else chip.classList.remove("active");
        });
        docNumberInput.value = doc.docNumber;
        docDateInput.value = doc.date;
        customerNameInput.value = doc.customerName;
        customerCodeInput.value = doc.customerCode || "";
        remarksInput.value = doc.remarks || "";
        // 載入品項
        items = doc.items.map(it => ({
            description: it.description,
            quantity: it.quantity,
            unitPrice: it.unitPrice
        }));
        if(items.length === 0) items.push({ description: "", quantity: 1, unitPrice: 0 });
        renderItems();
        updatePreview();
    }

    // 建立新單據主要邏輯 (儲存)
    function handleCreateDocument() {
        // 基本驗證: 至少要有客戶名稱與至少一個有效品項? 但寬容處理
        if(!docNumberInput.value.trim()) {
            if(!confirm("單據編號為空，系統將自動生成編號，繼續嗎？")) return;
        }
        const newDoc = getCurrentDocumentObject();
        // 確保品項不為空描述但不強制
        saveDocument(newDoc);
        alert(`✅ 已儲存 ${newDoc.docTypeTitle} 編號: ${newDoc.docNumber}`);
        // 儲存後不清空表單，但可重置為新增狀態，保留客戶資訊? 為了方便 保留當前內容，但讓用戶可以繼續開下一張，編號可提示變更?
        // 但使用者體驗上建議重置編號與品項？但保留客戶可能更方便，這裡做輕微重置編號提示
        docNumberInput.value = "";  // 清空編號讓下一張手動輸入
        // 保留客戶資料但也可以留，重新聚焦
        docNumberInput.focus();
        updatePreview();
        renderHistory();
    }

    // 重置表單 (清空所有欄位，品項保留一筆空白)
    function resetForm() {
        if(confirm("確定清空目前編輯中的所有資料？")) {
            docNumberInput.value = "";
            setDefaultDate();
            customerNameInput.value = "";
            customerCodeInput.value = "";
            remarksInput.value = "";
            items = [{ description: "", quantity: 1, unitPrice: 0 }];
            renderItems();
            updatePreview();
        }
    }

    // 清除全部歷史
    function clearAllHistory() {
        if(confirm("⚠️ 刪除所有儲存的單據記錄，無法復原，確定繼續嗎？")) {
            localStorage.removeItem(STORAGE_KEY);
            renderHistory();
            alert("歷史記錄已清除");
        }
    }

    // 切換文件類型
    function switchDocType(type) {
        currentDocType = type;
        // 更新 active 樣式
        document.querySelectorAll(".type-chip").forEach(chip => {
            if(chip.dataset.type === type) chip.classList.add("active");
            else chip.classList.remove("active");
        });
        updatePreview();
    }

    // 工具: 防止XSS
    function escapeHtml(str) {
        if(!str) return "";
        return str.replace(/[&<>]/g, function(m) {
            if(m === '&') return '&amp;';
            if(m === '<') return '&lt;';
            if(m === '>') return '&gt;';
            return m;
        });
    }

    // 初始化事件監聽與預設值
    function init() {
        setDefaultDate();
        // 品項初始一筆空白
        items = [{ description: "", quantity: 1, unitPrice: 0 }];
        renderItems();
        // 類型切換
        document.querySelectorAll(".type-chip").forEach(chip => {
            chip.addEventListener("click", (e) => {
                switchDocType(chip.dataset.type);
            });
        });
        document.getElementById("addItemBtn").addEventListener("click", addNewItem);
        document.getElementById("createDocBtn").addEventListener("click", handleCreateDocument);
        document.getElementById("resetFormBtn").addEventListener("click", resetForm);
        document.getElementById("clearHistoryBtn").addEventListener("click", clearAllHistory);
        // 監聽表單變化即時更新預覽
        docNumberInput.addEventListener("input", updatePreview);
        docDateInput.addEventListener("change", updatePreview);
        customerNameInput.addEventListener("input", updatePreview);
        customerCodeInput.addEventListener("input", updatePreview);
        remarksInput.addEventListener("input", updatePreview);
        // 載入歷史
        renderHistory();
        updatePreview();
    }

    init();
</script>
</body>
</html>
```
