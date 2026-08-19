let allCryptos = [];
let filteredCryptos = [];

const cryptoGrid = document.getElementById('crypto-grid');
const loadingGrid = document.getElementById('loading-grid');
const loadingSpinner = document.getElementById('loading-spinner');
const loadingText = document.getElementById('loading-text');
const errorDiv = document.getElementById('error')
const refreshBtn = document.getElementById('refresh-button')
const searchInput = document.getElementById('search-input')
const lastUpdated = document.getElementById('lastUpdated')

const topCryptos = [
    "bitcoin", "ethereum", "binancecoin", "cardano", "dogecoin", "stellar"
]

async function fetchCryptoData() {
    try {
        hideError();

        const response = await fetch(`https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=${topCryptos.join(',')}&price_change_percentage=1h,24h,7d&x_cg_demo_api_key=CG-NEdjZsS9uW2vBQVrFxb6uuBh`)

        if (!response.ok) {
            throw new Error(`HTTP Error status: ${response.status}`)
        }

        const data = await response.json()
        console.log(data)
        allCryptos = data;
        filteredCryptos = data

        displayCryptos(filteredCryptos);
        updateLastUpdatedTime();
    } catch (error) {
        console.error("error fetching the data", error)
        showError();
    }
}

function displayCryptos(cryptos) {
    if (cryptos.length === 0) {
        cryptoGrid.innerHTML = '<div style="text-align: center; color: white; padding: 40px;">No cryptocurrencies found matching your search</div>'
        return;
    }

    cryptoGrid.innerHTML = cryptos.map(crypto => {
        const priceChange1H = crypto.price_change_percentage_1h_in_currency ?? crypto.price_change_percentage_1h ?? 0;
        const priceChange24H = crypto.price_change_percentage_24h_in_currency ?? crypto.price_change_percentage_24h ?? 0;
        const priceChange7D = crypto.price_change_percentage_7d_in_currency ?? crypto.price_change_percentage_7d ?? 0;

        return `
        <div class="crypto-card">
      <div class="crypto-header">
        <div class="crypto-info">
          <div>
            <div class="crypto-name">${crypto.name}</div>
            <div class="crypto-symbol">${crypto.symbol}</div>
          </div>
        </div>
        <div class="crypto-rank">#${crypto.market_cap_rank || 'N/A'}</div>
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
    }).join(``);
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
    if (num >= 1e12) {
        return (num / 1e12).toFixed(2) + 'T';
    } else if (num >= 1e9) {
        return (num / 1e9).toFixed(2) + 'B';
    } else if (num >= 1e6) {
        return (num / 1e6).toFixed(2) + 'M';
    } else {
        return num.toLocaleString();
    }
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
    if (show){
        refreshBtn.classList.add('loading');
        refreshBtn.disabled = true;
    } else {
        refreshBtn.classList.remove('loading');
        refreshBtn.disabled = false;
    }
}

function showError(){
    errorDiv.classList.add('error-show');
}

function hideError(){
    errorDiv.classList.remove('error-show');
}

function updateLastUpdatedTime(){
    const now = new Date();
    lastUpdated.textContent = `Last Updated: ${now.toLocaleTimeString()}`;
}

function filterCryptos(searchTerm){
    const term = searchTerm.toLowerCase().trim();

    if (!term){
        filteredCryptos = allCryptos;
    }else {
        filteredCryptos = allCryptos.filter(crypto =>
            crypto.name.toLowerCase().includes(term) ||
            crypto.symbol.toLowerCase().includes(term)
        );
    }

    displayCryptos(filteredCryptos); 
}

refreshBtn.addEventListener('click', fetchCryptoData)

searchInput.addEventListener('input', (e) => {
    showLoading(true);
    filterCryptos(e.target.value);
    showLoading(false);
})

setInterval(fetchCryptoData, 60000);
fetchCryptoData();