import React from 'react'
import { Link } from 'react-router-dom'
import { User } from '../types'
import i18n from '../i18n'

interface NavbarProps {
  user: User | null
  onLogout: () => void
}

const Navbar: React.FC<NavbarProps> = ({ user, onLogout }) => {
  const changeLanguage = (language: 'ru' | 'en') => {
    i18n.setLanguage(language)
  }

  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <Link to="/">📚 Книговорот</Link>
      </div>
      <ul className="navbar-nav">
        <li><Link to="/">{i18n.t('main')}</Link></li>
        {user ? (
          <>
            <li><Link to="/books">{i18n.t('books')}</Link></li>
            <li><Link to="/reservations">{i18n.t('reservations')}</Link></li>
            <li><Link to="/calendar">{i18n.t('calendar')}</Link></li>
            <li><Link to="/statistics">{i18n.t('statistics')}</Link></li>
            <li><Link to="/profile">{i18n.t('profile')} ({user.full_name})</Link></li>
            <li>
              <button onClick={onLogout}>{i18n.t('logout')}</button>
            </li>
          </>
        ) : (
          <li><Link to="/">{i18n.t('login')}</Link></li>
        )}
        <li>
          <select
            value={i18n.getLanguage()}
            onChange={(e) => changeLanguage(e.target.value as 'ru' | 'en')}
            style={{
              background: 'none',
              border: '1px solid white',
              color: 'white',
              padding: '0.5rem',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            <option value="ru">RU</option>
            <option value="en">EN</option>
          </select>
        </li>
      </ul>
    </nav>
  )
}

export default Navbar
