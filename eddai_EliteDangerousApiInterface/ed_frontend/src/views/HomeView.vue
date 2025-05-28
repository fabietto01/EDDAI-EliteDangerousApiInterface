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
    <h1 class="scritta">Coming soon</h1>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  data() {
    return {
      cards: [
        // {
        //   id: 1,
        //   title: 'System',
        //   description: 'Discover detailed information about various systems across the galaxy. Each system page allows you to explore specific traits, enabling tailored filtering to match your interests and search preferences with ease.',
        //   link: '/systems/'
        // },
        // {
        //   id: 2,
        //   title: 'Station',
        //   description: 'Explore the characteristics of celestial bodies within each system. Use smart filtering tools to narrow down entities based on distinct features, making it easier to find what truly matters to you.',
        //   link: '#'
        // },
        // {
        //   id: 3,
        //   title: 'Body',
        //   description: 'Get in-depth data about every station in our network. Each page offers advanced filtering options, helping you browse based on functionality, location, or features that meet your unique criteria.',
        //   link: '#'
        // }
      ]
    };
  }
};
</script>

<style scoped>
.card {
  background-color: #aac9de;
}

</style>