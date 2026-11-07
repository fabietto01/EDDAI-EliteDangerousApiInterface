import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import NavBar from '../NavBar.vue'
import router from '../../router'

describe('Frontend shell', () => {
  it('renders the brand and Bootstrap navigation control', () => {
    const wrapper = mount(NavBar)
    expect(wrapper.get('a[href="/"]').text()).toContain('EDDAI')
    expect(wrapper.get('button').attributes('data-bs-target')).toBe('#FullScreenNav')
    expect(wrapper.find('#FullScreenNav').exists()).toBe(true)
  })

  it('loads the lazy route independently of Django templates', async () => {
    const route = router.getRoutes().find((entry) => entry.path === '/ScrollTextAnimation')
    expect(route).toBeDefined()
    const component = await route.components.default()
    expect(component.default).toBeDefined()
  })
})