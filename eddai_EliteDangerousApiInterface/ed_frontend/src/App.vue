<template>
  <NavBar />
  <RouterView />
</template>

<script>
  import { RouterLink, RouterView } from 'vue-router'
  import NavBar from '@/components/NavBar.vue'

  export default {
    name: 'App',
    components: {
      NavBar
    }
  }

</script>