import HomeTwoToneIcon from '@mui/icons-material/HomeTwoTone'
import { Button, Card, CardContent, Grid, Typography } from '@mui/material'
import { styled } from '@mui/material/styles'
import { FormattedMessage } from 'react-intl'
import { Link } from 'react-router-dom'
import { AnimateButton } from '../../../components/AnimateButton'
import { DASHBOARD_PATH } from '../../../configs/defaultConfig'
import { gridSpacing } from '../../../libs/redux/constants'

const ErrorWrapper = styled('div')({
  maxWidth: 350,
  margin: '0 auto',
  textAlign: 'center',
})

const ErrorCard = styled(Card)({
  minHeight: '100vh',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
})

const Forbidden = () => {
  return (
    <ErrorCard>
      <CardContent>
        <Grid container justifyContent="center" spacing={gridSpacing}>
          <Grid item xs={12}>
            <ErrorWrapper>
              <Grid container spacing={gridSpacing}>
                <Grid item xs={12}>
                  <Typography variant="h1" color="red" component="div">
                    <FormattedMessage id="errors.403" />
                  </Typography>
                </Grid>
                <Grid item xs={12}>
                  <Typography variant="h1" component="div">
                    <FormattedMessage id="maintenance.labels.somethingWrong" />
                  </Typography>
                </Grid>
                <Grid item xs={12}>
                  <Typography variant="body2">
                    <FormattedMessage id="maintenance.labels.forbidden" />
                  </Typography>
                </Grid>
                <Grid item xs={12}>
                  <AnimateButton>
                    <Button
                      variant="contained"
                      size="large"
                      component={Link}
                      to={DASHBOARD_PATH}
                    >
                      <HomeTwoToneIcon sx={{ fontSize: '1.3rem', mr: 0.75 }} />
                      <FormattedMessage id="input.labels.home" />
                    </Button>
                  </AnimateButton>
                </Grid>
              </Grid>
            </ErrorWrapper>
          </Grid>
        </Grid>
      </CardContent>
    </ErrorCard>
  )
}

export default Forbidden
