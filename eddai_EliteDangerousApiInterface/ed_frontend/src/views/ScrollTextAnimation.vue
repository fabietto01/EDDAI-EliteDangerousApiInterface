<template>
  <div>
    <!-- <div class="content-section">
      <h1>Scroll per vedere le animazioni</h1>
    </div> -->
    
    <div 
      ref="text1"
      class="scroll-text fade-in"
      :style="{ 
        opacity: textOpacity.text1,
        transform: `translateX(${textTransform.text1}px)` 
      }"
    >
      <h2>Testo che entra da sinistra</h2>
    </div>
    

  </div>
</template>

<script>
export default {
  name: 'ScrollTextAnimation',
  data() {
    return {
      scrollY: 0,
      textOpacity: {
        text1: 1,
        text2: 0,
        text3: 0
      },
      textTransform: {
        // text1: -100,
        text1: 0,
        text2: 50
      },
      textScale: {
        text3: 0.5
      }
    }
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
      const text1Offset = this.$refs.text1?.offsetTop || 0
      const text1Progress = this.calculateProgress(text1Offset, true) // true = prima sezione
      this.textOpacity.text1 = text1Progress
      this.textTransform.text1 = -100 + (100 * text1Progress)

      // Animazione testo 2 - slide dal basso
      /* const text2Offset = this.$refs.text2?.offsetTop || 0
      const text2Progress = this.calculateProgress(text2Offset)
      this.textOpacity.text2 = text2Progress
      this.textTransform.text2 = 50 - (100 * text2Progress) */

      // Animazione testo 3 - scale
      /* const text3Offset = this.$refs.text3?.offsetTop || 0
      const text3Progress = this.calculateProgress(text3Offset)
      this.textOpacity.text3 = text3Progress
      this.textScale.text3 = 0.5 + (0.5 * text3Progress) */
    },
    
    calculateProgress(elementTop, isFirst = false) {
      const windowHeight = window.innerHeight
      const elementPosition = elementTop - this.scrollY

      if (isFirst) {
        // Opacità 1 all'inizio, scende a 0 quando scrolli la prima viewport
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
.content-section {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  font-size: 2rem;
}

.scroll-text {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #2c3e50;
  color: white;
  font-size: 1.8rem;
  will-change: transform, opacity;
}

.scroll-text h2 {
  margin: 0;
  text-align: center;
}
</style>