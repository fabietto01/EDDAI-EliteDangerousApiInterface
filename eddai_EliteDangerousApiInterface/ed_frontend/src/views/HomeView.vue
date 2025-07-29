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
      <div class="container-md text-center">
        <h2 id="infoSectionTitle" class="fw-bold info-section-testo" style="color: #f36c1b;">Elite Dangerous Data Interface (EDDAI)</h2>
        <p class="info-section-testo">Elite Dangerous Data Interface (EDDAI) nasce con l’idea di ricreare il TOOL EDDB (Elite Dangerous Database).</p>
        <p class="info-section-testo">Si tratta di un database che fornisce un unico punto dove ricercare in maniera precisa tutte le informazioni relative a Elite Dangerous (materiali, sistemi stellari, stazioni, fazioni etc.) grazie all’integrazione con API CAPI (API fornite direttamente da Frontier) e EDDN (Elite Dangerous Data Network) che sono quindi fonti sicure e precise dei dati di EDDAI. </p>
        <p class="info-section-testo">E’ possibile applicare dei filtri per affinare la propria query in base alle necessità, arrivando a poter gestire anche ricerche granulari e quindi complesse. A differenza di altri tool esistenti, infatti, è possibile per esempio ricercare un particolare sistema che abbia dei parametri specifici in termini di caratteristiche dei pianeti che lo compongono. </p>
        <p class="info-section-testo">L’interfaccia consente un uso semplice e immediato del tool. Per i developer sono anche disponibili delle <a class="info-section-link" href="/api/schema/swagger-ui/" target="_blank" rel="noopener noreferrer">API REST</a> con cui è possibile integrarsi.</p>
        <p>Le tecnologie utilizzate per lo sviluppo di Elite Dangerous Data Interface sono: </p>
        <ul class="info-section-testo" style="margin-bottom: 2rem;">
          <li>Front-End: Vue.js</li>
          <li>Back-End: Python (Django)</li>
          <li>Database: PostgreSQL</li>
        </ul>
        <p>Il progetto è open-source ed è disponibile su <a class="info-section-link" href="https://github.com/fabietto01/EDDAI-EliteDangerousApiInterface" target="_blank" rel="noopener noreferrer">Github</a></p>
      </div>
    </section>


    <section class="full-screen">
      <p></p>
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

.info-section-testo {
  margin-bottom: 2rem;
}

.info-section ul {
  display: inline-block;
  text-align: left;
  margin: 0 auto;
}

.info-section a {
  color: #f36c1b;
  /* text-decoration: none; */
}

.info-section a:hover {
  color: #aac9de;
}



</style>