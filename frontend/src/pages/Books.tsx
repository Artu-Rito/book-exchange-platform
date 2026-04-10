import React, { useState, useEffect } from 'react'
import { getBooks, createReservation, getExchangePoints, createBook, getBookReviews, createReview, uploadFile } from '../api'
import BookForm from '../components/BookForm'
import BookCard from '../components/BookCard'
import { Book, ExchangePoint, Review } from '../types'
import i18n from '../i18n'

const Books: React.FC = () => {
  const [books, setBooks] = useState<Book[]>([])
  const [exchangePoints, setExchangePoints] = useState<ExchangePoint[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [showAddForm, setShowAddForm] = useState(false)
  const [bookFormLoading, setBookFormLoading] = useState(false)

  // Состояния для поиска и фильтрации
  const [searchTerm, setSearchTerm] = useState('')
  const [filterGenre, setFilterGenre] = useState('')
  const [filterStatus, setFilterStatus] = useState('')
  const [filterYear, setFilterYear] = useState('')

  // Состояния для отзывов
  const [bookReviews, setBookReviews] = useState<{ [key: number]: Review[] }>({})
  const [showReviewForm, setShowReviewForm] = useState<{ [key: number]: boolean }>({})
  const [reviewFormData, setReviewFormData] = useState<{ [key: number]: { rating: string; comment: string } }>({})
  const [reviewLoading, setReviewLoading] = useState<{ [key: number]: boolean }>({})

  useEffect(() => {
    loadAllData()
  }, [])

  const loadAllData = async () => {
    setLoading(true)
    setError('')
    try {
      const [booksResponse, pointsResponse] = await Promise.all([
        getBooks({ page: 1, page_size: 100 }),
        getExchangePoints()
      ])
      setBooks(booksResponse.data.items || [])
      setExchangePoints(pointsResponse.data)
    } catch (err: any) {
      console.error('Ошибка при загрузке данных:', err)
      setError(i18n.t('failedToLoadData'))
    } finally {
      setLoading(false)
    }
  }

  const loadBooks = async () => {
    try {
      const response = await getBooks({ page: 1, page_size: 100 })
      setBooks(response.data.items || [])
    } catch (err: any) {
      console.error('Не получилось загрузить книги:', err)
    }
  }

  const handleReserveBook = async (bookId: number, pickupPointId?: number) => {
    if (exchangePoints.length === 0) {
      setError(i18n.t('noAvailablePoints'))
      return
    }

    try {
      const reservationData = {
        book_id: bookId,
        exchange_point_id: pickupPointId || exchangePoints[0].id
      }
      await createReservation(reservationData)
      await loadBooks()
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || i18n.t('failedToReserve')
      throw new Error(errorMessage)
    }
  }

  const handleAddBook = async (bookData: { title: string; author: string; genre: string; year: number; description?: string }) => {
    setBookFormLoading(true)
    setError('')
    try {
      await createBook(bookData)
      setShowAddForm(false)
      await loadBooks()
      alert(i18n.t('bookAdded'))
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || i18n.t('failedToAddBook')
      setError(errorMessage)
    } finally {
      setBookFormLoading(false)
    }
  }

  const loadBookReviews = async (bookId: number) => {
    try {
      const response = await getBookReviews(bookId)
      setBookReviews(prev => ({
        ...prev,
        [bookId]: response.data
      }))
    } catch (err: any) {
      console.error('Не удалось загрузить отзывы:', err)
    }
  }

  const toggleReviewForm = (bookId: number) => {
    setShowReviewForm(prev => ({
      ...prev,
      [bookId]: !prev[bookId]
    }))

    if (!showReviewForm[bookId]) {
      loadBookReviews(bookId)
    }
  }

  const handleAddReview = async (bookId: number) => {
    const rating = reviewFormData[bookId]?.rating
    const comment = reviewFormData[bookId]?.comment

    if (!rating) {
      setError(i18n.t('pleaseRate'))
      return
    }

    setReviewLoading(prev => ({ ...prev, [bookId]: true }))
    setError('')

    try {
      await createReview({
        book_id: bookId,
        rating: parseInt(rating),
        comment: comment || ''
      })

      await loadBooks()
      await loadBookReviews(bookId)

      setReviewFormData(prev => ({
        ...prev,
        [bookId]: { rating: '', comment: '' }
      }))

      alert(i18n.t('reviewAdded'))
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || i18n.t('failedToAddReview')
      setError(errorMessage)
    } finally {
      setReviewLoading(prev => ({ ...prev, [bookId]: false }))
    }
  }

  const handleReviewChange = (bookId: number, field: 'rating' | 'comment', value: string) => {
    setReviewFormData(prev => ({
      ...prev,
      [bookId]: {
        ...prev[bookId],
        [field]: value
      }
    }))
  }

  // Фильтрация книг
  const filteredBooks = books.filter(book => {
    const matchesSearch = book.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          book.author.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesGenre = filterGenre ? book.genre === filterGenre : true
    const matchesStatus = filterStatus ? book.status === filterStatus : true
    const matchesYear = filterYear ? book.year.toString() === filterYear : true

    return matchesSearch && matchesGenre && matchesStatus && matchesYear
  })

  const genres = [...new Set(books.map(book => book.genre))]

  if (loading) {
    return (
      <div className="loading">
        <div>{i18n.t('loadingData')}</div>
        <div className="loading-spinner"></div>
      </div>
    )
  }

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h1>{i18n.t('books')}</h1>
        <button
          className="btn"
          onClick={() => setShowAddForm(true)}
          disabled={bookFormLoading}
        >
          {bookFormLoading ? i18n.t('loading') : i18n.t('addBook')}
        </button>
      </div>

      {error && (
        <div className="error-message">
          <strong>{i18n.t('error')}:</strong> {error}
        </div>
      )}

      {showAddForm && (
        <BookForm
          onSubmit={handleAddBook}
          onCancel={() => setShowAddForm(false)}
          loading={bookFormLoading}
        />
      )}

      {/* Панель поиска и фильтров */}
      <div style={{
        marginBottom: '2rem',
        padding: '1rem',
        background: '#f8f9fa',
        borderRadius: '8px',
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '1rem'
      }}>
        <div>
          <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>{i18n.t('search')}:</label>
          <input
            type="text"
            placeholder={i18n.t('searchPlaceholder')}
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            style={{
              width: '100%',
              padding: '0.5rem',
              border: '1px solid #ddd',
              borderRadius: '4px'
            }}
          />
        </div>

        <div>
          <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>{i18n.t('genre')}:</label>
          <select
            value={filterGenre}
            onChange={(e) => setFilterGenre(e.target.value)}
            style={{
              width: '100%',
              padding: '0.5rem',
              border: '1px solid #ddd',
              borderRadius: '4px'
            }}
          >
            <option value="">{i18n.t('allGenres')}</option>
            {genres.map(genre => (
              <option key={genre} value={genre}>{i18n.t(`genre${genre}`)}</option>
            ))}
          </select>
        </div>

        <div>
          <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>{i18n.t('status')}:</label>
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            style={{
              width: '100%',
              padding: '0.5rem',
              border: '1px solid #ddd',
              borderRadius: '4px'
            }}
          >
            <option value="">{i18n.t('allStatuses')}</option>
            <option value="available">{i18n.t('available')}</option>
            <option value="reserved">{i18n.t('reserved')}</option>
          </select>
        </div>

        <div>
          <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>{i18n.t('year')}:</label>
          <input
            type="number"
            placeholder={i18n.t('yearPlaceholder')}
            value={filterYear}
            onChange={(e) => setFilterYear(e.target.value)}
            style={{
              width: '100%',
              padding: '0.5rem',
              border: '1px solid #ddd',
              borderRadius: '4px'
            }}
            min="1000"
            max={new Date().getFullYear()}
          />
        </div>
      </div>

      <div style={{ marginBottom: '1rem', display: 'flex', gap: '2rem', alignItems: 'center' }}>
        <p><strong>{i18n.t('totalBooks')}:</strong> {books.length}</p>
        <p><strong>{i18n.t('availableForExchange')}:</strong> {books.filter(book => book.status === 'available').length}</p>
        <p><strong>{i18n.t('filteredBooks')}:</strong> {filteredBooks.length}</p>
      </div>

      <div className="book-list">
        {filteredBooks.map(book => (
          <BookCard
            key={book.id}
            book={book}
            exchangePoints={exchangePoints}
            onReserveBook={handleReserveBook}
            onReviewsToggle={toggleReviewForm}
            showReviews={showReviewForm}
            bookReviews={bookReviews}
            reviewFormData={reviewFormData}
            reviewLoading={reviewLoading}
            setReviewFormData={setReviewFormData}
            setReviewLoading={setReviewLoading}
            setError={setError}
            loadBooks={loadBooks}
            loadBookReviews={loadBookReviews}
            onAddReview={handleAddReview}
            onReviewChange={handleReviewChange}
          />
        ))}
      </div>

      {filteredBooks.length === 0 && !showAddForm && (
        <div style={{ textAlign: 'center', padding: '3rem', background: 'white', borderRadius: '8px' }}>
          <h3>{i18n.t('noBooksMatchFilters')}</h3>
          <p>{i18n.t('tryChangingSearch')}</p>
          <button
            className="btn"
            onClick={() => {
              setSearchTerm('')
              setFilterGenre('')
              setFilterStatus('')
              setFilterYear('')
            }}
            style={{ marginTop: '1rem' }}
          >
            {i18n.t('clearFilters')}
          </button>
        </div>
      )}
    </div>
  )
}

export default Books
