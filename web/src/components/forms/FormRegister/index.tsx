import { LockTwoTone, Visibility, VisibilityOff } from '@mui/icons-material'
import {
  Button,
  FormControl,
  FormHelperText,
  Grid,
  IconButton,
  InputAdornment,
  OutlinedInput,
  TextField,
} from '@mui/material'
import { useState } from 'react'
import { FieldValues, SubmitHandler, useForm } from 'react-hook-form'
import { FormattedMessage } from 'react-intl'
import { Link } from 'react-router-dom'
import useAuth from '../../../hooks/useAuth'
import { useLoading } from '../../../hooks/useLoading'
import { api } from '../../../libs/axios'
import { dispatch } from '../../../libs/redux'
import { openSnackbar } from '../../../libs/redux/slices/snackbar'
import { StringColorProps } from '../../../types'
import {
  strengthColor,
  strengthIndicator,
} from '../../../utils/passwordStrength'
import { AnimateButton } from '../../AnimateButton'
import InputLabel from '../../InputLabel'
import { PasswordIndicator } from '../../PasswordIndicator'
import './styles.css'

interface IFormInput {
  company: string
  hostname: string
  ipv4: string
  username: string
  port: number
  password: string
  admin_username: string
  admin_password: string
  organization_name: string
}

export const FormRegister = () => {
  const [showPassword, setShowPassword] = useState<boolean>(false)
  const [showAdminPassword, setShowAdminPassword] = useState<boolean>(false)

  const [strength, setStrength] = useState<number>(0)
  const [userStrength, setUserStrength] = useState<number>(0)

  const [level, setLevel] = useState<StringColorProps>()
  const [userLevel, setUserLevel] = useState<StringColorProps>()

  const { login } = useAuth()
  const { showLoading, hideLoading } = useLoading()

  const {
    register,
    handleSubmit,
    formState: { errors, isValid },
  } = useForm<IFormInput>({
    mode: 'all',
  })

  const onSubmit: SubmitHandler<FieldValues> = async (formData) => {
    showLoading()
    await api
      .request({
        method: 'POST',
        url: '/api/register',
        data: formData,
      })
      .then((response) => {
        dispatch(
          openSnackbar({
            open: true,
            message:
              response.status === 200 ? (
                <FormattedMessage id="snackbar.message.success.201" />
              ) : (
                <FormattedMessage id="snackbar.message.success.201" />
              ),
            transition: 'SlideUp',
            variant: 'alert',
            alert: {
              color: 'success',
            },
            close: true,
          }),
        )
      })
      .catch(() => {
        dispatch(
          openSnackbar({
            open: true,
            message: <FormattedMessage id="snackbar.message.error" />,
            transition: 'SlideUp',
            variant: 'alert',
            alert: {
              color: 'error',
            },
            close: true,
          }),
        )
      })
      .finally(async () => {
        hideLoading()
        await login(
          formData.admin_username,
          formData.admin_password,
          formData.company,
        )
      })
  }

  const handleMouseDownPassword = (event: React.SyntheticEvent) => {
    event.preventDefault()
  }

  const handleClickShowPassword = () => {
    setShowPassword(!showPassword)
  }

  const handleClickShowAdminPassword = () => {
    setShowAdminPassword(!showAdminPassword)
  }

  const changePasswordIndicator = (value: string) => {
    const temp = strengthIndicator(value)
    setStrength(temp)
    setLevel(strengthColor(temp))
  }

  const changeUserPasswordIndicator = (value: string) => {
    const temp = strengthIndicator(value)
    setUserStrength(temp)
    setUserLevel(strengthColor(temp))
  }

  return (
    <div className="form-register-container">
      <form onSubmit={handleSubmit(onSubmit)}>
        <main className="form-register-main">
          <Grid container spacing={2}>
            <Grid item xs={12} sm={12} md={12} lg={12} xl={12}>
              <FormControl fullWidth error={Boolean(errors.company)}>
                <InputLabel htmlFor="company-register">
                  <FormattedMessage id="register.labels.company" />
                </InputLabel>
                <OutlinedInput
                  id="company-register"
                  type="text"
                  label="Company"
                  inputProps={{}}
                  {...register('company', { required: true })}
                />
                {errors.company && errors.company?.type === 'required' && (
                  <FormHelperText error>
                    <FormattedMessage id="input.validation.required" />
                  </FormHelperText>
                )}
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={12} md={12} lg={12} xl={12}>
              <FormControl fullWidth error={Boolean(errors.hostname)}>
                <InputLabel htmlFor="hostname-register">
                  <FormattedMessage id="register.labels.hostname" />
                </InputLabel>
                <OutlinedInput
                  id="hostname-register"
                  type="text"
                  label="Hostname"
                  inputProps={{}}
                  {...register('hostname', { required: true })}
                />
                {errors.hostname && errors.hostname?.type === 'required' && (
                  <FormHelperText error>
                    <FormattedMessage id="input.validation.required" />
                  </FormHelperText>
                )}
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={12} md={12} lg={12} xl={12}>
              <FormControl fullWidth error={Boolean(errors.ipv4)}>
                <TextField
                  fullWidth
                  id="ipv4"
                  type="text"
                  label={<FormattedMessage id="register.labels.ipv4" />}
                  error={
                    errors.ipv4 &&
                    errors.ipv4?.type === 'required' &&
                    errors.ipv4?.type === 'pattern'
                  }
                  helperText={
                    errors.ipv4 ? (
                      <>
                        {errors.ipv4?.type === 'required' && (
                          <FormHelperText error>
                            <FormattedMessage id="input.validation.required" />
                          </FormHelperText>
                        )}
                        {errors.ipv4?.type === 'pattern' && (
                          <FormHelperText error>
                            <FormattedMessage id="input.validation.ipAddress" />
                          </FormHelperText>
                        )}
                      </>
                    ) : null
                  }
                  {...register('ipv4', {
                    required: true,
                    pattern:
                      /^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$/gi,
                  })}
                />
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={12} md={12} lg={12} xl={12}>
              <FormControl fullWidth error={Boolean(errors.port)}>
                <TextField
                  fullWidth
                  id="port"
                  type="number"
                  label={<FormattedMessage id="register.labels.port" />}
                  error={errors.port && errors.port?.type === 'required'}
                  helperText={
                    errors.port &&
                    errors.port?.type === 'required' && (
                      <FormHelperText error>
                        <FormattedMessage id="input.validation.required" />
                      </FormHelperText>
                    )
                  }
                  {...register('port', { required: true })}
                />
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={12} md={12} lg={12} xl={12}>
              <FormControl fullWidth error={Boolean(errors.username)}>
                <InputLabel htmlFor="username-register">
                  <FormattedMessage id="register.labels.username" />
                </InputLabel>
                <OutlinedInput
                  id="username-register"
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
                <InputLabel htmlFor="password-register">
                  <FormattedMessage id="register.labels.password" />
                </InputLabel>
                <OutlinedInput
                  id="password-register"
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
                  {...register('password', {
                    required: true,
                    onChange: (e) => changePasswordIndicator(e.target.value),
                  })}
                />
                {errors.password && errors.password?.type === 'required' && (
                  <FormHelperText error>
                    <FormattedMessage id="input.validation.required.password" />
                  </FormHelperText>
                )}
              </FormControl>
              {strength !== 0 && <PasswordIndicator level={level} />}
            </Grid>
            <Grid item xs={12} sm={12} md={12} lg={12} xl={12}>
              <FormControl fullWidth error={Boolean(errors.admin_username)}>
                <InputLabel htmlFor="admin-username-register">
                  <FormattedMessage id="register.labels.adminUsername" />
                </InputLabel>
                <OutlinedInput
                  id="admin-username-register"
                  type="text"
                  label="Admin username"
                  inputProps={{}}
                  {...register('admin_username', { required: true })}
                />
                {errors.admin_username &&
                  errors.admin_username?.type === 'required' && (
                    <FormHelperText error>
                      <FormattedMessage id="input.validation.required.username" />
                    </FormHelperText>
                  )}
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={12} md={12} lg={12} xl={12}>
              <FormControl fullWidth error={Boolean(errors.admin_password)}>
                <InputLabel htmlFor="admin-password-register">
                  <FormattedMessage id="register.labels.adminPassword" />
                </InputLabel>
                <OutlinedInput
                  id="admin-password-register"
                  type={showAdminPassword ? 'text' : 'password'}
                  startAdornment={
                    <InputAdornment position="start">
                      <LockTwoTone color="info" />
                    </InputAdornment>
                  }
                  endAdornment={
                    <InputAdornment position="end">
                      <IconButton
                        aria-label="toggle password visibility"
                        onClick={handleClickShowAdminPassword}
                        onMouseDown={handleMouseDownPassword}
                        edge="end"
                        size="large"
                      >
                        {showAdminPassword ? (
                          <Visibility color="info" />
                        ) : (
                          <VisibilityOff color="info" />
                        )}
                      </IconButton>
                    </InputAdornment>
                  }
                  label="Admin password"
                  inputProps={{}}
                  {...register('admin_password', {
                    required: true,
                    onChange: (e) =>
                      changeUserPasswordIndicator(e.target.value),
                  })}
                />
                {errors.admin_password &&
                  errors.admin_password?.type === 'required' && (
                    <FormHelperText error>
                      <FormattedMessage id="input.validation.required.password" />
                    </FormHelperText>
                  )}
              </FormControl>
              {userStrength !== 0 && <PasswordIndicator level={userLevel} />}
            </Grid>
            <Grid item xs={12} sm={12} md={12} lg={12} xl={12}>
              <FormControl fullWidth error={Boolean(errors.organization_name)}>
                <InputLabel htmlFor="organization-register">
                  <FormattedMessage id="register.labels.organization" />
                </InputLabel>
                <OutlinedInput
                  id="organization-register"
                  type="text"
                  label="organization"
                  inputProps={{}}
                  {...register('organization_name', { required: true })}
                />
                {errors.organization_name &&
                  errors.organization_name?.type === 'required' && (
                    <FormHelperText error>
                      <FormattedMessage id="input.validation.required" />
                    </FormHelperText>
                  )}
              </FormControl>
            </Grid>
          </Grid>
        </main>
        <footer className="form-register-footer">
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
              <FormattedMessage id="Register.Labels.SignUp" />
            </Button>
          </AnimateButton>
          <Link to="/">
            <FormattedMessage id="register.labels.goToLogin" />
          </Link>
        </footer>
      </form>
    </div>
  )
}
