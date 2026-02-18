const apiBase = "/api/v1";

const form = document.getElementById("shorten-form");
const longUrlInput = document.getElementById("long-url");
const descriptionInput = document.getElementById("description");
const shortenBtn = document.getElementById("shorten-btn");

const resultBlock = document.getElementById("result");
const shortUrlLink = document.getElementById("short-url");
const copyBtn = document.getElementById("copy-btn");

const errorBlock = document.getElementById("error");
const errorMessage = document.getElementById("error-message");

const historyList = document.getElementById("history-list");
const historyEmpty = document.getElementById("history-empty");
const refreshHistoryBtn = document.getElementById("refresh-history");

const statsClicks = document.getElementById("stats-clicks");
const statsStatus = document.getElementById("stats-status");
const statsUrl = document.getElementById("stats-url");
const statsPanel = document.getElementById("stats-panel");

const statusPill = document.getElementById("status-pill");

const hiddenLinkIds = new Set();

function buildShortUrl(shortCode) {
  const origin = window.location.origin;
  return `${origin}/${shortCode}`;
}

function setLoading(isLoading) {
  if (isLoading) {
    shortenBtn.disabled = true;
    shortenBtn.textContent = "Сокращаем…";
    statusPill.textContent = "Отправляем запрос…";
  } else {
    shortenBtn.disabled = false;
    shortenBtn.textContent = "Сократить";
    statusPill.textContent = "Готов к работе";
  }
}

function showError(message) {
  errorMessage.textContent = message;
  errorBlock.style.display = "flex";
}

function clearError() {
  errorBlock.style.display = "none";
  errorMessage.textContent = "";
}

function showResult(link) {
  const url = buildShortUrl(link.short_code);
  shortUrlLink.href = url;
  shortUrlLink.textContent = url;

  resultBlock.hidden = false;
}

async function handleSubmit(event) {
  event.preventDefault();
  clearError();

  const longUrl = longUrlInput.value.trim();
  const description = descriptionInput.value.trim() || null;

  if (!longUrl) {
    showError("Введите корректный URL.");
    return;
  }

  setLoading(true);

  try {
    const response = await fetch(`${apiBase}/links`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ long_url: longUrl, description }),
    });

    if (!response.ok) {
      let message = "Не удалось создать ссылку.";
      try {
        const data = await response.json();
        if (data && data.detail) {
          message = Array.isArray(data.detail)
            ? data.detail.map((e) => e.msg || e).join(", ")
            : data.detail;
        }
      } catch {
        // ignore
      }
      showError(message);
      return;
    }

    const link = await response.json();
    showResult(link);
    await loadHistory();
    await loadStats(link.id);
  } catch (e) {
    showError("Ошибка сети. Проверьте соединение и попробуйте ещё раз.");
  } finally {
    setLoading(false);
  }
}

async function copyShortUrl() {
  if (!shortUrlLink.href) return;
  try {
    await navigator.clipboard.writeText(shortUrlLink.href);
    copyBtn.classList.add("copied");
    setTimeout(() => copyBtn.classList.remove("copied"), 900);
  } catch {
    showError("Не удалось скопировать ссылку. Скопируйте её вручную.");
  }
}

async function loadHistory() {
  try {
    const response = await fetch(`${apiBase}/links?limit=10&offset=0`);
    if (!response.ok) return;

    const links = await response.json();
    historyList.innerHTML = "";

    if (!links.length) {
      historyEmpty.hidden = false;
      return;
    }

    historyEmpty.hidden = true;

    links
      .filter((link) => !hiddenLinkIds.has(link.id))
      .forEach((link) => {
      const wrapper = document.createElement("div");
      wrapper.className = "history-item";
      wrapper.dataset.id = link.id;

      const shortUrl = buildShortUrl(link.short_code);
      const description = link.description || "Без описания";
      let isActive = link.is_active;

      wrapper.innerHTML = `
        <button type="button" class="history-item__content">
          <div class="history-item__short">${shortUrl}</div>
          <div class="history-item__long">${link.long_url}</div>
          <div class="history-item__description">${description}</div>
          <div class="history-item__meta">
            <span class="pill ${isActive ? "pill-green" : "pill-red"}">
              ${isActive ? "Активна" : "Выключена"}
            </span>
            <button type="button" class="history-item__toggle">
              Откл.
            </button>
          </div>
        </button>
        <button type="button" class="history-item__dismiss" aria-label="Скрыть ссылку">×</button>
      `;

      const contentBtn = wrapper.querySelector(".history-item__content");
      const dismissBtn = wrapper.querySelector(".history-item__dismiss");
      const pill = wrapper.querySelector(".pill");
      const toggleBtn = wrapper.querySelector(".history-item__toggle");

      contentBtn.addEventListener("click", () => {
        showResult(link);
        loadStats(link.id);
      });

      // крестик: если ссылка ещё активна — сначала отключаем в бэке, потом убираем из списка;
      // если уже отключена — просто убираем из списка
      if (!isActive) {
        dismissBtn.style.display = "flex";
      }

      dismissBtn.addEventListener("click", async (event) => {
        event.stopPropagation();
        if (isActive) {
          try {
            const res = await fetch(`${apiBase}/links/${link.id}`, {
              method: "DELETE",
            });
            if (!res.ok && res.status !== 404) {
              showError("Не удалось отключить ссылку.");
              return;
            }
            isActive = false;
          } catch {
            showError("Ошибка сети при отключении ссылки.");
            return;
          }
        }
        hiddenLinkIds.add(link.id);
        wrapper.remove();
      });

      // кнопка Откл. — только отключает ссылку, не удаляя из списка
      toggleBtn.addEventListener("click", async (event) => {
        event.stopPropagation();

        if (!isActive) return;

        try {
          const res = await fetch(`${apiBase}/links/${link.id}`, {
            method: "DELETE",
          });
          if (!res.ok) {
            showError("Не удалось отключить ссылку.");
            return;
          }
          isActive = false;
          pill.textContent = "Выключена";
          pill.classList.remove("pill-green");
          pill.classList.add("pill-red");
          dismissBtn.style.display = "flex";
          toggleBtn.disabled = true;
        } catch {
          showError("Ошибка сети при отключении ссылки.");
        }
      });

      historyList.appendChild(wrapper);
    });
  } catch {
    // тихо игнорируем, это второстепенный функционал
  }
}

async function loadStats(id) {
  if (!id) return;
  try {
    const response = await fetch(`${apiBase}/links/${id}/stats`);
    if (!response.ok) return;

    const stats = await response.json();
    statsClicks.textContent = stats.click_count;
    statsStatus.textContent = stats.is_active ? "Активна" : "Выключена";
    statsUrl.textContent = stats.long_url;

    statsPanel.style.opacity = "1";
  } catch {
    // необязательная часть, не ломаем основной сценарий
  }
}

form.addEventListener("submit", handleSubmit);
copyBtn.addEventListener("click", copyShortUrl);
refreshHistoryBtn.addEventListener("click", loadHistory);

document.addEventListener("DOMContentLoaded", () => {
  clearError();
  loadHistory();
});

longUrlInput.addEventListener("input", clearError);
descriptionInput.addEventListener("input", clearError);

