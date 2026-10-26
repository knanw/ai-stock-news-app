<script setup lang="ts">
import { ref } from 'vue'
import { normalizeTicker } from '../utils.mjs'

defineProps<{ isLoading: boolean }>()
const emit = defineEmits<{ (e: 'submit-briefing', payload: { ticker: string; apiKey: string }): void }>()

const ticker = ref('')
const apiKey = ref('')

function onSubmit() {
  if (!normalizeTicker(ticker.value)) return
  emit('submit-briefing', { ticker: ticker.value, apiKey: apiKey.value })
}
</script>

<template>
  <form @submit.prevent="onSubmit" class="card">
    <div>
      <label class="block text-sm font-medium text-slate-300 mb-1">Stock Ticker</label>
      <input v-model="ticker" type="text" placeholder="e.g. AAPL, TSLA" required class="input-field uppercase">
    </div>
    <div>
      <label class="block text-sm font-medium text-slate-300 mb-1">OpenAI API Key (Optional)</label>
      <input v-model="apiKey" type="password" placeholder="sk-..." class="input-field text-sm">
    </div>
    <button type="submit" :disabled="isLoading" class="btn-primary">
      {{ isLoading ? "Analyzing via FastAPI & OpenAI..." : "Generate Briefing" }}
    </button>
  </form>
</template>