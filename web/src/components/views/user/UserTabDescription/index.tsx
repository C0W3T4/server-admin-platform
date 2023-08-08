import { DateRangeTwoTone, EmailTwoTone } from '@mui/icons-material'
import { Grid, Stack, Typography } from '@mui/material'
import { FormattedMessage } from 'react-intl'
import useConfig from '../../../../hooks/useConfig'
import { gridSpacing } from '../../../../libs/redux/constants'
import { userTypeMap } from '../../../../providers/userProvider'
import { DetailsViewProps } from '../../../../types'
import { UserProfile } from '../../../../types/user'
import { CardHeaderActions } from '../../../cards/CardHeaderActions'
import SubCard from '../../../cards/SubCard'

const iconSX = {
  width: 16,
  height: 16,
  verticalAlign: 'middle',
  mr: 0.5,
}

const labelSX = {
  flex: '1 1 33.33%',
  textAlign: 'right',
}

const infoSX = {
  flex: '1 1 66.66%',
  textAlign: 'left',
}

export const UserTabDescription = ({
  defaultValues,
}: DetailsViewProps<UserProfile>) => {
  const { locale } = useConfig()

  return (
    <SubCard title={defaultValues?.username} secondary={<CardHeaderActions />}>
      <Grid container spacing={gridSpacing}>
        <Grid item xs={12}>
          <Grid container spacing={gridSpacing}>
            <Grid item xs={12} sm={12} md={12} lg={12} xl={12}>
              <Stack spacing={2}>
                {defaultValues?.first_name && defaultValues?.last_name && (
                  <Stack
                    direction="row"
                    spacing={2}
                    sx={{ alignItems: 'center' }}
                  >
                    <Typography variant="subtitle1" sx={labelSX}>
                      <FormattedMessage id="users.labels.fullName" />
                      &#58;
                    </Typography>
                    <Typography variant="body2" sx={infoSX}>
                      {`${defaultValues.first_name} ${defaultValues.last_name}`}
                    </Typography>
                  </Stack>
                )}
                <Stack
                  direction="row"
                  spacing={2}
                  sx={{ alignItems: 'center' }}
                >
                  <Typography variant="subtitle1" sx={labelSX}>
                    <FormattedMessage id="users.labels.username" />
                    &#58;
                  </Typography>
                  <Typography variant="body2" sx={infoSX}>
                    {defaultValues!.username}
                  </Typography>
                </Stack>
                {defaultValues?.email && (
                  <Stack
                    direction="row"
                    spacing={2}
                    sx={{ alignItems: 'center' }}
                  >
                    <Typography variant="subtitle1" sx={labelSX}>
                      <FormattedMessage id="users.labels.email" />
                      &#58;
                    </Typography>
                    <Typography variant="body2" sx={infoSX}>
                      <EmailTwoTone sx={iconSX} />
                      {defaultValues.email}
                    </Typography>
                  </Stack>
                )}
                <Stack
                  direction="row"
                  spacing={2}
                  sx={{ alignItems: 'center' }}
                >
                  <Typography variant="subtitle1" sx={labelSX}>
                    <FormattedMessage id="users.labels.userType" />
                    &#58;
                  </Typography>
                  <Typography variant="body2" sx={infoSX}>
                    {userTypeMap.get(defaultValues!.user_type)?.icon}
                    <FormattedMessage
                      id={userTypeMap.get(defaultValues!.user_type)?.label}
                    />
                  </Typography>
                </Stack>
                <Stack
                  direction="row"
                  spacing={2}
                  sx={{ alignItems: 'center' }}
                >
                  <Typography variant="subtitle1" sx={labelSX}>
                    <FormattedMessage id="users.labels.createdAt" />
                    &#58;
                  </Typography>
                  <Typography variant="body2" sx={infoSX}>
                    <DateRangeTwoTone sx={iconSX} color="info" />
                    {new Intl.DateTimeFormat(locale, {
                      dateStyle: 'full',
                      timeStyle: 'medium',
                    }).format(new Date(defaultValues!.created_at))}
                  </Typography>
                </Stack>
                <Stack
                  direction="row"
                  spacing={2}
                  sx={{ alignItems: 'center' }}
                >
                  <Typography variant="subtitle1" sx={labelSX}>
                    <FormattedMessage id="users.labels.lastModifiedAt" />
                    &#58;
                  </Typography>
                  <Typography variant="body2" sx={infoSX}>
                    <DateRangeTwoTone sx={iconSX} color="info" />
                    {new Intl.DateTimeFormat(locale, {
                      dateStyle: 'full',
                      timeStyle: 'medium',
                    }).format(new Date(defaultValues!.last_modified_at))}
                  </Typography>
                </Stack>
                <Stack
                  direction="row"
                  spacing={2}
                  sx={{ alignItems: 'center' }}
                >
                  <Typography variant="subtitle1" sx={labelSX}>
                    <FormattedMessage id="users.labels.lastModifiedBy" />
                    &#58;
                  </Typography>
                  <Typography variant="body2" sx={infoSX}>
                    {defaultValues!.last_modified_by}
                  </Typography>
                </Stack>
              </Stack>
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    </SubCard>
  )
}
