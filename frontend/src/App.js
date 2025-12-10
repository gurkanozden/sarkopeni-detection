import React, { useState } from 'react';
import {
  Container,
  Paper,
  TextField,
  Button,
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  Alert,
  CircularProgress,
  LinearProgress,
} from '@mui/material';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

function App() {
  const [formData, setFormData] = useState({
    age: 72,
    sex: 'M',
    bmi: 26.5,
    grip_strength_max: 25.3,
    grip_strength_norm: 0.32,
    chair_stand_time: 15,
    gait_speed_m_s: 0.8,
    tug_time: 18,
    sppb_score: 7,
    asm_kg: 22.5,
    asmi_kg_m2: 8.2,
    sarc_f_score: 4,
    falls_last_year: 1,
    physical_activity_level: 'moderate',
    comorbidity_count: 2,
  });

  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'sex' || name === 'physical_activity_level' 
        ? value 
        : parseFloat(value) || value
    }));
  };

  const handlePredict = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post(`${API_URL}/predict`, formData);
      setPrediction(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Tahmin sırasında hata oluştu');
    } finally {
      setLoading(false);
    }
  };

  const getSarcopeniaLabel = (classNum) => {
    const labels = {
      '0': 'Normal (Sarkopeni Yok)',
      '1': 'Sarkopeni',
      '2': 'Şiddetli Sarkopeni'
    };
    return labels[classNum];
  };

  const getSarcopeniaColor = (classNum) => {
    const colors = {
      '0': '#4caf50', // Green
      '1': '#ff9800', // Orange
      '2': '#f44336'  // Red
    };
    return colors[classNum];
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h3" component="h1" gutterBottom sx={{ mb: 4, fontWeight: 'bold' }}>
        🏥 Sarkopeni Tespiti Sistemi
      </Typography>
      <Typography variant="subtitle1" gutterBottom sx={{ mb: 4, color: 'text.secondary' }}>
        EWGSOP2 kriterlerine dayalı yapay öğrenme ile sarkopeni tahminleme
      </Typography>

      <Grid container spacing={3}>
        {/* Sol kolon - Giriş Formu */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom sx={{ mb: 3 }}>
              📋 Hasta Bilgileri
            </Typography>

            <Box sx={{ display: 'grid', gap: 2 }}>
              {/* Demografik */}
              <Box sx={{ p: 2, bgcolor: '#f5f5f5', borderRadius: 1 }}>
                <Typography variant="subtitle2" sx={{ fontWeight: 'bold', mb: 2 }}>
                  Demografik Bilgiler
                </Typography>
                <Grid container spacing={2}>
                  <Grid item xs={6}>
                    <TextField
                      fullWidth
                      label="Yaş"
                      name="age"
                      type="number"
                      value={formData.age}
                      onChange={handleInputChange}
                      size="small"
                    />
                  </Grid>
                  <Grid item xs={6}>
                    <TextField
                      fullWidth
                      label="Cinsiyet"
                      name="sex"
                      select
                      value={formData.sex}
                      onChange={handleInputChange}
                      size="small"
                      SelectProps={{
                        native: true,
                      }}
                    >
                      <option value="M">Erkek</option>
                      <option value="F">Kadın</option>
                    </TextField>
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      label="BMI (kg/m²)"
                      name="bmi"
                      type="number"
                      value={formData.bmi}
                      onChange={handleInputChange}
                      size="small"
                      step="0.1"
                    />
                  </Grid>
                </Grid>
              </Box>

              {/* Kas Gücü */}
              <Box sx={{ p: 2, bgcolor: '#f5f5f5', borderRadius: 1 }}>
                <Typography variant="subtitle2" sx={{ fontWeight: 'bold', mb: 2 }}>
                  Kas Gücü
                </Typography>
                <Grid container spacing={2}>
                  <Grid item xs={6}>
                    <TextField
                      fullWidth
                      label="Kavrama Gücü (kg)"
                      name="grip_strength_max"
                      type="number"
                      value={formData.grip_strength_max}
                      onChange={handleInputChange}
                      size="small"
                      step="0.1"
                    />
                  </Grid>
                  <Grid item xs={6}>
                    <TextField
                      fullWidth
                      label="Sandalyeden Kalma (s)"
                      name="chair_stand_time"
                      type="number"
                      value={formData.chair_stand_time}
                      onChange={handleInputChange}
                      size="small"
                      step="0.1"
                    />
                  </Grid>
                </Grid>
              </Box>

              {/* Kas Kütlesi */}
              <Box sx={{ p: 2, bgcolor: '#f5f5f5', borderRadius: 1 }}>
                <Typography variant="subtitle2" sx={{ fontWeight: 'bold', mb: 2 }}>
                  Kas Kütlesi
                </Typography>
                <Grid container spacing={2}>
                  <Grid item xs={6}>
                    <TextField
                      fullWidth
                      label="ASM (kg)"
                      name="asm_kg"
                      type="number"
                      value={formData.asm_kg}
                      onChange={handleInputChange}
                      size="small"
                      step="0.1"
                    />
                  </Grid>
                  <Grid item xs={6}>
                    <TextField
                      fullWidth
                      label="ASMI (kg/m²)"
                      name="asmi_kg_m2"
                      type="number"
                      value={formData.asmi_kg_m2}
                      onChange={handleInputChange}
                      size="small"
                      step="0.1"
                    />
                  </Grid>
                </Grid>
              </Box>

              {/* Fiziksel Performans */}
              <Box sx={{ p: 2, bgcolor: '#f5f5f5', borderRadius: 1 }}>
                <Typography variant="subtitle2" sx={{ fontWeight: 'bold', mb: 2 }}>
                  Fiziksel Performans
                </Typography>
                <Grid container spacing={2}>
                  <Grid item xs={4}>
                    <TextField
                      fullWidth
                      label="Yürüyüş (m/s)"
                      name="gait_speed_m_s"
                      type="number"
                      value={formData.gait_speed_m_s}
                      onChange={handleInputChange}
                      size="small"
                      step="0.1"
                    />
                  </Grid>
                  <Grid item xs={4}>
                    <TextField
                      fullWidth
                      label="TUG (s)"
                      name="tug_time"
                      type="number"
                      value={formData.tug_time}
                      onChange={handleInputChange}
                      size="small"
                      step="0.1"
                    />
                  </Grid>
                  <Grid item xs={4}>
                    <TextField
                      fullWidth
                      label="SPPB"
                      name="sppb_score"
                      type="number"
                      value={formData.sppb_score}
                      onChange={handleInputChange}
                      size="small"
                      step="1"
                      inputProps={{ min: 0, max: 12 }}
                    />
                  </Grid>
                </Grid>
              </Box>

              {/* Ek Bilgiler */}
              <Box sx={{ p: 2, bgcolor: '#f5f5f5', borderRadius: 1 }}>
                <Typography variant="subtitle2" sx={{ fontWeight: 'bold', mb: 2 }}>
                  Ek Bilgiler
                </Typography>
                <Grid container spacing={2}>
                  <Grid item xs={6}>
                    <TextField
                      fullWidth
                      label="SARC-F Skoru"
                      name="sarc_f_score"
                      type="number"
                      value={formData.sarc_f_score}
                      onChange={handleInputChange}
                      size="small"
                      step="1"
                      inputProps={{ min: 0, max: 10 }}
                    />
                  </Grid>
                  <Grid item xs={6}>
                    <TextField
                      fullWidth
                      label="Düşme (son 1 yıl)"
                      name="falls_last_year"
                      type="number"
                      value={formData.falls_last_year}
                      onChange={handleInputChange}
                      size="small"
                      step="1"
                      inputProps={{ min: 0 }}
                    />
                  </Grid>
                  <Grid item xs={6}>
                    <TextField
                      fullWidth
                      label="Fiziksel Aktivite"
                      name="physical_activity_level"
                      select
                      value={formData.physical_activity_level}
                      onChange={handleInputChange}
                      size="small"
                      SelectProps={{
                        native: true,
                      }}
                    >
                      <option value="low">Düşük</option>
                      <option value="moderate">Orta</option>
                      <option value="high">Yüksek</option>
                    </TextField>
                  </Grid>
                  <Grid item xs={6}>
                    <TextField
                      fullWidth
                      label="Komorbidite Sayısı"
                      name="comorbidity_count"
                      type="number"
                      value={formData.comorbidity_count}
                      onChange={handleInputChange}
                      size="small"
                      step="1"
                      inputProps={{ min: 0 }}
                    />
                  </Grid>
                </Grid>
              </Box>

              <Button
                fullWidth
                variant="contained"
                size="large"
                onClick={handlePredict}
                disabled={loading}
                sx={{
                  bgcolor: '#1976d2',
                  '&:hover': { bgcolor: '#1565c0' },
                  py: 1.5
                }}
              >
                {loading ? <CircularProgress size={24} /> : '🔍 Tahmini Yap'}
              </Button>
            </Box>
          </Paper>
        </Grid>

        {/* Sağ kolon - Sonuçlar */}
        <Grid item xs={12} md={6}>
          <Box sx={{ display: 'grid', gap: 3 }}>
            {error && (
              <Alert severity="error">{error}</Alert>
            )}

            {prediction && (
              <>
                {/* Ana Tahmin */}
                <Card sx={{
                  background: `linear-gradient(135deg, ${getSarcopeniaColor(prediction.predicted_class)}40 0%, ${getSarcopeniaColor(prediction.predicted_class)}20 100%)`,
                  borderLeft: `4px solid ${getSarcopeniaColor(prediction.predicted_class)}`
                }}>
                  <CardContent>
                    <Typography color="textSecondary" gutterBottom>
                      TAHMINI SONUÇ
                    </Typography>
                    <Typography variant="h4" sx={{
                      fontWeight: 'bold',
                      color: getSarcopeniaColor(prediction.predicted_class),
                      mb: 2
                    }}>
                      {getSarcopeniaLabel(prediction.predicted_class)}
                    </Typography>
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="body2" sx={{ mb: 1 }}>
                        Güven Skoru: {(prediction.confidence * 100).toFixed(1)}%
                      </Typography>
                      <LinearProgress
                        variant="determinate"
                        value={prediction.confidence * 100}
                        sx={{
                          height: 8,
                          borderRadius: 4,
                          backgroundColor: '#e0e0e0',
                          '& .MuiLinearProgress-bar': {
                            backgroundColor: getSarcopeniaColor(prediction.predicted_class)
                          }
                        }}
                      />
                    </Box>
                    <Typography variant="body2" sx={{ fontStyle: 'italic', color: 'text.secondary' }}>
                      {prediction.recommendation}
                    </Typography>
                  </CardContent>
                </Card>

                {/* Olasılık Dağılımı */}
                <Card>
                  <CardContent>
                    <Typography color="textSecondary" gutterBottom>
                      SINIF OLASILIKLARI
                    </Typography>
                    <Box sx={{ display: 'grid', gap: 2, mt: 2 }}>
                      <Box>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                          <Typography variant="body2">Normal (Sarkopeni Yok)</Typography>
                          <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                            {(prediction.probability_class_0 * 100).toFixed(1)}%
                          </Typography>
                        </Box>
                        <LinearProgress
                          variant="determinate"
                          value={prediction.probability_class_0 * 100}
                          sx={{
                            backgroundColor: '#e8f5e9',
                            '& .MuiLinearProgress-bar': { backgroundColor: '#4caf50' }
                          }}
                        />
                      </Box>
                      <Box>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                          <Typography variant="body2">Sarkopeni</Typography>
                          <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                            {(prediction.probability_class_1 * 100).toFixed(1)}%
                          </Typography>
                        </Box>
                        <LinearProgress
                          variant="determinate"
                          value={prediction.probability_class_1 * 100}
                          sx={{
                            backgroundColor: '#fff3e0',
                            '& .MuiLinearProgress-bar': { backgroundColor: '#ff9800' }
                          }}
                        />
                      </Box>
                      <Box>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                          <Typography variant="body2">Şiddetli Sarkopeni</Typography>
                          <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                            {(prediction.probability_class_2 * 100).toFixed(1)}%
                          </Typography>
                        </Box>
                        <LinearProgress
                          variant="determinate"
                          value={prediction.probability_class_2 * 100}
                          sx={{
                            backgroundColor: '#ffebee',
                            '& .MuiLinearProgress-bar': { backgroundColor: '#f44336' }
                          }}
                        />
                      </Box>
                    </Box>
                  </CardContent>
                </Card>

                {/* Alt Kriterler */}
                {(prediction.low_strength_pred !== null || 
                  prediction.low_mass_pred !== null || 
                  prediction.low_performance_pred !== null) && (
                  <Card>
                    <CardContent>
                      <Typography color="textSecondary" gutterBottom>
                        ALT KRİTERLER ANALİZİ
                      </Typography>
                      <Box sx={{ display: 'grid', gap: 1, mt: 2 }}>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', p: 1, bgcolor: '#f5f5f5', borderRadius: 1 }}>
                          <Typography variant="body2">Düşük Kas Gücü</Typography>
                          <Typography variant="body2" sx={{
                            fontWeight: 'bold',
                            color: prediction.low_strength_pred ? '#f44336' : '#4caf50'
                          }}>
                            {prediction.low_strength_pred ? '✓ VAR' : '✗ YOK'}
                          </Typography>
                        </Box>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', p: 1, bgcolor: '#f5f5f5', borderRadius: 1 }}>
                          <Typography variant="body2">Düşük Kas Kütlesi</Typography>
                          <Typography variant="body2" sx={{
                            fontWeight: 'bold',
                            color: prediction.low_mass_pred ? '#f44336' : '#4caf50'
                          }}>
                            {prediction.low_mass_pred ? '✓ VAR' : '✗ YOK'}
                          </Typography>
                        </Box>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', p: 1, bgcolor: '#f5f5f5', borderRadius: 1 }}>
                          <Typography variant="body2">Düşük Fiziksel Performans</Typography>
                          <Typography variant="body2" sx={{
                            fontWeight: 'bold',
                            color: prediction.low_performance_pred ? '#f44336' : '#4caf50'
                          }}>
                            {prediction.low_performance_pred ? '✓ VAR' : '✗ YOK'}
                          </Typography>
                        </Box>
                      </Box>
                    </CardContent>
                  </Card>
                )}
              </>
            )}

            {!prediction && !error && (
              <Paper sx={{ p: 4, textAlign: 'center', bgcolor: '#f5f5f5' }}>
                <Typography variant="body1" color="textSecondary">
                  👉 Hasta bilgilerini girerek tahmini yapınız
                </Typography>
              </Paper>
            )}
          </Box>
        </Grid>
      </Grid>

      {/* Footer */}
      <Box sx={{ mt: 6, pt: 3, borderTop: '1px solid #e0e0e0', textAlign: 'center', color: 'text.secondary' }}>
        <Typography variant="caption">
          Sarkopeni Tespiti Sistemi v1.0 | EWGSOP2 Kriterleri | 
          ⚠️ Tıbbi Karar Verme Amacıyla Kullanılmaz
        </Typography>
      </Box>
    </Container>
  );
}

export default App;
