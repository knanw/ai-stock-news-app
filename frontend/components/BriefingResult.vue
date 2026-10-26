<script setup lang="ts">
import { ref } from 'vue'

interface Analysis {
  executiveSummary: string
  keyTakeaways: string[]
}

interface NewsItem {
  title: string
  publisher: string
  link: string
  publishTime: string
  summary?: string
}

defineProps<{
  result: {
    ticker: string
    analysis: Analysis
    news: NewsItem[]
  }
}>()

const activeNews = ref<NewsItem | null>(null)
</script>

<template>
  <main class="space-y-6">
    
     <!-- 1. Executive Summary -->
    <article class="card space-y-6">
      <header class="flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
          <h2 class="text-2xl font-bold font-mono text-indigo-400">{{ result.ticker }} Briefing</h2>
          <span class="text-xs text-slate-400">AI-powered portfolio news & summary</span>
        </div>
      </header>
      
      <section>
        <h3 class="text-xs uppercase text-slate-400 font-semibold mb-1 tracking-wider">Executive Summary</h3>
        <p class="text-slate-200 leading-relaxed">{{ result.analysis.executiveSummary }}</p>
      </section>

      <section>
        <h3 class="text-xs uppercase text-slate-400 font-semibold mb-2 tracking-wider">Key Takeaways</h3>
        <ul class="space-y-2">
          <li v-for="(takeaway, index) in result.analysis.keyTakeaways" :key="index" 
              class="bg-slate-950 p-3 rounded-xl border border-slate-800 text-sm text-slate-300">
            {{ String(index + 1).padStart(2, '0') }}. {{ takeaway }}
          </li>
        </ul>
      </section>
    </article>

    <!-- 2. Compact News List -->
    <section class="card space-y-3">
      <h3 class="text-xs uppercase text-slate-400 font-semibold tracking-wider">Current News-Feeds</h3>

      <div class="divide-y divide-slate-800 border border-slate-800 rounded-lg overflow-hidden bg-slate-950">
        <div v-for="(item, index) in result.news" :key="index"
             @click="activeNews = item"
             class="flex items-center justify-between p-3.5 hover:bg-slate-900 cursor-pointer transition">
          
          <div class="flex items-center space-x-3 truncate">
            <div class="w-7 h-7 rounded bg-slate-800 flex items-center text-indigo-400 justify-center font-bold text-xs shrink-0 border border-slate-700">
              {{ item.publisher.charAt(0).toUpperCase() }}
            </div>
            <div class="truncate">
              <h4 class="text-sm font-medium text-slate-200 truncate hover:text-indigo-300 transition">
                {{ item.title }}
              </h4>
              <p class="text-xs text-slate-400">
                {{ item.publisher }} • {{ item.publishTime }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

     <!-- Modal for Story-Details -->
    <div v-if="activeNews" class="fixed inset-0 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4 z-50" @click.self="activeNews = null">
      <div class="bg-slate-900 border border-slate-800 w-full max-w-lg rounded-xl p-6 shadow-2xl relative space-y-4">
        
        <!-- Header mit X -->
        <div class="flex justify-between items-center border-b border-slate-800 pb-3">
          <span class="text-xs text-slate-400">{{ activeNews.publisher }} • {{ activeNews.publishTime }}</span>
          <button @click="activeNews = null" class="text-slate-400 hover:text-white p-1 text-sm transition">
            ✕
          </button>
        </div>

        <!-- Titel & KI-Story-Summary -->
        <div class="space-y-3">
          <h3 class="text-lg font-bold text-slate-100 leading-snug">
            {{ activeNews.title }}
          </h3>
          <p class="text-slate-300 text-sm leading-relaxed">
            {{ activeNews.summary || activeNews.title }}
          </p>
        </div>

        <!-- Source Chip below the text -->
        <div class="pt-3 border-t border-slate-800">
          <a :href="activeNews.link" 
             target="_blank" 
             rel="noopener noreferrer"
             class="inline-block px-3 py-1.5 rounded-md bg-slate-800 text-slate-300 hover:bg-slate-700 hover:text-white text-xs font-medium transition cursor-pointer">
            {{ activeNews.publisher }}
          </a>
        </div>

      </div>
    </div>

  </main>
</template>