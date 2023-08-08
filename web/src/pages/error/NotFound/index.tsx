import HomeTwoToneIcon from '@mui/icons-material/HomeTwoTone'
import {
  Button,
  Card,
  CardContent,
  CardMedia,
  Grid,
  Typography,
} from '@mui/material'
import { styled, useTheme } from '@mui/material/styles'
import { FormattedMessage, useIntl } from 'react-intl'
import { Link } from 'react-router-dom'
import imageDarkBackground from '../../../assets/images/img-error-bg-dark.svg'
import imageBackground from '../../../assets/images/img-error-bg.svg'
import imageBlue from '../../../assets/images/img-error-blue.svg'
import imagePurple from '../../../assets/images/img-error-purple.svg'
import imageText from '../../../assets/images/img-error-text.svg'
import { AnimateButton } from '../../../components/AnimateButton'
import { DASHBOARD_PATH } from '../../../configs/defaultConfig'
import { gridSpacing } from '../../../libs/redux/constants'

const CardMediaWrapper = styled('div')({
  maxWidth: 720,
  margin: '0 auto',
  position: 'relative',
})

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

const CardMediaBlock = styled('img')({
  position: 'absolute',
  top: 0,
  left: 0,
  width: '100%',
  animation: '3s bounce ease-in-out infinite',
})

const CardMediaBlue = styled('img')({
  position: 'absolute',
  top: 0,
  left: 0,
  width: '100%',
  animation: '15s wings ease-in-out infinite',
})

const CardMediaPurple = styled('img')({
  position: 'absolute',
  top: 0,
  left: 0,
  width: '100%',
  animation: '12s wings ease-in-out infinite',
})

const Error = () => {
  const theme = useTheme()
  const { formatMessage } = useIntl()

  return (
    <ErrorCard>
      <CardContent>
        <Grid container justifyContent="center" spacing={gridSpacing}>
          <Grid item xs={12}>
            <CardMediaWrapper>
              <CardMedia
                component="img"
                image={
                  theme.palette.mode === 'dark'
                    ? imageDarkBackground
                    : imageBackground
                }
                alt="Slider 5 image"
                title={formatMessage({ id: 'tooltips.notFound' })}
              />
              <CardMediaBlock
                src={imageText}
                alt="Slider 1 image"
                title={formatMessage({ id: 'tooltips.notFound' })}
              />
              <CardMediaBlue
                src={imageBlue}
                alt="Slider 2 image"
                title={formatMessage({ id: 'tooltips.notFound' })}
              />
              <CardMediaPurple
                src={imagePurple}
                alt="Slider 3 image"
                title={formatMessage({ id: 'tooltips.notFound' })}
              />
            </CardMediaWrapper>
          </Grid>
          <Grid item xs={12}>
            <ErrorWrapper>
              <Grid container spacing={gridSpacing}>
                <Grid item xs={12}>
                  <Typography variant="h1" component="div">
                    <FormattedMessage id="maintenance.labels.somethingWrong" />
                  </Typography>
                </Grid>
                <Grid item xs={12}>
                  <Typography variant="body2">
                    <FormattedMessage id="maintenance.labels.pageNotFound" />
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

export default Error
