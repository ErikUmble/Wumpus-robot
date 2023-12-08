<template>
    <PageTitle>
        <template v-slot:title>Meeting Logs</template>
        <template v-slot:subtitle>The when and what of our project steps</template>
      </PageTitle>
    <div class="p-4 grid grid-cols-1 md:grid-cols-3 gap-4">
      <div v-for="(log, idx) in meeting_logs" :key="idx" class="bg-gray-800 rounded-lg p-4">
        <h1 class="text-lg font-semibold text-white mb-2 text-center">{{ log.date }}</h1>
        <p>{{ log.text }}</p>
      </div>
    </div>
  </template>

<script setup>
import meeting_logs from "@/assets/data/meeting_logs.json"

</script>