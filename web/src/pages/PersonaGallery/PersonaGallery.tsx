import React, { useEffect, useState } from 'react';
import {
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  Button,
  Chip,
  Avatar,
  TextField,
  InputAdornment,
  Tab,
  Tabs,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  LinearProgress,
  Divider,
  Badge
} from '@mui/material';
import {
  Search as SearchIcon,
  School as SchoolIcon,
  Work as WorkIcon,
  Person as PersonIcon,
  Psychology as PsychologyIcon,
  Memory as MemoryIcon,
  Settings as SettingsIcon,
  TrendingUp as TrendingUpIcon
} from '@mui/icons-material';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../../store/store';
import { setCurrentPersona, setAvailablePersonas, PersonaType } from '../../store/slices/personaSlice';

// Mock persona data based on README requirements
const mockPersonas: PersonaType[] = [
  // Student Personas (27 types)
  {
    id: 'undergrad_freshman',
    name: 'Sarah Chen - Freshman',
    type: 'student',
    category: 'Undergraduate - Freshman',
    description: 'First-year student navigating college transition, needs academic and social support',
    cognitiveProfile: {
      attentionParams: { focus_depth: 0.6, distractibility: 0.7, multitasking: 0.4 },
      learningParams: { absorption_rate: 0.8, retention: 0.6, adaptation: 0.9 },
      decisionParams: { risk_tolerance: 0.5, confidence: 0.4, deliberation_time: 0.8 }
    },
    capabilities: ['Study planning', 'Course selection', 'Campus navigation', 'Time management'],
    supportAreas: ['Academic transition', 'Social integration', 'Study skills', 'Stress management']
  },
  {
    id: 'grad_student_phd',
    name: 'Dr. Marcus Rodriguez - PhD Candidate',
    type: 'student',
    category: 'Graduate - Doctoral',
    description: 'Advanced doctoral student conducting dissertation research in Computer Science',
    cognitiveProfile: {
      attentionParams: { focus_depth: 0.9, distractibility: 0.2, multitasking: 0.7 },
      learningParams: { absorption_rate: 0.9, retention: 0.9, adaptation: 0.8 },
      decisionParams: { risk_tolerance: 0.7, confidence: 0.8, deliberation_time: 0.9 }
    },
    capabilities: ['Research methodology', 'Data analysis', 'Academic writing', 'Conference presentations'],
    supportAreas: ['Dissertation planning', 'Research collaboration', 'Academic networking', 'Career development']
  },
  {
    id: 'international_student',
    name: 'Yuki Tanaka - International Student',
    type: 'student',
    category: 'International - Exchange',
    description: 'International exchange student from Japan, needs cultural and academic adaptation support',
    cognitiveProfile: {
      attentionParams: { focus_depth: 0.7, distractibility: 0.6, multitasking: 0.5 },
      learningParams: { absorption_rate: 0.7, retention: 0.7, adaptation: 0.9 },
      decisionParams: { risk_tolerance: 0.4, confidence: 0.5, deliberation_time: 0.7 }
    },
    capabilities: ['Language learning', 'Cultural adaptation', 'Academic writing', 'Cross-cultural communication'],
    supportAreas: ['Language support', 'Cultural integration', 'Academic conventions', 'Visa assistance']
  },
  // Faculty Personas (12 types)
  {
    id: 'assistant_professor',
    name: 'Prof. Emily Watson - Assistant Professor',
    type: 'faculty',
    category: 'Faculty - Assistant Professor',
    description: 'Early-career faculty member focused on research and teaching excellence',
    cognitiveProfile: {
      attentionParams: { focus_depth: 0.8, distractibility: 0.3, multitasking: 0.8 },
      learningParams: { absorption_rate: 0.8, retention: 0.8, adaptation: 0.7 },
      decisionParams: { risk_tolerance: 0.6, confidence: 0.7, deliberation_time: 0.8 }
    },
    capabilities: ['Curriculum design', 'Research planning', 'Grant writing', 'Mentoring'],
    supportAreas: ['Tenure preparation', 'Research funding', 'Teaching effectiveness', 'Work-life balance']
  },
  {
    id: 'department_chair',
    name: 'Prof. Michael Thompson - Department Chair',
    type: 'faculty',
    category: 'Faculty - Administration',
    description: 'Senior faculty member leading department operations and strategic planning',
    cognitiveProfile: {
      attentionParams: { focus_depth: 0.7, distractibility: 0.4, multitasking: 0.9 },
      learningParams: { absorption_rate: 0.7, retention: 0.8, adaptation: 0.6 },
      decisionParams: { risk_tolerance: 0.8, confidence: 0.9, deliberation_time: 0.6 }
    },
    capabilities: ['Strategic planning', 'Budget management', 'Faculty development', 'Policy implementation'],
    supportAreas: ['Leadership skills', 'Conflict resolution', 'Resource allocation', 'Accreditation']
  },
  // Staff Personas (12 types)
  {
    id: 'academic_advisor',
    name: 'Dr. Lisa Park - Academic Advisor',
    type: 'staff',
    category: 'Academic Support',
    description: 'Experienced academic advisor helping students with degree planning and academic success',
    cognitiveProfile: {
      attentionParams: { focus_depth: 0.8, distractibility: 0.2, multitasking: 0.7 },
      learningParams: { absorption_rate: 0.7, retention: 0.9, adaptation: 0.8 },
      decisionParams: { risk_tolerance: 0.5, confidence: 0.8, deliberation_time: 0.7 }
    },
    capabilities: ['Degree planning', 'Student counseling', 'Academic policies', 'Career guidance'],
    supportAreas: ['Student success', 'Retention strategies', 'Academic interventions', 'Policy updates']
  },
  {
    id: 'it_specialist',
    name: 'Alex Kim - IT Specialist',
    type: 'staff',
    category: 'Technical Support',
    description: 'Technology support specialist managing campus IT infrastructure and user support',
    cognitiveProfile: {
      attentionParams: { focus_depth: 0.9, distractibility: 0.1, multitasking: 0.8 },
      learningParams: { absorption_rate: 0.8, retention: 0.8, adaptation: 0.9 },
      decisionParams: { risk_tolerance: 0.7, confidence: 0.8, deliberation_time: 0.5 }
    },
    capabilities: ['System administration', 'Technical troubleshooting', 'Security management', 'User training'],
    supportAreas: ['Technology upgrades', 'Security protocols', 'User education', 'System optimization']
  }
];

const PersonaGallery: React.FC = () => {
  const dispatch = useDispatch();
  const { currentPersona, availablePersonas } = useSelector((state: RootState) => state.persona);
  
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedTab, setSelectedTab] = useState('all');
  const [selectedPersona, setSelectedPersona] = useState<PersonaType | null>(null);
  const [detailDialogOpen, setDetailDialogOpen] = useState(false);

  useEffect(() => {
    // Initialize with mock personas
    dispatch(setAvailablePersonas(mockPersonas));
  }, [dispatch]);

  const handlePersonaSelect = (persona: PersonaType) => {
    dispatch(setCurrentPersona(persona));
    setSelectedPersona(persona);
    setDetailDialogOpen(true);
  };

  const filteredPersonas = availablePersonas.filter(persona => {
    const matchesSearch = persona.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         persona.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         persona.category.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesTab = selectedTab === 'all' || persona.type === selectedTab;
    return matchesSearch && matchesTab;
  });

  const getPersonaIcon = (type: string) => {
    switch (type) {
      case 'student': return <SchoolIcon />;
      case 'faculty': return <WorkIcon />;
      case 'staff': return <PersonIcon />;
      default: return <PersonIcon />;
    }
  };

  const getPersonaColor = (type: string) => {
    switch (type) {
      case 'student': return 'primary';
      case 'faculty': return 'secondary';
      case 'staff': return 'success';
      default: return 'default';
    }
  };

  const personaCounts = {
    all: availablePersonas.length,
    student: availablePersonas.filter(p => p.type === 'student').length,
    faculty: availablePersonas.filter(p => p.type === 'faculty').length,
    staff: availablePersonas.filter(p => p.type === 'staff').length,
  };

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom fontWeight="bold">
          Persona Gallery
        </Typography>
        <Typography variant="h6" color="text.secondary" sx={{ mb: 3 }}>
          Explore 51+ University Personas with Advanced Cognitive Profiles
        </Typography>

        {/* Current Persona Banner */}
        {currentPersona && (
          <Card sx={{ mb: 3, background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <Avatar sx={{ bgcolor: 'rgba(255,255,255,0.2)', width: 60, height: 60 }}>
                  {getPersonaIcon(currentPersona.type)}
                </Avatar>
                <Box sx={{ flexGrow: 1 }}>
                  <Typography variant="h5" gutterBottom>
                    Active: {currentPersona.name}
                  </Typography>
                  <Typography variant="body1" sx={{ opacity: 0.9 }}>
                    {currentPersona.description}
                  </Typography>
                </Box>
                <Button 
                  variant="contained" 
                  onClick={() => setSelectedPersona(null)}
                  sx={{ bgcolor: 'rgba(255,255,255,0.2)', '&:hover': { bgcolor: 'rgba(255,255,255,0.3)' } }}
                >
                  View Details
                </Button>
              </Box>
            </CardContent>
          </Card>
        )}
      </Box>

      {/* Search and Filters */}
      <Box sx={{ mb: 4 }}>
        <TextField
          fullWidth
          placeholder="Search personas by name, description, or category..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon />
              </InputAdornment>
            ),
          }}
          sx={{ mb: 2 }}
        />

        <Tabs value={selectedTab} onChange={(_, newValue) => setSelectedTab(newValue)}>
          <Tab 
            label={
              <Badge badgeContent={personaCounts.all} color="primary">
                All Personas
              </Badge>
            } 
            value="all" 
          />
          <Tab 
            label={
              <Badge badgeContent={personaCounts.student} color="primary">
                Students
              </Badge>
            } 
            value="student" 
          />
          <Tab 
            label={
              <Badge badgeContent={personaCounts.faculty} color="secondary">
                Faculty
              </Badge>
            } 
            value="faculty" 
          />
          <Tab 
            label={
              <Badge badgeContent={personaCounts.staff} color="success">
                Staff
              </Badge>
            } 
            value="staff" 
          />
        </Tabs>
      </Box>

      {/* Persona Grid */}
      <Grid container spacing={3}>
        {filteredPersonas.map((persona) => (
          <Grid item xs={12} sm={6} md={4} lg={3} key={persona.id}>
            <Card 
              sx={{ 
                height: '100%', 
                cursor: 'pointer',
                transition: 'transform 0.2s, box-shadow 0.2s',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  boxShadow: 4
                },
                border: currentPersona?.id === persona.id ? 2 : 0,
                borderColor: 'primary.main'
              }}
              onClick={() => handlePersonaSelect(persona)}
            >
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Avatar 
                    sx={{ 
                      bgcolor: `${getPersonaColor(persona.type)}.main`, 
                      mr: 2,
                      width: 48,
                      height: 48
                    }}
                  >
                    {getPersonaIcon(persona.type)}
                  </Avatar>
                  <Box sx={{ flexGrow: 1 }}>
                    <Typography variant="h6" component="div" noWrap>
                      {persona.name.split(' - ')[0]}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" noWrap>
                      {persona.category}
                    </Typography>
                  </Box>
                </Box>

                <Typography variant="body2" color="text.secondary" sx={{ mb: 2, height: 40, overflow: 'hidden' }}>
                  {persona.description}
                </Typography>

                <Box sx={{ mb: 2 }}>
                  <Chip 
                    label={persona.type} 
                    color={getPersonaColor(persona.type) as any}
                    size="small"
                    sx={{ mr: 1 }}
                  />
                  {currentPersona?.id === persona.id && (
                    <Chip label="Active" color="success" size="small" />
                  )}
                </Box>

                <Box sx={{ mb: 2 }}>
                  <Typography variant="caption" color="text.secondary" gutterBottom>
                    Cognitive Profile
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                    <Chip 
                      icon={<PsychologyIcon />}
                      label={`Focus: ${(persona.cognitiveProfile.attentionParams.focus_depth * 100).toFixed(0)}%`}
                      size="small"
                      variant="outlined"
                    />
                    <Chip 
                      icon={<MemoryIcon />}
                      label={`Learning: ${(persona.cognitiveProfile.learningParams.absorption_rate * 100).toFixed(0)}%`}
                      size="small"
                      variant="outlined"
                    />
                  </Box>
                </Box>

                <Button 
                  fullWidth 
                  variant={currentPersona?.id === persona.id ? "contained" : "outlined"}
                  onClick={(e) => {
                    e.stopPropagation();
                    handlePersonaSelect(persona);
                  }}
                >
                  {currentPersona?.id === persona.id ? "Current Persona" : "Select Persona"}
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Persona Detail Dialog */}
      <Dialog 
        open={detailDialogOpen} 
        onClose={() => setDetailDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        {selectedPersona && (
          <>
            <DialogTitle>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <Avatar sx={{ bgcolor: `${getPersonaColor(selectedPersona.type)}.main` }}>
                  {getPersonaIcon(selectedPersona.type)}
                </Avatar>
                <Box>
                  <Typography variant="h5">{selectedPersona.name}</Typography>
                  <Typography variant="subtitle1" color="text.secondary">
                    {selectedPersona.category}
                  </Typography>
                </Box>
              </Box>
            </DialogTitle>
            
            <DialogContent>
              <Typography variant="body1" sx={{ mb: 3 }}>
                {selectedPersona.description}
              </Typography>

              <Typography variant="h6" gutterBottom>
                <SettingsIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                Cognitive Profile
              </Typography>
              
              <Grid container spacing={2} sx={{ mb: 3 }}>
                <Grid item xs={12} md={4}>
                  <Typography variant="subtitle2" gutterBottom>Attention Parameters</Typography>
                  {Object.entries(selectedPersona.cognitiveProfile.attentionParams).map(([key, value]) => (
                    <Box key={key} sx={{ mb: 1 }}>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                        <Typography variant="caption">{key.replace('_', ' ')}</Typography>
                        <Typography variant="caption">{(value * 100).toFixed(0)}%</Typography>
                      </Box>
                      <LinearProgress variant="determinate" value={value * 100} />
                    </Box>
                  ))}
                </Grid>
                
                <Grid item xs={12} md={4}>
                  <Typography variant="subtitle2" gutterBottom>Learning Parameters</Typography>
                  {Object.entries(selectedPersona.cognitiveProfile.learningParams).map(([key, value]) => (
                    <Box key={key} sx={{ mb: 1 }}>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                        <Typography variant="caption">{key.replace('_', ' ')}</Typography>
                        <Typography variant="caption">{(value * 100).toFixed(0)}%</Typography>
                      </Box>
                      <LinearProgress variant="determinate" value={value * 100} color="secondary" />
                    </Box>
                  ))}
                </Grid>
                
                <Grid item xs={12} md={4}>
                  <Typography variant="subtitle2" gutterBottom>Decision Parameters</Typography>
                  {Object.entries(selectedPersona.cognitiveProfile.decisionParams).map(([key, value]) => (
                    <Box key={key} sx={{ mb: 1 }}>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                        <Typography variant="caption">{key.replace('_', ' ')}</Typography>
                        <Typography variant="caption">{(value * 100).toFixed(0)}%</Typography>
                      </Box>
                      <LinearProgress variant="determinate" value={value * 100} color="success" />
                    </Box>
                  ))}
                </Grid>
              </Grid>

              <Divider sx={{ my: 2 }} />

              <Grid container spacing={2}>
                <Grid item xs={12} md={6}>
                  <Typography variant="h6" gutterBottom>
                    <TrendingUpIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                    Capabilities
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                    {selectedPersona.capabilities.map((capability, index) => (
                      <Chip key={index} label={capability} variant="outlined" />
                    ))}
                  </Box>
                </Grid>
                
                <Grid item xs={12} md={6}>
                  <Typography variant="h6" gutterBottom>
                    <PersonIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                    Support Areas
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                    {selectedPersona.supportAreas.map((area, index) => (
                      <Chip key={index} label={area} color="primary" variant="outlined" />
                    ))}
                  </Box>
                </Grid>
              </Grid>
            </DialogContent>
            
            <DialogActions>
              <Button onClick={() => setDetailDialogOpen(false)}>
                Close
              </Button>
              <Button 
                variant="contained" 
                onClick={() => {
                  dispatch(setCurrentPersona(selectedPersona));
                  setDetailDialogOpen(false);
                }}
              >
                Activate Persona
              </Button>
            </DialogActions>
          </>
        )}
      </Dialog>
    </Container>
  );
};

export default PersonaGallery;