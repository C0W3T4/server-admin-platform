import React from 'react'
import ReactDOM from 'react-dom/client'
import { Provider } from 'react-redux'
import { BrowserRouter } from 'react-router-dom'
import App from './App'
import { BASE_PATH } from './configs/defaultConfig'
import { ConfigProvider } from './contexts/ConfigContext'
import { store } from './libs/redux'
import './styles/global.css'
import './styles/themeStyles.scss'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <Provider store={store}>
      <ConfigProvider>
        <BrowserRouter basename={BASE_PATH}>
          <App />
        </BrowserRouter>
      </ConfigProvider>
    </Provider>
  </React.StrictMode>,
)
