import { FormattedMessage } from 'react-intl'
import logo from '../../../assets/images/logo.png'
import { FormLogin } from '../../forms/FormLogin'
import './styles.css'

export const CardLogin = () => {
  return (
    <div className="card-login-container">
      <div className="card-login-wrapper">
        <header className="card-login-header">
          <div className="flex items-center">
            <img className="h-16 w-16" src={logo} alt="Logo" />
            <h4 className="uppercase">
              <FormattedMessage id="login.labels.title" />
            </h4>
          </div>
        </header>
        <main className="card-login-main">
          <h3 className="mb-4 text-theme-dark-secondary-main">
            <FormattedMessage id="login.labels.welcome" />
          </h3>
          <h6>
            <FormattedMessage id="login.labels.secondaryWelcome" />
          </h6>
        </main>
        <footer className="card-login-footer">
          <FormLogin />
        </footer>
      </div>
    </div>
  )
}
