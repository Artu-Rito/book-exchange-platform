import React, { useState, useEffect } from 'react'
import { getReservations, getBooks, getExchangePoints, cancelReservation, confirmPickup, confirmReturn } from '../api'
import { Reservation, Book, ExchangePoint } from '../types'
import i18n from '../i18n'

const Reservations: React.FC = () => {
  const [reservations, setReservations] = useState<Reservation[]>([])
  const [books, setBooks] = useState<{ [key: number]: Book }>({})
  const [exchangePoints, setExchangePoints] = useState<{ [key: number]: ExchangePoint }>({})
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [expandedCards, setExpandedCards] = useState<{ [key: number]: boolean }>({})

  useEffect(() => {
    loadAllData()
  }, [])

  const loadAllData = async () => {
    setLoading(true)
    setError('')
    try {
      const [reservationsResponse, booksResponse, pointsResponse] = await Promise.all([
        getReservations(),
        getBooks({ page: 1, page_size: 100 }),
        getExchangePoints()
      ])

      const booksMap: { [key: number]: Book } = {}
      booksResponse.data.items?.forEach((book: Book) => {
        booksMap[book.id] = book
      })

      const pointsMap: { [key: number]: ExchangePoint } = {}
      pointsResponse.data.forEach((point: ExchangePoint) => {
        pointsMap[point.id] = point
      })

      setReservations(reservationsResponse.data)
      setBooks(booksMap)
      setExchangePoints(pointsMap)
    } catch (err: any) {
      console.error('Не удалось загрузить данные:', err)
      setError(i18n.t('failedToLoadData'))
    } finally {
      setLoading(false)
    }
  }

  const toggleExpand = (id: number) => {
    setExpandedCards(prev => ({ ...prev, [id]: !prev[id] }))
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('ru-RU', {
      day: 'numeric',
      month: 'long',
      year: 'numeric'
    })
  }

  const getStatusColor = (status: string) => {
    const s = status.toUpperCase();
    switch (s) {
      case 'RESERVED': return '#e67e22'
      case 'PICKED_UP': return '#27ae60'
      case 'RETURNED': return '#95a5a6'
      case 'CANCELLED': return '#e74c3c'
      default: return '#95a5a6'
    }
  }

  const handleCancel = async (id: number) => {
    if (!window.confirm('Вы уверены, что хотите отменить бронирование?')) return

    try {
      await cancelReservation(id)
      await loadAllData()
      alert('Бронирование отменено')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Не удалось отменить бронирование')
    }
  }

  const handleConfirmPickup = async (id: number) => {
    if (!window.confirm('Подтвердите получение книги')) return

    try {
      await confirmPickup(id)
      await loadAllData()
      alert('✅ Книга получена!')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Не удалось подтвердить получение')
    }
  }

  const handleConfirmReturn = async (id: number) => {
    if (!window.confirm('Подтвердите возврат книги')) return

    try {
      await confirmReturn(id)
      await loadAllData()
      alert('✅ Книга возвращена!')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Не удалось подтвердить возврат')
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

  return (
    <div>
      <h1>{i18n.t('myReservations')}</h1>

      {error && (
        <div className="error-message">
          <strong>{i18n.t('error')}:</strong> {error}
        </div>
      )}

      {reservations.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '3rem', background: 'white', borderRadius: '8px' }}>
          <h3>{i18n.t('noReservations')}</h3>
          <p>{i18n.t('startByBrowsing')}</p>
          <a href="/books" className="btn" style={{ marginTop: '1rem' }}>{i18n.t('browseBooks')}</a>
        </div>
      ) : (
        <div className="book-list">
          {reservations.map(reservation => {
            const book = books[reservation.book_id]
            const exchangePoint = exchangePoints[reservation.exchange_point_id]
            const isExpanded = expandedCards[reservation.id]

            if (!book) return null

            return (
              <div key={reservation.id} className="reservation-card" style={{
                background: 'white',
                borderRadius: '8px',
                padding: '1.5rem',
                marginBottom: '1rem',
                boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
                border: `2px solid ${getStatusColor(reservation.status)}`
              }}>
                {/* Заголовок */}
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                  <div style={{ flex: 1 }}>
                    <h3 style={{ margin: 0, fontSize: '1.25rem' }}>{book.title}</h3>
                    <p style={{ margin: '0.25rem 0', color: '#666' }}>{book.author}</p>
                  </div>
                  <span style={{
                    padding: '0.5rem 1rem',
                    borderRadius: '20px',
                    background: getStatusColor(reservation.status),
                    color: 'white',
                    fontWeight: 'bold',
                    fontSize: '0.875rem'
                  }}>
                    {i18n.t(`status${reservation.status.charAt(0).toUpperCase() + reservation.status.slice(1)}`)}
                  </span>
                </div>

                {/* Основная информация */}
                <div style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                  gap: '1rem',
                  padding: '1rem',
                  background: '#f8f9fa',
                  borderRadius: '8px',
                  marginBottom: '1rem'
                }}>
                  <div>
                    <p style={{ margin: 0, fontSize: '0.875rem', color: '#666' }}>{i18n.t('reservedOn')}</p>
                    <p style={{ margin: 0, fontWeight: 'bold' }}>{formatDate(reservation.reservation_date)}</p>
                  </div>
                  <div>
                    <p style={{ margin: 0, fontSize: '0.875rem', color: '#666' }}>{i18n.t('pickupBy')}</p>
                    <p style={{ margin: 0, fontWeight: 'bold' }}>{formatDate(reservation.pickup_date)}</p>
                  </div>
                  <div>
                    <p style={{ margin: 0, fontSize: '0.875rem', color: '#666' }}>{i18n.t('returnBy')}</p>
                    <p style={{ margin: 0, fontWeight: 'bold' }}>{formatDate(reservation.return_date)}</p>
                  </div>
                </div>

                {/* Пункт выдачи - компактно */}
                {exchangePoint && (
                  <div style={{
                    padding: '1rem',
                    background: '#e3f2fd',
                    borderRadius: '8px',
                    marginBottom: '1rem'
                  }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                      <div>
                        <h4 style={{ margin: '0 0 0.5rem 0', color: '#1976d2', fontSize: '0.95rem' }}>📍 {exchangePoint.name}</h4>
                        <p style={{ margin: '0.25rem 0', fontSize: '0.875rem', color: '#555' }}>{exchangePoint.address}</p>
                        <p style={{ margin: '0.25rem 0', fontSize: '0.875rem', color: '#555' }}>🕒 {exchangePoint.working_hours}</p>
                        {exchangePoint.contact_person && (
                          <p style={{ margin: '0.25rem 0', fontSize: '0.875rem', color: '#555' }}>
                            👤 {exchangePoint.contact_person}
                            {exchangePoint.phone && ` | 📞 ${exchangePoint.phone}`}
                          </p>
                        )}
                      </div>
                    </div>
                  </div>
                )}

                {/* Статус и действия */}
                {reservation.status.toUpperCase() === 'RESERVED' && (
                  <>
                    <div style={{
                      padding: '0.75rem',
                      background: '#fff3cd',
                      borderRadius: '8px',
                      marginBottom: '1rem',
                      border: '1px solid #ffeaa7'
                    }}>
                      <p style={{ margin: 0, color: '#856404', fontWeight: 'bold' }}>
                        ⏳ Книга забронирована. Заберите до: {formatDate(reservation.pickup_date)}
                      </p>
                    </div>
                    <div className="book-actions" style={{ display: 'flex', gap: '0.5rem' }}>
                      <button className="btn" onClick={() => handleConfirmPickup(reservation.id)}>
                        📦 Я получил книгу
                      </button>
                      <button className="btn btn-secondary" onClick={() => handleCancel(reservation.id)}>
                        {i18n.t('cancel')}
                      </button>
                    </div>
                  </>
                )}

                {reservation.status.toUpperCase() === 'PICKED_UP' && (
                  <>
                    <div style={{
                      padding: '0.75rem',
                      background: '#d4edda',
                      borderRadius: '8px',
                      marginBottom: '1rem',
                      border: '1px solid #c3e6cb'
                    }}>
                      <p style={{ margin: 0, color: '#155724', fontWeight: 'bold' }}>
                        ✅ Книга у вас. Верните до: {formatDate(reservation.return_date)}
                      </p>
                    </div>
                    <div className="book-actions">
                      <button className="btn" onClick={() => handleConfirmReturn(reservation.id)}>
                        📚 Я вернул книгу
                      </button>
                    </div>
                  </>
                )}

                {(reservation.status.toUpperCase() === 'RETURNED' || reservation.status.toUpperCase() === 'CANCELLED') && (
                  <div style={{
                    padding: '0.75rem',
                    background: '#e9ecef',
                    borderRadius: '8px',
                    textAlign: 'center'
                  }}>
                    <p style={{ margin: 0, color: '#6c757d' }}>
                      {reservation.status.toUpperCase() === 'RETURNED' ? '✅ Возвращено' : '❌ Отменено'}
                    </p>
                  </div>
                )}
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}

export default Reservations
