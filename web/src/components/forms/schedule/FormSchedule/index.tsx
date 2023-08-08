import {
  Button,
  CardActions,
  Chip,
  Divider,
  FormControl,
  FormHelperText,
  Grid,
  Input,
  MenuItem,
  Select,
  Stack,
  TextField,
  Typography,
  useTheme,
} from '@mui/material'
import { DateTimePicker, LocalizationProvider } from '@mui/x-date-pickers'
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs'
import {
  Controller,
  FieldValues,
  SubmitHandler,
  useForm,
} from 'react-hook-form'
import { FormattedMessage } from 'react-intl'
import { useNavigate, useParams } from 'react-router-dom'
import useAuth from '../../../../hooks/useAuth'
import { useAxiosGet } from '../../../../hooks/useAxiosGet'
import { useLoading } from '../../../../hooks/useLoading'
import { api } from '../../../../libs/axios'
import { dispatch } from '../../../../libs/redux'
import { openSnackbar } from '../../../../libs/redux/slices/snackbar'
import {
  scheduleRepeatFrequencyMap,
  scheduleTypeMap,
  weekdays,
} from '../../../../providers/ScheduleProvider'
import { FormProps } from '../../../../types'
import { UserOrganizationsDataProps } from '../../../../types/access'
import {
  ScheduleDataProps,
  ScheduleRepeatFrequency,
  ScheduleType,
  ScheduleWeekdays,
} from '../../../../types/schedule'
import { AnimateButton } from '../../../AnimateButton'
import { CardHeaderActions } from '../../../cards/CardHeaderActions'
import SubCard from '../../../cards/SubCard'

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
  name: string
  description?: string
  schedule_type: ScheduleType
  start_date_time: Date
  repeat_frequency: ScheduleRepeatFrequency
  every?: number
  week_days?: number[]
  organization_id: string
}

export const FormSchedule = ({
  defaultValues,
  mode,
}: FormProps<ScheduleDataProps>) => {
  const { showLoading, hideLoading } = useLoading()

  const { id } = useParams()
  const navigate = useNavigate()
  const theme = useTheme()
  const { user } = useAuth()

  const { data: myOrganizations, error: myOrganizationsError } = useAxiosGet<
    UserOrganizationsDataProps[]
  >(`api/assigns/users-organizations/${user?.id}/organizations`)

  const {
    register,
    handleSubmit,
    control,
    watch,
    formState: { errors, isValid },
  } = useForm<IFormInput>({
    defaultValues: {
      name: defaultValues?.name,
      description: defaultValues?.description,
      schedule_type: defaultValues?.schedule_type,
      start_date_time: defaultValues?.start_date_time,
      repeat_frequency: defaultValues?.repeat_frequency,
      every: defaultValues?.every,
      week_days: defaultValues?.week_days ?? [],
      organization_id: defaultValues?.organization.id,
    },
    mode: 'all',
    shouldUnregister: true,
  })

  const onSubmit: SubmitHandler<FieldValues> = async (formData) => {
    showLoading()
    await api
      .request({
        method: mode === 'create' ? 'POST' : 'PUT',
        url: mode === 'create' ? '/api/schedules' : `/api/schedules/${id}`,
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
            <FormattedMessage id="schedules.labels.new" />
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
                  label={<FormattedMessage id="schedules.labels.name" />}
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
                  label={<FormattedMessage id="schedules.labels.description" />}
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
              {mode === 'create' && (
                <Grid item xs={12} sm={12} md={6} lg={6} xl={6}>
                  <TextField
                    fullWidth
                    id="schedule-type"
                    select
                    label={
                      <FormattedMessage id="schedules.labels.selectScheduleType" />
                    }
                    defaultValue={
                      defaultValues
                        ? defaultValues.schedule_type
                        : scheduleTypeMap.keys().next().value
                    }
                    error={
                      errors.schedule_type &&
                      errors.schedule_type?.type === 'required'
                    }
                    helperText={
                      errors.schedule_type &&
                      errors.schedule_type?.type === 'required' && (
                        <FormHelperText error>
                          <FormattedMessage id="input.validation.required" />
                        </FormHelperText>
                      )
                    }
                    {...register('schedule_type', { required: true })}
                  >
                    {[...scheduleTypeMap.entries()].map(
                      ([key, option], index) => (
                        <MenuItem key={index} value={key}>
                          {option.icon}
                          <FormattedMessage id={option.label} />
                        </MenuItem>
                      ),
                    )}
                  </TextField>
                </Grid>
              )}
              <Grid item xs={12} sm={12} md={6} lg={6} xl={6}>
                <Controller
                  name="start_date_time"
                  control={control}
                  defaultValue={
                    defaultValues
                      ? defaultValues.start_date_time
                      : new Date(new Date().setHours(24, 0, 0, 0))
                  }
                  rules={{
                    required: true,
                  }}
                  render={({ field: { ref, onBlur, name, ...field } }) => (
                    <LocalizationProvider dateAdapter={AdapterDayjs}>
                      <DateTimePicker
                        {...field}
                        inputRef={ref}
                        label={
                          <FormattedMessage id="schedules.labels.dateTime" />
                        }
                        hideTabs={false}
                        ampm={false}
                        renderInput={(inputProps) => (
                          <TextField
                            {...inputProps}
                            onBlur={onBlur}
                            name={name}
                            fullWidth
                            id="start-date-time"
                            error={
                              errors.start_date_time &&
                              errors.start_date_time?.type === 'required'
                            }
                            helperText={
                              errors.start_date_time ? (
                                <>
                                  {errors.start_date_time?.type ===
                                    'required' && (
                                    <FormHelperText error>
                                      <FormattedMessage id="input.validation.required" />
                                    </FormHelperText>
                                  )}
                                </>
                              ) : null
                            }
                          />
                        )}
                      />
                    </LocalizationProvider>
                  )}
                />
              </Grid>
              <Grid item xs={12} sm={12} md={6} lg={6} xl={6}>
                <TextField
                  fullWidth
                  id="repeat-frequency"
                  select
                  label={
                    <FormattedMessage id="schedules.labels.repeatFrequency" />
                  }
                  defaultValue={
                    defaultValues
                      ? defaultValues.repeat_frequency
                      : scheduleRepeatFrequencyMap.keys().next().value
                  }
                  error={
                    errors.repeat_frequency &&
                    errors.repeat_frequency?.type === 'required'
                  }
                  helperText={
                    errors.repeat_frequency &&
                    errors.repeat_frequency?.type === 'required' && (
                      <FormHelperText error>
                        <FormattedMessage id="input.validation.required" />
                      </FormHelperText>
                    )
                  }
                  {...register('repeat_frequency', { required: true })}
                >
                  {[...scheduleRepeatFrequencyMap.entries()].map(
                    ([key, option], index) => (
                      <MenuItem key={index} value={key}>
                        <FormattedMessage id={option.label} />
                      </MenuItem>
                    ),
                  )}
                </TextField>
              </Grid>
              {watch().repeat_frequency !== ScheduleRepeatFrequency.RUN_ONCE &&
                watch().repeat_frequency !== ScheduleRepeatFrequency.YEAR &&
                watch().repeat_frequency !== ScheduleRepeatFrequency.WEEK && (
                  <Grid item xs={12} sm={12} md={6} lg={6} xl={6}>
                    <TextField
                      fullWidth
                      id="every"
                      type="number"
                      label={<FormattedMessage id="schedules.labels.every" />}
                      defaultValue={
                        defaultValues?.every ? defaultValues.every : 1
                      }
                      error={errors.every && errors.every?.type === 'min'}
                      helperText={
                        errors.every ? (
                          <>
                            {errors.every?.type === 'min' && (
                              <FormHelperText error>
                                <FormattedMessage id="input.validation.min" />
                              </FormHelperText>
                            )}
                          </>
                        ) : null
                      }
                      {...register('every', { min: 1, valueAsNumber: true })}
                    />
                  </Grid>
                )}
              {watch().repeat_frequency === ScheduleRepeatFrequency.WEEK && (
                <Grid item xs={12} sm={12} md={6} lg={6} xl={6}>
                  <FormControl
                    fullWidth
                    error={Boolean(errors.week_days)}
                    sx={{ ...theme.typography.customInput }}
                  >
                    <Select
                      id="weekday"
                      multiple
                      fullWidth
                      defaultValue={defaultValues?.week_days ?? []}
                      value={watch().week_days}
                      input={<Input id="weekday" />}
                      renderValue={(selected) => (
                        <div>
                          {typeof selected !== 'string' &&
                            selected.map((value) => (
                              <Chip key={value} label={value} />
                            ))}
                        </div>
                      )}
                      MenuProps={MenuProps}
                      {...register('week_days')}
                    >
                      {weekdays &&
                        weekdays.map(
                          (weekday: ScheduleWeekdays, index: number) => (
                            <MenuItem key={index} value={index}>
                              <FormattedMessage
                                id={`enums.weekday.${weekday}`}
                              />
                            </MenuItem>
                          ),
                        )}
                    </Select>
                  </FormControl>
                </Grid>
              )}
              <Grid item xs={12} sm={12} md={6} lg={6} xl={6}>
                <TextField
                  id="organization-id"
                  select
                  label={
                    <FormattedMessage id="schedules.labels.selectOrganization" />
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
                      <FormattedMessage id="schedules.labels.organization" />
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
