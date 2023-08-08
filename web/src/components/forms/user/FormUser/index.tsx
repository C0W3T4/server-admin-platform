import {
  EmailTwoTone,
  LockTwoTone,
  Visibility,
  VisibilityOff,
} from '@mui/icons-material'
import {
  Button,
  CardActions,
  Divider,
  FormHelperText,
  Grid,
  IconButton,
  InputAdornment,
  MenuItem,
  TextField,
  useTheme,
} from '@mui/material'
import { useState } from 'react'
import { FieldValues, SubmitHandler, useForm } from 'react-hook-form'
import { FormattedMessage } from 'react-intl'
import { useNavigate, useParams } from 'react-router-dom'
import { useLoading } from '../../../../hooks/useLoading'
import { api } from '../../../../libs/axios'
import { dispatch } from '../../../../libs/redux'
import { openSnackbar } from '../../../../libs/redux/slices/snackbar'
import { userTypeMap } from '../../../../providers/userProvider'
import { FormProps, StringColorProps } from '../../../../types'
import { UserProfile } from '../../../../types/user'
import {
  strengthColor,
  strengthIndicator,
} from '../../../../utils/passwordStrength'
import { AnimateButton } from '../../../AnimateButton'
import { PasswordIndicator } from '../../../PasswordIndicator'
import { CardHeaderActions } from '../../../cards/CardHeaderActions'
import SubCard from '../../../cards/SubCard'

export interface IFormInput {
  first_name?: string
  last_name?: string
  email?: string
  username: string
  password?: string
  user_type: string
  roles?: string[]
}

export const FormUser = ({ defaultValues, mode }: FormProps<UserProfile>) => {
  const { showLoading, hideLoading } = useLoading()
  const [showPassword, setShowPassword] = useState(false)

  const [strength, setStrength] = useState<number>(0)
  const [level, setLevel] = useState<StringColorProps>()

  const { id } = useParams()
  const navigate = useNavigate()
  const theme = useTheme()

  const {
    register,
    handleSubmit,
    formState: { errors, isValid },
  } = useForm<IFormInput>({
    defaultValues: {
      first_name: defaultValues?.first_name,
      last_name: defaultValues?.last_name,
      email: defaultValues?.email,
      username: defaultValues?.username,
      user_type: defaultValues?.user_type,
    },
    mode: 'all',
  })

  const onSubmit: SubmitHandler<FieldValues> = async (formData) => {
    showLoading()
    if (!formData.email) {
      delete formData.email
    }

    const payload = { ...formData, roles: ['GENERIC'] } // TODO -> roles

    await api
      .request({
        method: mode === 'create' ? 'POST' : 'PUT',
        url: mode === 'create' ? '/api/users' : `/api/users/${id}`,
        data: payload,
      })
      .then((response) => {
        dispatch(
          openSnackbar({
            open: true,
            message:
              response.status === 200 ? (
                <FormattedMessage id="snackbar.message.success.200.updated" />
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
        setTimeout(() => {
          navigate('../list', { replace: true })
        }, 1)
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
      .finally(() => hideLoading())
  }

  const handleMouseDownPassword = (event: React.SyntheticEvent) => {
    event.preventDefault()
  }

  const handleClickShowPassword = () => {
    setShowPassword(!showPassword)
  }

  const changePasswordIndicator = (value: string) => {
    const temp = strengthIndicator(value)
    setStrength(temp)
    setLevel(strengthColor(temp))
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <SubCard
        title={
          mode === 'edit' ? (
            defaultValues?.username
          ) : (
            <FormattedMessage id="users.labels.new" />
          )
        }
        secondary={<CardHeaderActions />}
      >
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} sm={6} md={4} lg={4} xl={3}>
            <TextField
              fullWidth
              id="first_name"
              label={<FormattedMessage id="users.labels.firstName" />}
              {...register('first_name')}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={4} lg={4} xl={3}>
            <TextField
              fullWidth
              id="last_name"
              label={<FormattedMessage id="users.labels.lastName" />}
              {...register('last_name')}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={4} lg={4} xl={3}>
            <TextField
              fullWidth
              id="email"
              type="email"
              label={<FormattedMessage id="users.labels.email" />}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <EmailTwoTone />
                  </InputAdornment>
                ),
              }}
              {...register('email')}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={4} lg={4} xl={3}>
            <TextField
              fullWidth
              id="username"
              type="text"
              hidden={true}
              label={<FormattedMessage id="users.labels.username" />}
              error={errors.username && errors.username?.type === 'required'}
              helperText={
                errors.username &&
                errors.username?.type === 'required' && (
                  <FormHelperText error>
                    <FormattedMessage id="input.validation.required" />
                  </FormHelperText>
                )
              }
              {...register('username', { required: true })}
            />
          </Grid>
          {mode === 'create' && (
            <Grid item xs={12} sm={6} md={4} lg={4} xl={3}>
              <TextField
                fullWidth
                id="password"
                type={showPassword ? 'text' : 'password'}
                label={<FormattedMessage id="users.labels.password" />}
                error={errors.password && errors.password?.type === 'required'}
                helperText={
                  errors.password &&
                  errors.password?.type === 'required' && (
                    <FormHelperText error>
                      <FormattedMessage id="input.validation.required" />
                    </FormHelperText>
                  )
                }
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <LockTwoTone color="info" />
                    </InputAdornment>
                  ),
                  endAdornment: (
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
                  ),
                }}
                {...register('password', {
                  required: true,
                  onChange: (e) => changePasswordIndicator(e.target.value),
                })}
              />
              {strength !== 0 && <PasswordIndicator level={level} />}
            </Grid>
          )}
          <Grid item xs={12} sm={6} md={4} lg={4} xl={3}>
            <TextField
              fullWidth
              id="user_type"
              select
              label={<FormattedMessage id="users.labels.userType" />}
              defaultValue={
                defaultValues
                  ? defaultValues.user_type
                  : userTypeMap.keys().next().value
              }
              error={errors.user_type && errors.user_type?.type === 'required'}
              helperText={
                errors.user_type &&
                errors.user_type?.type === 'required' && (
                  <FormHelperText error>
                    <FormattedMessage id="input.validation.required" />
                  </FormHelperText>
                )
              }
              {...register('user_type', { required: true })}
            >
              {[...userTypeMap.entries()].map(([key, option], index) => (
                <MenuItem key={index} value={key}>
                  {option.icon}
                  <FormattedMessage id={option.label} />
                </MenuItem>
              ))}
            </TextField>
          </Grid>
        </Grid>
        <Divider sx={{ paddingTop: '16px' }} />
        <CardActions>
          <Grid
            container
            alignItems="center"
            justifyContent="flex-end"
            spacing={2}
          >
            <Grid item>
              <AnimateButton scale={{ hover: 1.1, tap: 0.9 }}>
                <Button
                  variant="contained"
                  color="secondary"
                  type="submit"
                  disabled={!isValid}
                  sx={{
                    boxShadow: theme.customShadows.secondary,
                    ':hover': { boxShadow: 'none' },
                  }}
                >
                  <FormattedMessage id="input.labels.submit" />
                </Button>
              </AnimateButton>
            </Grid>
          </Grid>
        </CardActions>
      </SubCard>
    </form>
  )
}
