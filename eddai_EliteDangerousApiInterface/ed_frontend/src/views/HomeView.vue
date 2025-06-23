<template>
  <div class="container pt-5 d-none">
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

  <div>
    <!-- Sezione Coming Soon -->
    <section class="coming-soon full-screen">
      <h1 ref="text1"
          class="scroll-text" 
          :style="{
            opacity: textOpacity.text1,
            transform: `translateX(${textTransform.text1}px)`
          }"
        >
        Coming Soon
      </h1>
    </section>

    <!-- Sezione Informazioni -->
    <section class="info-section">
      <h2>Informazioni sul progetto</h2>
      <p>Questo progetto ha lo scopo di offrire un portale per la consultazione di informazioni strutturate.</p>
      <p></p>
      <div>
        <a href="https://github.com/tuo-progetto" target="_blank">Repository GitHub</a><br />
      </div>
      <div>
        <a href="https://tuo-backend.com/swagger" target="_blank">Swagger API</a>
      </div>

    </section>


    <section class="full-screen">
      <p>fabio culo</p>
    </section>
  </div>
  
</template>

<script>
export default {
  name: 'HomeView',
  data() {
    return {
      cards: [],
      scrollY: 0,
      textOpacity: {
        text1: 1,
        text2: 0,
        text3: 0
      },
      textTransform: {
        text1: 0,
        text2: 50
      },
      textScale: {
        text3: 0.5
      }
    };
  },
  mounted() {
    window.addEventListener('scroll', this.handleScroll)
    this.handleScroll() // Calcola posizione iniziale
  },
  beforeUnmount() {
    window.removeEventListener('scroll', this.handleScroll)
  },
  methods: {
    handleScroll() {
      this.scrollY = window.scrollY
      this.animateTexts()
    },
    animateTexts() {
      // Animazione testo 1 - fade out verso l'alto
      const text1Offset = this.$refs?.text1?.offsetTop || 0
      const text1Progress = this.calculateProgress(text1Offset, true)
      this.textOpacity.text1 = Math.max(0, Math.min(1, text1Progress))
      // this.textTransform.text1 = -100 + (100 * text1Progress)
      // Altre animazioni commentate come prima
    },
    calculateProgress(elementTop, isFirst = false) {
      const windowHeight = window.innerHeight
      const elementPosition = elementTop - this.scrollY

      if (isFirst) {
        if (this.scrollY >= windowHeight) return 0
        const progress = 1 - Math.min(Math.max(this.scrollY / windowHeight, 0), 1)
        return progress
      }

      const startAnimation = windowHeight * 0.8
      const endAnimation = windowHeight * 0.2

      if (elementPosition > startAnimation || elementPosition < endAnimation) {
        return 0
      }
      return 1 - Math.abs((elementPosition - (startAnimation + endAnimation) / 2) / ((startAnimation - endAnimation) / 2))
    }
  }
}
</script>





<style scoped>

.scroll-text{
  font-size: 5rem;
  color: white;
  will-change: transform, opacity;
}

.my-cont {
  height: 75vh;
  display: flex;
  justify-content: center;
  align-items: center;
}


/* parte nuova */

/* Full screen coming soon */
.full-screen {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #121212;
  color: white;
  font-size: 3em;
  font-weight: bold;
}

/* Info section */
.info-section {
  padding: 2rem;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #121212;
}







</style>