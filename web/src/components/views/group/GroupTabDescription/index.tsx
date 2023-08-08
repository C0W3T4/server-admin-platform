import { DateRangeTwoTone } from '@mui/icons-material'
import { Grid, Stack, Typography } from '@mui/material'
import { FormattedMessage } from 'react-intl'
import useConfig from '../../../../hooks/useConfig'
import { gridSpacing } from '../../../../libs/redux/constants'
import { DetailsViewProps } from '../../../../types'
import { GroupDataProps } from '../../../../types/group'
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

export const GroupTabDescription = ({
  defaultValues,
}: DetailsViewProps<GroupDataProps>) => {
  const { locale } = useConfig()

  return (
    <SubCard title={defaultValues?.name} secondary={<CardHeaderActions />}>
      <Grid container spacing={gridSpacing}>
        <Grid item xs={12}>
          <Grid container spacing={gridSpacing}>
            <Grid item xs={12} sm={12} md={12} lg={12} xl={12}>
              <Stack spacing={2}>
                <Stack
                  direction="row"
                  spacing={2}
                  sx={{ alignItems: 'center' }}
                >
                  <Typography variant="subtitle1" sx={labelSX}>
                    <FormattedMessage id="groups.labels.name" />
                    &#58;
                  </Typography>
                  <Typography variant="body2" sx={infoSX}>
                    {defaultValues!.name}
                  </Typography>
                </Stack>
                {defaultValues?.description && (
                  <Stack
                    direction="row"
                    spacing={2}
                    sx={{ alignItems: 'center' }}
                  >
                    <Typography variant="subtitle1" sx={labelSX}>
                      <FormattedMessage id="groups.labels.description" />
                      &#58;
                    </Typography>
                    <Typography variant="body2" sx={infoSX}>
                      {defaultValues.description}
                    </Typography>
                  </Stack>
                )}
                <Stack
                  direction="row"
                  spacing={2}
                  sx={{ alignItems: 'center' }}
                >
                  <Typography variant="subtitle1" sx={labelSX}>
                    <FormattedMessage id="groups.labels.organizationName" />
                    &#58;
                  </Typography>
                  <Typography variant="body2" sx={infoSX}>
                    {defaultValues!.organization.name}
                  </Typography>
                </Stack>
                <Stack
                  direction="row"
                  spacing={2}
                  sx={{ alignItems: 'center' }}
                >
                  <Typography variant="subtitle1" sx={labelSX}>
                    <FormattedMessage id="groups.labels.createdAt" />
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
                    <FormattedMessage id="groups.labels.lastModifiedAt" />
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
                    <FormattedMessage id="groups.labels.createdBy" />
                    &#58;
                  </Typography>
                  <Typography variant="body2" sx={infoSX}>
                    {defaultValues!.created_by}
                  </Typography>
                </Stack>
                <Stack
                  direction="row"
                  spacing={2}
                  sx={{ alignItems: 'center' }}
                >
                  <Typography variant="subtitle1" sx={labelSX}>
                    <FormattedMessage id="groups.labels.lastModifiedBy" />
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
