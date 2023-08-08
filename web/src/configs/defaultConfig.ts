import { ConfigProps } from '../types/config'

export const BASE_PATH = ''
export const DASHBOARD_PATH = '/dashboard/default'

const defaultConfig: ConfigProps = {
  fontFamily: `'Roboto', sans-serif`,
  borderRadius: 8,
  outlinedFilled: true,
  navType: 'dark',
  presetColor: 'theme1',
  locale: 'en',
  rtlLayout: false,
  container: false,
}

export default defaultConfig
