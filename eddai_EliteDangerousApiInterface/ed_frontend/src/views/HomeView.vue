<template>

  <div class="container d-flex justify-content-center align-items-center mt-4">
    <div class="row g-2">
      <div class="col-md-6" v-for="card in cards" :key="card.id">
        <div class="card">
          <div class="d-flex align-items-center p-3 border-bottom border-dark">
            <div class="me-3">
              <i class="bi bi-sun"></i>
            </div>
            <h5 class="mb-0">{{ card.title }}</h5>
          </div>
          <div class="card-body">
            <p class="card-text">{{ card.description }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  data() {
    return {
      cards: [
        {
          id: 1,
          title: 'System',
          description: 'Description for Card 1',
          link: '#'
        },
        {
          id: 2,
          title: 'Station',
          description: 'Description for Card 2',
          link: '#'
        },
      ]
    };
  }
};
</script>

<style>
.card {
  background-color: #aac9de;
  border: none;
  border-radius: 10px;
  padding: 5px; /* Imposta i margini interni della card */
  max-width: 400px;
}



/* Aggiungi eventuali stili personalizzati qui */
</style>