import { combineReducers } from 'redux'
import menuReducer from './slices/menu'
import snackbarReducer from './slices/snackbar'

const reducer = combineReducers({
  menu: menuReducer,
  snackbar: snackbarReducer,
})

export default reducer
