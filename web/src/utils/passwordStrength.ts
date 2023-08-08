import value from '../styles/_themes-vars.module.scss'
import { NumbColorFunc, StringBoolFunc, StringNumFunc } from '../types'

// has number
const hasNumber: StringBoolFunc = (number: string) => /[0-9]/.test(number)

// has mix of small and capitals
const hasMixed: StringBoolFunc = (number: string) =>
  /[a-z]/.test(number) && /[A-Z]/.test(number)

// has special chars
const hasSpecial: StringBoolFunc = (number: string) =>
  /[!#@$%^&*)(+=._-]/.test(number)

// set color based on password strength
export const strengthColor: NumbColorFunc = (count: number) => {
  if (count < 2) return { label: 'Poor', color: value.errorMain }
  if (count < 3) return { label: 'Weak', color: value.warningDark }
  if (count < 4) return { label: 'Normal', color: value.orangeMain }
  if (count < 5) return { label: 'Good', color: value.successMain }
  if (count < 6) return { label: 'Strong', color: value.successDark }
  return { label: 'Poor', color: value.errorMain }
}

// password strength indicator
export const strengthIndicator: StringNumFunc = (number: string) => {
  let strengths = 0
  if (number.length > 5) strengths += 1
  if (number.length > 7) strengths += 1
  if (hasNumber(number)) strengths += 1
  if (hasSpecial(number)) strengths += 1
  if (hasMixed(number)) strengths += 1
  return strengths
}
