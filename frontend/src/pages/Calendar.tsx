import React, { useState, useEffect } from 'react'
import { getReservations } from '../api'
import { Reservation } from '../types'
import i18n from '../i18n'

const Calendar: React.FC = () => {
  const [reservations, setReservations] = useState<Reservation[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [currentDate, setCurrentDate] = useState(new Date())

  useEffect(() => {
    loadReservations()
  }, [])

  const loadReservations = async () => {
    try {
      setLoading(true)
      const response = await getReservations()
      setReservations(response.data)
    } catch (err: any) {
      console.error('Error loading reservations:', err)
      setError(i18n.t('failedToLoadData'))
    } finally {
      setLoading(false)
    }
  }

  const getPickupReservationsForDate = (date: Date) => {
    return reservations.filter(reservation => {
      const pickupDate = new Date(reservation.pickup_date)
      return pickupDate.toDateString() === date.toDateString()
    })
  }

  const getReturnReservationsForDate = (date: Date) => {
    return reservations.filter(reservation => {
      const returnDate = new Date(reservation.return_date)
      return returnDate.toDateString() === date.toDateString()
    })
  }

  const getDaysInMonth = (year: number, month: number) => {
    return new Date(year, month + 1, 0).getDate()
  }

  const getFirstDayOfMonth = (year: number, month: number) => {
    const day = new Date(year, month, 1).getDay()
    return day === 0 ? 6 : day - 1 // Преобразуем: 0 (Вс) -> 6, 1 (Пн) -> 0, и т.д.
  }

  const renderCalendar = () => {
    const year = currentDate.getFullYear()
    const month = currentDate.getMonth()
    const daysInMonth = getDaysInMonth(year, month)
    const firstDayOfMonth = getFirstDayOfMonth(year, month)

    const days: JSX.Element[] = []

    // Пустые ячейки до начала месяца
    for (let i = 0; i < firstDayOfMonth; i++) {
      days.push(<div key={`empty-${i}`} className="calendar-day empty"></div>)
    }

    // Дни месяца
    for (let day = 1; day <= daysInMonth; day++) {
      const date = new Date(year, month, day)
      const pickupReservations = getPickupReservationsForDate(date)
      const returnReservations = getReturnReservationsForDate(date)

      const totalEvents = pickupReservations.length + returnReservations.length

      let dayClass = 'calendar-day'
      if (totalEvents > 0) dayClass += ' has-events'
      if (date.toDateString() === new Date().toDateString()) dayClass += ' today'

      days.push(
        <div key={`day-${day}`} className={dayClass}>
          <div className="day-number">{day}</div>
          <div className="day-events">
            {pickupReservations.length > 0 && (
              <div className="event pickup-event" title={i18n.t('pickups')}>
                📦 {pickupReservations.length}
              </div>
            )}
            {returnReservations.length > 0 && (
              <div className="event return-event" title={i18n.t('returns')}>
                📚 {returnReservations.length}
              </div>
            )}
          </div>
        </div>
      )
    }

    return days
  }

  const goToPreviousMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() - 1, 1))
  }

  const goToNextMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 1))
  }

  const goToToday = () => {
    setCurrentDate(new Date())
  }

  if (loading) {
    return (
      <div className="loading">
        <div>{i18n.t('loadingCalendar')}</div>
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

  const upcomingEvents = reservations
    .filter(res => {
      const today = new Date()
      const returnDate = new Date(res.return_date)
      return returnDate >= today
    })
    .sort((a, b) => new Date(a.return_date).getTime() - new Date(b.return_date).getTime())
    .slice(0, 5)

  return (
    <div>
      <h1>{i18n.t('calendar')}</h1>

      <div style={{ marginBottom: '1.5rem', textAlign: 'center' }}>
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '1rem', marginBottom: '1rem' }}>
          <button className="btn btn-secondary" onClick={goToPreviousMonth}>
            &lt; {i18n.t('previousMonth')}
          </button>
          <h2 style={{ margin: 0 }}>
            {currentDate.toLocaleDateString(i18n.getLanguage(), { month: 'long', year: 'numeric' })}
          </h2>
          <button className="btn btn-secondary" onClick={goToNextMonth}>
            {i18n.t('nextMonth')} &gt;
          </button>
        </div>
        <button className="btn" onClick={goToToday}>
          {i18n.t('today')}
        </button>
      </div>

      <div className="calendar" style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(7, 1fr)',
        gap: '1px',
        backgroundColor: '#ddd',
        borderRadius: '8px',
        overflow: 'hidden'
      }}>
        {[i18n.t('monday'), i18n.t('tuesday'), i18n.t('wednesday'), i18n.t('thursday'),
          i18n.t('friday'), i18n.t('saturday'), i18n.t('sunday')].map((day, index) => (
          <div key={index} style={{
            background: '#e9ecef',
            padding: '10px',
            textAlign: 'center',
            fontWeight: 'bold'
          }}>
            {day}
          </div>
        ))}
        {renderCalendar()}
      </div>

      <div style={{ marginTop: '1.5rem', padding: '1rem', background: '#f8f9fa', borderRadius: '8px' }}>
        <h3>{i18n.t('legend')}:</h3>
        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', marginTop: '0.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <div style={{ width: '16px', height: '16px', background: '#d4edda', border: '1px solid #c3e6cb' }}></div>
            <span>📦 {i18n.t('pickups')}</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <div style={{ width: '16px', height: '16px', background: '#f8d7da', border: '1px solid #f5c6cb' }}></div>
            <span>📚 {i18n.t('returns')}</span>
          </div>
        </div>
      </div>

      {upcomingEvents.length > 0 && (
        <div style={{ marginTop: '1.5rem' }}>
          <h3>{i18n.t('upcomingEvents')}</h3>
          {upcomingEvents.map(res => (
            <div key={res.id} style={{
              padding: '1rem',
              margin: '0.5rem 0',
              background: '#f8f9fa',
              borderRadius: '4px',
              borderLeft: '4px solid #3498db'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <strong>{new Date(res.return_date).toLocaleDateString(i18n.getLanguage())}</strong> - {i18n.t(`status${res.status.charAt(0).toUpperCase() + res.status.slice(1)}`)}
                </div>
                <div style={{ fontSize: '0.9rem', color: '#6c757d' }}>
                  {new Date(res.return_date).toLocaleDateString(i18n.getLanguage(), { weekday: 'short' })}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default Calendar
