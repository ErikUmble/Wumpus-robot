<template>
    <div v-for="log, idx in meeting_logs" :key="idx" class="container w-full mx-2">
        <h1 class="text-lg text-white">{{ log.date }}</h1>
        <p>{{ log.text }}</p>
        <br/>
    </div>
</template>

<script setup>
import meeting_logs from "@/assets/data/meeting_logs.json"

</script>