<template>
  <div class="container pt-5">
    <div class="row g-3">
      <div class="col-md-4 d-flex" v-for="card in cards" :key="card.id">
        <a class="card p-1 h-100 w-100 text-decoration-none" :href="card.link">
          <div class="d-flex justify-content-between align-items-center p-2 border-bottom border-dark">
            <div>
              <i class="bi bi-sun"></i>
            </div>
            <h5 class="mb-0 text-end">{{ card.title }}</h5>
          </div>
          <div class="card-body d-flex flex-column">
            <p class="card-text">{{ card.description }}</p>
          </div>
        </a>
      </div>
    </div>
    
  </div>
  <div class="container my-cont w-100">
    <h1 class="scritta">Comin soon</h1>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  data() {
    return {
      cards: [
      ]
    };
  }
};
</script>

<style scoped>

.scritta {
  color: white;
  font-size: 88px;
}

.my-cont {
  height: 75vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

body {
  /* todo: aggiungere immagine di sfondo */
  background-image: none;
}

</style>