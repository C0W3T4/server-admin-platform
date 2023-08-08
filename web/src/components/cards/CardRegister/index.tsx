import { FormattedMessage } from 'react-intl'
import logo from '../../../assets/images/logo.png'
import { FormRegister } from '../../forms/FormRegister'
import './styles.css'

export const CardRegister = () => {
  return (
    <div className="card-register-container">
      <div className="card-register-wrapper">
        <header className="card-register-header">
          <div className="flex items-center">
            <img className="h-16 w-16" src={logo} alt="Logo" />
            <h4 className="uppercase">
              <FormattedMessage id="register.labels.title" />
            </h4>
          </div>
        </header>
        <main className="card-register-main">
          <h3 className="mb-4 text-theme-dark-secondary-main">
            <FormattedMessage id="register.labels.welcome" />
          </h3>
          <h6>
            <FormattedMessage id="register.labels.secondaryWelcome" />
          </h6>
        </main>
        <footer className="card-register-footer">
          <FormRegister />
        </footer>
      </div>
    </div>
  )
}
