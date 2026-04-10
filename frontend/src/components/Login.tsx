import React, { useState } from 'react'
import { login, register } from '../api'
import i18n from '../i18n'

interface LoginProps {
  onLogin: (token: string) => void
}

const Login: React.FC<LoginProps> = ({ onLogin }) => {
  const [isLogin, setIsLogin] = useState(true)
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    full_name: '',
    phone: ''
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      if (isLogin) {
        const response = await login({
          email: formData.email,
          password: formData.password
        })
        onLogin(response.data.access_token)
      } else {
        await register({
          email: formData.email,
          password: formData.password,
          full_name: formData.full_name,
          phone: formData.phone || undefined
        })

        const loginResponse = await login({
          email: formData.email,
          password: formData.password
        })
        onLogin(loginResponse.data.access_token)
      }
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || err.message || 'An error occurred'
      setError(errorMessage)
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  return (
    <div className="form">
      <h2>{isLogin ? i18n.t('login') : i18n.t('register')}</h2>
      {error && (
        <div className="error-message">
          <strong>{i18n.t('error')}:</strong> {error}
        </div>
      )}
      <form onSubmit={handleSubmit}>
        {!isLogin && (
          <>
            <div className="form-group">
              <label>{i18n.t('fullName')}:</label>
              <input
                type="text"
                name="full_name"
                value={formData.full_name}
                onChange={handleChange}
                required
                disabled={loading}
              />
            </div>
            <div className="form-group">
              <label>{i18n.t('phone')} (optional):</label>
              <input
                type="tel"
                name="phone"
                value={formData.phone}
                onChange={handleChange}
                disabled={loading}
                placeholder="+1234567890"
              />
            </div>
          </>
        )}
        <div className="form-group">
          <label>{i18n.t('email')}:</label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
            disabled={loading}
          />
        </div>
        <div className="form-group">
          <label>{i18n.t('password')}:</label>
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
            disabled={loading}
            minLength={6}
          />
        </div>
        <button
          type="submit"
          className="btn"
          disabled={loading}
          style={{ width: '100%' }}
        >
          {loading ? (isLogin ? i18n.t('login') + '...' : i18n.t('register') + '...') :
            (isLogin ? i18n.t('login') : i18n.t('register'))}
        </button>
      </form>
      <p style={{ marginTop: '1rem', textAlign: 'center' }}>
        {isLogin ? i18n.t('noAccount') : i18n.t('haveAccount')}
        <button
          type="button"
          className="btn btn-secondary"
          onClick={() => {
            setIsLogin(!isLogin)
            setError('')
          }}
          disabled={loading}
          style={{ marginLeft: '0.5rem' }}
        >
          {isLogin ? i18n.t('register') : i18n.t('login')}
        </button>
      </p>
    </div>
  )
}

export default Login
