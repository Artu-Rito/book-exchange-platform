import React, { useState, useEffect } from 'react'
import { Book } from '../types'
import i18n from '../i18n'

interface BookFormProps {
  onSubmit: (bookData: { title: string; author: string; genre: string; year: number; description?: string }) => void
  onCancel?: () => void
  loading: boolean
}

const BookForm: React.FC<BookFormProps> = ({ onSubmit, onCancel, loading }) => {
  const [formData, setFormData] = useState({
    title: '',
    author: '',
    genre: 'Fiction',
    year: new Date().getFullYear(),
    description: ''
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit(formData)
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const genres = [
    'Fiction', 'Mystery', 'SciFi', 'Fantasy', 'Romance', 'Horror',
    'Thriller', 'Historical', 'Biography', 'Autobiography',
    'SelfHelp', 'Science', 'Philosophy', 'Travel', 'Cooking',
    'Poetry', 'Drama', 'Classic', 'NonFiction', 'Other'
  ]

  return (
    <div className="form">
      <h2>{i18n.t('add')}</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>{i18n.t('title')}:</label>
          <input
            type="text"
            name="title"
            value={formData.title}
            onChange={handleChange}
            required
            placeholder={i18n.t('enterBookTitle')}
            disabled={loading}
          />
        </div>
        <div className="form-group">
          <label>{i18n.t('author')}:</label>
          <input
            type="text"
            name="author"
            value={formData.author}
            onChange={handleChange}
            required
            placeholder={i18n.t('enterAuthorName')}
            disabled={loading}
          />
        </div>
        <div className="form-group">
          <label>{i18n.t('genre')}:</label>
          <select
            name="genre"
            value={formData.genre}
            onChange={handleChange}
            required
            disabled={loading}
            style={{ width: '100%', padding: '0.5rem', border: '1px solid #ddd', borderRadius: '4px', fontSize: '1rem' }}
          >
            <option value="">{i18n.t('selectGenre')}</option>
            {genres.map(genre => (
              <option key={genre} value={genre}>{i18n.t(`genre${genre}`)}</option>
            ))}
          </select>
        </div>
        <div className="form-group">
          <label>{i18n.t('year')}:</label>
          <input
            type="number"
            name="year"
            value={formData.year}
            onChange={handleChange}
            required
            min="1000"
            max={new Date().getFullYear()}
            placeholder={i18n.t('enterYear')}
            disabled={loading}
          />
        </div>
        <div className="form-group">
          <label>{i18n.t('description')}:</label>
          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            rows={3}
            disabled={loading}
          />
        </div>
        <div style={{ display: 'flex', gap: '1rem', marginTop: '1.5rem' }}>
          <button type="submit" className="btn" style={{ flex: 1 }} disabled={loading}>
            {loading ? i18n.t('adding') : i18n.t('add') + ' ' + i18n.t('book')}
          </button>
          {onCancel && (
            <button type="button" className="btn btn-secondary" onClick={onCancel} disabled={loading}>
              {i18n.t('cancel')}
            </button>
          )}
        </div>
      </form>
    </div>
  )
}

export default BookForm
