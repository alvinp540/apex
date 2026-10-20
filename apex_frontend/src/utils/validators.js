export const required = (v) => !!v || 'This field is required'

export const email = (v) =>
  /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) || 'Invalid email address'

export const minLength = (n) => (v) =>
  (v && v.length >= n) || `Minimum ${n} characters`

export const maxLength = (n) => (v) =>
  !v || v.length <= n || `Maximum ${n} characters`

export const passwordStrength = (v) => {
  if (!v || v.length < 8) return 'At least 8 characters'
  if (!/[A-Z]/.test(v)) return 'Must contain an uppercase letter'
  if (!/[0-9]/.test(v)) return 'Must contain a number'
  return true
}
