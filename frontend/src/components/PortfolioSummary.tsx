import React from 'react';
import { useState, useEffect } from 'react';
import { Box, Card, CardContent, Typography, Slider, styled } from '@mui/material';

interface SummaryStats {
  totalValue: number;
  riskAppetite: number;
  sustainability: number;
}

const StyledCard = styled(Card)({
  minWidth: 275,
  flex: '1 1 300px',
  backgroundColor: 'var(--card-bg)',
  borderRadius: '8px',
  border: '1px solid var(--border-color)',
  boxShadow: '0 2px 4px rgba(0, 0, 0, 0.3)',
});

const IntensitySlider = styled(Slider)({
  height: 8,
  marginTop: '24px',
  '& .MuiSlider-track': {
    background: 'linear-gradient(90deg, #ff0000 0%, #ffd700 50%, #00ff00 100%)',
    border: 'none',
  },
  '& .MuiSlider-rail': {
    backgroundColor: 'var(--border-color)',
  },
  '& .MuiSlider-thumb': {
    height: 24,
    width: 24,
    backgroundColor: 'transparent',
    '&:before': {
      content: '""',
      display: 'block',
      width: 0,
      height: 0,
      borderLeft: '12px solid transparent',
      borderRight: '12px solid transparent',
      borderBottom: '16px solid var(--accent-color)',
      transform: 'translateY(-8px)',
    },
  },
});

const PortfolioSummary = ({data, data2}) => {
  // Example case where holdings is null
  const total = Object.values(data2 ?? {}).reduce((sum, value) => sum + (value ?? 0), 0);
  const stats: SummaryStats = {
    totalValue: total,
    riskAppetite: data.total_risk,
    sustainability: data.total_ethics,
  };



  useEffect(() => {
    console.log(data.holdings);
  });



  return (
    <Box sx={{
      display: 'flex',
      gap: '20px',
      flexWrap: 'wrap',
      justifyContent: 'center',
      padding: '20px',
      backgroundColor: 'var(--card-bg)',
    }}>
      <StyledCard>
        <CardContent>
          <Typography variant="h6" sx={{ color: 'var(--accent-color)', mb: 2 }}>
            Total Value
          </Typography>
          <Typography variant="h4" sx={{ fontWeight: 'bold', color: 'var(--primary-text)' }}>
            ${stats.totalValue.toLocaleString()}
          </Typography>
        </CardContent>
      </StyledCard>

      <StyledCard>
        <CardContent>
          <Typography variant="h6" sx={{ color: 'var(--accent-color)', mb: 2 }}>
            Risk Appetite
          </Typography>
          <IntensitySlider
            value={stats.riskAppetite ?? 5}
            min={0}
            max={1}
            step={0.01}
            disabled
          />
          <Typography variant="caption" sx={{ color: 'var(--secondary-text)', display: 'block', mt: 1 }}>
            {stats.riskAppetite >= 0.6 ? 'High Risk' : 
             stats.riskAppetite >= 0.3 ? 'Moderate Risk' : 'Low Risk'}
          </Typography>
        </CardContent>
      </StyledCard>

      <StyledCard>
        <CardContent>
          <Typography variant="h6" sx={{ color: 'var(--accent-color)', mb: 2 }}>
            Sustainability
          </Typography>
          <IntensitySlider
            value={stats.sustainability ?? 5}
            min={0}
            max={1}
            step={0.01}
            disabled
          />
          <Typography variant="caption" sx={{ color: 'var(--secondary-text)', display: 'block', mt: 1 }}>
            {stats.sustainability >= 0.6 ? 'High Sustainability' : 
             stats.sustainability >= 0.3 ? 'Moderate Sustainability' : 'Low Sustainability'}
          </Typography>
        </CardContent>
      </StyledCard>
    </Box>
  );
};

export default PortfolioSummary;