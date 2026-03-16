<!DOCTYPE html>
<html lang="en" style="background:#0a0a0f">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Reconciliation Tool — Portfolio Demo</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Instrument+Serif:ital@0;1&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
:root{
  --bg:#0a0a0f;--surface:#13131a;--surface2:#1a1a24;--surface3:#20202e;
  --border:#252535;--border2:#30304a;
  --text:#eaeaf5;--text2:#8888aa;--text3:#44445a;
  --accent:#5b8dee;--accent2:#3b6fd4;
  --green:#2dd4a0;--green-bg:rgba(45,212,160,0.07);
  --red:#f56565;--red-bg:rgba(245,101,101,0.07);
  --amber:#f5c842;--amber-bg:rgba(245,200,66,0.07);
  --purple:#a78bfa;--purple-bg:rgba(167,139,250,0.08);
  --mono:'DM Mono',monospace;--serif:'Instrument Serif',serif;--sans:'DM Sans',sans-serif;
}
*{margin:0;padding:0;box-sizing:border-box;}
body{background:var(--bg);color:var(--text);font-family:var(--sans);font-size:14px;min-height:100vh;line-height:1.6;}
body::before{content:'';position:fixed;inset:0;background-image:linear-gradient(rgba(91,141,238,0.02) 1px,transparent 1px),linear-gradient(90deg,rgba(91,141,238,0.02) 1px,transparent 1px);background-size:40px 40px;pointer-events:none;z-index:0;}
.shell{display:flex;min-height:100vh;position:relative;z-index:1;}

/* SIDEBAR */
.sidebar{width:248px;flex-shrink:0;background:var(--surface);border-right:1px solid var(--border);padding:24px 0;display:flex;flex-direction:column;}
.logo{padding:0 20px 24px;border-bottom:1px solid var(--border);margin-bottom:18px;}
.logo-mark{font-family:var(--serif);font-size:19px;color:var(--text);font-style:italic;}
.logo-mark span{color:var(--accent);font-style:normal;}
.logo-sub{font-size:10px;color:var(--text3);font-family:var(--mono);letter-spacing:0.1em;text-transform:uppercase;margin-top:3px;}
.nav-section{padding:0 10px;margin-bottom:6px;}
.nav-label{font-size:10px;color:var(--text3);font-family:var(--mono);text-transform:uppercase;letter-spacing:0.1em;padding:0 8px;margin-bottom:3px;}
.nav-item{display:flex;align-items:center;gap:9px;padding:8px 10px;border-radius:6px;cursor:pointer;color:var(--text2);font-size:13px;transition:all 0.15s;border:1px solid transparent;user-select:none;}
.nav-item:hover{background:var(--surface2);color:var(--text);}
.nav-item.active{background:rgba(91,141,238,0.1);color:var(--accent);border-color:rgba(91,141,238,0.2);}
.nav-icon{width:15px;height:15px;opacity:0.65;flex-shrink:0;}
.nav-item.active .nav-icon{opacity:1;}
.nav-badge{margin-left:auto;font-size:10px;font-family:var(--mono);background:rgba(91,141,238,0.15);color:var(--accent);padding:1px 6px;border-radius:8px;}
.sidebar-footer{margin-top:auto;padding:14px 18px;border-top:1px solid var(--border);}
.status-badge{display:inline-flex;align-items:center;gap:5px;font-size:11px;font-family:var(--mono);color:var(--green);background:var(--green-bg);border:1px solid rgba(45,212,160,0.2);padding:4px 9px;border-radius:20px;}
.status-dot{width:5px;height:5px;border-radius:50%;background:var(--green);animation:pulse 2s infinite;}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.3}}

/* MAIN */
.main{flex:1;overflow-y:auto;display:flex;flex-direction:column;}
.view{display:none;flex:1;flex-direction:column;}
.view.active{display:flex;}
.topbar{display:flex;align-items:center;justify-content:space-between;padding:14px 28px;border-bottom:1px solid var(--border);background:var(--surface);position:sticky;top:0;z-index:10;flex-shrink:0;}
.topbar-left{display:flex;align-items:center;gap:12px;}
.topbar-title{font-family:var(--serif);font-size:17px;font-style:italic;color:var(--text);}
.topbar-chip{font-size:10px;font-family:var(--mono);padding:3px 8px;border-radius:10px;letter-spacing:0.05em;}
.chip-bank{background:rgba(91,141,238,0.12);color:var(--accent);border:1px solid rgba(91,141,238,0.2);}
.chip-ic{background:var(--purple-bg);color:var(--purple);border:1px solid rgba(167,139,250,0.2);}
.chip-ap{background:var(--amber-bg);color:var(--amber);border:1px solid rgba(245,200,66,0.2);}
.topbar-meta{font-family:var(--mono);font-size:11px;color:var(--text3);}
.content{padding:28px;flex:1;}

/* UPLOAD STRIP */
.upload-strip{display:grid;grid-template-columns:1fr 1fr auto;gap:14px;margin-bottom:24px;}
.upload-card{background:var(--surface);border:1px dashed var(--border2);border-radius:9px;padding:16px 18px;}
.upload-card.loaded{border-style:solid;border-color:var(--green);background:var(--green-bg);}
.upload-card.run-card{border-style:solid;display:flex;align-items:center;justify-content:center;}
.ul-label{font-size:10px;font-family:var(--mono);color:var(--text3);text-transform:uppercase;letter-spacing:0.08em;margin-bottom:5px;}
.ul-title{font-size:13px;color:var(--text);font-weight:500;margin-bottom:2px;}
.ul-sub{font-size:11px;color:var(--text3);}
.ul-status{display:flex;align-items:center;gap:5px;margin-top:8px;font-size:11px;font-family:var(--mono);color:var(--green);}

/* KPI ROW */
.kpi-row{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-bottom:24px;}
.kpi-card{background:var(--surface);border:1px solid var(--border);border-radius:9px;padding:15px 17px;}
.kpi-label{font-size:10px;font-family:var(--mono);color:var(--text3);text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px;}
.kpi-value{font-family:var(--serif);font-size:24px;color:var(--text);line-height:1;margin-bottom:3px;}
.kpi-delta{font-size:11px;font-family:var(--mono);}
.d-green{color:var(--green);}.d-red{color:var(--red);}.d-neu{color:var(--text3);}.d-amber{color:var(--amber);}

/* TABS */
.tab-row{display:flex;gap:0;margin-bottom:20px;border:1px solid var(--border);border-radius:8px;overflow:hidden;background:var(--surface);}
.tab{flex:1;padding:9px 14px;text-align:center;font-size:12px;font-family:var(--mono);color:var(--text2);cursor:pointer;transition:all 0.15s;border-right:1px solid var(--border);}
.tab:last-child{border-right:none;}
.tab:hover{background:var(--surface2);color:var(--text);}
.tab.active{background:rgba(91,141,238,0.1);color:var(--accent);}
.tab-count{display:inline-flex;align-items:center;justify-content:center;width:16px;height:16px;border-radius:50%;font-size:9px;margin-left:6px;}
.tc-green{background:var(--green-bg);color:var(--green);}
.tc-red{background:var(--red-bg);color:var(--red);}
.tc-amber{background:var(--amber-bg);color:var(--amber);}
.tc-blue{background:rgba(91,141,238,0.12);color:var(--accent);}

/* SECTION */
.section-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;}
.section-title{font-family:var(--serif);font-size:16px;font-style:italic;color:var(--text);}
.section-actions{display:flex;gap:8px;}
.btn{display:inline-flex;align-items:center;gap:6px;padding:6px 13px;border-radius:6px;font-size:12px;font-family:var(--mono);cursor:pointer;transition:all 0.15s;border:1px solid transparent;}
.btn-ghost{background:transparent;border-color:var(--border2);color:var(--text2);}
.btn-ghost:hover{border-color:var(--accent);color:var(--accent);}
.btn-primary{background:var(--accent);color:white;border-color:var(--accent);}
.btn-primary:hover{background:var(--accent2);}
.btn-run{background:var(--accent);color:white;border-color:var(--accent);padding:10px 22px;font-size:13px;}
.btn-run:hover{background:var(--accent2);}

/* TABLE */
.table-wrap{background:var(--surface);border:1px solid var(--border);border-radius:9px;overflow:hidden;margin-bottom:22px;}
.tab-content{display:none;}.tab-content.active{display:block;}
table{width:100%;border-collapse:collapse;}
thead tr{background:var(--surface2);border-bottom:1px solid var(--border);}
th{padding:9px 14px;text-align:left;font-size:10px;font-family:var(--mono);color:var(--text3);text-transform:uppercase;letter-spacing:0.07em;font-weight:400;}
th.r{text-align:right;}
td{padding:10px 14px;font-size:12px;color:var(--text2);border-bottom:1px solid var(--border);}
tbody tr:last-child td{border-bottom:none;}
tbody tr:hover{background:var(--surface2);}
td.r{text-align:right;font-family:var(--mono);font-size:11px;}
td.bold{color:var(--text);font-weight:500;}
td.muted{color:var(--text3);font-size:11px;}

/* CONFIDENCE BAR */
.conf-bar{display:flex;align-items:center;gap:8px;}
.conf-track{flex:1;height:4px;background:var(--border);border-radius:2px;overflow:hidden;}
.conf-fill{height:100%;border-radius:2px;}
.conf-label{font-family:var(--mono);font-size:10px;width:30px;text-align:right;}

/* STATUS PILLS */
.pill{display:inline-flex;align-items:center;gap:3px;font-size:10px;font-family:var(--mono);padding:2px 7px;border-radius:8px;}
.pill-match{background:var(--green-bg);color:var(--green);border:1px solid rgba(45,212,160,0.2);}
.pill-unmatch{background:var(--red-bg);color:var(--red);border:1px solid rgba(245,101,101,0.2);}
.pill-timing{background:var(--amber-bg);color:var(--amber);border:1px solid rgba(245,200,66,0.2);}
.pill-dup{background:var(--purple-bg);color:var(--purple);border:1px solid rgba(167,139,250,0.2);}
.pill-partial{background:rgba(91,141,238,0.1);color:var(--accent);border:1px solid rgba(91,141,238,0.2);}

/* AI SUMMARY BOX */
.ai-box{background:var(--surface);border:1px solid var(--border);border-radius:9px;overflow:hidden;margin-bottom:22px;}
.ai-box-header{display:flex;align-items:center;justify-content:space-between;padding:12px 18px;border-bottom:1px solid var(--border);background:var(--surface2);}
.ai-box-left{display:flex;align-items:center;gap:9px;}
.ai-chip{display:inline-flex;align-items:center;gap:4px;font-size:10px;font-family:var(--mono);color:var(--accent);background:rgba(91,141,238,0.1);border:1px solid rgba(91,141,238,0.2);padding:3px 7px;border-radius:8px;text-transform:uppercase;letter-spacing:0.06em;}
.ai-box-title{font-size:13px;color:var(--text);font-weight:500;}
.ai-body{padding:22px 24px;line-height:1.8;}
.ai-body p{color:var(--text2);font-size:13px;margin-bottom:14px;}
.ai-body p:last-child{margin-bottom:0;}
.ai-body p strong{color:var(--text);font-weight:500;}
.ai-placeholder{padding:32px;text-align:center;color:var(--text3);font-size:12px;}
.ai-placeholder svg{display:block;margin:0 auto 10px;opacity:0.25;}
.generating{padding:24px;display:flex;align-items:center;gap:12px;}
.gen-dots{display:flex;gap:4px;}
.gen-dot{width:5px;height:5px;border-radius:50%;background:var(--accent);}
.gen-dot:nth-child(1){animation:gd 1.2s infinite;}
.gen-dot:nth-child(2){animation:gd 1.2s 0.15s infinite;}
.gen-dot:nth-child(3){animation:gd 1.2s 0.3s infinite;}
@keyframes gd{0%,80%,100%{opacity:0.2;transform:scale(0.8)}40%{opacity:1;transform:scale(1)}}
.gen-text{font-family:var(--mono);font-size:11px;color:var(--text3);}

/* CHARTS */
.chart-row{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:22px;}
.chart-card{background:var(--surface);border:1px solid var(--border);border-radius:9px;padding:20px;}
.chart-card-title{font-family:var(--serif);font-size:15px;font-style:italic;color:var(--text);margin-bottom:4px;}
.chart-card-sub{font-size:11px;font-family:var(--mono);color:var(--text3);margin-bottom:16px;}
.chart-wrap{position:relative;height:220px;}

/* FOOTER */
.page-footer{padding:16px 28px;border-top:1px solid var(--border);display:flex;align-items:center;justify-content:space-between;font-family:var(--mono);font-size:10px;color:var(--text3);flex-shrink:0;}
.dl-btn{display:inline-flex;align-items:center;gap:6px;background:var(--surface2);border:1px solid var(--border2);color:var(--text2);padding:6px 12px;border-radius:6px;font-size:11px;font-family:var(--mono);cursor:pointer;text-decoration:none;transition:all 0.15s;}
.dl-btn:hover{border-color:var(--green);color:var(--green);}

::-webkit-scrollbar{width:4px;}
::-webkit-scrollbar-thumb{background:var(--border2);border-radius:2px;}
</style>
</head>
<body>
<div class="shell">

<!-- SIDEBAR -->
<nav class="sidebar">
  <div class="logo">
    <div class="logo-mark">Recon<span>AI</span></div>
    <div class="logo-sub">Reconciliation Engine v1.0</div>
  </div>
  <div class="nav-section">
    <div class="nav-label">Reconciliations</div>
    <div class="nav-item active" id="nav-bank" onclick="showView('bank')">
      <svg class="nav-icon" viewBox="0 0 15 15" fill="none" stroke="currentColor" stroke-width="1.4"><rect x="1" y="3" width="13" height="9" rx="1"/><path d="M1 6h13M4 9h2M8 9h3"/></svg>
      Bank reconciliation
      <span class="nav-badge">14</span>
    </div>
    <div class="nav-item" id="nav-ic" onclick="showView('ic')">
      <svg class="nav-icon" viewBox="0 0 15 15" fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="4" cy="7" r="2.5"/><circle cx="11" cy="7" r="2.5"/><path d="M6.5 7h2"/></svg>
      Intercompany
      <span class="nav-badge">8</span>
    </div>
    <div class="nav-item" id="nav-ap" onclick="showView('ap')">
      <svg class="nav-icon" viewBox="0 0 15 15" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M3 3h9v9H3z"/><path d="M6 6h3M6 9h3M6 3v2M9 3v2"/></svg>
      Accounts payable
      <span class="nav-badge">11</span>
    </div>
  </div>
  <div class="nav-section" style="margin-top:10px">
    <div class="nav-label">Reports</div>
    <div class="nav-item" onclick="toast('Generates audit-ready sign-off PDF — connected to report_engine.py')">
      <svg class="nav-icon" viewBox="0 0 15 15" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M9 1H4a1 1 0 00-1 1v11a1 1 0 001 1h7a1 1 0 001-1V5L9 1z"/><path d="M9 1v4h4"/></svg>
      Export sign-off PDF
    </div>
    <div class="nav-item" onclick="toast('Exports all exceptions to Excel — connected to exception_engine.py')">
      <svg class="nav-icon" viewBox="0 0 15 15" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M13 10v2a1 1 0 01-1 1H3a1 1 0 01-1-1v-2M7.5 2v8M5 7.5l2.5 2.5 2.5-2.5"/></svg>
      Export exceptions
    </div>
  </div>
  <div class="sidebar-footer">
    <div class="status-badge"><div class="status-dot"></div>GPT-4o connected</div>
  </div>
</nav>

<!-- MAIN -->
<div class="main">

<!-- ═══════════════════════════════════════════════════
     VIEW 1: BANK RECONCILIATION
═══════════════════════════════════════════════════ -->
<div class="view active" id="view-bank">
  <div class="topbar">
    <div class="topbar-left">
      <div class="topbar-title">Bank reconciliation</div>
      <div class="topbar-chip chip-bank">HSBC Operating Account</div>
    </div>
    <div class="topbar-meta">June 2024 · GBP</div>
  </div>
  <div class="content">

    <div class="upload-strip">
      <div class="upload-card loaded">
        <div class="ul-label">Source A</div><div class="ul-title">Bank statement</div><div class="ul-sub">HSBC · June 2024 · 142 lines</div>
        <div class="ul-status"><svg width="10" height="10" viewBox="0 0 10 10" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="1,5 4,8 9,2"/></svg>Loaded</div>
      </div>
      <div class="upload-card loaded">
        <div class="ul-label">Source B</div><div class="ul-title">General ledger extract</div><div class="ul-sub">SAP · Cash account 10001 · 138 lines</div>
        <div class="ul-status"><svg width="10" height="10" viewBox="0 0 10 10" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="1,5 4,8 9,2"/></svg>Loaded</div>
      </div>
      <div class="upload-card run-card" style="min-width:160px">
        <div class="btn btn-run" id="bank-run-btn" onclick="runBankRecon()">
          <svg width="13" height="13" viewBox="0 0 13 13" fill="none" stroke="currentColor" stroke-width="1.5"><polygon points="2,1 12,6.5 2,12"/></svg>
          Run reconciliation
        </div>
      </div>
    </div>

    <div class="kpi-row" id="bank-kpis">
      <div class="kpi-card"><div class="kpi-label">Total lines</div><div class="kpi-value">142</div><div class="kpi-delta d-neu">Bank statement</div></div>
      <div class="kpi-card"><div class="kpi-label">Matched</div><div class="kpi-value" style="color:var(--green)" id="bk-matched">—</div><div class="kpi-delta d-green" id="bk-matched-sub">Run to calculate</div></div>
      <div class="kpi-card"><div class="kpi-label">Exceptions</div><div class="kpi-value" style="color:var(--red)" id="bk-exceptions">—</div><div class="kpi-delta d-red" id="bk-ex-sub">Require investigation</div></div>
      <div class="kpi-card"><div class="kpi-label">Timing diffs</div><div class="kpi-value" style="color:var(--amber)" id="bk-timing">—</div><div class="kpi-delta d-amber" id="bk-timing-sub">Expected to clear</div></div>
      <div class="kpi-card"><div class="kpi-label">Match rate</div><div class="kpi-value" id="bk-rate">—</div><div class="kpi-delta d-neu" id="bk-rate-sub">Confidence score</div></div>
    </div>

    <div id="bank-results" style="display:none">
      <div class="chart-row">
        <div class="chart-card">
          <div class="chart-card-title">Reconciliation breakdown</div>
          <div class="chart-card-sub">Distribution of all 142 items by match status</div>
          <div class="chart-wrap"><canvas id="bankDonut"></canvas></div>
        </div>
        <div class="chart-card">
          <div class="chart-card-title">Exception value by type £</div>
          <div class="chart-card-sub">Unmatched items grouped by exception category</div>
          <div class="chart-wrap"><canvas id="bankBar"></canvas></div>
        </div>
      </div>

      <div class="tab-row">
        <div class="tab active" onclick="switchTab('bank','matched')">Matched items<span class="tab-count tc-green" id="tc-bk-m">128</span></div>
        <div class="tab" onclick="switchTab('bank','exceptions')">Exceptions<span class="tab-count tc-red" id="tc-bk-e">8</span></div>
        <div class="tab" onclick="switchTab('bank','timing')">Timing differences<span class="tab-count tc-amber" id="tc-bk-t">6</span></div>
        <div class="tab" onclick="switchTab('bank','ai')">AI summary<span class="tab-count tc-blue">GPT</span></div>
      </div>

      <!-- Matched -->
      <div class="tab-content active" id="bank-tab-matched">
        <div class="section-header"><div class="section-title">Matched items — 128 of 142</div><div class="section-actions"><div class="btn btn-ghost" onclick="toast('Filter logic: df[df.match_type == exact] — see recon_engine.py')">Exact only</div></div></div>
        <div class="table-wrap"><table>
          <thead><tr><th>Date</th><th>Bank description</th><th>GL description</th><th class="r">Amount £</th><th>Match type</th><th>Confidence</th></tr></thead>
          <tbody id="bank-matched-tbody"></tbody>
        </table></div>
      </div>

      <!-- Exceptions -->
      <div class="tab-content" id="bank-tab-exceptions">
        <div class="section-header"><div class="section-title">Exceptions requiring investigation</div><div class="section-actions"><div class="btn btn-primary" id="bank-ai-btn" onclick="generateBankSummary()"><svg width="11" height="11" viewBox="0 0 11 11" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M5.5 1l1.2 2.8 3 .4-2.2 2 .5 3L5.5 8 3 9.2l.5-3L1.3 4.2l3-.4z"/></svg>Generate AI actions</div></div></div>
        <div class="table-wrap"><table>
          <thead><tr><th>Date</th><th>Description</th><th>Source</th><th class="r">Amount £</th><th>Type</th><th>AI suggested action</th></tr></thead>
          <tbody id="bank-exc-tbody"></tbody>
        </table></div>
      </div>

      <!-- Timing -->
      <div class="tab-content" id="bank-tab-timing">
        <div class="section-header"><div class="section-title">Timing differences — expected to clear next period</div></div>
        <div class="table-wrap"><table>
          <thead><tr><th>Date (bank)</th><th>Expected GL date</th><th>Description</th><th class="r">Amount £</th><th>Reason</th></tr></thead>
          <tbody id="bank-timing-tbody"></tbody>
        </table></div>
      </div>

      <!-- AI Summary -->
      <div class="tab-content" id="bank-tab-ai">
        <div class="ai-box">
          <div class="ai-box-header">
            <div class="ai-box-left"><div class="ai-chip"><svg width="7" height="7" viewBox="0 0 7 7" fill="currentColor"><circle cx="3.5" cy="3.5" r="3"/></svg>GPT-4o</div><div class="ai-box-title">Reconciliation sign-off summary</div></div>
            <div id="bank-copy-btn" style="display:none"><div class="btn btn-ghost" onclick="copyText('bank-ai-text')">Copy</div></div>
          </div>
          <div id="bank-ai-content"><div class="ai-placeholder"><svg width="30" height="30" viewBox="0 0 30 30" fill="none" stroke="currentColor" stroke-width="1"><path d="M15 3l2 6h6l-5 3.5 2 6-5-3.5-5 3.5 2-6L7 9h6z"/></svg>Click "Generate AI actions" on the Exceptions tab to produce the full summary.</div></div>
        </div>
      </div>
    </div>
  </div>
  <div class="page-footer"><span>ReconAI · Bank reconciliation · Built with Python + fuzzy matching + GPT-4o</span><a class="dl-btn" href="#" onclick="toast('Exports audit-ready Excel — connected to report_engine.py');return false;"><svg width="11" height="11" viewBox="0 0 11 11" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M9 7v2a1 1 0 01-1 1H2a1 1 0 01-1-1V7M5 1v7M2.5 5L5 7.5 7.5 5"/></svg>Export report</a></div>
</div>

<!-- ═══════════════════════════════════════════════════
     VIEW 2: INTERCOMPANY
═══════════════════════════════════════════════════ -->
<div class="view" id="view-ic">
  <div class="topbar">
    <div class="topbar-left">
      <div class="topbar-title">Intercompany reconciliation</div>
      <div class="topbar-chip chip-ic">Entity A ↔ Entity B</div>
    </div>
    <div class="topbar-meta">June 2024 · GBP</div>
  </div>
  <div class="content">
    <div class="upload-strip">
      <div class="upload-card loaded">
        <div class="ul-label">Entity A</div><div class="ul-title">UK HoldCo ledger</div><div class="ul-sub">Interco payable / receivable · 52 lines</div>
        <div class="ul-status"><svg width="10" height="10" viewBox="0 0 10 10" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="1,5 4,8 9,2"/></svg>Loaded</div>
      </div>
      <div class="upload-card loaded">
        <div class="ul-label">Entity B</div><div class="ul-title">EU OpCo ledger</div><div class="ul-sub">Interco payable / receivable · 49 lines</div>
        <div class="ul-status"><svg width="10" height="10" viewBox="0 0 10 10" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="1,5 4,8 9,2"/></svg>Loaded</div>
      </div>
      <div class="upload-card run-card" style="min-width:160px">
        <div class="btn btn-run" id="ic-run-btn" onclick="runICRecon()">
          <svg width="13" height="13" viewBox="0 0 13 13" fill="none" stroke="currentColor" stroke-width="1.5"><polygon points="2,1 12,6.5 2,12"/></svg>
          Run reconciliation
        </div>
      </div>
    </div>

    <div class="kpi-row">
      <div class="kpi-card"><div class="kpi-label">Entity A balance</div><div class="kpi-value">£2.84m</div><div class="kpi-delta d-neu">Interco receivable</div></div>
      <div class="kpi-card"><div class="kpi-label">Entity B balance</div><div class="kpi-value">£2.84m</div><div class="kpi-delta d-neu">Interco payable</div></div>
      <div class="kpi-card"><div class="kpi-label">In-agreement</div><div class="kpi-value" style="color:var(--green)" id="ic-agree">—</div><div class="kpi-delta d-green" id="ic-agree-sub">Run to calculate</div></div>
      <div class="kpi-card"><div class="kpi-label">Disagreements</div><div class="kpi-value" style="color:var(--red)" id="ic-dis">—</div><div class="kpi-delta d-red" id="ic-dis-sub">Require elimination</div></div>
      <div class="kpi-card"><div class="kpi-label">Net difference</div><div class="kpi-value" id="ic-diff">—</div><div class="kpi-delta d-neu" id="ic-diff-sub">Must be zero at group level</div></div>
    </div>

    <div id="ic-results" style="display:none">
      <div class="chart-row">
        <div class="chart-card">
          <div class="chart-card-title">Agreement status breakdown</div>
          <div class="chart-card-sub">52 intercompany transactions between entities</div>
          <div class="chart-wrap"><canvas id="icDonut"></canvas></div>
        </div>
        <div class="chart-card">
          <div class="chart-card-title">Disagreement value by category £</div>
          <div class="chart-card-sub">FX timing, cut-off differences, posting errors</div>
          <div class="chart-wrap"><canvas id="icBar"></canvas></div>
        </div>
      </div>

      <div class="tab-row">
        <div class="tab active" onclick="switchTab('ic','agreed')">In agreement<span class="tab-count tc-green">44</span></div>
        <div class="tab" onclick="switchTab('ic','disagree')">Disagreements<span class="tab-count tc-red">5</span></div>
        <div class="tab" onclick="switchTab('ic','fx')">FX differences<span class="tab-count tc-amber">3</span></div>
        <div class="tab" onclick="switchTab('ic','ai')">AI summary<span class="tab-count tc-blue">GPT</span></div>
      </div>

      <div class="tab-content active" id="ic-tab-agreed">
        <div class="section-header"><div class="section-title">Transactions in agreement — 44 of 52</div></div>
        <div class="table-wrap"><table>
          <thead><tr><th>Transaction ref</th><th>Description</th><th>Entity A £</th><th>Entity B £</th><th>Difference</th><th>Status</th></tr></thead>
          <tbody id="ic-agreed-tbody"></tbody>
        </table></div>
      </div>

      <div class="tab-content" id="ic-tab-disagree">
        <div class="section-header"><div class="section-title">Disagreements requiring elimination</div><div class="section-actions"><div class="btn btn-primary" onclick="generateICSummary()"><svg width="11" height="11" viewBox="0 0 11 11" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M5.5 1l1.2 2.8 3 .4-2.2 2 .5 3L5.5 8 3 9.2l.5-3L1.3 4.2l3-.4z"/></svg>Generate AI analysis</div></div></div>
        <div class="table-wrap"><table>
          <thead><tr><th>Ref</th><th>Description</th><th>Entity A £</th><th>Entity B £</th><th>Difference £</th><th>Root cause</th></tr></thead>
          <tbody id="ic-dis-tbody"></tbody>
        </table></div>
      </div>

      <div class="tab-content" id="ic-tab-fx">
        <div class="section-header"><div class="section-title">FX translation differences</div></div>
        <div class="table-wrap"><table>
          <thead><tr><th>Ref</th><th>Description</th><th>EUR amount</th><th>Entity A rate</th><th>Entity B rate</th><th>GBP difference £</th></tr></thead>
          <tbody id="ic-fx-tbody"></tbody>
        </table></div>
      </div>

      <div class="tab-content" id="ic-tab-ai">
        <div class="ai-box">
          <div class="ai-box-header">
            <div class="ai-box-left"><div class="ai-chip"><svg width="7" height="7" viewBox="0 0 7 7" fill="currentColor"><circle cx="3.5" cy="3.5" r="3"/></svg>GPT-4o</div><div class="ai-box-title">Intercompany elimination analysis</div></div>
            <div id="ic-copy-btn" style="display:none"><div class="btn btn-ghost" onclick="copyText('ic-ai-text')">Copy</div></div>
          </div>
          <div id="ic-ai-content"><div class="ai-placeholder"><svg width="30" height="30" viewBox="0 0 30 30" fill="none" stroke="currentColor" stroke-width="1"><path d="M15 3l2 6h6l-5 3.5 2 6-5-3.5-5 3.5 2-6L7 9h6z"/></svg>Click "Generate AI analysis" on the Disagreements tab.</div></div>
        </div>
      </div>
    </div>
  </div>
  <div class="page-footer"><span>ReconAI · Intercompany reconciliation · IFRS 10 elimination support</span><a class="dl-btn" href="#" onclick="toast('Exports group elimination schedule');return false;"><svg width="11" height="11" viewBox="0 0 11 11" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M9 7v2a1 1 0 01-1 1H2a1 1 0 01-1-1V7M5 1v7M2.5 5L5 7.5 7.5 5"/></svg>Export report</a></div>
</div>

<!-- ═══════════════════════════════════════════════════
     VIEW 3: ACCOUNTS PAYABLE
═══════════════════════════════════════════════════ -->
<div class="view" id="view-ap">
  <div class="topbar">
    <div class="topbar-left">
      <div class="topbar-title">Accounts payable reconciliation</div>
      <div class="topbar-chip chip-ap">Supplier statements vs ledger</div>
    </div>
    <div class="topbar-meta">June 2024 · 6 suppliers</div>
  </div>
  <div class="content">
    <div class="upload-strip">
      <div class="upload-card loaded">
        <div class="ul-label">Source A</div><div class="ul-title">Supplier statements</div><div class="ul-sub">6 suppliers · 87 invoices total</div>
        <div class="ul-status"><svg width="10" height="10" viewBox="0 0 10 10" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="1,5 4,8 9,2"/></svg>Loaded</div>
      </div>
      <div class="upload-card loaded">
        <div class="ul-label">Source B</div><div class="ul-title">AP ledger extract</div><div class="ul-sub">SAP · Vendor accounts · 83 invoices</div>
        <div class="ul-status"><svg width="10" height="10" viewBox="0 0 10 10" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="1,5 4,8 9,2"/></svg>Loaded</div>
      </div>
      <div class="upload-card run-card" style="min-width:160px">
        <div class="btn btn-run" id="ap-run-btn" onclick="runAPRecon()">
          <svg width="13" height="13" viewBox="0 0 13 13" fill="none" stroke="currentColor" stroke-width="1.5"><polygon points="2,1 12,6.5 2,12"/></svg>
          Run reconciliation
        </div>
      </div>
    </div>

    <div class="kpi-row">
      <div class="kpi-card"><div class="kpi-label">Total supplier value</div><div class="kpi-value">£487k</div><div class="kpi-delta d-neu">Per statements</div></div>
      <div class="kpi-card"><div class="kpi-label">Matched invoices</div><div class="kpi-value" style="color:var(--green)" id="ap-matched">—</div><div class="kpi-delta d-green" id="ap-matched-sub">Run to calculate</div></div>
      <div class="kpi-card"><div class="kpi-label">Missing in ledger</div><div class="kpi-value" style="color:var(--red)" id="ap-missing">—</div><div class="kpi-delta d-red" id="ap-missing-sub">Invoices not posted</div></div>
      <div class="kpi-card"><div class="kpi-label">Duplicates flagged</div><div class="kpi-value" style="color:var(--purple)" id="ap-dups">—</div><div class="kpi-delta" style="color:var(--purple)" id="ap-dups-sub">Potential double-pays</div></div>
      <div class="kpi-card"><div class="kpi-label">Value at risk</div><div class="kpi-value" style="color:var(--red)" id="ap-risk">—</div><div class="kpi-delta d-red" id="ap-risk-sub">Unreconciled amount</div></div>
    </div>

    <div id="ap-results" style="display:none">
      <div class="chart-row">
        <div class="chart-card">
          <div class="chart-card-title">AP reconciliation status</div>
          <div class="chart-card-sub">87 supplier invoices by match outcome</div>
          <div class="chart-wrap"><canvas id="apDonut"></canvas></div>
        </div>
        <div class="chart-card">
          <div class="chart-card-title">Exceptions by supplier £</div>
          <div class="chart-card-sub">Value of unmatched invoices per supplier</div>
          <div class="chart-wrap"><canvas id="apBar"></canvas></div>
        </div>
      </div>

      <div class="tab-row">
        <div class="tab active" onclick="switchTab('ap','matched')">Matched<span class="tab-count tc-green">72</span></div>
        <div class="tab" onclick="switchTab('ap','missing')">Missing in ledger<span class="tab-count tc-red">9</span></div>
        <div class="tab" onclick="switchTab('ap','dups')">Duplicate risk<span class="tab-count" style="background:var(--purple-bg);color:var(--purple)">4</span></div>
        <div class="tab" onclick="switchTab('ap','ai')">AI summary<span class="tab-count tc-blue">GPT</span></div>
      </div>

      <div class="tab-content active" id="ap-tab-matched">
        <div class="section-header"><div class="section-title">Matched invoices — 72 of 87</div></div>
        <div class="table-wrap"><table>
          <thead><tr><th>Invoice #</th><th>Supplier</th><th>Invoice date</th><th class="r">Amount £</th><th>GL posting ref</th><th>Status</th></tr></thead>
          <tbody id="ap-matched-tbody"></tbody>
        </table></div>
      </div>

      <div class="tab-content" id="ap-tab-missing">
        <div class="section-header"><div class="section-title">Invoices missing from ledger</div><div class="section-actions"><div class="btn btn-primary" onclick="generateAPSummary()"><svg width="11" height="11" viewBox="0 0 11 11" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M5.5 1l1.2 2.8 3 .4-2.2 2 .5 3L5.5 8 3 9.2l.5-3L1.3 4.2l3-.4z"/></svg>Generate AI actions</div></div></div>
        <div class="table-wrap"><table>
          <thead><tr><th>Invoice #</th><th>Supplier</th><th>Invoice date</th><th class="r">Amount £</th><th>Days outstanding</th><th>AI recommended action</th></tr></thead>
          <tbody id="ap-missing-tbody"></tbody>
        </table></div>
      </div>

      <div class="tab-content" id="ap-tab-dups">
        <div class="section-header"><div class="section-title">Potential duplicate payments — urgent review required</div></div>
        <div class="table-wrap"><table>
          <thead><tr><th>Invoice #</th><th>Supplier</th><th class="r">Amount £</th><th>Original posting</th><th>Potential duplicate</th><th>Risk level</th></tr></thead>
          <tbody id="ap-dups-tbody"></tbody>
        </table></div>
      </div>

      <div class="tab-content" id="ap-tab-ai">
        <div class="ai-box">
          <div class="ai-box-header">
            <div class="ai-box-left"><div class="ai-chip"><svg width="7" height="7" viewBox="0 0 7 7" fill="currentColor"><circle cx="3.5" cy="3.5" r="3"/></svg>GPT-4o</div><div class="ai-box-title">AP reconciliation exception report</div></div>
            <div id="ap-copy-btn" style="display:none"><div class="btn btn-ghost" onclick="copyText('ap-ai-text')">Copy</div></div>
          </div>
          <div id="ap-ai-content"><div class="ai-placeholder"><svg width="30" height="30" viewBox="0 0 30 30" fill="none" stroke="currentColor" stroke-width="1"><path d="M15 3l2 6h6l-5 3.5 2 6-5-3.5-5 3.5 2-6L7 9h6z"/></svg>Click "Generate AI actions" on the Missing in ledger tab.</div></div>
        </div>
      </div>
    </div>
  </div>
  <div class="page-footer"><span>ReconAI · AP reconciliation · Duplicate detection + exception flagging</span><a class="dl-btn" href="#" onclick="toast('Exports AP exception schedule to Excel');return false;"><svg width="11" height="11" viewBox="0 0 11 11" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M9 7v2a1 1 0 01-1 1H2a1 1 0 01-1-1V7M5 1v7M2.5 5L5 7.5 7.5 5"/></svg>Export report</a></div>
</div>

</div><!-- end .main -->
</div><!-- end .shell -->

<script>
// ─── VIEW SWITCHING ───────────────────────────────────────────────────────────
function showView(name) {
  document.querySelectorAll('.view').forEach(v=>v.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n=>n.classList.remove('active'));
  document.getElementById('view-'+name).classList.add('active');
  document.getElementById('nav-'+name).classList.add('active');
}

function switchTab(view, tab) {
  const wrap = document.getElementById('view-'+view);
  wrap.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
  wrap.querySelectorAll('.tab-content').forEach(t=>t.classList.remove('active'));
  event.currentTarget.classList.add('active');
  document.getElementById(view+'-tab-'+tab).classList.add('active');
}

// ─── TOAST ────────────────────────────────────────────────────────────────────
function toast(msg) {
  const t=document.createElement('div');
  t.style.cssText='position:fixed;bottom:22px;right:22px;background:#13131a;border:1px solid var(--green);color:var(--green);font-family:var(--mono);font-size:11px;padding:10px 16px;border-radius:7px;z-index:999;transition:opacity 0.3s;max-width:360px;';
  t.textContent='✓ '+msg; document.body.appendChild(t);
  setTimeout(()=>{t.style.opacity='0';setTimeout(()=>t.remove(),300);},2800);
}

function copyText(id) {
  const el=document.getElementById(id);
  if(el) navigator.clipboard.writeText(el.innerText).then(()=>toast('Copied to clipboard'));
}

// ─── CHART HELPERS ────────────────────────────────────────────────────────────
function donut(id, labels, data, colors) {
  new Chart(document.getElementById(id),{
    type:'doughnut',
    data:{labels,datasets:[{data,backgroundColor:colors,borderColor:'#13131a',borderWidth:3,hoverOffset:4}]},
    options:{responsive:true,maintainAspectRatio:false,cutout:'68%',
      plugins:{legend:{position:'right',labels:{color:'#8888aa',font:{family:"'DM Mono'",size:10},padding:12,boxWidth:10}},
      tooltip:{backgroundColor:'#1a1a24',borderColor:'#252535',borderWidth:1,titleColor:'#eaeaf5',bodyColor:'#8888aa',titleFont:{family:"'DM Mono'",size:10},bodyFont:{family:"'DM Mono'",size:10}}}}
  });
}

function bar(id, labels, data, colors) {
  new Chart(document.getElementById(id),{
    type:'bar',
    data:{labels,datasets:[{label:'£',data,backgroundColor:colors,borderColor:colors,borderWidth:1,borderRadius:4}]},
    options:{responsive:true,maintainAspectRatio:false,
      plugins:{legend:{display:false},
      tooltip:{backgroundColor:'#1a1a24',borderColor:'#252535',borderWidth:1,titleColor:'#eaeaf5',bodyColor:'#8888aa',titleFont:{family:"'DM Mono'",size:10},bodyFont:{family:"'DM Mono'",size:10},callbacks:{label:c=>' £'+c.raw.toLocaleString()}}},
      scales:{
        x:{ticks:{color:'#44445a',font:{family:"'DM Mono'",size:10}},grid:{color:'rgba(255,255,255,0.03)'},border:{color:'#252535'}},
        y:{ticks:{color:'#44445a',font:{family:"'DM Mono'",size:10},callback:v=>'£'+v.toLocaleString()},grid:{color:'rgba(255,255,255,0.03)'},border:{color:'#252535'}}
      }}
  });
}

function confBar(score) {
  const c = score>=95?'var(--green)':score>=80?'var(--amber)':'var(--red)';
  return `<div class="conf-bar"><div class="conf-track"><div class="conf-fill" style="width:${score}%;background:${c}"></div></div><div class="conf-label" style="color:${c};font-family:var(--mono);font-size:10px">${score}%</div></div>`;
}

function pill(type) {
  const map={match:'<span class="pill pill-match">✓ Matched</span>',unmatch:'<span class="pill pill-unmatch">✗ Unmatched</span>',timing:'<span class="pill pill-timing">⏱ Timing</span>',dup:'<span class="pill pill-dup">⚠ Duplicate</span>',partial:'<span class="pill pill-partial">~ Partial</span>',agree:'<span class="pill pill-match">✓ Agreed</span>',dis:'<span class="pill pill-unmatch">✗ Disagree</span>',fx:'<span class="pill pill-timing">FX diff</span>'};
  return map[type]||'';
}

// ─── BANK RECON ───────────────────────────────────────────────────────────────
function runBankRecon() {
  const btn=document.getElementById('bank-run-btn');
  btn.innerHTML='<div style="display:flex;align-items:center;gap:6px"><div class="gen-dots"><div class="gen-dot" style="animation:gd 1.2s infinite"></div><div class="gen-dot" style="animation:gd 1.2s 0.15s infinite"></div><div class="gen-dot" style="animation:gd 1.2s 0.3s infinite"></div></div>Running…</div>';

  setTimeout(()=>{
    document.getElementById('bk-matched').textContent='128';
    document.getElementById('bk-matched-sub').textContent='90.1% of 142 lines';
    document.getElementById('bk-exceptions').textContent='8';
    document.getElementById('bk-ex-sub').textContent='£34,250 unreconciled';
    document.getElementById('bk-timing').textContent='6';
    document.getElementById('bk-timing-sub').textContent='£12,800 timing diffs';
    document.getElementById('bk-rate').textContent='94.2%';
    document.getElementById('bk-rate-sub').style.color='var(--green)';
    document.getElementById('bk-rate-sub').textContent='Excellent match rate';
    document.getElementById('bank-results').style.display='block';
    btn.innerHTML='<svg width="11" height="11" viewBox="0 0 11 11" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="1,5 4,8 9,2"/></svg> Complete — 128 matched';
    btn.style.cssText='background:var(--green);border-color:var(--green);color:white;padding:10px 22px;font-size:13px;border-radius:6px;cursor:default;display:inline-flex;align-items:center;gap:6px;font-family:var(--mono);';

    donut('bankDonut',['Matched','Exceptions','Timing diffs'],[128,8,6],['rgba(45,212,160,0.7)','rgba(245,101,101,0.7)','rgba(245,200,66,0.7)']);
    bar('bankBar',['Missing entry','Duplicate','Wrong amount','Bank error'],[14200,8300,7600,4150],['rgba(245,101,101,0.6)','rgba(167,139,250,0.6)','rgba(245,200,66,0.6)','rgba(91,141,238,0.6)']);

    const matched=[
      ['01 Jun','BACS — Payroll June','Payroll June 2024','£287,450','Exact',99],
      ['03 Jun','CHAPS — Rent Q2','Office rent Q2 2024','£45,000','Exact',100],
      ['05 Jun','DD — AWS Services','Cloud infrastructure','£8,420','Exact',98],
      ['07 Jun','BACS — Supplier A','Supplier A INV-2241','£12,300','Fuzzy',91],
      ['10 Jun','BACS — Supplier B','Supplier B payment','£6,750','Fuzzy',87],
      ['12 Jun','CHAPS — HMRC VAT','VAT payment June','£62,100','Exact',100],
      ['15 Jun','DD — Utilities','Electricity & gas','£2,840','Exact',96],
      ['18 Jun','BACS — Supplier C','Supplier C INV-0882','£9,120','Fuzzy',89],
    ];
    document.getElementById('bank-matched-tbody').innerHTML=matched.map(r=>`<tr><td class="muted">${r[0]}</td><td class="bold">${r[1]}</td><td>${r[2]}</td><td class="r">£${r[3].replace('£','')}</td><td><span class="pill ${r[4]==='Exact'?'pill-match':'pill-partial'}">${r[4]}</span></td><td>${confBar(r[5])}</td></tr>`).join('');

    const exc=[
      ['22 Jun','Unknown BACS credit','Bank','£14,200','Missing entry','Investigate source — no matching GL entry found'],
      ['14 Jun','Duplicate CHAPS payment','GL','£8,300','Duplicate','Possible double-posting — verify with AP team'],
      ['19 Jun','INV-4421 — amount mismatch','Bank','£5,600','Wrong amount','Bank shows £5,600, GL shows £4,900 — request invoice copy'],
      ['25 Jun','BACS — unidentified ref','Bank','£3,100','Missing entry','Reference code not recognised — contact bank'],
      ['28 Jun','Reversal not posted','GL','£1,800','Missing entry','Reversal entry missing in GL — post journal ref JNL-882'],
      ['29 Jun','FX adjustment','Bank','£780','Wrong amount','FX rate difference — check USD conversion rate used'],
      ['30 Jun','Bank charges','Bank','£320','Missing entry','Monthly bank charges not accrued — post to finance costs'],
      ['30 Jun','Interest income','Bank','£150','Missing entry','Interest credit — post to interest income account 8200'],
    ];
    document.getElementById('bank-exc-tbody').innerHTML=exc.map(r=>`<tr><td class="muted">${r[0]}</td><td class="bold">${r[1]}</td><td>${r[2]}</td><td class="r" style="color:var(--red)">−${r[3]}</td><td><span class="pill pill-unmatch">${r[4]}</span></td><td style="color:var(--text2);font-size:11px;max-width:220px">${r[5]}</td></tr>`).join('');

    const timing=[
      ['28 Jun','02 Jul','BACS — Supplier D','£8,400','Payment sent end of month — expected to clear 2 Jul'],
      ['29 Jun','01 Jul','DD — Insurance','£1,920','DD presented 29 Jun, GL posting date 1 Jul'],
      ['30 Jun','01 Jul','CHAPS — Supplier E','£1,200','Late CHAPS — bank received 30 Jun, GL next working day'],
      ['27 Jun','03 Jul','Cheque 004421','£980','Cheque issued 27 Jun, not yet cleared'],
      ['30 Jun','02 Jul','BACS — Expenses','£180','Expense BACS run — bank settlement T+2'],
      ['30 Jun','01 Jul','Bank interest accrual','£120','Month-end accrual — posting date 1 Jul'],
    ];
    document.getElementById('bank-timing-tbody').innerHTML=timing.map(r=>`<tr><td class="muted">${r[0]}</td><td class="muted">${r[1]}</td><td class="bold">${r[2]}</td><td class="r" style="color:var(--amber)">${r[3]}</td><td style="font-size:11px;color:var(--text2)">${r[4]}</td></tr>`).join('');

  }, 1800);
}

let bankDone=false;
function generateBankSummary() {
  if(bankDone)return; bankDone=true;
  switchTabDirect('bank','ai');
  const c=document.getElementById('bank-ai-content');
  c.innerHTML=`<div class="generating"><div class="gen-dots"><div class="gen-dot" style="animation:gd 1.2s infinite"></div><div class="gen-dot" style="animation:gd 1.2s 0.15s infinite"></div><div class="gen-dot" style="animation:gd 1.2s 0.3s infinite"></div></div><div class="gen-text">Analysing 8 exceptions · Generating sign-off narrative · Drafting investigation actions…</div></div>`;
  const txt=`The HSBC Operating Account bank reconciliation for June 2024 has been completed with a match rate of 94.2%, representing 128 of 142 transactions successfully reconciled. The reconciliation is materially complete; the remaining unreconciled balance of £34,250 comprises eight exception items requiring investigation and six timing differences of £12,800 which are expected to clear in early July.

The most significant exception is an unidentified BACS credit of £14,200 received on 22 June with no corresponding general ledger entry. This item should be investigated immediately with the treasury team to establish the source and post the appropriate entry. A potential duplicate CHAPS payment of £8,300 posted on 14 June requires urgent review by the AP team — if confirmed, recovery action should be initiated. The remaining exceptions relate to three amount discrepancies totalling £6,380 and two missing GL postings of £470 which can be resolved through standard journal entries.

All six timing differences are routine month-end items and are confirmed to have cleared by 3 July. This reconciliation is approved for sign-off subject to resolution of the two priority items (unidentified BACS credit and potential duplicate payment) before the management accounts are finalised.`;

  setTimeout(()=>{
    c.innerHTML=`<div class="ai-body"><p id="bank-ai-text"></p></div>`;
    document.getElementById('bank-copy-btn').style.display='block';
    typeAI('bank-ai-text',txt);
  },1600);
}

// ─── IC RECON ─────────────────────────────────────────────────────────────────
function runICRecon() {
  const btn=document.getElementById('ic-run-btn');
  btn.innerHTML='<div style="display:flex;align-items:center;gap:6px"><div class="gen-dots"><div class="gen-dot" style="animation:gd 1.2s infinite"></div><div class="gen-dot" style="animation:gd 1.2s 0.15s infinite"></div><div class="gen-dot" style="animation:gd 1.2s 0.3s infinite"></div></div>Running…</div>';

  setTimeout(()=>{
    document.getElementById('ic-agree').textContent='44';
    document.getElementById('ic-agree-sub').textContent='84.6% in agreement';
    document.getElementById('ic-dis').textContent='5';
    document.getElementById('ic-dis-sub').textContent='£38,400 to eliminate';
    document.getElementById('ic-diff').textContent='£nil';
    document.getElementById('ic-diff').style.color='var(--green)';
    document.getElementById('ic-diff-sub').textContent='Net position confirmed zero';
    document.getElementById('ic-results').style.display='block';
    btn.innerHTML='<svg width="11" height="11" viewBox="0 0 11 11" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="1,5 4,8 9,2"/></svg> Complete — 44 agreed';
    btn.style.cssText='background:var(--green);border-color:var(--green);color:white;padding:10px 22px;font-size:13px;border-radius:6px;cursor:default;display:inline-flex;align-items:center;gap:6px;font-family:var(--mono);';

    donut('icDonut',['In agreement','Disagreements','FX differences'],[44,5,3],['rgba(45,212,160,0.7)','rgba(245,101,101,0.7)','rgba(245,200,66,0.7)']);
    bar('icBar',['Cut-off diff','Rate diff','Posting error','Missing entry'],[18400,11200,5800,3000],['rgba(245,200,66,0.6)','rgba(91,141,238,0.6)','rgba(245,101,101,0.6)','rgba(167,139,250,0.6)']);

    const agreed=[
      ['IC-001','Management fee Q2','£180,000','£180,000','£0'],
      ['IC-002','IT services recharge','£45,200','£45,200','£0'],
      ['IC-003','Shared services cost','£32,100','£32,100','£0'],
      ['IC-004','Royalty payment Jun','£28,500','£28,500','£0'],
      ['IC-005','HR services recharge','£14,800','£14,800','£0'],
      ['IC-006','Legal recharge Q2','£9,400','£9,400','£0'],
    ];
    document.getElementById('ic-agreed-tbody').innerHTML=agreed.map(r=>`<tr><td class="muted">${r[0]}</td><td class="bold">${r[1]}</td><td class="r" style="color:var(--text2)">${r[2]}</td><td class="r" style="color:var(--text2)">${r[3]}</td><td class="r" style="color:var(--green)">£0</td><td>${pill('agree')}</td></tr>`).join('');

    const dis=[
      ['IC-047','Recharge INV-2241','£24,000','£18,400','£5,600','Cut-off — posted June vs July in OpCo'],
      ['IC-052','Consulting recharge','£12,800','£16,200','£3,400','Amount dispute — rate applied differs between entities'],
      ['IC-058','Software licence fee','£8,100','£6,700','£1,400','Missing invoice — OpCo not received copy'],
      ['IC-061','Travel recharge','£4,200','£2,800','£1,400','Partial posting — OpCo posted 67% of invoice'],
      ['IC-063','Shared costs Apr','£3,200','£1,800','£1,400','Timing — different period recognised between entities'],
    ];
    document.getElementById('ic-dis-tbody').innerHTML=dis.map(r=>`<tr><td class="muted">${r[0]}</td><td class="bold">${r[1]}</td><td class="r" style="color:var(--text2)">${r[2]}</td><td class="r" style="color:var(--text2)">${r[3]}</td><td class="r" style="color:var(--red)">£${r[4]}</td><td style="font-size:11px;color:var(--amber)">${r[5]}</td></tr>`).join('');

    const fx=[
      ['IC-034','EUR recharge Jun','€42,000','1.1682','1.1741','£212'],
      ['IC-041','EUR consulting','€18,500','1.1682','1.1741','£93'],
      ['IC-048','EUR software','€8,200','1.1682','1.1741','£41'],
    ];
    document.getElementById('ic-fx-tbody').innerHTML=fx.map(r=>`<tr><td class="muted">${r[0]}</td><td class="bold">${r[1]}</td><td class="r" style="color:var(--text2)">${r[2]}</td><td class="r" style="color:var(--text2)">${r[3]}</td><td class="r" style="color:var(--text2)">${r[4]}</td><td class="r" style="color:var(--amber)">£${r[5]}</td></tr>`).join('');
  },1800);
}

let icDone=false;
function generateICSummary() {
  if(icDone)return; icDone=true;
  switchTabDirect('ic','ai');
  const c=document.getElementById('ic-ai-content');
  c.innerHTML=`<div class="generating"><div class="gen-dots"><div class="gen-dot" style="animation:gd 1.2s infinite"></div><div class="gen-dot" style="animation:gd 1.2s 0.15s infinite"></div><div class="gen-dot" style="animation:gd 1.2s 0.3s infinite"></div></div><div class="gen-text">Analysing entity positions · Calculating elimination entries · Drafting group commentary…</div></div>`;
  const txt=`The intercompany reconciliation between UK HoldCo and EU OpCo for June 2024 has been substantially completed, with 44 of 52 transactions (84.6%) in full agreement. The net intercompany position confirms to zero at group level, satisfying the IFRS 10 consolidation requirement. Five disagreements totalling £13,200 require resolution before consolidation, supplemented by three FX translation differences of £346 attributable to the use of different spot rates.

The most material disagreement is IC-047, a management recharge of £24,000 recognised in June by UK HoldCo which has been posted to July by EU OpCo — a timing difference requiring a cut-off journal in the OpCo books. IC-052 relates to a consulting recharge where the entities have applied different hourly rates; the group finance team should confirm the agreed rate and instruct the lower-value entity to raise a correcting entry. IC-058 arises from a missing invoice at OpCo which should be reissued by HoldCo immediately.

The three FX differences total £346 and are immaterial for consolidation purposes; these arise from intra-period spot rate movements and will reverse on retranslation. Elimination entries for the £2,840,000 agreed intercompany balances should be processed as standard at consolidation. This reconciliation is recommended for sign-off subject to resolution of IC-047 and IC-052 before the group pack is submitted.`;

  setTimeout(()=>{
    c.innerHTML=`<div class="ai-body"><p id="ic-ai-text"></p></div>`;
    document.getElementById('ic-copy-btn').style.display='block';
    typeAI('ic-ai-text',txt);
  },1600);
}

// ─── AP RECON ─────────────────────────────────────────────────────────────────
function runAPRecon() {
  const btn=document.getElementById('ap-run-btn');
  btn.innerHTML='<div style="display:flex;align-items:center;gap:6px"><div class="gen-dots"><div class="gen-dot" style="animation:gd 1.2s infinite"></div><div class="gen-dot" style="animation:gd 1.2s 0.15s infinite"></div><div class="gen-dot" style="animation:gd 1.2s 0.3s infinite"></div></div>Running…</div>';

  setTimeout(()=>{
    document.getElementById('ap-matched').textContent='72';
    document.getElementById('ap-matched-sub').textContent='82.8% of 87 invoices';
    document.getElementById('ap-missing').textContent='11';
    document.getElementById('ap-missing-sub').textContent='Not posted in ledger';
    document.getElementById('ap-dups').textContent='4';
    document.getElementById('ap-dups-sub').textContent='Verify before payment run';
    document.getElementById('ap-risk').textContent='£28,640';
    document.getElementById('ap-risk-sub').textContent='Unreconciled value';
    document.getElementById('ap-results').style.display='block';
    btn.innerHTML='<svg width="11" height="11" viewBox="0 0 11 11" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="1,5 4,8 9,2"/></svg> Complete — 72 matched';
    btn.style.cssText='background:var(--green);border-color:var(--green);color:white;padding:10px 22px;font-size:13px;border-radius:6px;cursor:default;display:inline-flex;align-items:center;gap:6px;font-family:var(--mono);';

    donut('apDonut',['Matched','Missing in ledger','Duplicate risk'],[72,11,4],['rgba(45,212,160,0.7)','rgba(245,101,101,0.7)','rgba(167,139,250,0.7)']);
    bar('apBar',['Acme Corp','TechSupply Ltd','Global Parts','Fast Logistics','DataSoft Inc'],[8400,6200,5800,4900,3340],['rgba(245,101,101,0.5)','rgba(245,101,101,0.5)','rgba(245,200,66,0.5)','rgba(245,200,66,0.5)','rgba(91,141,238,0.5)']);

    const matched=[
      ['INV-8821','Acme Corp','04 Jun 2024','£12,400','GL-40021'],
      ['INV-8842','TechSupply Ltd','06 Jun 2024','£8,900','GL-40198'],
      ['INV-0041','Global Parts','08 Jun 2024','£7,200','GL-40231'],
      ['INV-2241','Fast Logistics','10 Jun 2024','£6,400','GL-40088'],
      ['INV-5519','DataSoft Inc','12 Jun 2024','£4,100','GL-40302'],
      ['INV-7712','Acme Corp','15 Jun 2024','£3,800','GL-40421'],
    ];
    document.getElementById('ap-matched-tbody').innerHTML=matched.map(r=>`<tr><td class="bold">${r[0]}</td><td>${r[1]}</td><td class="muted">${r[2]}</td><td class="r" style="color:var(--text2)">£${r[3].replace('£','')}</td><td class="muted">${r[4]}</td><td>${pill('match')}</td></tr>`).join('');

    const missing=[
      ['INV-9012','Acme Corp','18 Jun 2024','£8,400','8','Post immediately — payment due 18 Jul'],
      ['INV-3341','TechSupply Ltd','20 Jun 2024','£6,200','6','Request invoice copy — verify receipt of goods'],
      ['INV-0089','Global Parts','22 Jun 2024','£4,800','4','Accrual required — goods received, invoice in transit'],
      ['INV-7821','Fast Logistics','25 Jun 2024','£4,100','1','Chase posting — approved invoice sat in AP queue'],
      ['INV-1142','DataSoft Inc','26 Jun 2024','£2,900','0','New supplier — check PO raised and approved'],
      ['INV-4490','Acme Corp','28 Jun 2024','£1,200','0','Month-end cut-off — post to June, not July'],
    ];
    document.getElementById('ap-missing-tbody').innerHTML=missing.map(r=>`<tr><td class="bold">${r[0]}</td><td>${r[1]}</td><td class="muted">${r[2]}</td><td class="r" style="color:var(--red)">${r[3]}</td><td class="r" style="color:${parseInt(r[4])>5?'var(--red)':parseInt(r[4])>0?'var(--amber)':'var(--text2)'}">${r[4]} days</td><td style="font-size:11px;color:var(--text2)">${r[5]}</td></tr>`).join('');

    const dups=[
      ['INV-8821','Acme Corp','£12,400','GL-40021 (04 Jun)','GL-40488 (15 Jun)','<span class="pill pill-unmatch">High</span>'],
      ['INV-2103','TechSupply Ltd','£5,800','GL-40102 (01 Jun)','GL-40389 (22 Jun)','<span class="pill pill-timing">Medium</span>'],
      ['INV-4421','Global Parts','£3,200','GL-40231 (08 Jun)','GL-40502 (28 Jun)','<span class="pill pill-timing">Medium</span>'],
      ['INV-0041','Fast Logistics','£1,440','GL-40088 (10 Jun)','GL-40611 (30 Jun)','<span class="pill pill-partial">Low</span>'],
    ];
    document.getElementById('ap-dups-tbody').innerHTML=dups.map(r=>`<tr><td class="bold">${r[0]}</td><td>${r[1]}</td><td class="r" style="color:var(--red)">${r[2]}</td><td class="muted">${r[3]}</td><td class="muted">${r[4]}</td><td>${r[5]}</td></tr>`).join('');

  },1800);
}

let apDone=false;
function generateAPSummary() {
  if(apDone)return; apDone=true;
  switchTabDirect('ap','ai');
  const c=document.getElementById('ap-ai-content');
  c.innerHTML=`<div class="generating"><div class="gen-dots"><div class="gen-dot" style="animation:gd 1.2s infinite"></div><div class="gen-dot" style="animation:gd 1.2s 0.15s infinite"></div><div class="gen-dot" style="animation:gd 1.2s 0.3s infinite"></div></div><div class="gen-text">Reviewing 11 missing invoices · Scanning for duplicate risk · Writing exception report…</div></div>`;
  const txt=`The accounts payable supplier statement reconciliation for June 2024 identified 72 of 87 invoices (82.8%) matched successfully to the AP ledger, with a total unreconciled value of £28,640 across 15 items. Four items have been flagged as potential duplicate payments with a combined value of £22,840 — these require immediate attention before the July payment run is processed.

The highest-priority action is the review of INV-8821 from Acme Corp, where a duplicate GL posting of £12,400 has been identified across two separate postings on 4 June and 15 June. This should be suspended from the next payment run pending confirmation from the AP team. INV-2103 from TechSupply Ltd presents a medium-risk duplication of £5,800 requiring vendor confirmation of the original invoice number. The AP team should contact all four suppliers with duplicate flags before 5 July to obtain written confirmation.

Eleven invoices are missing from the ledger totalling £27,600, of which £8,400 relates to an Acme Corp invoice with a payment due date of 18 July — this should be posted immediately to avoid a late payment. Three further invoices require accrual entries at 30 June to ensure correct period recognition. A blanket approval to post all confirmed missing invoices is recommended, with the duplicate items placed on hold pending supplier verification. This reconciliation should not be closed until duplicate risk items are resolved.`;

  setTimeout(()=>{
    c.innerHTML=`<div class="ai-body"><p id="ap-ai-text"></p></div>`;
    document.getElementById('ap-copy-btn').style.display='block';
    typeAI('ap-ai-text',txt);
  },1600);
}

// ─── TYPEWRITER ───────────────────────────────────────────────────────────────
function typeAI(id,text) {
  const paras=text.split('\n\n');
  let pi=0,ci=0;
  function tick(){
    if(pi>=paras.length)return;
    const p=paras[pi];
    if(ci<=p.length){
      let h='';
      for(let i=0;i<pi;i++)h+=`<p>${hl(paras[i])}</p>`;
      h+=`<p>${hl(p.substring(0,ci))}<span style="border-right:2px solid var(--accent);margin-left:1px">&nbsp;</span></p>`;
      const el=document.getElementById(id);
      if(el)el.parentElement.innerHTML=`<div class="ai-body">${h}</div>`;
      ci++;setTimeout(tick,10);
    }else{pi++;ci=0;setTimeout(tick,250);}
  }
  tick();
}

function hl(t){return t.replace(/£[\d,]+/g,'<strong>$&</strong>').replace(/[+\-−][\d.]+%/g,'<strong>$&</strong>').replace(/INV-\d+/g,'<strong>$&</strong>');}

function switchTabDirect(view,tab){
  const wrap=document.getElementById('view-'+view);
  wrap.querySelectorAll('.tab').forEach((t,i)=>{
    const tabs=['matched','exceptions','timing','ai','agreed','disagree','fx','missing','dups'];
    t.classList.remove('active');
    if(t.onclick&&t.onclick.toString().includes("'"+tab+"'"))t.classList.add('active');
  });
  wrap.querySelectorAll('.tab-content').forEach(t=>t.classList.remove('active'));
  const el=document.getElementById(view+'-tab-'+tab);
  if(el)el.classList.add('active');
  wrap.querySelectorAll('.tab').forEach(t=>{
    if(t.getAttribute('onclick')&&t.getAttribute('onclick').includes("'"+tab+"'"))t.classList.add('active');
  });
}
</script>
</body>
</html>
