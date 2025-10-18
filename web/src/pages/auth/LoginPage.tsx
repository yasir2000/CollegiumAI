import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  TextField,
  Button,
  Typography,
  Alert,
  CircularProgress,
  InputAdornment,
  IconButton,
  FormControlLabel,
  Checkbox,
} from '@mui/material';
import { Visibility, VisibilityOff, Email, Lock } from '@mui/icons-material';
import { useFormik } from 'formik';
import * as yup from 'yup';
import { RootState, AppDispatch } from '../../store';
import { loginUser, clearError } from '../../store/features/auth/authSlice';

const validationSchema = yup.object({
  email: yup
    .string()
    .email('Enter a valid email')
    .required('Email is required'),
  password: yup
    .string()
    .min(6, 'Password should be of minimum 6 characters length')
    .required('Password is required'),
});

const LoginPage: React.FC = () => {
  const [showPassword, setShowPassword] = useState(false);
  const dispatch = useDispatch<AppDispatch>();
  const navigate = useNavigate();
  
  const { isLoading, error } = useSelector((state: RootState) => state.auth);

  const formik = useFormik({
    initialValues: {
      email: '',
      password: '',
      rememberMe: false,
    },
    validationSchema: validationSchema,
    onSubmit: async (values) => {
      dispatch(clearError());
      try {
        const result = await dispatch(loginUser({
          email: values.email,
          password: values.password,
        }));
        
        if (loginUser.fulfilled.match(result)) {
          navigate('/dashboard');
        }
      } catch (error) {
        console.error('Login failed:', error);
      }
    },
  });

  const handleClickShowPassword = () => {
    setShowPassword(!showPassword);
  };

  return (
    <Box component="form" onSubmit={formik.handleSubmit} noValidate>
      <Typography
        variant="h5"
        component="h2"
        fontWeight="600"
        textAlign="center"
        mb={3}
        color="text.primary"
      >
        Sign In to Your Account
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <TextField
        fullWidth
        id="email"
        name="email"
        label="Email Address"
        type="email"
        value={formik.values.email}
        onChange={formik.handleChange}
        onBlur={formik.handleBlur}
        error={formik.touched.email && Boolean(formik.errors.email)}
        helperText={formik.touched.email && formik.errors.email}
        margin="normal"
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <Email color="action" />
            </InputAdornment>
          ),
        }}
      />

      <TextField
        fullWidth
        id="password"
        name="password"
        label="Password"
        type={showPassword ? 'text' : 'password'}
        value={formik.values.password}
        onChange={formik.handleChange}
        onBlur={formik.handleBlur}
        error={formik.touched.password && Boolean(formik.errors.password)}
        helperText={formik.touched.password && formik.errors.password}
        margin="normal"
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <Lock color="action" />
            </InputAdornment>
          ),
          endAdornment: (
            <InputAdornment position="end">
              <IconButton
                aria-label="toggle password visibility"
                onClick={handleClickShowPassword}
                edge="end"
              >
                {showPassword ? <VisibilityOff /> : <Visibility />}
              </IconButton>
            </InputAdornment>
          ),
        }}
      />

      <FormControlLabel
        control={
          <Checkbox
            checked={formik.values.rememberMe}
            onChange={formik.handleChange}
            name="rememberMe"
            color="primary"
          />
        }
        label="Remember me"
        sx={{ mt: 2, mb: 2 }}
      />

      <Button
        color="primary"
        variant="contained"
        fullWidth
        type="submit"
        disabled={isLoading}
        sx={{
          mt: 2,
          mb: 2,
          py: 1.5,
          fontWeight: 600,
          fontSize: '1.1rem',
        }}
      >
        {isLoading ? (
          <CircularProgress size={24} color="inherit" />
        ) : (
          'Sign In'
        )}
      </Button>

      <Box textAlign="center" mt={3}>
        <Typography variant="body2" color="text.secondary">
          Demo Credentials:
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
          <strong>Student:</strong> student@collegiumai.edu / password123
        </Typography>
        <Typography variant="body2" color="text.secondary">
          <strong>Faculty:</strong> professor@collegiumai.edu / password123
        </Typography>
        <Typography variant="body2" color="text.secondary">
          <strong>Admin:</strong> admin@collegiumai.edu / password123
        </Typography>
      </Box>
    </Box>
  );
};

export default LoginPage;