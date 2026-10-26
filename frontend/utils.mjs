/** Pure request helpers shared by the UI and Node's built-in test runner. */
export function normalizeTicker(ticker) {
  return String(ticker ?? '').trim().toUpperCase()
}

export function buildSummaryRequest(ticker, apiKey = '') {
  return {
    ticker: normalizeTicker(ticker),
    api_key: String(apiKey ?? '').trim() || null,
  }
}

export function getApiErrorMessage(data, fallback = 'Server error') {
  return typeof data?.detail === 'string' && data.detail.trim()
    ? data.detail
    : fallback
}
