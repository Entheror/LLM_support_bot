<template>
  <div class="container">
    <h1>Поддержка Telegram: Оператор</h1>
    <NewMessages :messages="newMessages" @response-generated="fetchData" />
    <PendingResponses :responses="pendingResponses" @response-updated="fetchData" />
  </div>
</template>

<style>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}
h1 {
  text-align: center;
}
</style>

<script>
import axios from 'axios'
import NewMessages from './components/NewMessages.vue'
import PendingResponses from './components/PendingResponses.vue'

export default {
  components: { NewMessages, PendingResponses },
  data() {
    return {
      newMessages: [],
      pendingResponses: []
    }
  },
  methods: {
    async fetchData() {
      try {
        const [newMessages, pendingResponses] = await Promise.all([
          axios.get('/api/messages/new'),
          axios.get('/api/responses/pending')
        ])
        this.newMessages = newMessages.data
        this.pendingResponses = pendingResponses.data
      } catch (error) {
        console.error('Ошибка загрузки данных:', error)
      }
    }
  },
  mounted() {
    this.fetchData()
    setInterval(this.fetchData, 5000)
  }
}
</script>