<template>
  <div>
    <h2>Новые сообщения</h2>
    <div v-if="error" style="color: red;">Ошибка: {{ error }}</div>
    <div v-else-if="messages.length === 0">Нет новых сообщений</div>
    <ul>
      <li v-for="message in messages" :key="message.id">
        {{ message.owner }}: {{ message.text }}
        <button @click="generateResponse(message)">Ответить</button>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      messages: [],
      error: null
    };
  },
  mounted() {
    this.fetchMessages();
  },
  methods: {
    async fetchMessages() {
      try {
        const response = await axios.get('/api/messages/new', {
          headers: { 'Accept': 'application/json' }
        });
        console.log('Response status:', response.status);
        console.log('Response data:', response.data);
        this.messages = Array.isArray(response.data) ? response.data : [];
        this.error = null;
      } catch (error) {
        this.error = error.message || 'Не удалось загрузить сообщения';
        console.error('Fetch messages error:', error);
        if (error.response) {
          console.error('Response status:', error.response.status);
          console.error('Response data:', error.response.data);
        }
      }
    },
    async generateResponse(message) {
      try {
        const response = await axios.post('/llm/generate', {
          text: message.text,
          chat_id: String(message.chat_id)
        });
        await axios.post('/api/messages/generate', {
          chat_id: Number(message.chat_id),
          text: response.data.response
        });
        this.fetchMessages();
      } catch (error) {
        this.error = error.message || 'Не удалось сгенерировать ответ';
        console.error('Generate response error:', error);
        if (error.response) {
          console.error('Error status:', error.response.status);
          console.error('Error data:', error.response.data); 
        }
      }
    }
  }
};
</script>