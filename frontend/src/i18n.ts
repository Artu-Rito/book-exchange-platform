// i18n.ts - Система локализации

export type Language = 'ru' | 'en';

export interface Translation {
  [key: string]: string;
}

export interface Translations {
  ru: Translation;
  en: Translation;
}

const translations: Translations = {
  ru: {
    // Общие
    main: 'Главная',
    books: 'Книги',
    reservations: 'Мои брони',
    calendar: 'Календарь',
    statistics: 'Статистика',
    profile: 'Профиль',
    login: 'Войти',
    logout: 'Выйти',
    addBook: '➕ Добавить книгу',
    reserveBook: '📚 Забронировать',
    showReviews: 'Показать отзывы',
    hideReviews: 'Скрыть отзывы',
    noReviews: 'Пока нет отзывов',
    clearFilters: 'Сбросить фильтры',
    search: 'Поиск',
    genre: 'Жанр',
    status: 'Статус',
    year: 'Год',
    allGenres: 'Все жанры',
    allStatuses: 'Все статусы',
    available: 'Доступна',
    reserved: 'Забронирована',
    loading: 'Загрузка...',
    loadingData: 'Загрузка данных...',
    error: 'Ошибка',

    // Книги
    title: 'Название',
    author: 'Автор',
    rating: 'Рейтинг',
    filteredBooks: 'Отфильтровано книг',
    noBooksMatchFilters: 'Нет книг по заданным фильтрам',
    tryChangingSearch: 'Попробуйте изменить параметры поиска',
    totalBooks: 'Всего книг',
    availableForExchange: 'Доступно для обмена',

    // Резервации
    myReservations: 'Мои резервации',
    noReservations: 'Нет резерваций',
    browseBooks: 'Просмотреть книги',
    reservationDetails: 'Детали резервации',
    reservedOn: 'Забронировано',
    pickupBy: 'Получить до',
    returnBy: 'Вернуть до',
    pickupPoint: 'Место получения',
    readyForPickup: 'Готово к выдаче! Пожалуйста, заберите книгу в указанном месте.',
    startByBrowsing: 'Начните с просмотра каталога и забронируйте свою первую книгу!',

    // Отзывы
    leaveReview: 'Оставить отзыв',
    comment: 'Комментарий',
    chooseRating: 'Выберите оценку',
    addReview: 'Добавить отзыв',
    reviews: 'Отзывы',
    pleaseRate: 'Пожалуйста, поставьте оценку',
    reviewAdded: '✅ Отзыв добавлен!',
    bookReserved: '✅ Книга забронирована! Заберите её в течение 2 дней.',
    bookAdded: '✅ Книга добавлена!',

    // Профиль
    myProfile: 'Мой профиль',
    booksAdded: 'Книг добавлено',
    booksReserved: 'Книг забронировано',
    onPlatformSince: 'На платформе с',
    active: 'Активен',
    myActivity: 'Моя активность',
    accountStats: 'Статистика аккаунта',
    accountInfo: 'Информация об аккаунте',

    // Статистика
    platformStatistics: 'Статистика платформы',
    totalReservations: 'Всего резерваций',
    activeReservations: 'Активных резерваций',
    myBooks: 'Мои книги',
    booksByGenre: 'Книги по жанрам',
    topRatedBooks: 'Топ рейтинговых книг',
    booksByYear: 'Книги по годам',
    detailedStats: 'Детальная статистика',
    refreshStats: 'Обновить статистику',

    // Календарь
    previousMonth: 'Пред.',
    nextMonth: 'След.',
    today: 'Сегодня',
    pickups: '📦 Получения',
    returns: '📚 Возвраты',
    newReservations: '✅ Новые',
    legend: 'Легенда',
    upcomingEvents: 'Ближайшие события',

    // Формы
    fullName: 'ФИО',
    email: 'Почта',
    password: 'Пароль',
    phone: 'Телефон',
    loginOrRegister: 'Вход или Регистрация',
    register: 'Регистрация',
    noAccount: 'Нет аккаунта? ',
    haveAccount: 'Уже есть аккаунт? ',
    submit: 'Отправить',
    edit: 'Редактировать',
    add: 'Добавить',
    update: 'Обновить',
    updating: 'Обновление...',
    adding: 'Добавление...',
    cancel: 'Отмена',
    confirmReservation: 'Подтвердить',
    selectPickupPoint: 'Выберите пункт выдачи',
    pleaseSelectPickupPoint: 'Выберите пункт выдачи',
    enterBookTitle: 'Введите название книги',
    enterAuthorName: 'Введите имя автора',
    enterExampleGenre: 'Например, Фантастика, Наука',
    enterYear: 'Год издания',
    selectGenre: 'Выберите жанр',
    yearPlaceholder: 'Год',
    searchPlaceholder: 'Название или автор',

    // Жанры
    genreFiction: 'Художественная',
    genreMystery: 'Детектив',
    genreSciFi: 'Научная фантастика',
    genreFantasy: 'Фэнтези',
    genreRomance: 'Роман',
    genreHorror: 'Ужасы',
    genreThriller: 'Триллер',
    genreHistorical: 'Историческая',
    genreBiography: 'Биография',
    genreAutobiography: 'Автобиография',
    genreSelfHelp: 'Саморазвитие',
    genreScience: 'Наука',
    genrePhilosophy: 'Философия',
    genreTravel: 'Путешествия',
    genreCooking: 'Кулинария',
    genrePoetry: 'Поэзия',
    genreDrama: 'Драма',
    genreClassic: 'Классика',
    genreNonFiction: 'Научпоп',
    genreOther: 'Другое',

    // Статусы
    statusReserved: 'Забронирована',
    statusPickedUp: 'Получена',
    statusReturned: 'Возвращена',
    statusAvailable: 'Доступна',

    // Дни недели
    monday: 'Пн',
    tuesday: 'Вт',
    wednesday: 'Ср',
    thursday: 'Чт',
    friday: 'Пт',
    saturday: 'Сб',
    sunday: 'Вс',

    // Ошибки
    failedToLoadData: 'Не удалось загрузить данные',
    failedToLoadStats: 'Не удалось загрузить статистику',
    failedToLoadReviews: 'Не удалось загрузить отзывы',
    failedToReserve: 'Не удалось забронировать книгу',
    failedToAddReview: 'Не удалось добавить отзыв',
    failedToAddBook: 'Не удалось добавить книгу',
    noAvailablePoints: 'Нет доступных пунктов обмена',
  },
  en: {
    // Common
    main: 'Main',
    books: 'Books',
    reservations: 'My Reservations',
    calendar: 'Calendar',
    statistics: 'Statistics',
    profile: 'Profile',
    login: 'Log In',
    logout: 'Log Out',
    addBook: '➕ Add Book',
    reserveBook: '📚 Reserve',
    showReviews: 'Show Reviews',
    hideReviews: 'Hide Reviews',
    noReviews: 'No reviews yet',
    clearFilters: 'Clear Filters',
    search: 'Search',
    genre: 'Genre',
    status: 'Status',
    year: 'Year',
    allGenres: 'All genres',
    allStatuses: 'All statuses',
    available: 'Available',
    reserved: 'Reserved',
    loading: 'Loading...',
    loadingData: 'Loading data...',
    error: 'Error',

    // Books
    title: 'Title',
    author: 'Author',
    rating: 'Rating',
    filteredBooks: 'Filtered books',
    noBooksMatchFilters: 'No books match your filters',
    tryChangingSearch: 'Try changing your search criteria',
    totalBooks: 'Total books',
    availableForExchange: 'Available for exchange',

    // Reservations
    myReservations: 'My Reservations',
    noReservations: 'No reservations yet',
    browseBooks: 'Browse Books',
    reservationDetails: 'Reservation Details',
    reservedOn: 'Reserved on',
    pickupBy: 'Pickup by',
    returnBy: 'Return by',
    pickupPoint: 'Pickup point',
    readyForPickup: 'Ready for pickup! Please collect your book.',
    startByBrowsing: 'Start by browsing the catalog and reserve your first book!',

    // Reviews
    leaveReview: 'Leave a review',
    comment: 'Comment',
    chooseRating: 'Choose rating',
    addReview: 'Add Review',
    reviews: 'Reviews',
    pleaseRate: 'Please provide a rating',
    reviewAdded: '✅ Review added!',
    bookReserved: '✅ Book reserved! Pick it up within 2 days.',
    bookAdded: '✅ Book added!',

    // Profile
    myProfile: 'My Profile',
    booksAdded: 'Books added',
    booksReserved: 'Books reserved',
    onPlatformSince: 'On platform since',
    active: 'Active',
    myActivity: 'My Activity',
    accountStats: 'Account Statistics',
    accountInfo: 'Account Information',

    // Statistics
    platformStatistics: 'Platform Statistics',
    totalReservations: 'Total Reservations',
    activeReservations: 'Active Reservations',
    myBooks: 'My Books',
    booksByGenre: 'Books by Genre',
    topRatedBooks: 'Top Rated Books',
    booksByYear: 'Books by Year',
    detailedStats: 'Detailed Statistics',
    refreshStats: 'Refresh Statistics',

    // Calendar
    previousMonth: 'Prev',
    nextMonth: 'Next',
    today: 'Today',
    pickups: '📦 Pickups',
    returns: '📚 Returns',
    newReservations: '✅ New',
    legend: 'Legend',
    upcomingEvents: 'Upcoming Events',

    // Forms
    fullName: 'Full Name',
    email: 'Email',
    password: 'Password',
    phone: 'Phone',
    loginOrRegister: 'Login or Register',
    register: 'Register',
    noAccount: 'No account? ',
    haveAccount: 'Already have an account? ',
    submit: 'Submit',
    edit: 'Edit',
    add: 'Add',
    update: 'Update',
    updating: 'Updating...',
    adding: 'Adding...',
    cancel: 'Cancel',
    confirmReservation: 'Confirm',
    selectPickupPoint: 'Select pickup point',
    pleaseSelectPickupPoint: 'Please select a pickup point',
    enterBookTitle: 'Enter book title',
    enterAuthorName: 'Enter author name',
    enterExampleGenre: 'e.g., Fiction, Science',
    enterYear: 'Publication year',
    selectGenre: 'Select genre',
    yearPlaceholder: 'Year',
    searchPlaceholder: 'Title or author',

    // Genres
    genreFiction: 'Fiction',
    genreMystery: 'Mystery',
    genreSciFi: 'Science Fiction',
    genreFantasy: 'Fantasy',
    genreRomance: 'Romance',
    genreHorror: 'Horror',
    genreThriller: 'Thriller',
    genreHistorical: 'Historical',
    genreBiography: 'Biography',
    genreAutobiography: 'Autobiography',
    genreSelfHelp: 'Self-Help',
    genreScience: 'Science',
    genrePhilosophy: 'Philosophy',
    genreTravel: 'Travel',
    genreCooking: 'Cooking',
    genrePoetry: 'Poetry',
    genreDrama: 'Drama',
    genreClassic: 'Classic',
    genreNonFiction: 'Non-Fiction',
    genreOther: 'Other',

    // Statuses
    statusReserved: 'Reserved',
    statusPickedUp: 'Picked Up',
    statusReturned: 'Returned',
    statusAvailable: 'Available',

    // Days
    monday: 'Mo',
    tuesday: 'Tu',
    wednesday: 'We',
    thursday: 'Th',
    friday: 'Fr',
    saturday: 'Sa',
    sunday: 'Su',

    // Errors
    failedToLoadData: 'Failed to load data',
    failedToLoadStats: 'Failed to load statistics',
    failedToLoadReviews: 'Failed to load reviews',
    failedToReserve: 'Failed to reserve book',
    failedToAddReview: 'Failed to add review',
    failedToAddBook: 'Failed to add book',
    noAvailablePoints: 'No available exchange points',
  },
};

class I18n {
  private currentLanguage: Language;

  constructor() {
    const saved = localStorage.getItem('language') as Language;
    this.currentLanguage = saved && translations[saved] ? saved : 'ru';
  }

  t(key: string): string {
    return translations[this.currentLanguage]?.[key] || key;
  }

  setLanguage(language: Language): void {
    if (translations[language]) {
      this.currentLanguage = language;
      localStorage.setItem('language', language);
      window.location.reload();
    }
  }

  getLanguage(): Language {
    return this.currentLanguage;
  }

  getAvailableLanguages(): Language[] {
    return Object.keys(translations) as Language[];
  }
}

const i18n = new I18n();
export default i18n;
