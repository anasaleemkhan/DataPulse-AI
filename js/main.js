/**
 * DataPulse-AI Portfolio Showcase Main Logic
 * Interactive Charts, Telemetry Filters, Terminal Simulation, and Bilingual Toggle
 */

let currentCity = "All";
let currentLang = "en";
let telemetryChart = null;
let distributionChart = null;

document.addEventListener("DOMContentLoaded", () => {
  initStatsCounters();
  initCityFilters();
  initCharts();
  renderDataTable();
  renderCorrelationHeatmap();
  renderOutliers();
  renderGeminiReport("en");
  initTerminal();
  initCopyButtons();
});

/* 1. Counter Animations */
function initStatsCounters() {
  const statElements = document.querySelectorAll(".stat-value[data-target]");
  statElements.forEach(el => {
    const target = parseFloat(el.getAttribute("data-target"));
    const decimals = parseInt(el.getAttribute("data-decimals") || "0");
    const prefix = el.getAttribute("data-prefix") || "";
    const suffix = el.getAttribute("data-suffix") || "";

    let current = 0;
    const step = target / 35;
    const timer = setInterval(() => {
      current += step;
      if (current >= target) {
        current = target;
        clearInterval(timer);
      }
      el.textContent = `${prefix}${current.toFixed(decimals)}${suffix}`;
    }, 25);
  });
}

/* 2. City Filtering & Telemetry Updates */
function initCityFilters() {
  const filterBtns = document.querySelectorAll(".city-btn");
  filterBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      filterBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      currentCity = btn.getAttribute("data-city");
      updateTelemetryDashboard();
    });
  });
}

function getFilteredRecords() {
  if (currentCity === "All") {
    return DATA_PULSE_DATA.rawRecords;
  }
  return DATA_PULSE_DATA.rawRecords.filter(r => r.city === currentCity);
}

function updateTelemetryDashboard() {
  const records = getFilteredRecords();
  if (!records.length) return;

  const avgPm25 = (records.reduce((a, b) => a + b.pm25, 0) / records.length).toFixed(1);
  const avgNo2 = (records.reduce((a, b) => a + b.no2, 0) / records.length).toFixed(1);
  const avgPm10 = (records.reduce((a, b) => a + b.pm10, 0) / records.length).toFixed(1);
  const avgTraffic = (records.reduce((a, b) => a + b.traffic, 0) / records.length).toFixed(1);
  const avgTemp = (records.reduce((a, b) => a + b.temp, 0) / records.length).toFixed(1);

  document.getElementById("val-pm25").textContent = avgPm25;
  document.getElementById("val-no2").textContent = avgNo2;
  document.getElementById("val-pm10").textContent = avgPm10;
  document.getElementById("val-traffic").textContent = avgTraffic;
  document.getElementById("val-temp").textContent = avgTemp;

  updateCharts(records);
  renderDataTable();
}

/* 3. Chart.js Visualizations */
function initCharts() {
  const records = getFilteredRecords();
  const ctxTelemetry = document.getElementById("chart-telemetry").getContext("2d");
  const ctxDistribution = document.getElementById("chart-distribution").getContext("2d");

  // Chart 1: Time Series / Observations
  const labels = records.map(r => `${r.city.substring(0,3)} ${r.timestamp.split(" ")[1]}`);

  telemetryChart = new Chart(ctxTelemetry, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          label: "PM2.5 (µg/m³)",
          data: records.map(r => r.pm25),
          borderColor: "#38BDF8",
          backgroundColor: "rgba(56, 189, 248, 0.15)",
          borderWidth: 2.5,
          tension: 0.3,
          fill: true
        },
        {
          label: "Traffic Index",
          data: records.map(r => r.traffic),
          borderColor: "#F59E0B",
          borderDash: [5, 5],
          borderWidth: 2,
          tension: 0.3,
          yAxisID: "yTraffic"
        },
        {
          label: "NO₂ (ppb)",
          data: records.map(r => r.no2),
          borderColor: "#A78BFA",
          borderWidth: 2,
          tension: 0.3
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: "index", intersect: false },
      plugins: {
        legend: { labels: { color: "#94A3B8", font: { family: "Inter", size: 11 } } },
        tooltip: {
          backgroundColor: "rgba(15, 23, 42, 0.95)",
          titleColor: "#F8FAFC",
          bodyColor: "#CBD5E1",
          borderColor: "rgba(255,255,255,0.1)",
          borderWidth: 1
        }
      },
      scales: {
        x: {
          ticks: { color: "#64748B", font: { size: 10 } },
          grid: { color: "rgba(255, 255, 255, 0.04)" }
        },
        y: {
          ticks: { color: "#64748B" },
          grid: { color: "rgba(255, 255, 255, 0.04)" },
          title: { display: true, text: "Concentration / Index", color: "#64748B" }
        },
        yTraffic: {
          position: "right",
          ticks: { color: "#F59E0B" },
          grid: { drawOnChartArea: false },
          title: { display: true, text: "Traffic Index (0-100)", color: "#F59E0B" }
        }
      }
    }
  });

  // Chart 2: City Comparison Averages
  const cityAverages = DATA_PULSE_DATA.cities.map(city => {
    const cityRecs = DATA_PULSE_DATA.rawRecords.filter(r => r.city === city);
    return {
      city,
      avgPm25: cityRecs.reduce((a, b) => a + b.pm25, 0) / cityRecs.length,
      avgTraffic: cityRecs.reduce((a, b) => a + b.traffic, 0) / cityRecs.length
    };
  });

  distributionChart = new Chart(ctxDistribution, {
    type: "bar",
    data: {
      labels: cityAverages.map(c => c.city),
      datasets: [
        {
          label: "Avg PM2.5 (µg/m³)",
          data: cityAverages.map(c => c.avgPm25.toFixed(1)),
          backgroundColor: ["#3B82F6", "#06B6D4", "#8B5CF6", "#10B981"],
          borderRadius: 6
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false }
      },
      scales: {
        x: { ticks: { color: "#94A3B8" }, grid: { display: false } },
        y: {
          ticks: { color: "#64748B" },
          grid: { color: "rgba(255, 255, 255, 0.04)" },
          title: { display: true, text: "PM2.5 (µg/m³)", color: "#64748B" }
        }
      }
    }
  });
}

function updateCharts(records) {
  if (!telemetryChart) return;
  telemetryChart.data.labels = records.map(r => `${r.city.substring(0,3)} ${r.timestamp.split(" ")[1]}`);
  telemetryChart.data.datasets[0].data = records.map(r => r.pm25);
  telemetryChart.data.datasets[1].data = records.map(r => r.traffic);
  telemetryChart.data.datasets[2].data = records.map(r => r.no2);
  telemetryChart.update();
}

/* 4. Data Table Rendering */
function renderDataTable() {
  const records = getFilteredRecords();
  const tbody = document.getElementById("table-body");
  if (!tbody) return;

  tbody.innerHTML = records.map(r => `
    <tr>
      <td style="font-family: var(--font-mono); color: #93C5FD;">${r.timestamp}</td>
      <td><strong>${r.city}</strong></td>
      <td>${r.temp}°C</td>
      <td>${r.humidity}%</td>
      <td style="color: ${r.pm25 > 50 ? '#F87171' : '#34D399'}; font-weight: 600;">${r.pm25}</td>
      <td>${r.pm10}</td>
      <td>${r.no2}</td>
      <td>${r.co2}</td>
      <td><span style="display:inline-block; padding: 2px 8px; border-radius: 4px; background: rgba(245, 158, 11, 0.15); color: #FBBF24;">${r.traffic}</span></td>
    </tr>
  `).join("");
}

/* 5. Pearson Correlation Heatmap */
function renderCorrelationHeatmap() {
  const container = document.getElementById("corr-heatmap");
  if (!container) return;

  const { features, matrix } = DATA_PULSE_DATA.correlationMatrix;
  const shortNames = ["Temp", "Humidity", "PM2.5", "PM10", "NO₂", "CO₂", "Traffic"];

  let html = `<table class="corr-table"><thead><tr><th>Feature</th>`;
  shortNames.forEach(f => { html += `<th>${f}</th>`; });
  html += `</tr></thead><tbody>`;

  matrix.forEach((row, i) => {
    html += `<tr><th>${shortNames[i]}</th>`;
    row.forEach((val, j) => {
      let bgColor = "";
      let textColor = "#FFF";

      if (val === 1.0) {
        bgColor = "rgba(59, 130, 246, 0.4)";
      } else if (val > 0.8) {
        bgColor = "rgba(16, 185, 129, 0.35)";
      } else if (val > 0.5) {
        bgColor = "rgba(16, 185, 129, 0.2)";
      } else if (val < -0.7) {
        bgColor = "rgba(239, 68, 68, 0.35)";
      } else {
        bgColor = "rgba(239, 68, 68, 0.2)";
      }

      html += `<td class="corr-cell" style="background:${bgColor}; color:${textColor};" title="${features[i]} ↔ ${features[j]}: r = ${val.toFixed(3)}">${val.toFixed(2)}</td>`;
    });
    html += `</tr>`;
  });

  html += `</tbody></table>`;
  container.innerHTML = html;
}

/* 6. Outlier Auditing List */
function renderOutliers() {
  const container = document.getElementById("outlier-list");
  if (!container) return;

  const entries = Object.entries(DATA_PULSE_DATA.iqrOutliers);
  container.innerHTML = entries.map(([feature, data]) => `
    <div class="outlier-item">
      <div>
        <div class="outlier-feature">${feature}</div>
        <div class="outlier-bounds">IQR Bounds: [${data.lower} to ${data.upper}]</div>
      </div>
      <div>
        <span class="outlier-badge badge-clean">0 Outliers (${data.pct})</span>
      </div>
    </div>
  `).join("");
}

/* 7. Gemini Report Rendering (Bilingual) */
function renderGeminiReport(lang) {
  const report = DATA_PULSE_DATA.geminiReport[lang];
  const bodyEl = document.getElementById("report-content");
  if (!bodyEl) return;

  document.getElementById("report-title").textContent = report.title;
  document.getElementById("report-subtitle").textContent = report.subtitle;

  bodyEl.innerHTML = report.sections.map(sec => `
    <div class="academic-section-card">
      <span class="academic-section-badge">Section ${sec.num}</span>
      <h4>${sec.heading}</h4>
      <p>${sec.content.replace(/\n/g, "<br>")}</p>
    </div>
  `).join("");
}

window.switchReportLang = function(lang) {
  currentLang = lang;
  document.querySelectorAll(".report-tab-btn").forEach(btn => {
    btn.classList.toggle("active", btn.getAttribute("data-lang") === lang);
  });
  renderGeminiReport(lang);
};

/* 8. Interactive Terminal Simulator */
let terminalInterval = null;

function initTerminal() {
  runCliPreset("en");
}

window.runCliPreset = function(preset) {
  document.querySelectorAll(".cli-btn-preset").forEach(btn => {
    btn.classList.toggle("active", btn.getAttribute("data-preset") === preset);
  });

  const lines = DATA_PULSE_DATA.cliSimulations[preset];
  const screen = document.getElementById("terminal-screen");
  if (!screen || !lines) return;

  if (terminalInterval) clearInterval(terminalInterval);
  screen.innerHTML = "";

  let lineIdx = 0;
  terminalInterval = setInterval(() => {
    if (lineIdx >= lines.length) {
      clearInterval(terminalInterval);
      return;
    }

    const lineText = lines[lineIdx];
    const div = document.createElement("div");
    div.className = "terminal-line";

    if (lineText.startsWith("$")) {
      div.className += " term-cmd";
    } else if (lineText.startsWith("[SUCCESS]") || lineText.startsWith("[DONE]") || lineText.startsWith("[READY]")) {
      div.className += " term-success";
    } else if (lineText.startsWith("#") || lineText.startsWith("Dataset:")) {
      div.className += " term-header";
    } else {
      div.className += " term-info";
    }

    div.textContent = lineText;
    screen.appendChild(div);
    screen.scrollTop = screen.scrollHeight;
    lineIdx++;
  }, 90);
};

/* 9. Copy to Clipboard Functionality */
function initCopyButtons() {
  document.querySelectorAll(".btn-copy").forEach(btn => {
    btn.addEventListener("click", () => {
      const targetId = btn.getAttribute("data-copy-target");
      const textToCopy = document.getElementById(targetId)?.innerText || "";

      navigator.clipboard.writeText(textToCopy).then(() => {
        const originalText = btn.innerHTML;
        btn.innerHTML = `<span style="color:#34D399;">✓ Copied!</span>`;
        setTimeout(() => {
          btn.innerHTML = originalText;
        }, 2000);
      }).catch(err => {
        console.error("Copy failed", err);
      });
    });
  });
}
