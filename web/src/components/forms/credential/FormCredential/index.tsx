import { LockTwoTone, Visibility, VisibilityOff } from '@mui/icons-material'
import {
  Button,
  CardActions,
  Divider,
  FormHelperText,
  Grid,
  IconButton,
  InputAdornment,
  MenuItem,
  Stack,
  TextField,
  Typography,
  useTheme,
} from '@mui/material'
import { useState } from 'react'
import { FieldValues, SubmitHandler, useForm } from 'react-hook-form'
import { FormattedMessage } from 'react-intl'
import { useNavigate, useParams } from 'react-router-dom'
import useAuth from '../../../../hooks/useAuth'
import { useAxiosGet } from '../../../../hooks/useAxiosGet'
import { useLoading } from '../../../../hooks/useLoading'
import { api } from '../../../../libs/axios'
import { dispatch } from '../../../../libs/redux'
import { openSnackbar } from '../../../../libs/redux/slices/snackbar'
import { credentialTypeMap } from '../../../../providers/CredentialProvider'
import { FormProps, StringColorProps } from '../../../../types'
import { UserOrganizationsDataProps } from '../../../../types/access'
import {
  CredentialDataProps,
  CredentialType,
} from '../../../../types/credential'
import {
  strengthColor,
  strengthIndicator,
} from '../../../../utils/passwordStrength'
import { AnimateButton } from '../../../AnimateButton'
import { PasswordIndicator } from '../../../PasswordIndicator'
import { CardHeaderActions } from '../../../cards/CardHeaderActions'
import SubCard from '../../../cards/SubCard'

export interface IFormInput {
  name: string
  description: string
  username: string
  port: number
  password: string
  credential_type: CredentialType
  organization_id: string
}

export const FormCredential = ({
  defaultValues,
  mode,
}: FormProps<CredentialDataProps>) => {
  const [showPassword, setShowPassword] = useState(false)

  const [strength, setStrength] = useState<number>(0)
  const [level, setLevel] = useState<StringColorProps>()

  const { id } = useParams()
  const { user } = useAuth()
  const navigate = useNavigate()
  const theme = useTheme()
  const { showLoading, hideLoading } = useLoading()

  const { data: myOrganizations, error: myOrganizationsError } = useAxiosGet<
    UserOrganizationsDataProps[]
  >(`api/assigns/users-organizations/${user?.id}/organizations`)

  const {
    register,
    handleSubmit,
    formState: { errors, isValid },
  } = useForm<IFormInput>({
    defaultValues: {
      name: defaultValues?.name,
      description: defaultValues?.description,
      username: defaultValues?.username,
      port: defaultValues?.port,
      credential_type: defaultValues?.credential_type,
      organization_id: defaultValues?.organization.id,
    },
    mode: 'all',
  })

  const onSubmit: SubmitHandler<FieldValues> = async (formData) => {
    showLoading()
    await api
      .request({
        method: mode === 'create' ? 'POST' : 'PUT',
        url: mode === 'create' ? '/api/credentials' : `/api/credentials/${id}`,
        data: formData,
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
            defaultValues?.name
          ) : (
            <FormattedMessage id="credentials.labels.new" />
          )
        }
        secondary={<CardHeaderActions />}
      >
        {myOrganizations ? (
          <>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={12} md={6} lg={6} xl={6}>
                <TextField
                  fullWidth
                  id="name"
                  label={<FormattedMessage id="credentials.labels.name" />}
                  error={errors.name && errors.name?.type === 'required'}
                  helperText={
                    errors.name &&
                    errors.name?.type === 'required' && (
                      <FormHelperText error>
                        <FormattedMessage id="input.validation.required" />
                      </FormHelperText>
                    )
                  }
                  {...register('name', { required: true })}
                />
              </Grid>
              <Grid item xs={12} sm={12} md={6} lg={6} xl={6}>
                <TextField
                  fullWidth
                  id="description"
                  multiline
                  rows={1}
                  label={
                    <FormattedMessage id="credentials.labels.description" />
                  }
                  error={
                    errors.description &&
                    errors.description?.type === 'required'
                  }
                  helperText={
                    errors.description &&
                    errors.description?.type === 'required' && (
                      <FormHelperText error>
                        <FormattedMessage id="input.validation.required" />
                      </FormHelperText>
                    )
                  }
                  {...register('description')}
                />
              </Grid>
              <Grid item xs={12} sm={12} md={6} lg={6} xl={6}>
                <TextField
                  fullWidth
                  id="credential-type"
                  select
                  label={
                    <FormattedMessage id="credentials.labels.selectCredentialType" />
                  }
                  defaultValue={
                    defaultValues ? defaultValues.credential_type : ''
                  }
                  error={
                    errors.credential_type &&
                    errors.credential_type?.type === 'required'
                  }
                  helperText={
                    errors.credential_type &&
                    errors.credential_type?.type === 'required' && (
                      <FormHelperText error>
                        <FormattedMessage id="input.validation.required" />
                      </FormHelperText>
                    )
                  }
                  {...register('credential_type', { required: true })}
                >
                  {[...credentialTypeMap.entries()].map(
                    ([key, option], index) => (
                      <MenuItem key={index} value={key}>
                        {option.icon}
                        <FormattedMessage id={option.label} />
                      </MenuItem>
                    ),
                  )}
                </TextField>
              </Grid>
              <Grid item xs={12} sm={12} md={6} lg={6} xl={6}>
                <TextField
                  fullWidth
                  id="username"
                  label={<FormattedMessage id="credentials.labels.username" />}
                  error={
                    errors.username && errors.username?.type === 'required'
                  }
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
              <Grid item xs={12} sm={12} md={6} lg={6} xl={6}>
                <TextField
                  fullWidth
                  id="port"
                  type="number"
                  label={<FormattedMessage id="credentials.labels.port" />}
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
              </Grid>
              {mode === 'create' && (
                <Grid item xs={12} sm={12} md={6} lg={6} xl={6}>
                  <TextField
                    fullWidth
                    id="password"
                    type={showPassword ? 'text' : 'password'}
                    label={<FormattedMessage id="users.labels.password" />}
                    error={
                      errors.password && errors.password?.type === 'required'
                    }
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
              <Grid item xs={12} sm={12} md={6} lg={6} xl={6}>
                <TextField
                  id="organization-id"
                  select
                  label={
                    <FormattedMessage id="credentials.labels.selectOrganization" />
                  }
                  fullWidth
                  defaultValue={
                    defaultValues ? defaultValues.organization.id : ''
                  }
                  error={
                    errors.organization_id &&
                    errors.organization_id?.type === 'required'
                  }
                  helperText={
                    errors.organization_id &&
                    errors.organization_id?.type === 'required' && (
                      <FormHelperText error>
                        <FormattedMessage id="input.validation.required" />
                      </FormHelperText>
                    )
                  }
                  {...register('organization_id', { required: true })}
                >
                  {myOrganizations?.map((option) => (
                    <MenuItem
                      key={option.organization.id}
                      value={option.organization.id}
                    >
                      {option.organization.name}
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
          </>
        ) : (
          myOrganizationsError?.response?.status === 404 && (
            <Stack spacing={2}>
              <Stack
                direction="row"
                spacing={2}
                sx={{
                  alignItems: 'center',
                  justifyContent: 'center',
                  textAlign: 'center',
                }}
              >
                <Typography variant="h4">
                  <FormattedMessage id="input.validation.required.needCreate" />
                  &#58;
                  <br />
                  {myOrganizationsError && (
                    <>
                      <br />
                      <FormattedMessage id="credentials.labels.organization" />
                    </>
                  )}
                </Typography>
              </Stack>
            </Stack>
          )
        )}
      </SubCard>
    </form>
  )
}
