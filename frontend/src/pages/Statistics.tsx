import React, { useState, useEffect } from 'react'
import { getStatistics, getBooks } from '../api'
import i18n from '../i18n'

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

interface DetailedStats {
  booksByGenre: { genre: string; count: number }[]
  booksByYear: { year: number; count: number }[]
  topRatedBooks: { id: number; title: string; author: string; average_rating: number; year: number }[]
}

const Statistics: React.FC = () => {
  const [stats, setStats] = useState<StatisticsData | null>(null)
  const [detailedStats, setDetailedStats] = useState<DetailedStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    loadStatistics()
  }, [])

  const loadStatistics = async () => {
    try {
      setLoading(true)
      const [statsResponse, booksResponse] = await Promise.all([
        getStatistics(),
        getBooks({ page: 1, page_size: 100 })
      ])

      setStats(statsResponse.data)

      // Вычисляем статистику по жанрам и годам
      const books = booksResponse.data.items || []
      
      const genreCount: { [key: string]: number } = {}
      const yearCount: { [key: number]: number } = {}
      
      books.forEach((book: any) => {
        genreCount[book.genre] = (genreCount[book.genre] || 0) + 1
        yearCount[book.year] = (yearCount[book.year] || 0) + 1
      })

      const booksByGenre = Object.entries(genreCount).map(([genre, count]) => ({ genre, count }))
      const booksByYear = Object.entries(yearCount)
        .map(([year, count]) => ({ year: parseInt(year), count }))
        .sort((a, b) => b.year - a.year)
        .slice(0, 10)

      const topRatedBooks = books
        .filter((book: any) => book.average_rating > 0)
        .sort((a: any, b: any) => b.average_rating - a.average_rating)
        .slice(0, 5)

      setDetailedStats({
        booksByGenre,
        booksByYear,
        topRatedBooks
      })
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
        <div>{i18n.t('loading')}</div>
        <div className="loading-spinner"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="error-message">
        <strong>{i18n.t('error')}:</strong> {error}
      </div>
    )
  }

  return (
    <div>
      <h1>{i18n.t('platformStatistics')}</h1>

      {stats && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.5rem', marginBottom: '2rem' }}>
          <div className="stat-card">
            <h3 style={{ color: '#3498db' }}>{i18n.t('totalBooks')}</h3>
            <p style={{ fontSize: '2rem', fontWeight: 'bold' }}>{stats.platform.total_books}</p>
          </div>
          <div className="stat-card">
            <h3 style={{ color: '#27ae60' }}>{i18n.t('availableForExchange')}</h3>
            <p style={{ fontSize: '2rem', fontWeight: 'bold' }}>{stats.platform.available_books}</p>
          </div>
          <div className="stat-card">
            <h3 style={{ color: '#e67e22' }}>{i18n.t('totalReservations')}</h3>
            <p style={{ fontSize: '2rem', fontWeight: 'bold' }}>{stats.platform.total_reservations}</p>
          </div>
          <div className="stat-card">
            <h3 style={{ color: '#9b59b6' }}>{i18n.t('activeReservations')}</h3>
            <p style={{ fontSize: '2rem', fontWeight: 'bold' }}>{stats.platform.active_reservations}</p>
          </div>
          <div className="stat-card">
            <h3 style={{ color: '#3498db' }}>{i18n.t('myBooks')}</h3>
            <p style={{ fontSize: '2rem', fontWeight: 'bold' }}>{stats.user.my_books}</p>
          </div>
          <div className="stat-card">
            <h3 style={{ color: '#e74c3c' }}>{i18n.t('myReservations')}</h3>
            <p style={{ fontSize: '2rem', fontWeight: 'bold' }}>{stats.user.my_reservations}</p>
          </div>
        </div>
      )}

      {detailedStats && (
        <div style={{ marginTop: '2rem' }}>
          <h2>{i18n.t('detailedStats')}</h2>

          <div style={{ marginBottom: '2rem' }}>
            <h3>{i18n.t('booksByGenre')}</h3>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '1rem' }}>
              {detailedStats.booksByGenre.map((item) => (
                <div key={item.genre} style={{
                  background: '#f8f9fa',
                  padding: '1rem',
                  borderRadius: '4px',
                  borderLeft: '4px solid #3498db'
                }}>
                  <p style={{ margin: 0, fontWeight: 'bold' }}>{i18n.t(`genre${item.genre}`) || item.genre}</p>
                  <p style={{ margin: '0.25rem 0 0', color: '#7f8c8d' }}>{item.count} книг</p>
                </div>
              ))}
            </div>
          </div>

          <div style={{ marginBottom: '2rem' }}>
            <h3>{i18n.t('topRatedBooks')}</h3>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1rem' }}>
              {detailedStats.topRatedBooks.map((book) => (
                <div key={book.id} style={{
                  background: 'white',
                  padding: '1rem',
                  borderRadius: '8px',
                  boxShadow: '0 2px 5px rgba(0,0,0,0.1)'
                }}>
                  <p style={{ margin: 0, fontWeight: 'bold' }}>{book.title}</p>
                  <p style={{ margin: '0.25rem 0 0', fontSize: '0.9rem', color: '#7f8c8d' }}>{book.author}</p>
                  <p style={{ margin: '0.25rem 0 0', color: '#f39c12', fontWeight: 'bold' }}>
                    ★ {book.average_rating.toFixed(1)}
                  </p>
                </div>
              ))}
            </div>
          </div>

          <div style={{ marginBottom: '2rem' }}>
            <h3>{i18n.t('booksByYear')}</h3>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '1rem' }}>
              {detailedStats.booksByYear.map((item) => (
                <div key={item.year} style={{
                  background: '#e8f4f8',
                  padding: '1rem',
                  borderRadius: '4px',
                  borderLeft: '4px solid #2980b9'
                }}>
                  <p style={{ margin: 0, fontWeight: 'bold' }}>{item.year}</p>
                  <p style={{ margin: '0.25rem 0 0', color: '#7f8c8d' }}>{item.count} книг</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      <button className="btn" onClick={loadStatistics} style={{ marginTop: '2rem' }}>
        {i18n.t('refreshStats')}
      </button>
    </div>
  )
}

export default Statistics
