#!/usr/bin/env python3
"""
CollegiumAI Integration Demonstration Runner
===========================================

This script demonstrates the complete CollegiumAI framework with advanced AI agent
capabilities, autonomous team collaboration, complex reasoning, and sophisticated
decision-making across multiple integration scenarios.

Usage:
    python run_integration_demo.py [--config-path PATH] [--scenario SCENARIO_ID]

Examples:
    # Run full comprehensive demonstration
    python run_integration_demo.py

    # Run specific scenario
    python run_integration_demo.py --scenario global_mobility_program

    # Use custom configuration
    python run_integration_demo.py --config-path ./custom_config
"""

import asyncio
import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

# Import CollegiumAI integration systems
from examples.integration import ComprehensiveIntegrationDemo

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="CollegiumAI Comprehensive Integration Demonstration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        '--config-path',
        type=Path,
        default=Path('./config'),
        help='Path to configuration directory (default: ./config)'
    )
    
    parser.add_argument(
        '--scenario',
        type=str,
        choices=['global_mobility_program', 'research_excellence_network', 'adaptive_learning_ecosystem'],
        help='Run specific scenario only (default: run all scenarios)'
    )
    
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path('./results'),
        help='Directory to save results (default: ./results)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    return parser.parse_args()

def setup_environment(config_path: Path, output_dir: Path):
    """Setup demonstration environment"""
    
    # Create directories if they don't exist
    config_path.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create subdirectories for different systems
    system_dirs = ['agents', 'enrollment', 'research', 'content', 'partnerships']
    for dir_name in system_dirs:
        (config_path / dir_name).mkdir(exist_ok=True)
    
    print(f"✅ Environment setup completed")
    print(f"📁 Configuration path: {config_path.absolute()}")
    print(f"📁 Output directory: {output_dir.absolute()}")

async def run_comprehensive_demonstration(demo: ComprehensiveIntegrationDemo, 
                                        output_dir: Path, 
                                        verbose: bool = False):
    """Run the comprehensive integration demonstration"""
    
    print("\n🚀 Starting CollegiumAI Comprehensive Integration Demonstration")
    print("=" * 80)
    print("🤖 Advanced AI Agent Capabilities:")
    print("   • Autonomous Team Collaboration")
    print("   • Complex Reasoning Strategies (8 types)")
    print("   • Advanced Decision-Making Frameworks (8 types)")
    print("   • Multi-Agent Orchestration")
    print("   • Intelligent Workflow Integration")
    print("=" * 80)
    
    try:
        # Run comprehensive demonstration
        results = await demo.run_comprehensive_demonstration()
        
        # Save results to file
        results_file = output_dir / f"demonstration_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Convert datetime objects to strings for JSON serialization
        json_results = convert_datetime_to_string(results)
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(json_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n📊 Results saved to: {results_file}")
        
        # Print summary
        print_demonstration_summary(results, verbose)
        
        return results
        
    except Exception as e:
        print(f"❌ Error during demonstration: {str(e)}")
        if verbose:
            import traceback
            traceback.print_exc()
        return None

async def run_specific_scenario(demo: ComprehensiveIntegrationDemo, 
                              scenario_id: str, 
                              output_dir: Path,
                              verbose: bool = False):
    """Run a specific integration scenario"""
    
    print(f"\n🎯 Running Specific Scenario: {scenario_id}")
    print("=" * 60)
    
    # Find the scenario
    scenario = None
    for s in demo.scenarios:
        if s.id == scenario_id:
            scenario = s
            break
    
    if not scenario:
        print(f"❌ Scenario '{scenario_id}' not found")
        return None
    
    try:
        # Execute specific scenario
        scenario_results = await demo._execute_integration_scenario(scenario)
        
        # Save results
        results_file = output_dir / f"scenario_{scenario_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        json_results = convert_datetime_to_string(scenario_results)
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(json_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n📊 Scenario results saved to: {results_file}")
        
        # Print scenario summary
        print_scenario_summary(scenario, scenario_results, verbose)
        
        return scenario_results
        
    except Exception as e:
        print(f"❌ Error during scenario execution: {str(e)}")
        if verbose:
            import traceback
            traceback.print_exc()
        return None

def convert_datetime_to_string(obj):
    """Convert datetime objects to strings for JSON serialization"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {key: convert_datetime_to_string(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_datetime_to_string(item) for item in obj]
    else:
        return obj

def print_demonstration_summary(results: dict, verbose: bool = False):
    """Print comprehensive demonstration summary"""
    
    print("\n🎊 COMPREHENSIVE DEMONSTRATION SUMMARY")
    print("=" * 80)
    
    # Overall metrics
    print(f"⏱️  Total Duration: {results.get('total_duration', 0):.2f} seconds")
    print(f"🎯 Scenarios Executed: {len(results.get('scenarios', {}))}")
    
    # System performance
    system_perf = results.get('system_performance', {})
    print(f"🤖 AI Agents Deployed: {system_perf.get('total_ai_agents_deployed', 0)}")
    print(f"🧠 Autonomous Decisions: {system_perf.get('total_autonomous_decisions', 0)}")
    print(f"🤝 Collaboration Sessions: {system_perf.get('total_collaboration_sessions', 0)}")
    print(f"💭 Reasoning Cycles: {system_perf.get('total_reasoning_cycles', 0)}")
    
    print(f"\n📈 SYSTEM PERFORMANCE METRICS")
    print(f"   • System Efficiency: {system_perf.get('system_efficiency', 0):.2%}")
    print(f"   • Scalability Factor: {system_perf.get('scalability_factor', 0):.2%}")
    print(f"   • Reliability Score: {system_perf.get('reliability_score', 0):.2%}")
    print(f"   • Integration Seamlessness: {system_perf.get('integration_seamlessness', 0):.2%}")
    
    # AI agent analytics
    agent_analytics = results.get('ai_agent_analytics', {})
    print(f"\n🤖 AI AGENT PERFORMANCE")
    print(f"   • Average Agent Efficiency: {agent_analytics.get('average_agent_efficiency', 0):.2%}")
    print(f"   • Autonomous Decision Accuracy: {agent_analytics.get('autonomous_decision_accuracy', 0):.2%}")
    print(f"   • Collaborative Effectiveness: {agent_analytics.get('collaborative_effectiveness', 0):.2%}")
    print(f"   • Reasoning Sophistication: {agent_analytics.get('reasoning_sophistication', 0):.2%}")
    
    # Scenario results
    print(f"\n🎯 SCENARIO RESULTS")
    scenarios = results.get('scenarios', {})
    for scenario_id, scenario_data in scenarios.items():
        success_rate = scenario_data.get('overall_success_rate', 0)
        print(f"   • {scenario_id.replace('_', ' ').title()}: {success_rate:.2%} success rate")
    
    if verbose:
        print("\n📊 DETAILED ANALYTICS")
        
        # Collaboration metrics
        collab_metrics = results.get('collaboration_metrics', {})
        print("🤝 Collaboration Patterns:")
        patterns = collab_metrics.get('collaboration_patterns', {})
        for pattern, percentage in patterns.items():
            print(f"   • {pattern.replace('_', ' ').title()}: {percentage:.1%}")
        
        # Decision making analysis
        decision_analysis = results.get('decision_making_analysis', {})
        print("🎯 Decision Frameworks Used:")
        frameworks = decision_analysis.get('decision_frameworks_used', {})
        for framework, percentage in frameworks.items():
            print(f"   • {framework.replace('_', ' ').title()}: {percentage:.1%}")
        
        # Reasoning effectiveness
        reasoning_analysis = results.get('reasoning_effectiveness', {})
        print("💭 Reasoning Strategies Used:")
        strategies = reasoning_analysis.get('reasoning_strategies_used', {})
        for strategy, percentage in strategies.items():
            print(f"   • {strategy.replace('_', ' ').title()}: {percentage:.1%}")

def print_scenario_summary(scenario, results: dict, verbose: bool = False):
    """Print specific scenario summary"""
    
    print(f"\n🎯 SCENARIO SUMMARY: {scenario.name}")
    print("=" * 60)
    print(f"📋 Description: {scenario.description}")
    print(f"⏱️  Duration: {results.get('duration', 0):.2f} seconds")
    print(f"🎭 Complexity Level: {scenario.complexity_level}")
    print(f"🤖 AI Agents Deployed: {results.get('ai_agents_deployed', 0)}")
    print(f"🧠 Autonomous Decisions: {results.get('autonomous_decisions', 0)}")
    print(f"🤝 Collaboration Sessions: {results.get('collaboration_sessions', 0)}")
    print(f"💭 Reasoning Cycles: {results.get('reasoning_cycles', 0)}")
    print(f"📈 Overall Success Rate: {results.get('overall_success_rate', 0):.2%}")
    
    # Success metrics
    success_metrics = results.get('success_metrics', {})
    if success_metrics:
        print(f"\n📊 SUCCESS METRICS")
        for metric, value in success_metrics.items():
            print(f"   • {metric.replace('_', ' ').title()}: {value:.2%}")
    
    if verbose:
        # Phases
        phases = results.get('phases', {})
        if phases:
            print(f"\n📋 EXECUTION PHASES")
            for phase_name, phase_data in phases.items():
                print(f"   • {phase_name.replace('_', ' ').title()}: {len(phase_data)} items processed")

async def main():
    """Main demonstration runner"""
    
    args = parse_arguments()
    
    print("🎓 CollegiumAI Framework - Comprehensive Integration Demonstration")
    print("Advanced AI Agents • Autonomous Collaboration • Complex Reasoning")
    print("=" * 80)
    
    # Setup environment
    setup_environment(args.config_path, args.output_dir)
    
    # Initialize comprehensive integration demo
    try:
        demo = ComprehensiveIntegrationDemo(args.config_path)
        print("✅ CollegiumAI Integration Demo initialized successfully")
        
        # Run demonstration
        if args.scenario:
            results = await run_specific_scenario(
                demo, args.scenario, args.output_dir, args.verbose
            )
        else:
            results = await run_comprehensive_demonstration(
                demo, args.output_dir, args.verbose
            )
        
        if results:
            print("\n🎉 Demonstration completed successfully!")
            print("🔍 Check the generated reports for detailed analysis")
        else:
            print("\n❌ Demonstration failed - check error messages above")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Failed to initialize demonstration: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    # Run the demonstration
    asyncio.run(main())