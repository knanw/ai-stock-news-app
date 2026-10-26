import test from 'node:test'
import assert from 'node:assert/strict'
import { buildSummaryRequest, getApiErrorMessage, normalizeTicker } from '../utils.mjs'

test('normalizeTicker trims whitespace and uppercases symbols', () => {
  assert.equal(normalizeTicker('  aapl '), 'AAPL')
})

test('normalizeTicker safely handles empty values', () => {
  assert.equal(normalizeTicker('  '), '')
  assert.equal(normalizeTicker(null), '')
})

test('buildSummaryRequest uses backend field names and omits a blank API key', () => {
  assert.deepEqual(buildSummaryRequest(' msft ', '  '), { ticker: 'MSFT', api_key: null })
})

test('buildSummaryRequest includes a provided API key', () => {
  assert.deepEqual(buildSummaryRequest('tsla', 'secret'), { ticker: 'TSLA', api_key: 'secret' })
})

test('getApiErrorMessage returns backend detail when available', () => {
  assert.equal(getApiErrorMessage({ detail: 'Invalid API key' }), 'Invalid API key')
})

test('getApiErrorMessage uses fallback for malformed error bodies', () => {
  assert.equal(getApiErrorMessage({}, 'Request failed'), 'Request failed')
  assert.equal(getApiErrorMessage({ detail: '' }), 'Server error')
})
