let allCryptos = [];
let filteredCryptos = [];
let favorites = JSON.parse(localStorage.getItem('cryptoFavorites')) || [];

const cryptoGrid = document.getElementById('crypto-grid');
const loadingGrid = document.getElementById('loading-grid');
const loadingSpinner = document.getElementById('loading-spinner');
const loadingText = document.getElementById('loading-text');
const errorDiv = document.getElementById('error');
const refreshBtn = document.getElementById('refresh-button');
const searchInput = document.getElementById('search-input');
const lastUpdated = document.getElementById('lastUpdated');

const topCryptos = [
    "bitcoin", "ethereum", "binancecoin", "cardano", "dogecoin", "stellar"
];

// Helper functions for Favorites
function saveFavorites() {
    localStorage.setItem('cryptoFavorites', JSON.stringify(favorites));
}

function toggleFavorite(id) {
    if (favorites.includes(id)) {
        favorites = favorites.filter(favId => favId !== id);
    } else {
        favorites.push(id);
    }
    saveFavorites();
    displayCryptos(filteredCryptos);
}

async function fetchCryptoData() {
    try {
        hideError();

        const response = await fetch(`https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=20&page=1&sparkline=false&price_change_percentage=1h,24h,7d&x_cg_demo_api_key=CG-NEdjZsS9uW2vBQVrFxb6uuBh`);

        if (!response.ok) {
            throw new Error(`HTTP Error status: ${response.status}`);
        }

        const data = await response.json();
        allCryptos = data;
        filteredCryptos = data;

        displayCryptos(filteredCryptos);
        updateLastUpdatedTime();
    } catch (error) {
        console.error("error fetching the data", error);
        showError();
    }
}

function displayCryptos(cryptos) {
    if (cryptos.length === 0) {
        cryptoGrid.innerHTML = '<div style="text-align: center; color: var(--text-2); padding: 40px; grid-column: 1/-1;">No cryptocurrencies found matching your search</div>';
        return;
    }

    // Sort favorited coins to the top
    const sortedCryptos = [...cryptos].sort((a, b) => {
        const isAFav = favorites.includes(a.id);
        const isBFav = favorites.includes(b.id);
        if (isAFav && !isBFav) return -1;
        if (!isAFav && isBFav) return 1;
        return 0;
    });

    cryptoGrid.innerHTML = sortedCryptos.map(crypto => {
        const priceChange1H = crypto.price_change_percentage_1h_in_currency ?? crypto.price_change_percentage_1h ?? 0;
        const priceChange24H = crypto.price_change_percentage_24h_in_currency ?? crypto.price_change_percentage_24h ?? 0;
        const priceChange7D = crypto.price_change_percentage_7d_in_currency ?? crypto.price_change_percentage_7d ?? 0;
        const isFav = favorites.includes(crypto.id);

        return `
        <div class="crypto-card ${isFav ? 'favorited' : ''}">
          <div class="crypto-header">
            <div class="crypto-info">
              <div>
                <div class="crypto-name">${crypto.name}</div>
                <div class="crypto-symbol">${crypto.symbol}</div>
              </div>
            </div>
            <div class="crypto-header-actions">
              <button class="star-btn ${isFav ? 'active' : ''}" data-id="${crypto.id}" aria-label="Favorite ${crypto.name}">
                <svg class="star-icon" viewBox="0 0 24 24" width="20" height="20">
                  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                </svg>
              </button>
              <div class="crypto-rank">#${crypto.market_cap_rank || 'N/A'}</div>
            </div>
          </div>
          <div class="crypto-price">$${formatPrice(crypto.current_price)}</div>
          <div class="market-cap">Market Cap: $${formatLargeNumber(crypto.market_cap)}</div>
          <div class="crypto-changes">
            <div class="change-item">
              <div class="change-label">1H</div>
              <div class="change-value ${getChangedClass(priceChange1H)}">${formatPercentage(priceChange1H)}</div>
            </div>
            <div class="change-item">
              <div class="change-label">24H</div>
              <div class="change-value ${getChangedClass(priceChange24H)}">${formatPercentage(priceChange24H)}</div>
            </div>
            <div class="change-item">
              <div class="change-label">7D</div>
              <div class="change-value ${getChangedClass(priceChange7D)}">${formatPercentage(priceChange7D)}</div>
            </div>
            <div class="change-item">
              <div class="change-label">Volume 24H</div>
              <div class="change-value neutral">${formatLargeNumber(crypto.total_volume)}</div>
            </div>
          </div>
        </div>
        `;
    }).join('');
}

function formatPrice(price) {
    if (price >= 1) {
        return price.toLocaleString('en-US', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    } else {
        return price.toFixed(6);
    }
}

function formatLargeNumber(num) {
    if (num >= 1e12) return (num / 1e12).toFixed(2) + 'T';
    if (num >= 1e9) return (num / 1e9).toFixed(2) + 'B';
    if (num >= 1e6) return (num / 1e6).toFixed(2) + 'M';
    return num.toLocaleString();
}

function getChangedClass(percentage) {
    if (percentage > 0) return 'position';
    if (percentage < 0) return 'negative';
    return 'neutral';
}

function formatPercentage(percentage) {
    return `${percentage > 0 ? '+' : ''}${percentage.toFixed(2)}%`;
}

function showLoading(show) {
    loadingGrid.style.display = show ? 'block' : 'none';
    loadingSpinner.style.display = show ? 'block' : 'none';
    loadingText.style.display = show ? 'block' : 'none';
    if (show) {
        refreshBtn.classList.add('loading');
        refreshBtn.disabled = true;
    } else {
        refreshBtn.classList.remove('loading');
        refreshBtn.disabled = false;
    }
}

function showError() {
    errorDiv.classList.add('error-show');
}

function hideError() {
    errorDiv.classList.remove('error-show');
}

function updateLastUpdatedTime() {
    const now = new Date();
    lastUpdated.textContent = `Last Updated: ${now.toLocaleTimeString()}`;
}

function filterCryptos(searchTerm) {
    const term = searchTerm.toLowerCase().trim();

    if (!term) {
        filteredCryptos = allCryptos;
    } else {
        filteredCryptos = allCryptos.filter(crypto =>
            crypto.name.toLowerCase().includes(term) ||
            crypto.symbol.toLowerCase().includes(term)
        );
    }

    displayCryptos(filteredCryptos);
}

// Event Delegation for Star Buttons
cryptoGrid.addEventListener('click', (e) => {
    const starBtn = e.target.closest('.star-btn');
    if (starBtn) {
        const cryptoId = starBtn.dataset.id;
        toggleFavorite(cryptoId);
    }
});

refreshBtn.addEventListener('click', fetchCryptoData);

searchInput.addEventListener('input', (e) => {
    filterCryptos(e.target.value);
});

setInterval(fetchCryptoData, 60000);
fetchCryptoData();