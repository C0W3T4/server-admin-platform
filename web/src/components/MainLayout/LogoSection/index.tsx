import { Link } from '@mui/material'
import { Link as RouterLink } from 'react-router-dom'
import logoImg from '../../../assets/images/logo.png'
import { DASHBOARD_PATH } from '../../../configs/defaultConfig'

const LogoSection = () => (
  <Link
    component={RouterLink}
    to={DASHBOARD_PATH}
    className="flex items-center"
  >
    <img src={logoImg} alt="Portal" width="34" height="34" />
    <h5 className="uppercase">Server Admin Platform</h5>
  </Link>
)

export default LogoSection
