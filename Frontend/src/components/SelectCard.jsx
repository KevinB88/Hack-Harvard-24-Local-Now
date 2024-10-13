
import Card from '@mui/material/Card';
 import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';  // Ensure Box is imported and capitalized

export default function SelectCard() {
  return (
    
    <Card sx={{ display: 'flex' }}>
      <CardMedia
        component="img"
        sx={{ width: 200, height: 'auto', objectFit: 'cover' }}
        image="https://res.cloudinary.com/grubhub/image/upload/d_search:browse-images:default.jpg/w_auto,q_auto:low,fl_lossy,dpr_2.0,c_pad,f_auto,h_168/pcizrfonnwrelygiynw2"
        alt="green iguana"
      />
      
      {/* Capitalize Box and structure correctly */}
      <Box sx={{ display: 'flex', flexDirection: 'column', flex: 1 }}>
        <CardContent>
          <Typography component="div" variant="h5">
            Item
          </Typography>
          <Typography variant="body2" sx={{ color: 'text.secondary' }}>
            Item description
          </Typography>
        </CardContent>

        {/* Correct Box for the button to be in the bottom-right corner */}
        <Box sx={{ display: 'flex', justifyContent: 'flex-end', p: 2, marginTop: '100px'}}>
          <Button size="small">Select</Button>
        </Box>
      </Box>
    </Card>
  );
}
