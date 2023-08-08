import { NavigationScroll } from './components/NavigationScroll'
import { Snackbar } from './components/Snackbar'
import Locales from './configs/Locales'
import { JWTProvider } from './contexts/JWTContext'
import { LoadingProvider } from './contexts/LoadingContext'
import { AppRoutes } from './routes'
import ThemeCustomization from './themes'

function App() {
  return (
    <ThemeCustomization>
      <Locales>
        <NavigationScroll>
          <JWTProvider>
            <LoadingProvider>
              <AppRoutes />
              <Snackbar />
            </LoadingProvider>
          </JWTProvider>
        </NavigationScroll>
      </Locales>
    </ThemeCustomization>
  )
}

export default App
