export function normalizeTicker(ticker: unknown): string
export function buildSummaryRequest(ticker: unknown, apiKey?: unknown): { ticker: string; api_key: string | null }
export function getApiErrorMessage(data: unknown, fallback?: string): string
