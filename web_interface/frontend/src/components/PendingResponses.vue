<template>
  <div>
    <h2>Модерация ответов</h2>
    <div v-for="response in responses" :key="response.id" class="response">
      <p><strong>Chat ID:</strong> {{ response.chat_id }}</p>
      <p><strong>Ответ:</strong></p>
      <textarea v-model="response.text" rows="4" cols="50"></textarea>
      <div class="buttons">
        <button @click="acceptResponse(response.id)">Принять</button>
        <button @click="editResponse(response.id, response.chat_id, response.text)">Сохранить изменения</button>
        <button @click="rejectResponse(response.id)">Отклонить</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      responses: []
    }
  },
  mounted() {
    this.fetchPendingResponses()
  },
  methods: {
    async fetchPendingResponses() {
      try {
        const response = await axios.get('/api/responses/pending')
        this.responses = response.data
      } catch (error) {
        console.error('Ошибка при загрузке ответов:', error)
        alert('Ошибка при загрузке ответов')
      }
    },
    async acceptResponse(message_id) {
      try {
        await axios.post('/api/messages/status', {
          message_id,
          status: 'answered',
          chat_id: this.responses.find(r => r.id === message_id).chat_id
        })
        this.fetchPendingResponses()
        alert('Ответ принят')
      } catch (error) {
        console.error('Ошибка при принятии ответа:', error)
        alert('Ошибка сервера при принятии ответа')
      }
    },
    async editResponse(message_id, chat_id, text) {
      try {
        await axios.post('/api/messages/status', {
          message_id,
          status: 'edited',
          chat_id,
          text
        })
        this.fetchPendingResponses()
        alert('Изменения сохранены')
      } catch (error) {
        console.error('Ошибка при редактировании ответа:', error)
        alert('Ошибка сервера при сохранении изменений')
      }
    },
    async rejectResponse(message_id) {
      try {
        await axios.post('/api/messages/status', {
          message_id,
          status: 'rejected'
        })
        this.fetchPendingResponses()
        alert('Ответ отклонён')
      } catch (error) {
        console.error('Ошибка при отклонении ответа:', error)
        alert('Ошибка сервера при отклонении ответа')
      }
    }
  }
}
</script>

<style scoped>
.response {
  border: 1px solid #ccc;
  padding: 10px;
  margin: 10px 0;
  border-radius: 5px;
}
.buttons {
  margin-top: 10px;
}
button {
  margin-right: 10px;
  background-color: #4CAF50;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:nth-child(2) {
  background-color: #2196F3;
}
button:nth-child(3) {
  background-color: #f44336;
}
button:hover {
  opacity: 0.9;
}
textarea {
  width: 100%;
  border-radius: 4px;
}
</style>