<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{ sentiment: 'Bullish' | 'Bearish' | 'Neutral' }>()

const badgeClass = computed(() => {
  if (props.sentiment === 'Bullish') return 'badge-bullish'
  if (props.sentiment === 'Bearish') return 'badge-bearish'
  return 'badge-neutral'
})
</script>

<template>
  <span :class="badgeClass">
    {{ sentiment }}
  </span>
</template>