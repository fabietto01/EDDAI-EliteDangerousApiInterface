<template>

  <div class="container">
    <div class="row align-items-center row-cols-3 g-2 mt-5">
      <div class="col" v-for="card in cards" :key="card.id">
        <div class="card h-100">
          <div class="d-flex align-items-center p-2 border-bottom border-dark">
            <div class="me-3">
              <i class="bi bi-sun"></i>
            </div>
            <h5 class="mb-0 ms-auto text-end">{{ card.title }}</h5>
          </div>
          <div class="card-body flex-grow-1">
            <p class="card-text">{{ card.description }}</p>
          </div>
        </div>
      </div>
    </div>
    <div>

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
          description: 'Find the system that best suits your needs.',
          link: '/systems/'
        },
        {
          id: 2,
          title: 'Station',
          description: 'Find the space station that meets your needs.',
          link: '#'
        },
        {
          id: 3,
          title: 'Body',
          description: 'Find the body that meets your needs.',
          link: '#'
        }
      ]
    };
  }
};
</script>

<style scoped>
.card {
  background-color: #aac9de;
  border: none;
  border-radius: 10px;
  padding: 5px;
  max-width: 400px;
}

.row.g-2 {
  display: flex;
  flex-wrap: wrap;
}

.col-md-6 {
  display: flex;
}
</style>