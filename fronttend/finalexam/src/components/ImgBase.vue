<template>
    <div>
      <button @click="fetchImage">Загрузить изображение</button>
      <div v-if="imageSrc">
        <img :src="imageSrc" alt="Visualization" />
      </div>
      <p v-else>Нажмите на кнопку, чтобы загрузить изображение.</p>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        imageSrc: null, // Хранит base64 URL изображения
      };
    },
    methods: {
      async fetchImage() {
        try {
          const response = await fetch('http://127.0.0.1:5000/api/visualize'); // Запрос к вашему API
          if (!response.ok) {
            throw new Error(`Ошибка запроса: ${response.status}`);
          }
          const data = await response.json();
          this.imageSrc = data.plot_url; // Установка изображения
        } catch (error) {
          console.error('Ошибка загрузки изображения:', error);
        }
      },
    },
  };
  </script>
  
  <style scoped>
  img {
    max-width: 100%;
    height: auto;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  button {
    margin-bottom: 10px;
    padding: 8px 16px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  button:hover {
    background-color: #45a049;
  }
  </style>
  