<script setup lang="ts">
import { ref } from 'vue'
import { buildSummaryRequest, getApiErrorMessage } from './utils.mjs'

const config = useRuntimeConfig()
const isLoading = ref(false)
const errorMessage = ref('')
const result = ref<any>(null)

async function getSummary({ ticker, apiKey }: { ticker: string; apiKey: string }) {
  isLoading.value = true
  errorMessage.value = ''
  result.value = null

  try {
    const response = await fetch(`${config.public.apiBaseUrl}/api/summary`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(buildSummaryRequest(ticker, apiKey))
    })

    const data = await response.json()
    if (!response.ok) throw new Error(getApiErrorMessage(data))

    result.value = data
  } catch (err: any) {
    errorMessage.value = err.message
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="bg-slate-950 text-slate-100 min-h-screen p-6 md:p-12">
    <div class="max-w-3xl mx-auto space-y-8">
      
      <header class="text-center space-y-2">
        <h1 class="text-3xl font-bold">Trader News</h1>
        <p class="text-slate-400">AI-powered stock news</p>
      </header>

      <BriefingForm :is-loading="isLoading" @submit-briefing="getSummary" />

      <div v-if="errorMessage" class="bg-rose-950 border border-rose-800 text-rose-200 p-4 rounded-xl" role="alert">
        {{ errorMessage }}
      </div>

      <BriefingResult v-if="result" :result="result" />

    </div>
  </div>
</template>