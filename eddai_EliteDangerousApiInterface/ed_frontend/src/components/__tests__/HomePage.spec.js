import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { createMemoryHistory, createRouter } from 'vue-router'
import App from '../../App.vue'
import applicationRouter from '../../router'

describe('Home page', () => {
  it('reaches and renders the home page at /', async () => {
    const router = createRouter({
      history: createMemoryHistory(),
      routes: applicationRouter.options.routes,
    })
    await router.push('/')
    await router.isReady()

    const wrapper = mount(App, { global: { plugins: [router] } })
    try {
      expect(router.currentRoute.value.name).toBe('home')
      expect(wrapper.get('h1').text()).toBe('Coming Soon')
      expect(wrapper.get('#infoSectionTitle').text()).toBe(
        'Elite Dangerous Data Interface (EDDAI)',
      )
      expect(wrapper.get('a.navbar-brand').attributes('href')).toBe('/')
    } finally {
      wrapper.unmount()
    }
  })
})