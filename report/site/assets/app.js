// app.js for V2 Dashboard (ECharts)

// Pre-defined Label Map (Fallback if data doesn't have it, but consistent with Python)
const LABEL_MAP = {
    "IRRITATION": "자극/따가움",
    "OILINESS": "유분/피지",
    "DRYNESS": "건조/속당김",
    "PILLING": "밀림/때처럼 밀림",
    "TONEUP": "톤업(자연스러움)",
    "WHITECAST": "백탁/회끼/동동 뜸",
    "EYE_STING": "눈시림",
    "FLAKING": "각질 부각/들뜸",
    "LONGEVITY": "지속력(시간 지나면 무너짐)",
    "TEXTURE_HEAVY": "무거운 사용감/답답함",
    "ABSORPTION": "흡수/겉돎",
    "TROUBLE": "트러블/뒤집어짐",
    "SCENT": "향",
    "MOISTURE": "보습",
    "STICKINESS": "끈적임",
    "SPREADABILITY": "발림성",
    "STAINING": "묻어남",
    "ALL": "전체",
    "OTHER": "기타",
    "TEXTURE": "제형",
    "COOLING": "쿨링감",
    "WATERPROOF": "워터프루프",
    "CLEANSING": "세정력"
};

function getLabel(key) {
    if (LABEL_MAP[key]) return `${LABEL_MAP[key]} (${key})`;
    return key;
}

document.addEventListener("DOMContentLoaded", () => {
    if (!window.DASHBOARD_DATA) {
        console.error("DASHBOARD_DATA missing!");
        document.body.innerHTML += "<h1 style='color:red'>Data Missing. Run build script.</h1>";
        return;
    }
    const data = window.DASHBOARD_DATA;

    // Set Header Info
    document.getElementById("report-date").innerText = data.meta.generated_at;

    // Render Sections
    renderQualityCards(data.quality_gate);
    renderTop5Cards(data.action_plan.cards);
    renderPolarityChart(data.polarity_overview);
    renderOpportunityMap(data.opportunity_map);
    renderMarketPain(data.market_pain);
    renderGoldenNugget(data.golden_nugget);
    renderContextChart(data.context_analysis); // Initial
    renderSeasonChart(data.seasonality);
    renderActionTables(data.action_plan);
    renderEvidence(data.evidence);
    renderGlossary(data.glossary);

    // Inject Text Content
    injectText("text-polarity", data.polarity_overview.text);
    injectText("text-opportunity", data.opportunity_map.text);
    injectText("text-pain", data.market_pain.text);
    injectText("text-golden", data.golden_nugget.text);
    injectText("text-context", data.context_analysis.text);
    injectText("text-season", data.seasonality.text);
    injectText("text-action", data.action_plan.text);
    injectText("text-evidence", data.evidence.text);

    // Filter dropdown init
    initEvidenceFilter(data.evidence.samples);
});

// Helper: Text Injection with localized labels
function injectText(id, textData) {
    const el = document.getElementById(id);
    if (!el) return;
    el.innerHTML = `
        <h4>💡 요약</h4>
        <p><strong>핵심 관찰:</strong> ${textData.observation || textData.takeaway}</p>
        <p><strong>해석:</strong> ${textData.interpretation}</p>
        <div class="caveat">※ 확인 필요: ${textData.caveat}</div>
    `;
}

// 0. Quality Cards
function renderQualityCards(qData) {
    const container = document.getElementById("quality-gate-cards");
    container.innerHTML = qData.metrics.map(d => `
        <div class="stat-card">
            <span class="val">${d.value}</span>
            <span class="label">${d.label}</span>
        </div>
    `).join("");
}

// 0. Top 5 Cards
function renderTop5Cards(cards) {
    const container = document.getElementById("top5-cards");
    container.innerHTML = cards.map((c, i) => `
        <div class="needs-card">
            <h3>${i + 1}. ${c.name} <small>(${c.id})</small></h3>
            <div class="desc">${c.desc}</div>
            <div style="font-size:0.8em; margin-bottom:5px;">
                <strong>Repeat:</strong> ${c.stats.repeat} | <strong>Unmet:</strong> ${c.stats.unmet}
            </div>
            <ul>${c.reqs.map(r => `<li>${r}</li>`).join("")}</ul>
        </div>
    `).join("");
}

// 1. Polarity Chart
function renderPolarityChart(data) {
    const chart = echarts.init(document.getElementById("chart-polarity"));
    const raw = data.chart_data;
    const buckets = raw.map(d => d.bucket);

    const option = {
        tooltip: {
            trigger: 'axis', axisPointer: { type: 'shadow' }, formatter: (params) => {
                let res = params[0].name + '<br/>';
                params.forEach(p => {
                    res += `${p.seriesName}: ${(p.value * 100).toFixed(1)}%<br/>`;
                });
                return res;
            }
        },
        legend: { bottom: 0 },
        grid: { left: '3%', right: '4%', bottom: '10%', containLabel: true },
        xAxis: { type: 'value', max: 1, axisLabel: { formatter: v => (v * 100) + '%' } },
        yAxis: { type: 'category', data: buckets },
        series: [
            { name: 'Met', type: 'bar', stack: 'total', data: raw.map(d => d.met_rate), color: '#27ae60' },
            { name: 'Mixed', type: 'bar', stack: 'total', data: raw.map(d => d.mixed_rate), color: '#f39c12' },
            { name: 'Unmet', type: 'bar', stack: 'total', data: raw.map(d => d.unmet_rate), color: '#c0392b' },
            { name: 'Unknown', type: 'bar', stack: 'total', data: raw.map(d => d.unknown_rate), color: '#bdc3c7' }
        ]
    };
    chart.setOption(option);
}

// 2. Opportunity Map
function renderOpportunityMap(data) {
    const chart = echarts.init(document.getElementById("chart-opportunity"));
    const filtered = data.chart_data.filter(d => d.goods_cnt_any >= 10);

    const seriesData = filtered.map(d => {
        return {
            value: [d.goods_repeat_rate, d.reviews_unmet_like_cnt, d.goods_cnt_any],
            name: getLabel(d.aspect), // Use mapped name
            aspect: d.aspect
        };
    });

    const option = {
        tooltip: {
            formatter: (params) => {
                return `<b>${params.data.name}</b><br/>
                        Repeat Rate: ${(params.value[0] * 100).toFixed(1)}%<br/>
                        Unmet Vol: ${params.value[1]}<br/>
                        Goods Cnt: ${params.value[2]}`;
            }
        },
        xAxis: { name: 'Repeatability (반복성)', type: 'value', axisLabel: { formatter: v => (v * 100) + '%' } },
        yAxis: { name: 'Unmet Volume (규모)', type: 'value' },
        series: [{
            type: 'scatter',
            symbolSize: (data) => Math.sqrt(data[2]) * 5,
            data: seriesData,
            label: {
                show: true,
                formatter: params => LABEL_MAP[params.data.aspect] ? LABEL_MAP[params.data.aspect] : params.data.aspect,
                position: 'top',
                fontSize: 10
            },
            itemStyle: {
                color: (params) => {
                    const top5 = ['IRRITATION', 'OILINESS', 'PILLING', 'DRYNESS', 'TONEUP'];
                    return top5.includes(params.data.aspect) ? '#c0392b' : '#3498db';
                },
                opacity: 0.7
            }
        }]
    };
    chart.setOption(option);
}

// 3. Market Pain
function renderMarketPain(data) {
    const chart = echarts.init(document.getElementById("chart-pain"));
    const raw = data.chart_data;
    const labels = raw.map(d => getLabel(d.aspect));

    const option = {
        title: { text: 'Top 10 Unmet Rate', left: 'center' },
        tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
        grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
        xAxis: { type: 'category', data: labels, axisLabel: { interval: 0, rotate: 30, formatter: v => v.split('(')[0] } },
        yAxis: { type: 'value', axisLabel: { formatter: v => v * 100 + '%' } },
        series: [{
            data: raw.map(d => d.unmet_like_rate),
            type: 'bar',
            color: '#c0392b',
            label: { show: true, position: 'top', formatter: p => (p.value * 100).toFixed(1) + '%' }
        }]
    };
    chart.setOption(option);

    // Table (Simplified label)
    const tbody = document.querySelector("#table-pain tbody");
    tbody.innerHTML = raw.map(d => `
        <tr><td>${getLabel(d.aspect)}</td><td>${d.unmet_like_cnt}</td><td>${d.n_items}</td><td>${d.unmet_like_rate_pct}</td></tr>
    `).join("");
}

// 4. Golden Nugget
function renderGoldenNugget(data) {
    const chart = echarts.init(document.getElementById("chart-golden"));
    const raw = data.chart_data;
    const labels = raw.map(d => getLabel(d.aspect));

    const option = {
        title: { text: 'Unmet vs Met Volume', left: 'center' },
        tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
        legend: { bottom: 0 },
        xAxis: { type: 'category', data: labels, axisLabel: { rotate: 30, formatter: v => v.split('(')[0] } },
        yAxis: { type: 'value' },
        series: [
            { name: 'Unmet+Mix', type: 'bar', stack: 'total', data: raw.map(d => d.unmet_acc), color: '#f39c12' },
            { name: 'Met', type: 'bar', stack: 'total', data: raw.map(d => d.met_cnt), color: '#27ae60' }
        ]
    };
    chart.setOption(option);

    const tbody = document.querySelector("#table-golden tbody");
    tbody.innerHTML = raw.map(d => `
        <tr><td>${getLabel(d.aspect)}</td><td>${d.unmet_acc}</td><td>${d.met_cnt}</td><td>${d.n_items}</td></tr>
    `).join("");
}

// 5. Context
function renderContextChart(dataInput) {
    const data = dataInput || window.DASHBOARD_DATA.context_analysis;
    const chart = echarts.init(document.getElementById("chart-context"));

    const minN = parseInt(document.getElementById("ctx-min-n").value) || 20;
    const filtered = data.chart_data.filter(d => d.n_reviews >= minN && d.context_tag !== 'NONE_RULE');
    const sorted = filtered.sort((a, b) => b.unmet_like_cnt - a.unmet_like_cnt).slice(0, 15);

    const option = {
        title: { text: `Top Context Pairs (n>=${minN})`, left: 'center' },
        tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
        grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
        xAxis: { type: 'value' },
        yAxis: { type: 'category', data: sorted.map(d => `${d.context_tag} - ${getLabel(d.aspect).split('(')[0]}`).reverse() },
        series: [{
            type: 'bar',
            data: sorted.map(d => d.unmet_like_cnt).reverse(),
            color: '#8e44ad',
            label: { show: true, position: 'right' }
        }]
    };
    chart.setOption(option);
}

// 6. Seasonality
function renderSeasonChart(data) {
    const chart = echarts.init(document.getElementById("chart-season"));
    const raw = data.chart_data;

    const topAspects = [...new Set(raw.filter(d => d.unmet_like_cnt > 10).sort((a, b) => b.unmet_like_cnt - a.unmet_like_cnt).map(d => d.aspect))].slice(0, 8);
    const topLabels = topAspects.map(a => getLabel(a).split('(')[0]);

    const summerData = topAspects.map(asp => {
        const found = raw.find(d => d.aspect === asp && d.season === 'summer');
        return found ? found.unmet_like_cnt : 0;
    });
    const winterData = topAspects.map(asp => {
        const found = raw.find(d => d.aspect === asp && d.season === 'winter');
        return found ? found.unmet_like_cnt : 0;
    });

    const option = {
        tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
        legend: { bottom: 0 },
        xAxis: { type: 'category', data: topLabels },
        yAxis: { type: 'value' },
        series: [
            { name: 'Summer', type: 'bar', data: summerData, color: '#e74c3c' },
            { name: 'Winter', type: 'bar', data: winterData, color: '#3498db' }
        ]
    };
    chart.setOption(option);
}

// 7. Action Tables
function renderActionTables(data) {
    const iceTbody = document.querySelector("#table-ice tbody");
    iceTbody.innerHTML = data.ice.map(d => `
        <tr>
            <td><strong>${getLabel(d.needs).split('(')[0]}</strong></td>
            <td>${d.name}</td>
            <td>${d.impact}</td>
            <td>${d.confidence}</td>
            <td>${d.ease}</td>
            <td><strong>${d.score}</strong></td>
            <td>${d.note}</td>
        </tr>
    `).join("");

    const specTbody = document.querySelector("#table-spec tbody");
    specTbody.innerHTML = data.spec.map(d => `
        <tr>
            <td>${d.req}</td>
            <td>${getLabel(d.aspect)}</td>
            <td>${d.context}</td>
            <td>${d.kpi}</td>
            <td>${d.test}</td>
        </tr>
    `).join("");
}

// 8. Evidence
function initEvidenceFilter(samples) {
    const sel = document.getElementById("evidence-filter");
    // Clear first
    sel.innerHTML = '<option value="ALL">전체 보기</option>';
    samples.forEach(s => {
        sel.innerHTML += `<option value="${s.id}">${getLabel(s.id)}</option>`;
    });
}
function filterEvidence() {
    const sel = document.getElementById("evidence-filter");
    const val = sel.value;
    const items = document.querySelectorAll(".evidence-card");
    items.forEach(item => {
        if (val === "ALL" || item.dataset.id === val) item.style.display = "block";
        else item.style.display = "none";
    });
}
function renderEvidence(data) {
    const container = document.getElementById("evidence-container");
    container.innerHTML = data.samples.map(s => `
        <div class="evidence-card" data-id="${s.id}">
            <h4>${getLabel(s.id)}</h4>
            <ul>${s.quotes.map(q => `<li>"${q}"</li>`).join("")}</ul>
        </div>
    `).join("");
}

// 9. Glossary
function renderGlossary(list) {
    const container = document.getElementById("glossary-grid");
    if (!container || !list) return;

    container.innerHTML = list.map(item => `
        <div class="glossary-card">
            <h5>${item.term}</h5>
            <div class="krname">${item.kr}</div>
            <div class="desc">${item.desc}</div>
        </div>
    `).join("");
}
