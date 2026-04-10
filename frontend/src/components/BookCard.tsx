import React, { useState, useEffect } from 'react'
import { Book, ExchangePoint, Review } from '../types'
import i18n from '../i18n'

interface BookCardProps {
  book: Book
  exchangePoints: ExchangePoint[]
  onReserveBook: (bookId: number, pickupPointId?: number) => void
  onReviewsToggle: (bookId: number) => void
  showReviews: { [key: number]: boolean }
  bookReviews: { [key: number]: Review[] }
  reviewFormData: { [key: number]: { rating: string; comment: string } }
  reviewLoading: { [key: number]: boolean }
  setReviewFormData: React.Dispatch<React.SetStateAction<{ [key: number]: { rating: string; comment: string } }>>
  setReviewLoading: React.Dispatch<React.SetStateAction<{ [key: number]: boolean }>>
  setError: (error: string) => void
  loadBooks: () => void
  loadBookReviews: (bookId: number) => void
  onAddReview: (bookId: number) => void
  onReviewChange: (bookId: number, field: 'rating' | 'comment', value: string) => void
}

const BookCard: React.FC<BookCardProps> = ({
  book,
  exchangePoints,
  onReserveBook,
  onReviewsToggle,
  showReviews,
  bookReviews,
  reviewFormData,
  reviewLoading,
  setReviewFormData,
  setReviewLoading,
  setError,
  loadBooks,
  loadBookReviews,
  onAddReview,
  onReviewChange,
}) => {
  const [reservingBookId, setReservingBookId] = useState<number | null>(null)
  const [showPickupModal, setShowPickupModal] = useState(false)
  const [selectedPickupPoint, setSelectedPickupPoint] = useState<number | null>(null)

  const handleReserveBook = async () => {
    if (exchangePoints.length === 0) {
      setError(i18n.t('noAvailablePoints'))
      return
    }

    // Открываем модальное окно выбора пункта выдачи
    setShowPickupModal(true)
    setSelectedPickupPoint(exchangePoints[0]?.id || null)
  }

  const confirmReservation = async () => {
    if (!selectedPickupPoint) {
      setError(i18n.t('pleaseSelectPickupPoint'))
      return
    }

    setReservingBookId(book.id)
    setError('')

    try {
      const reservationData = {
        book_id: book.id,
        exchange_point_id: selectedPickupPoint
      }
      await onReserveBook(book.id, selectedPickupPoint)
      setShowPickupModal(false)
      alert(i18n.t('bookReserved'))
    } catch (err: any) {
      console.error('Ошибка при бронировании:', err)
      setError(err.response?.data?.detail || i18n.t('failedToReserve'))
    } finally {
      setReservingBookId(null)
    }
  }

  const handleAddReview = () => {
    onAddReview(book.id)
  }

  const handleReviewChange = (field: 'rating' | 'comment', value: string) => {
    onReviewChange(book.id, field, value)
  }

  return (
    <div className="book-card" style={{
      display: 'flex',
      flexDirection: 'column',
      height: '100%',
      background: 'white',
      borderRadius: '12px',
      boxShadow: '0 4px 12px rgba(0,0,0,0.08)',
      transition: 'transform 0.2s, box-shadow 0.2s',
      overflow: 'hidden',
      border: '1px solid #e8e8e8'
    }}>
      {/* Header с цветом по статусу */}
      <div style={{
        padding: '1rem',
        background: book.status === 'available' 
          ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
          : book.status === 'reserved'
          ? 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'
          : 'linear-gradient(135deg, #d7d2cc 0%, #304352 100%)',
        color: 'white',
        minHeight: '80px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between'
      }}>
        <h3 style={{ margin: 0, fontSize: '1.1rem', flex: 1 }}>{book.title}</h3>
        <span style={{
          padding: '0.25rem 0.75rem',
          borderRadius: '12px',
          background: 'rgba(255,255,255,0.2)',
          fontSize: '0.75rem',
          fontWeight: 'bold',
          marginLeft: '0.5rem'
        }}>
          {i18n.t(`status${book.status.charAt(0).toUpperCase() + book.status.slice(1)}`)}
        </span>
      </div>

      {/* Контент */}
      <div style={{ padding: '1rem', flex: 1 }}>
        <p style={{ margin: '0 0 0.75rem 0', color: '#2c3e50', fontWeight: '500' }}>
          👤 {book.author}
        </p>
        
        <div style={{ 
          display: 'flex', 
          flexDirection: 'column', 
          gap: '0.5rem',
          marginBottom: '1rem',
          fontSize: '0.875rem',
          color: '#555'
        }}>
          <p style={{ margin: 0 }}>
            <strong>{i18n.t('genre')}:</strong> {i18n.t(`genre${book.genre}`) || book.genre}
          </p>
          <p style={{ margin: 0 }}>
            <strong>{i18n.t('year')}:</strong> {book.year}
          </p>
          <p style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <strong>{i18n.t('rating')}:</strong>
            <span style={{ color: '#f39c12', fontWeight: 'bold' }}>
              {'★'.repeat(Math.round(book.average_rating || 0))}
              {'☆'.repeat(5 - Math.round(book.average_rating || 0))}
            </span>
            <span style={{ color: '#7f8c8d', fontSize: '0.8rem' }}>
              ({(book.average_rating || 0).toFixed(1)})
            </span>
          </p>
        </div>

        {book.description && (
          <p style={{
            fontSize: '0.875rem',
            color: '#666',
            lineHeight: '1.5',
            marginBottom: '1rem',
            display: '-webkit-box',
            WebkitLineClamp: 3,
            WebkitBoxOrient: 'vertical',
            overflow: 'hidden'
          }}>
            {book.description}
          </p>
        )}
      </div>

      {/* Actions */}
      {book.status === 'available' && (
        <div className="book-actions" style={{
          padding: '1rem',
          borderTop: '1px solid #eee',
          display: 'flex',
          flexDirection: 'column',
          gap: '0.5rem'
        }}>
          <button
            className="btn"
            onClick={handleReserveBook}
            disabled={reservingBookId === book.id}
            style={{
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              border: 'none',
              padding: '0.75rem 1rem',
              fontWeight: 'bold'
            }}
          >
            {reservingBookId === book.id ? i18n.t('loading') : i18n.t('reserveBook')}
          </button>
          <button
            className="btn btn-secondary"
            onClick={() => onReviewsToggle(book.id)}
            style={{
              background: 'transparent',
              border: '1px solid #ddd',
              padding: '0.75rem 1rem'
            }}
          >
            {showReviews[book.id] ? i18n.t('hideReviews') : i18n.t('showReviews')}
            {bookReviews[book.id]?.length > 0 && (
              <span style={{ marginLeft: '0.5rem', background: '#667eea', color: 'white', padding: '0.125rem 0.5rem', borderRadius: '10px', fontSize: '0.75rem' }}>
                {bookReviews[book.id].length}
              </span>
            )}
          </button>
        </div>
      )}

      {book.status === 'reserved' && (
        <div style={{
          background: '#fff3cd',
          padding: '1rem',
          borderTop: '1px solid #ffeaa7',
          textAlign: 'center'
        }}>
          <p style={{ margin: 0, color: '#856404', fontWeight: 'bold', fontSize: '0.875rem' }}>
            ⚠️ {i18n.t('statusReserved')}
          </p>
        </div>
      )}

      {/* Отзывы */}
      {showReviews[book.id] && (
        <div style={{
          padding: '1rem',
          background: '#f8f9fa',
          borderTop: '1px solid #eee'
        }}>
          <div style={{ marginBottom: '1rem' }}>
            <h4 style={{ margin: '0 0 0.75rem 0', fontSize: '0.95rem' }}>{i18n.t('leaveReview')}</h4>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
              <label style={{ fontSize: '0.875rem' }}>{i18n.t('rating')}:</label>
              <select
                value={reviewFormData[book.id]?.rating || ''}
                onChange={(e) => handleReviewChange('rating', e.target.value)}
                style={{
                  padding: '0.5rem',
                  border: '1px solid #ddd',
                  borderRadius: '6px',
                  fontSize: '0.875rem'
                }}
              >
                <option value="">{i18n.t('chooseRating')}</option>
                {[1, 2, 3, 4, 5].map(rating => (
                  <option key={rating} value={rating}>{rating} ★</option>
                ))}
              </select>
            </div>
            <textarea
              placeholder={i18n.t('comment')}
              value={reviewFormData[book.id]?.comment || ''}
              onChange={(e) => handleReviewChange('comment', e.target.value)}
              style={{
                width: '100%',
                height: '80px',
                padding: '0.5rem',
                border: '1px solid #ddd',
                borderRadius: '6px',
                marginBottom: '0.5rem',
                fontSize: '0.875rem',
                resize: 'vertical'
              }}
            />
            <button
              className="btn"
              onClick={handleAddReview}
              disabled={reviewLoading[book.id]}
              style={{
                width: '100%',
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                border: 'none'
              }}
            >
              {reviewLoading[book.id] ? i18n.t('loading') : i18n.t('addReview')}
            </button>
          </div>

          {bookReviews[book.id] && bookReviews[book.id].length > 0 ? (
            <div>
              <h4 style={{ margin: '0 0 0.75rem 0', fontSize: '0.95rem' }}>
                {i18n.t('reviews')} ({bookReviews[book.id].length})
              </h4>
              {bookReviews[book.id].map(review => (
                <div key={review.id} style={{
                  background: 'white',
                  padding: '0.75rem',
                  borderRadius: '8px',
                  marginBottom: '0.5rem',
                  boxShadow: '0 1px 3px rgba(0,0,0,0.08)'
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
                    <span style={{ color: '#f39c12', fontWeight: 'bold', fontSize: '0.875rem' }}>
                      {'★'.repeat(review.rating)}{'☆'.repeat(5 - review.rating)}
                    </span>
                  </div>
                  {review.comment && (
                    <p style={{ margin: '0.25rem 0', fontSize: '0.875rem', color: '#333' }}>{review.comment}</p>
                  )}
                  <p style={{ margin: '0.25rem 0 0 0', fontSize: '0.75rem', color: '#95a5a6' }}>
                    {new Date(review.created_at).toLocaleDateString(i18n.getLanguage() === 'ru' ? 'ru-RU' : 'en-US')}
                  </p>
                </div>
              ))}
            </div>
          ) : (
            <p style={{ color: '#7f8c8d', fontStyle: 'italic', textAlign: 'center', padding: '0.5rem', fontSize: '0.875rem' }}>
              {i18n.t('noReviews')}
            </p>
          )}
        </div>
      )}

      {/* Модальное окно выбора пункта выдачи */}
      {showPickupModal && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(0,0,0,0.5)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000
        }}>
          <div style={{
            background: 'white',
            padding: '2rem',
            borderRadius: '12px',
            maxWidth: '500px',
            width: '90%',
            maxHeight: '80vh',
            overflow: 'auto'
          }}>
            <h3 style={{ marginTop: 0 }}>{i18n.t('selectPickupPoint')}</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', marginBottom: '1.5rem' }}>
              {exchangePoints.map(point => (
                <label
                  key={point.id}
                  style={{
                    display: 'flex',
                    alignItems: 'flex-start',
                    padding: '1rem',
                    border: `2px solid ${selectedPickupPoint === point.id ? '#667eea' : '#ddd'}`,
                    borderRadius: '8px',
                    cursor: 'pointer',
                    transition: 'border-color 0.2s'
                  }}
                >
                  <input
                    type="radio"
                    name="pickupPoint"
                    value={point.id}
                    checked={selectedPickupPoint === point.id}
                    onChange={() => setSelectedPickupPoint(point.id)}
                    style={{ marginRight: '0.75rem', marginTop: '0.25rem' }}
                  />
                  <div style={{ flex: 1 }}>
                    <div style={{ fontWeight: 'bold', marginBottom: '0.25rem' }}>{point.name}</div>
                    <div style={{ fontSize: '0.875rem', color: '#666' }}>{point.address}</div>
                    <div style={{ fontSize: '0.875rem', color: '#666' }}>🕒 {point.working_hours}</div>
                    {point.contact_person && (
                      <div style={{ fontSize: '0.875rem', color: '#666' }}>
                        👤 {point.contact_person}
                        {point.phone && <span> | 📞 {point.phone}</span>}
                      </div>
                    )}
                  </div>
                </label>
              ))}
            </div>
            <div style={{ display: 'flex', gap: '0.5rem', justifyContent: 'flex-end' }}>
              <button
                className="btn btn-secondary"
                onClick={() => setShowPickupModal(false)}
                disabled={reservingBookId === book.id}
              >
                {i18n.t('cancel')}
              </button>
              <button
                className="btn"
                onClick={confirmReservation}
                disabled={reservingBookId === book.id}
              >
                {reservingBookId === book.id ? i18n.t('loading') : i18n.t('confirmReservation')}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default BookCard
