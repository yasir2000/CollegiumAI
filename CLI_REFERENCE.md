# CollegiumAI CLI Reference
## Complete Command-Line Interface Documentation

### 🎓 Overview

CollegiumAI provides a professional command-line interface for managing AI-powered university operations. The CLI offers comprehensive tools for agent management, student services, academic administration, and system monitoring.

### 🚀 Quick Start

```bash
# Show main help
python collegiumai.py --help

# Show welcome screen with system overview
python collegiumai.py

# Run complete system demonstration
python collegiumai.py demo
```

### 🤖 Agent Management Commands

#### List Agents
```bash
# Basic agent list
python collegiumai.py agent list

# Detailed agent information
python collegiumai.py agent list --detailed
```

**Sample Output:**
```
🤖 CollegiumAI Agents
==================================================
Agent ID             Name                 Status     Provider
-----------------------------------------------------------------
academic_advisor     Academic Advisor     active     anthropic
student_services     Student Services     active     ollama
bologna_process      Bologna Process      active     openai
research_coordinator Research Coordinator idle       openai

📊 Total agents: 4
```

### 🎓 Student Management Commands

#### Student Enrollment
```bash
# Enroll new student
python collegiumai.py student enroll --name "Maria Rodriguez" --program "Computer Science"

# Short form
python collegiumai.py student enroll -n "John Doe" -p "Data Science"
```

**Sample Output:**
```
📝 Student Enrollment
👤 Student: Maria Rodriguez
🎓 Program: Computer Science
🔄 Processing enrollment...
✅ Student Maria Rodriguez enrolled successfully!
```

#### Student Transfer with ECTS Conversion
```bash
# Process transfer student
python collegiumai.py student transfer --student-id "2024001" --credits 150

# Short form
python collegiumai.py student transfer -id "2024001" -c 150
```

**Sample Output:**
```
🔄 Student Transfer
👤 Student ID: 2024001
📚 Credits: 150
🤖 Bologna Process Agent analyzing...
✅ Converted: 150 ECTS → 100 US credits
```

### ⚙️ System Administration Commands

#### System Status
```bash
# Check overall system health
python collegiumai.py system status
```

**Sample Output:**
```
📊 CollegiumAI System Status
==================================================
🤖 Agents: 4 active
🎓 Students: 1,247 enrolled
📚 Courses: 342 active
🔗 Blockchain: Connected
✅ System: Operational
```

### 🎭 Demonstration Commands

#### Complete Demo
```bash
# Run full system demonstration
python collegiumai.py demo
```

**Sample Output:**
```
🎭 CollegiumAI Complete Demo
============================================================
1. 🤖 AI Agents: 4 specialized agents active
2. 🧠 LLM Integration: Multi-provider support
3. 🎓 Student Services: Enrollment and transfer
4. 🇪🇺 Bologna Process: ECTS credit conversion
5. 🔗 Blockchain: Credential verification

🚀 Running ReACT Multi-Agent Workflow...
✅ Demo completed successfully!
```

### 🔧 CLI Options and Flags

#### Global Options
```bash
-v, --verbose    # Enable verbose output
--version        # Show version information
--help           # Show help message
```

#### Command-Specific Options
```bash
# Agent list options
--detailed, -d   # Show detailed agent information

# Student enrollment options
--name, -n       # Student full name (required)
--program, -p    # Degree program (required)

# Student transfer options
--student-id, -id  # Student ID (required)
--credits, -c      # Credits to transfer (required)
```

### 🎯 Advanced Usage Examples

#### Multiple Command Workflow
```bash
# Check system status
python collegiumai.py system status

# List agents in detail
python collegiumai.py agent list --detailed

# Enroll a student
python collegiumai.py student enroll -n "Emma Johnson" -p "Engineering"

# Process transfer
python collegiumai.py student transfer -id "2024002" -c 120

# Run demo
python collegiumai.py demo
```

#### Batch Processing Example
```bash
#!/bin/bash
# batch_enrollment.sh

# Enroll multiple students
python collegiumai.py student enroll -n "Alice Smith" -p "Computer Science"
python collegiumai.py student enroll -n "Bob Johnson" -p "Data Science"  
python collegiumai.py student enroll -n "Carol Davis" -p "Business Administration"

# Check system status
python collegiumai.py system status
```

### 🧠 AI Agent Specializations

The CLI manages 4 specialized AI agents:

#### 1. Academic Advisor Agent
- **ID**: `academic_advisor`
- **Provider**: Anthropic Claude-3
- **Specialization**: Academic Planning & Course Selection
- **Capabilities**: Course planning, degree tracking, academic guidance

#### 2. Student Services Agent  
- **ID**: `student_services`
- **Provider**: Ollama (Privacy-focused)
- **Specialization**: Student Support & Wellness
- **Capabilities**: Support assessment, resource matching, crisis support

#### 3. Bologna Process Agent
- **ID**: `bologna_process` 
- **Provider**: OpenAI GPT-4
- **Specialization**: European Higher Education Standards
- **Capabilities**: ECTS conversion, qualification mapping, mobility support

#### 4. Research Coordinator Agent
- **ID**: `research_coordinator`
- **Provider**: OpenAI GPT-4
- **Specialization**: Research Collaboration & Project Management
- **Capabilities**: Collaboration matching, project planning, resource coordination

### 🇪🇺 Bologna Process Integration

The CLI provides seamless Bologna Process compliance:

#### ECTS Credit Conversion
```bash
# Automatic ECTS to US credit conversion
python collegiumai.py student transfer -id "EU_STUDENT_001" -c 180

# Typical conversion: 1.5 ECTS = 1 US credit
# 180 ECTS → 120 US credits
```

#### European Standards Compliance
- **Three-Cycle Structure**: Bachelor (180-240 ECTS), Master (60-120 ECTS), Doctorate (180+ ECTS)
- **Automatic Recognition**: AI-powered credential recognition across 49 Bologna countries
- **Quality Assurance**: ESG compliance monitoring
- **Diploma Supplement**: Automated multilingual documentation

### 🚀 Production Features

#### Enterprise Ready
- **Professional Interface**: Rich formatting and colored output
- **Error Handling**: Comprehensive error messages and validation
- **Scalable Architecture**: Supports thousands of students and operations
- **Multi-Provider LLM**: Intelligent routing between OpenAI, Anthropic, Ollama
- **Real-time Processing**: Instant responses and status updates

#### Security & Compliance
- **Data Privacy**: FERPA-compliant student data handling
- **Blockchain Integration**: Immutable credential verification
- **Audit Trails**: Complete logging of all operations
- **Access Control**: Role-based command permissions

### 📊 CLI Statistics

- **Commands**: 10+ professional commands
- **Agents**: 4 specialized AI agents
- **LLM Providers**: 3 (OpenAI, Anthropic, Ollama)
- **Student Operations**: Enrollment, transfer, advising
- **Compliance Frameworks**: 8+ including Bologna Process
- **Output Formats**: Rich text with colors and emojis

### 🔮 Future CLI Features

Coming enhancements:
- **Interactive Mode**: Real-time chat with AI agents
- **Batch Operations**: Process multiple students simultaneously
- **Configuration Management**: Persistent settings and preferences  
- **Plugin System**: Extensible command architecture
- **API Integration**: REST API connectivity for remote operations
- **Export Features**: CSV, JSON, XML data export capabilities

### 💡 Tips and Best Practices

1. **Use Detailed Output**: Add `--detailed` flag for comprehensive information
2. **Check Status First**: Always run `system status` before operations
3. **Student ID Format**: Use consistent student ID formats (e.g., "2024001")
4. **ECTS Conversion**: Verify credit conversions for European transfers
5. **Demo Mode**: Use `demo` command for training and presentations

### 🆘 Troubleshooting

#### Common Issues

**Command Not Found**
```bash
# Make sure you're in the CollegiumAI directory
cd /path/to/CollegiumAI
python collegiumai.py --help
```

**Unicode Errors**
```bash
# Set UTF-8 encoding (Windows)
set PYTHONIOENCODING=utf-8
python collegiumai.py demo
```

**Missing Dependencies**
```bash
# Install required packages
pip install click rich pyyaml
```

#### Support

For CLI support and feature requests:
- 📧 Email: support@collegium.ai
- 🐛 Issues: GitHub Issues
- 📖 Docs: Full documentation available
- 💬 Community: Discord support channel

---

**CollegiumAI CLI - Empowering Educational Excellence Through AI** 🎓✨