import {
  Button,
  Chip,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControl,
  FormHelperText,
  Grid,
  Input,
  MenuItem,
  Select,
  Slide,
  SlideProps,
  Typography,
} from '@mui/material'
import { useTheme } from '@mui/material/styles'
import { forwardRef } from 'react'
import { FieldValues, SubmitHandler, useForm } from 'react-hook-form'
import { FormattedMessage, useIntl } from 'react-intl'
import { useParams } from 'react-router-dom'
import { useAxiosGet } from '../../../../hooks/useAxiosGet'
import { useLoading } from '../../../../hooks/useLoading'
import { api } from '../../../../libs/axios'
import { dispatch } from '../../../../libs/redux'
import { gridSpacing } from '../../../../libs/redux/constants'
import { openSnackbar } from '../../../../libs/redux/slices/snackbar'
import { DialogFormProps } from '../../../../types'
import { UsersOrganizationDataProps } from '../../../../types/access'
import { OrganizationDataProps } from '../../../../types/organization'
import { UserProfile } from '../../../../types/user'
import { AnimateButton } from '../../../AnimateButton'

const Transition = forwardRef((props: SlideProps, ref) => (
  <Slide direction="up" ref={ref} {...props} />
))
Transition.displayName = 'Transition'

const ITEM_HEIGHT = 48
const ITEM_PADDING_TOP = 8
const MenuProps = {
  PaperProps: {
    style: {
      maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
      width: 250,
    },
  },
  chip: {
    margin: 2,
  },
}

export interface IFormInput {
  users_id: string[]
  organization_id: string
}

export const FormOrganizationUsers = ({
  open,
  handleCloseDialog,
  data: organizationData,
  setNewData,
  oldData,
}: DialogFormProps<OrganizationDataProps, UsersOrganizationDataProps[]>) => {
  const theme = useTheme()
  const { id } = useParams()
  const { formatMessage } = useIntl()

  const { showLoading, hideLoading } = useLoading()

  const { data } = useAxiosGet<UserProfile[]>('api/users')

  const {
    register,
    handleSubmit,
    watch,
    reset,
    formState: { errors, isValid },
  } = useForm<IFormInput>({
    defaultValues: {
      users_id: [],
      organization_id: id,
    },
    mode: 'all',
  })

  const onSubmit: SubmitHandler<FieldValues> = async (formData) => {
    showLoading()
    await api
      .request({
        method: 'POST',
        url: '/api/assigns/users-organizations',
        data: formData,
      })
      .then((response) => {
        if (setNewData && oldData) {
          setNewData([
            ...oldData,
            {
              user_organization_id: response.data.user_organization_id,
              user: response.data.user,
            },
          ])
        } else if (setNewData && !oldData) {
          setNewData([
            {
              user_organization_id: response.data.user_organization_id,
              user: response.data.user,
            },
          ])
        }

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
      .finally(() => {
        hideLoading()
        reset()
        handleCloseDialog()
      })
  }

  return (
    <Dialog
      open={open}
      TransitionComponent={Transition}
      keepMounted
      onClose={handleCloseDialog}
      sx={{
        '&>div:nth-of-type(3)': {
          justifyContent: 'center',
          '&>div': {
            m: 0,
            flex: '1 1 auto',
            borderRadius: '0px',
            maxHeight: '100%',
          },
        },
      }}
    >
      {open && (
        <form onSubmit={handleSubmit(onSubmit)}>
          <DialogTitle>{`${formatMessage({
            id: 'organizations.users.dialog.title',
          })} -> ${organizationData!.name}`}</DialogTitle>
          <DialogContent>
            <Grid container spacing={gridSpacing} sx={{ mt: 0.25 }}>
              <Grid item xs={12}>
                <Grid container spacing={1}>
                  <Grid item xs={12} sm={12} md={12} lg={12} xl={12}>
                    <Typography variant="subtitle1" align="left">
                      <FormattedMessage id="organizations.labels.users" />
                    </Typography>
                  </Grid>
                  <Grid item xs={12} sm={12} md={12} lg={12} xl={12}>
                    <FormControl
                      fullWidth
                      error={Boolean(errors.users_id)}
                      sx={{ ...theme.typography.customInput }}
                    >
                      <Select
                        id="multiple-users"
                        multiple
                        fullWidth
                        defaultValue={[]}
                        value={watch().users_id}
                        input={<Input id="select-multiple-users" />}
                        renderValue={(selected) => (
                          <div>
                            {typeof selected !== 'string' &&
                              selected.map((value) => (
                                <Chip key={value} label={value} />
                              ))}
                          </div>
                        )}
                        MenuProps={MenuProps}
                        {...register('users_id', {
                          required: true,
                          minLength: 1,
                        })}
                      >
                        {data &&
                          data.map((user) => (
                            <MenuItem key={user.id} value={user.id}>
                              {user.username}
                            </MenuItem>
                          ))}
                      </Select>
                      {errors.users_id && (
                        <FormHelperText error>
                          <FormattedMessage id="input.validation.required" />
                        </FormHelperText>
                      )}
                    </FormControl>
                  </Grid>
                </Grid>
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
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
            <AnimateButton scale={{ hover: 1.1, tap: 0.9 }}>
              <Button variant="text" color="error" onClick={handleCloseDialog}>
                <FormattedMessage id="input.labels.close" />
              </Button>
            </AnimateButton>
          </DialogActions>
        </form>
      )}
    </Dialog>
  )
}
