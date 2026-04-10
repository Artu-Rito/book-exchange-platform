import React from 'react'
import Login from '../components/Login'
import { User } from '../types'
import i18n from '../i18n'

interface HomeProps {
  user: User | null
  onLogin: (token: string) => void
}

const Home: React.FC<HomeProps> = ({ user, onLogin }) => {
  if (!user) {
    return (
      <div>
        <div className="hero">
          <h1>Книговорот</h1>
          <p>Делитесь книгами, открывайте для себя новые истории и общайтесь с читателями</p>
        </div>
        <Login onLogin={onLogin} />

        <div className="features">
          <div className="feature-card">
            <h3>📚 Каталог</h3>
            <p>Просматривайте сотни книг самых разных жанров</p>
          </div>
          <div className="feature-card">
            <h3>🔄 Простой обмен</h3>
            <p>Простая система бронирования с удобными пунктами самовывоза</p>
          </div>
          <div className="feature-card">
            <h3>📊 Отслеживание прочитанного</h3>
            <p>Следите за своими привычками к чтению и историей обмена</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div>
      <div className="hero">
        <h1>С возвращением, {user.full_name}!</h1>
        <p>Готовы открыть для себя свою следующую любимую книгу?</p>
      </div>

      <div className="features">
        <div className="feature-card">
          <h3>Добавьте свои книги</h3>
          <p>Делитесь книгами из своей коллекции с сообществом</p>
          <a href="/books" className="btn" style={{ marginTop: '1rem' }}>Мои книги</a>
        </div>
        <div className="feature-card">
          <h3>Изучите каталог</h3>
          <p>Откройте для себя книги, доступные для обмена</p>
          <a href="/books" className="btn" style={{ marginTop: '1rem' }}>За книгами</a>
        </div>
        <div className="feature-card">
          <h3>Управление бронью</h3>
          <p>Отслеживайте свои текущие и прошлые обмены книгами</p>
          <a href="/reservations" className="btn" style={{ marginTop: '1rem' }}>Мои обмены</a>
        </div>
      </div>
    </div>
  )
}

export default Home
