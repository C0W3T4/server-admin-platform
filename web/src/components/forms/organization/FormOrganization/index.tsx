import {
  Button,
  CardActions,
  Divider,
  FormHelperText,
  Grid,
  TextField,
  useTheme,
} from '@mui/material'
import { FieldValues, SubmitHandler, useForm } from 'react-hook-form'
import { FormattedMessage } from 'react-intl'
import { useNavigate, useParams } from 'react-router-dom'
import { useLoading } from '../../../../hooks/useLoading'
import { api } from '../../../../libs/axios'
import { dispatch } from '../../../../libs/redux'
import { openSnackbar } from '../../../../libs/redux/slices/snackbar'
import { FormProps } from '../../../../types'
import { OrganizationDataProps } from '../../../../types/organization'
import { AnimateButton } from '../../../AnimateButton'
import { CardHeaderActions } from '../../../cards/CardHeaderActions'
import SubCard from '../../../cards/SubCard'

export interface IFormInput {
  name: string
  description?: string
}

export const FormOrganization = ({
  defaultValues,
  mode,
}: FormProps<OrganizationDataProps>) => {
  const { showLoading, hideLoading } = useLoading()

  const { id } = useParams()
  const navigate = useNavigate()
  const theme = useTheme()

  const {
    register,
    handleSubmit,
    formState: { errors, isValid },
  } = useForm<IFormInput>({
    defaultValues: {
      name: defaultValues?.name,
      description: defaultValues?.description,
    },
    mode: 'all',
  })

  const onSubmit: SubmitHandler<FieldValues> = async (formData) => {
    showLoading()
    await api
      .request({
        method: mode === 'create' ? 'POST' : 'PUT',
        url:
          mode === 'create' ? '/api/organizations' : `/api/organizations/${id}`,
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

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <SubCard
        title={
          mode === 'edit' ? (
            defaultValues?.name
          ) : (
            <FormattedMessage id="organizations.labels.new" />
          )
        }
        secondary={<CardHeaderActions />}
      >
        <Grid container spacing={2}>
          <Grid item xs={12} sm={12} md={6} lg={6} xl={6}>
            <TextField
              fullWidth
              id="name"
              label={<FormattedMessage id="organizations.labels.name" />}
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
              label={<FormattedMessage id="organizations.labels.description" />}
              {...register('description')}
            />
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
