import React, { useState, useEffect } from 'react'
import { getStatistics } from '../api'
import { User } from '../types'
import i18n from '../i18n'

interface ProfileProps {
  user: User
}

interface StatisticsData {
  platform: {
    total_books: number
    available_books: number
    total_reservations: number
    active_reservations: number
  }
  user: {
    my_books: number
    my_reservations: number
  }
}

const Profile: React.FC<ProfileProps> = ({ user }) => {
  const [stats, setStats] = useState<StatisticsData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    loadStatistics()
  }, [])

  const loadStatistics = async () => {
    try {
      const response = await getStatistics()
      setStats(response.data)
    } catch (err: any) {
      console.error('Error loading statistics:', err)
      setError(i18n.t('failedToLoadStats'))
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="loading">
        <div>{i18n.t('loadingProfile')}</div>
        <div className="loading-spinner"></div>
      </div>
    )
  }

  const initials = user.full_name
    .split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)

  return (
    <div>
      <h1>{i18n.t('myProfile')}</h1>

      {error && (
        <div className="error-message">
          <strong>{i18n.t('error')}:</strong> {error}
        </div>
      )}

      <div className="form" style={{ maxWidth: '600px' }}>
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <div style={{
            width: '100px',
            height: '100px',
            borderRadius: '50%',
            background: '#3498db',
            color: 'white',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '2.5rem',
            fontWeight: 'bold',
            margin: '0 auto 1rem'
          }}>
            {initials}
          </div>
          <h2>{user.full_name}</h2>
          <p style={{ color: '#7f8c8d' }}>{user.email}</p>
          {user.phone && <p style={{ color: '#7f8c8d' }}>📞 {user.phone}</p>}
          <p style={{ color: '#27ae60', fontWeight: 'bold' }}>{i18n.t('active')}</p>
        </div>

        <div style={{ marginTop: '2rem' }}>
          <h3>{i18n.t('accountStats')}</h3>
          {stats && (
            <div style={{ display: 'grid', gap: '1rem', marginTop: '1rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem 0', borderBottom: '1px solid #eee' }}>
                <span style={{ fontWeight: 'bold' }}>{i18n.t('booksAdded')}:</span>
                <span style={{ color: '#3498db', fontWeight: 'bold' }}>{stats.user.my_books}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem 0', borderBottom: '1px solid #eee' }}>
                <span style={{ fontWeight: 'bold' }}>{i18n.t('booksReserved')}:</span>
                <span style={{ color: '#3498db', fontWeight: 'bold' }}>{stats.user.my_reservations}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem 0', borderBottom: '1px solid #eee' }}>
                <span style={{ fontWeight: 'bold' }}>{i18n.t('totalBooks')}:</span>
                <span style={{ color: '#3498db', fontWeight: 'bold' }}>{stats.platform.total_books}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem 0', borderBottom: '1px solid #eee' }}>
                <span style={{ fontWeight: 'bold' }}>{i18n.t('availableForExchange')}:</span>
                <span style={{ color: '#27ae60', fontWeight: 'bold' }}>{stats.platform.available_books}</span>
              </div>
            </div>
          )}
        </div>

        <div style={{ marginTop: '2rem' }}>
          <h3>{i18n.t('accountInfo')}</h3>
          <div style={{ display: 'grid', gap: '1rem', marginTop: '1rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem 0', borderBottom: '1px solid #eee' }}>
              <span style={{ fontWeight: 'bold' }}>{i18n.t('onPlatformSince')}:</span>
              <span>2024</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem 0', borderBottom: '1px solid #eee' }}>
              <span style={{ fontWeight: 'bold' }}>{i18n.t('status')}:</span>
              <span style={{ color: '#27ae60', fontWeight: 'bold' }}>{i18n.t('active')}</span>
            </div>
          </div>
        </div>
      </div>

      <div style={{ marginTop: '2rem', background: '#f8f9fa', padding: '1.5rem', borderRadius: '8px' }}>
        <h3>{i18n.t('myActivity')}</h3>
        <p style={{ marginTop: '1rem' }}>{i18n.t('profileActivityPlaceholder')}</p>
      </div>
    </div>
  )
}

export default Profile
