import { LockTwoTone, Visibility, VisibilityOff } from '@mui/icons-material'
import {
  Button,
  FormControl,
  FormHelperText,
  Grid,
  IconButton,
  InputAdornment,
  OutlinedInput,
} from '@mui/material'
import { AxiosError } from 'axios'
import { useState } from 'react'
import { FieldValues, SubmitHandler, useForm } from 'react-hook-form'
import { FormattedMessage, useIntl } from 'react-intl'
import { Link } from 'react-router-dom'
import useAuth from '../../../hooks/useAuth'
import { useLoading } from '../../../hooks/useLoading'
import { dispatch } from '../../../libs/redux'
import { openSnackbar } from '../../../libs/redux/slices/snackbar'
import { AnimateButton } from '../../AnimateButton'
import InputLabel from '../../InputLabel'
import './styles.css'

interface IFormInput {
  username: string
  password: string
  company: string
}

export const FormLogin = () => {
  const [showPassword, setShowPassword] = useState(false)

  const { login } = useAuth()
  const { formatMessage } = useIntl()
  const { showLoading, hideLoading } = useLoading()

  const {
    register,
    handleSubmit,
    formState: { errors, isValid },
  } = useForm<IFormInput>({
    mode: 'all',
  })

  const onSubmit: SubmitHandler<FieldValues> = async (data) => {
    showLoading()
    await login(data.username, data.password, data.company)
      .catch((error: AxiosError) => {
        if (error.response?.status === 401) {
          dispatch(
            openSnackbar({
              open: true,
              message: formatMessage({
                id: 'snackbar.message.error.invalidCredentials',
              }),
              transition: 'SlideUp',
              variant: 'alert',
              alert: {
                color: 'error',
              },
              close: true,
            }),
          )
        }
      })
      .finally(() => hideLoading())
  }

  const handleMouseDownPassword = (event: React.SyntheticEvent) => {
    event.preventDefault()
  }

  const handleClickShowPassword = () => {
    setShowPassword(!showPassword)
  }

  return (
    <div className="form-login-container">
      <form onSubmit={handleSubmit(onSubmit)}>
        <main className="form-login-main">
          <Grid container spacing={2}>
            <Grid item xs={12} sm={12} md={12} lg={12} xl={12}>
              <FormControl fullWidth error={Boolean(errors.company)}>
                <InputLabel htmlFor="company-login">
                  <FormattedMessage id="input.labels.company" />
                </InputLabel>
                <OutlinedInput
                  id="company-login"
                  type="text"
                  label="Company"
                  inputProps={{}}
                  {...register('company', { required: true })}
                />
                {errors.company && errors.company?.type === 'required' && (
                  <FormHelperText error>
                    <FormattedMessage id="input.validation.required.username" />
                  </FormHelperText>
                )}
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={12} md={12} lg={12} xl={12}>
              <FormControl fullWidth error={Boolean(errors.username)}>
                <InputLabel htmlFor="username-login">
                  <FormattedMessage id="input.labels.username" />
                </InputLabel>
                <OutlinedInput
                  id="username-login"
                  type="text"
                  label="Username"
                  inputProps={{}}
                  {...register('username', { required: true })}
                />
                {errors.username && errors.username?.type === 'required' && (
                  <FormHelperText error>
                    <FormattedMessage id="input.validation.required.username" />
                  </FormHelperText>
                )}
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={12} md={12} lg={12} xl={12}>
              <FormControl fullWidth error={Boolean(errors.password)}>
                <InputLabel htmlFor="password-login">
                  <FormattedMessage id="input.labels.password" />
                </InputLabel>
                <OutlinedInput
                  id="password-login"
                  type={showPassword ? 'text' : 'password'}
                  startAdornment={
                    <InputAdornment position="start">
                      <LockTwoTone color="info" />
                    </InputAdornment>
                  }
                  endAdornment={
                    <InputAdornment position="end">
                      <IconButton
                        aria-label="toggle password visibility"
                        onClick={handleClickShowPassword}
                        onMouseDown={handleMouseDownPassword}
                        edge="end"
                        size="large"
                      >
                        {showPassword ? (
                          <Visibility color="info" />
                        ) : (
                          <VisibilityOff color="info" />
                        )}
                      </IconButton>
                    </InputAdornment>
                  }
                  label="Password"
                  inputProps={{}}
                  {...register('password', { required: true })}
                />
                {errors.password && errors.password?.type === 'required' && (
                  <FormHelperText error>
                    <FormattedMessage id="input.validation.required.password" />
                  </FormHelperText>
                )}
              </FormControl>
            </Grid>
          </Grid>
        </main>
        <footer className="form-login-footer">
          <AnimateButton>
            <Button
              disableElevation
              fullWidth
              size="large"
              type="submit"
              variant="contained"
              color="secondary"
              disabled={!isValid}
              sx={{ marginBottom: '1rem' }}
            >
              <FormattedMessage id="Login.Labels.SignIn" />
            </Button>
          </AnimateButton>
          <Link to="register">
            <FormattedMessage id="login.labels.createAccount" />
          </Link>
        </footer>
      </form>
    </div>
  )
}
