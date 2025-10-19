import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Grid,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  IconButton,
  Paper,
  Divider,
  Avatar,
  Tooltip,
  Alert
} from '@mui/material';
import {
  Add as AddIcon,
  AccountTree as WorkflowIcon,
  PlayArrow as PlayIcon,
  Pause as PauseIcon,
  Stop as StopIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Timeline as TimelineIcon,
  Assignment as AssignmentIcon,
  Groups as GroupsIcon,
  AutoFixHigh as AutoIcon,
  Psychology as PsychologyIcon,
  Engineering as EngineeringIcon,
  School as SchoolIcon,
  Security as SecurityIcon,
  Assessment as AssessmentIcon,
  Message as MessageIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Schedule as ScheduleIcon
} from '@mui/icons-material';

interface WorkflowStep {
  id: string;
  name: string;
  type: 'agent-task' | 'decision' | 'parallel' | 'sequential' | 'condition';
  agentType?: string;
  dependencies: string[];
  status: 'pending' | 'running' | 'completed' | 'failed';
  description: string;
  estimatedTime: number;
  actualTime?: number;
}

interface Workflow {
  id: string;
  name: string;
  description: string;
  status: 'draft' | 'active' | 'paused' | 'completed' | 'failed';
  steps: WorkflowStep[];
  createdAt: string;
  lastModified: string;
  totalSteps: number;
  completedSteps: number;
  estimatedDuration: number;
  actualDuration?: number;
}

const WorkflowDesigner: React.FC = () => {
  const [workflows, setWorkflows] = useState<Workflow[]>([
    {
      id: 'wf-001',
      name: 'Research Paper Analysis Pipeline',
      description: 'Automated pipeline for analyzing research papers with multiple AI agents',
      status: 'active',
      steps: [
        {
          id: 'step-001',
          name: 'Document Ingestion',
          type: 'agent-task',
          agentType: 'Research',
          dependencies: [],
          status: 'completed',
          description: 'Parse and extract content from uploaded documents',
          estimatedTime: 10,
          actualTime: 8
        },
        {
          id: 'step-002',
          name: 'Content Analysis',
          type: 'parallel',
          dependencies: ['step-001'],
          status: 'running',
          description: 'Parallel analysis of different document sections',
          estimatedTime: 30
        },
        {
          id: 'step-003',
          name: 'Summary Generation',
          type: 'agent-task',
          agentType: 'Analytics',
          dependencies: ['step-002'],
          status: 'pending',
          description: 'Generate comprehensive summary and insights',
          estimatedTime: 15
        }
      ],
      createdAt: '2025-10-19T08:00:00Z',
      lastModified: '2025-10-19T15:30:00Z',
      totalSteps: 3,
      completedSteps: 1,
      estimatedDuration: 55,
      actualDuration: 38
    },
    {
      id: 'wf-002',
      name: 'Code Review and Testing',
      description: 'Comprehensive code review workflow with automated testing',
      status: 'draft',
      steps: [
        {
          id: 'step-004',
          name: 'Code Analysis',
          type: 'agent-task',
          agentType: 'Engineering',
          dependencies: [],
          status: 'pending',
          description: 'Static code analysis and quality checks',
          estimatedTime: 20
        },
        {
          id: 'step-005',
          name: 'Security Audit',
          type: 'agent-task',
          agentType: 'Security',
          dependencies: ['step-004'],
          status: 'pending',
          description: 'Security vulnerability assessment',
          estimatedTime: 25
        }
      ],
      createdAt: '2025-10-19T10:00:00Z',
      lastModified: '2025-10-19T14:00:00Z',
      totalSteps: 2,
      completedSteps: 0,
      estimatedDuration: 45
    }
  ]);

  const [openWorkflowDialog, setOpenWorkflowDialog] = useState(false);
  const [selectedWorkflow, setSelectedWorkflow] = useState<Workflow | null>(null);
  const [openStepDialog, setOpenStepDialog] = useState(false);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'success';
      case 'running': return 'primary';
      case 'completed': return 'success';
      case 'failed': return 'error';
      case 'paused': return 'warning';
      case 'draft': return 'default';
      default: return 'default';
    }
  };

  const getStepStatusIcon = (status: string) => {
    switch (status) {
      case 'completed': return <CheckCircleIcon color="success" />;
      case 'running': return <PlayIcon color="primary" />;
      case 'failed': return <ErrorIcon color="error" />;
      default: return <ScheduleIcon color="disabled" />;
    }
  };

  const getAgentIcon = (type?: string) => {
    switch (type) {
      case 'Research': return <SchoolIcon />;
      case 'Engineering': return <EngineeringIcon />;
      case 'Analytics': return <AssessmentIcon />;
      case 'Communication': return <MessageIcon />;
      case 'Security': return <SecurityIcon />;
      default: return <PsychologyIcon />;
    }
  };

  const handleCreateWorkflow = () => {
    setOpenWorkflowDialog(true);
  };

  const handleEditWorkflow = (workflow: Workflow) => {
    setSelectedWorkflow(workflow);
    setOpenWorkflowDialog(true);
  };

  return (
    <Box>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h5" fontWeight="bold">
          <WorkflowIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
          Workflow Designer
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={handleCreateWorkflow}
        >
          Create Workflow
        </Button>
      </Box>

      {/* Workflow Templates */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Quick Start Templates
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6} md={3}>
              <Paper sx={{ p: 2, textAlign: 'center', cursor: 'pointer', '&:hover': { bgcolor: 'action.hover' } }}>
                <SchoolIcon sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
                <Typography variant="subtitle2">Research Pipeline</Typography>
                <Typography variant="caption" color="text.secondary">
                  Document analysis and summarization
                </Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Paper sx={{ p: 2, textAlign: 'center', cursor: 'pointer', '&:hover': { bgcolor: 'action.hover' } }}>
                <EngineeringIcon sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
                <Typography variant="subtitle2">Code Review</Typography>
                <Typography variant="caption" color="text.secondary">
                  Automated code analysis and testing
                </Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Paper sx={{ p: 2, textAlign: 'center', cursor: 'pointer', '&:hover': { bgcolor: 'action.hover' } }}>
                <AssessmentIcon sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
                <Typography variant="subtitle2">Data Processing</Typography>
                <Typography variant="caption" color="text.secondary">
                  ETL and analytics workflow
                </Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Paper sx={{ p: 2, textAlign: 'center', cursor: 'pointer', '&:hover': { bgcolor: 'action.hover' } }}>
                <AutoIcon sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
                <Typography variant="subtitle2">Custom Workflow</Typography>
                <Typography variant="caption" color="text.secondary">
                  Build from scratch
                </Typography>
              </Paper>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Active Workflows */}
      <Grid container spacing={3}>
        {workflows.map((workflow) => (
          <Grid item xs={12} lg={6} key={workflow.id}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', mb: 2 }}>
                  <Box>
                    <Typography variant="h6" fontWeight="bold">
                      {workflow.name}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      {workflow.description}
                    </Typography>
                    <Chip 
                      label={workflow.status} 
                      size="small" 
                      color={getStatusColor(workflow.status) as any}
                    />
                  </Box>
                  <Box sx={{ display: 'flex', gap: 0.5 }}>
                    <Tooltip title="Edit Workflow">
                      <IconButton size="small" onClick={() => handleEditWorkflow(workflow)}>
                        <EditIcon />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title="Play Workflow">
                      <IconButton size="small" color="success">
                        <PlayIcon />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title="Pause Workflow">
                      <IconButton size="small" color="warning">
                        <PauseIcon />
                      </IconButton>
                    </Tooltip>
                  </Box>
                </Box>

                {/* Progress */}
                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" color="text.secondary">
                    Progress: {workflow.completedSteps}/{workflow.totalSteps} steps
                  </Typography>
                  <Box sx={{ width: '100%', bgcolor: 'grey.200', borderRadius: 1, height: 6, mt: 0.5 }}>
                    <Box
                      sx={{
                        width: `${(workflow.completedSteps / workflow.totalSteps) * 100}%`,
                        bgcolor: 'primary.main',
                        height: '100%',
                        borderRadius: 1
                      }}
                    />
                  </Box>
                </Box>

                {/* Workflow Steps */}
                <Typography variant="subtitle2" gutterBottom>
                  Workflow Steps
                </Typography>
                <List dense>
                  {workflow.steps.map((step, index) => (
                    <ListItem key={step.id} sx={{ pl: 0 }}>
                      <ListItemIcon sx={{ minWidth: 36 }}>
                        {getStepStatusIcon(step.status)}
                      </ListItemIcon>
                      <ListItemText
                        primary={
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <Typography variant="body2">{step.name}</Typography>
                            {step.agentType && (
                              <Avatar sx={{ width: 20, height: 20 }}>
                                {getAgentIcon(step.agentType)}
                              </Avatar>
                            )}
                          </Box>
                        }
                        secondary={
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <Typography variant="caption" color="text.secondary">
                              {step.description}
                            </Typography>
                            <Chip label={step.type} size="small" variant="outlined" />
                          </Box>
                        }
                      />
                    </ListItem>
                  ))}
                </List>

                <Divider sx={{ my: 2 }} />

                {/* Workflow Stats */}
                <Grid container spacing={2}>
                  <Grid item xs={6}>
                    <Typography variant="caption" color="text.secondary">
                      Estimated Duration
                    </Typography>
                    <Typography variant="body2">
                      {workflow.estimatedDuration} min
                    </Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography variant="caption" color="text.secondary">
                      {workflow.actualDuration ? 'Actual Duration' : 'Elapsed Time'}
                    </Typography>
                    <Typography variant="body2">
                      {workflow.actualDuration || 38} min
                    </Typography>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Create/Edit Workflow Dialog */}
      <Dialog open={openWorkflowDialog} onClose={() => setOpenWorkflowDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>
          {selectedWorkflow ? 'Edit Workflow' : 'Create New Workflow'}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 2 }}>
            <TextField
              fullWidth
              label="Workflow Name"
              placeholder="Enter workflow name"
              defaultValue={selectedWorkflow?.name || ''}
              sx={{ mb: 2 }}
            />
            <TextField
              fullWidth
              label="Description"
              placeholder="Enter workflow description"
              defaultValue={selectedWorkflow?.description || ''}
              multiline
              rows={3}
              sx={{ mb: 2 }}
            />
            
            <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
              Workflow Steps
            </Typography>
            
            {selectedWorkflow?.steps.map((step, index) => (
              <Paper key={step.id} sx={{ p: 2, mb: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                  <Typography variant="subtitle2">
                    Step {index + 1}: {step.name}
                  </Typography>
                  <Box>
                    <IconButton size="small" onClick={() => setOpenStepDialog(true)}>
                      <EditIcon />
                    </IconButton>
                    <IconButton size="small" color="error">
                      <DeleteIcon />
                    </IconButton>
                  </Box>
                </Box>
                <Typography variant="body2" color="text.secondary">
                  {step.description}
                </Typography>
                <Box sx={{ display: 'flex', gap: 1, mt: 1 }}>
                  <Chip label={step.type} size="small" />
                  {step.agentType && <Chip label={step.agentType} size="small" variant="outlined" />}
                  <Chip label={`${step.estimatedTime} min`} size="small" color="info" />
                </Box>
              </Paper>
            ))}
            
            <Button
              variant="outlined"
              startIcon={<AddIcon />}
              onClick={() => setOpenStepDialog(true)}
              fullWidth
            >
              Add Step
            </Button>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => {
            setOpenWorkflowDialog(false);
            setSelectedWorkflow(null);
          }}>
            Cancel
          </Button>
          <Button variant="contained" onClick={() => {
            setOpenWorkflowDialog(false);
            setSelectedWorkflow(null);
          }}>
            {selectedWorkflow ? 'Update' : 'Create'} Workflow
          </Button>
        </DialogActions>
      </Dialog>

      {/* Add/Edit Step Dialog */}
      <Dialog open={openStepDialog} onClose={() => setOpenStepDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Add Workflow Step</DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 2 }}>
            <TextField
              fullWidth
              label="Step Name"
              placeholder="Enter step name"
              sx={{ mb: 2 }}
            />
            <FormControl fullWidth sx={{ mb: 2 }}>
              <InputLabel>Step Type</InputLabel>
              <Select defaultValue="agent-task" label="Step Type">
                <MenuItem value="agent-task">Agent Task</MenuItem>
                <MenuItem value="decision">Decision Point</MenuItem>
                <MenuItem value="parallel">Parallel Execution</MenuItem>
                <MenuItem value="sequential">Sequential</MenuItem>
                <MenuItem value="condition">Conditional</MenuItem>
              </Select>
            </FormControl>
            <FormControl fullWidth sx={{ mb: 2 }}>
              <InputLabel>Agent Type</InputLabel>
              <Select defaultValue="Research" label="Agent Type">
                <MenuItem value="Research">Research Agent</MenuItem>
                <MenuItem value="Engineering">Engineering Agent</MenuItem>
                <MenuItem value="Analytics">Analytics Agent</MenuItem>
                <MenuItem value="Communication">Communication Agent</MenuItem>
                <MenuItem value="Security">Security Agent</MenuItem>
              </Select>
            </FormControl>
            <TextField
              fullWidth
              label="Description"
              placeholder="Enter step description"
              multiline
              rows={3}
              sx={{ mb: 2 }}
            />
            <TextField
              fullWidth
              label="Estimated Time (minutes)"
              type="number"
              defaultValue="15"
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenStepDialog(false)}>Cancel</Button>
          <Button variant="contained" onClick={() => setOpenStepDialog(false)}>
            Add Step
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default WorkflowDesigner;