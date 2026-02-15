# Implementation Plan: TrialPulse-AI

## Overview

This implementation plan breaks down the TrialPulse-AI system into discrete coding tasks that build incrementally. The system consists of a Python FastAPI backend for data processing and API services, and a React TypeScript frontend for visualization and user interaction. Each task references specific requirements and includes property-based tests to validate correctness properties from the design document.

## Tasks

- [x] 1. Set up project infrastructure and testing frameworks
  - Create Python virtual environment and install dependencies (FastAPI, uvicorn, pandas, google-generativeai, python-dotenv, openpyxl, hypothesis)
  - Configure pytest for backend testing
  - Install frontend dependencies and configure fast-check for property-based testing
  - Set up environment configuration (.env file structure)
  - _Requirements: 8.4, 8.5, 9.6_

- [x] 2. Implement EDRR data loading and parsing
  - [x] 2.1 Create data_loader.py with Excel parsing logic
    - Implement `load_real_subjects()` function to read EDRR Excel files
    - Extract Site ID from Subject ID (format: XXX-YYY)
    - Aggregate open issues and patient counts by site
    - Handle missing files with appropriate error messages
    - _Requirements: 1.1, 1.2, 1.4_
  
  - [ ]* 2.2 Write property test for EDRR parsing completeness
    - **Property 1: EDRR Parsing Completeness**
    - **Validates: Requirements 1.1**
  
  - [ ]* 2.3 Write property test for site aggregation correctness
    - **Property 2: Site Aggregation Correctness**
    - **Validates: Requirements 1.2**
  
  - [ ]* 2.4 Write property test for invalid input error handling
    - **Property 4: Invalid Input Error Handling**
    - **Validates: Requirements 1.4**
  
  - [ ]* 2.5 Write unit tests for data loader edge cases
    - Test empty files, missing columns, malformed Subject IDs
    - Test non-numeric issue counts
    - _Requirements: 1.4_

- [x] 3. Implement DQI calculation and schema generation
  - [x] 3.1 Create schema_generator.py with DQI calculation logic
    - Implement `generate_master_dataset()` function
    - Calculate composite DQI scores from component metrics
    - Identify crisis sites (max open issues) and assign DQI 40-58
    - Assign normal sites DQI 82-98
    - Generate geographic coordinates for visualization
    - Flag sites with DQI < 60 as 'Critical'
    - _Requirements: 1.3, 2.2, 2.4, 7.2, 7.3_
  
  - [x] 3.2 Implement `get_dqi_breakdown()` function
    - Return detailed component scores (visit completion, query resolution, safety)
    - _Requirements: 1.3_
  
  - [ ]* 3.3 Write property test for DQI calculation consistency
    - **Property 3: DQI Calculation Consistency**
    - **Validates: Requirements 1.3**
  
  - [ ]* 3.4 Write property test for critical site threshold detection
    - **Property 6: Critical Site Threshold Detection**
    - **Validates: Requirements 2.2, 2.4, 7.2, 7.3**
  
  - [ ]* 3.5 Write unit tests for DQI calculation
    - Test with known component scores
    - Test boundary values (DQI = 0, 60, 100)
    - _Requirements: 1.3_

- [x] 4. Implement data persistence
  - [x] 4.1 Add data persistence logic to schema_generator.py
    - Store aggregated site data for retrieval
    - Implement retrieval functions
    - _Requirements: 1.5_
  
  - [ ]* 4.2 Write property test for data persistence round trip
    - **Property 5: Data Persistence Round Trip**
    - **Validates: Requirements 1.5**

- [ ] 5. Checkpoint - Ensure backend data processing tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 6. Implement FastAPI backend routes
  - [x] 6.1 Create main.py with FastAPI app initialization
    - Configure CORS middleware for local development
    - Load Gemini API key from environment
    - Initialize Gemini 1.5 Flash model
    - _Requirements: 9.5, 6.2_
  
  - [x] 6.2 Implement GET /api/sites endpoint
    - Call `generate_master_dataset()` to get site data
    - Return JSON response with site list
    - Handle errors with appropriate HTTP status codes
    - _Requirements: 9.1, 9.3, 9.6_
  
  - [x] 6.3 Implement POST /api/nl-query endpoint
    - Define QueryRequest Pydantic model
    - Process query with Gemini 1.5 Flash
    - Retrieve relevant site data as context
    - Return AI response with supporting data
    - Handle API failures with fallback messages
    - _Requirements: 9.2, 9.3, 9.4, 9.6, 6.1, 6.2, 6.3, 6.4_
  
  - [ ]* 6.4 Write property test for API endpoint availability
    - **Property 21: API Endpoint Availability**
    - **Validates: Requirements 9.1, 9.2, 9.6**
  
  - [ ]* 6.5 Write property test for API request validation
    - **Property 22: API Request Validation**
    - **Validates: Requirements 9.3, 9.4**
  
  - [ ]* 6.6 Write property test for CORS policy enforcement
    - **Property 23: CORS Policy Enforcement**
    - **Validates: Requirements 9.5**
  
  - [ ]* 6.7 Write unit tests for API routes
    - Test with mock data
    - Test Gemini API integration with mocked responses
    - Test error handling for invalid requests
    - _Requirements: 9.3, 9.4_

- [x] 7. Implement multi-agent investigation system
  - [x] 7.1 Create agent_simulator.py with scripted analysis
    - Implement `run_agent_simulation(site_id)` function
    - Return scripted analysis for Site 042
    - Include DataQuality agent findings (DQI 45, safety lag > 14 days)
    - Include SitePerformance agent findings (CRA resignation Oct 12)
    - Include Orchestrator agent synthesis (CRA reassignment, remote audit)
    - Return structured JSON with agent results and timestamps
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8_
  
  - [ ] 7.1a Add GET /api/agents/run/{site_id} endpoint to main.py
    - Create endpoint that calls run_agent_simulation()
    - Return agent analysis JSON
    - _Requirements: 3.1, 3.8_
  
  - [ ]* 7.2 Write property test for multi-agent workflow completeness
    - **Property 8: Multi-Agent Workflow Completeness**
    - **Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.8**
  
  - [ ]* 7.3 Write unit tests for agent simulator
    - Test scripted analysis for Site 042
    - Test fallback for non-scripted sites
    - _Requirements: 3.1, 3.8_

- [ ] 8. Checkpoint - Ensure backend API and agent tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 9. Set up React frontend structure
  - [x] 9.1 Create frontend directory structure
    - Set up src/views/, src/components/ui/, src/components/visuals/, src/lib/, src/types/
    - Configure Vite, TypeScript, Tailwind CSS
    - Create index.html and main.tsx entry points
    - _Requirements: 2.1_
  
  - [x] 9.2 Create App.tsx root component
    - Implement view routing state (currentView, context)
    - Implement `handleNavigate()` function
    - Create bottom navigation bar for view switching
    - _Requirements: 2.1_
  
  - [x] 9.3 Create reusable UI components
    - Implement src/components/ui/button.tsx
    - Implement src/components/ui/card.tsx
    - Implement src/components/ui/badge.tsx
    - Implement src/components/ui/input.tsx
    - _Requirements: 2.1_

- [x] 10. Implement Command Center dashboard
  - [x] 10.1 Create CommandCenter.tsx view component
    - Fetch site data from /api/sites on mount using axios
    - Display stat cards (average DQI, critical alerts, active sites, DB lock timeline)
    - Implement site click handler to navigate to Agent Workspace
    - _Requirements: 2.1, 2.6_
  
  - [x] 10.2 Create WorldMap.tsx visualization component
    - Use react-simple-maps for geographic visualization
    - Display site markers with color-coded status
    - Add pulsing animation for critical sites
    - _Requirements: 2.3, 2.5_
  
  - [x] 10.3 Create RiskTimeline.tsx visualization component
    - Use recharts for timeline chart
    - Display DQI trends over time
    - _Requirements: 2.1_
  
  - [x] 10.4 Create operational feed component
    - Display live alerts with color-coded severity
    - _Requirements: 7.5_
  
  - [ ]* 10.5 Write property test for dashboard rendering completeness
    - **Property 7: Dashboard Rendering Completeness**
    - **Validates: Requirements 2.1, 2.3, 2.5**
  
  - [ ]* 10.6 Write unit tests for Command Center
    - Test stat card rendering with sample data
    - Test site click navigation
    - Test data fetching error handling
    - _Requirements: 2.1, 2.6_

- [x] 11. Implement Agent Workspace view
  - [x] 11.1 Create AgentWorkspace.tsx view component
    - Implement state management (logs, isRunning, activeAgent, showPlan, isReviewing, isAuthorized)
    - Implement investigation protocol execution
    - Display sequential agent logs with type-based styling
    - _Requirements: 3.1, 3.6_
  
  - [x] 11.2 Create AgentNetwork.tsx visualization component
    - Display agent interaction diagram
    - Show active agent highlighting
    - _Requirements: 3.1_
  
  - [x] 11.3 Implement HITL gate interface
    - Display mitigation plan with full investigation report
    - Show proposed actions, expected outcomes, estimated costs
    - Implement approval/rejection workflow with e-signature
    - Record approval timestamp and supervisor identity
    - Prevent execution without approval
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7_
  
  - [ ]* 11.4 Write property test for HITL authorization requirements
    - **Property 9: HITL Authorization Requirements**
    - **Validates: Requirements 4.2, 4.3, 4.7**
  
  - [ ]* 11.5 Write property test for HITL review interface completeness
    - **Property 10: HITL Review Interface Completeness**
    - **Validates: Requirements 4.1, 4.4**
  
  - [ ]* 11.6 Write unit tests for Agent Workspace
    - Test simulation execution flow
    - Test approval/rejection workflows
    - Test agent log display
    - _Requirements: 3.1, 4.1_

- [ ] 12. Checkpoint - Ensure Command Center and Agent Workspace tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 13. Implement Digital Twin simulation view
  - [x] 13.1 Create DigitalTwin.tsx view component
    - Implement state management (activeScenario, staffCapacity)
    - Implement Monte Carlo simulation logic (1000+ iterations)
    - Calculate projected backlog and timeline delay
    - Implement dynamic recalculation on parameter changes
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.8_
  
  - [x] 13.2 Create simulation visualization components
    - Area chart for workload vs backlog projection (recharts)
    - Bar chart for current vs projected metrics
    - Display probability distribution, median forecast, 90% confidence interval
    - _Requirements: 5.6, 5.7_
  
  - [x] 13.3 Implement scenario switching
    - Three scenarios: baseline, CRA reassignment, SLA change
    - Update simulation parameters based on scenario
    - _Requirements: 5.1_
  
  - [x] 13.4 Implement human calibration slider
    - Staff availability slider (50-150%)
    - Apply capacity multiplier to backlog calculation
    - _Requirements: 5.3, 5.4_
  
  - [ ]* 13.5 Write property test for Monte Carlo iteration count
    - **Property 12: Monte Carlo Iteration Count**
    - **Validates: Requirements 5.2, 5.6, 5.7**
  
  - [ ]* 13.6 Write property test for dynamic recalculation
    - **Property 13: Digital Twin Dynamic Recalculation**
    - **Validates: Requirements 5.3, 5.4**
  
  - [ ]* 13.7 Write property test for simulation parameter acceptance
    - **Property 14: Simulation Parameter Acceptance**
    - **Validates: Requirements 5.5**
  
  - [ ]* 13.8 Write unit tests for Digital Twin
    - Test scenario switching
    - Test chart rendering with sample data
    - Test parameter validation
    - _Requirements: 5.1, 5.8_

- [x] 14. Implement Natural Language Interface view
  - [x] 14.1 Create NLInterface.tsx view component
    - Implement state management (query, messages, loading, isListening)
    - Implement query submission to /api/nl-query
    - Display conversation history with role-based styling
    - Handle loading states and errors
    - _Requirements: 6.1, 6.7_
  
  - [x] 14.2 Implement feedback mechanism
    - Add thumbs up/down buttons to AI messages
    - Prompt for expert correction on negative feedback
    - Store corrections for active learning
    - _Requirements: 6.5, 6.6_
  
  - [x] 14.3 Implement voice input (optional)
    - Add microphone button for voice queries
    - Use Web Speech API for speech-to-text
    - _Requirements: 6.1_
  
  - [ ]* 14.4 Write property test for NL query processing pipeline
    - **Property 15: NL Query Processing Pipeline**
    - **Validates: Requirements 6.1, 6.2, 6.3, 6.4**
  
  - [ ]* 14.5 Write property test for active learning correction round trip
    - **Property 16: Active Learning Correction Round Trip**
    - **Validates: Requirements 6.6**
  
  - [ ]* 14.6 Write unit tests for NL Interface
    - Test message display and input handling
    - Test feedback UI interactions
    - Test error handling for API failures
    - _Requirements: 6.1, 6.7, 6.8_

- [ ] 15. Checkpoint - Ensure Digital Twin and NL Interface tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 16. Implement risk detection and alerting
  - [ ] 16.1 Add risk monitoring logic to schema_generator.py
    - Implement continuous monitoring for DQI < 60
    - Implement monitoring for overdue items > 10
    - Implement enrollment rate monitoring (< 50% target for 2 weeks)
    - Generate appropriate alert types ('Critical', 'High Risk', 'Performance Warning')
    - _Requirements: 7.1, 7.2, 7.3, 7.4_
  
  - [ ] 16.2 Implement audit logging for risk alerts
    - Log timestamp, site identifier, risk type, triggering metric values
    - _Requirements: 7.6_
  
  - [ ]* 16.3 Write property test for enrollment rate alert generation
    - **Property 17: Enrollment Rate Alert Generation**
    - **Validates: Requirements 7.4, 7.5**
  
  - [ ]* 16.4 Write property test for audit logging completeness
    - **Property 11: Audit Logging Completeness**
    - **Validates: Requirements 4.6, 7.6, 8.6**
  
  - [ ]* 16.5 Write unit tests for risk detection
    - Test alert generation for each risk type
    - Test audit log format
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.6_

- [ ] 17. Implement authentication and authorization (stub implementation)
  - [ ] 17.1 Add authentication middleware to main.py
    - Implement basic authentication check (stub for now)
    - Reject requests without valid credentials
    - _Requirements: 8.1_
  
  - [ ] 17.2 Implement role-based access control
    - Define roles: Trial Manager, Human Supervisor, Read-Only Viewer
    - Implement permission verification
    - _Requirements: 8.2, 8.3_
  
  - [ ] 17.3 Implement data access logging
    - Log user identity, timestamp, resource accessed, action performed
    - _Requirements: 8.6_
  
  - [ ]* 17.4 Write property test for authentication enforcement
    - **Property 18: Authentication Enforcement**
    - **Validates: Requirements 8.1**
  
  - [ ]* 17.5 Write property test for role-based authorization
    - **Property 19: Role-Based Authorization**
    - **Validates: Requirements 8.2, 8.3**
  
  - [ ]* 17.6 Write unit tests for authentication and authorization
    - Test authentication rejection
    - Test role permission checks
    - Test access logging
    - _Requirements: 8.1, 8.2, 8.3, 8.6_

- [ ] 18. Implement encryption (configuration only)
  - [ ] 18.1 Document encryption requirements
    - Add configuration notes for AES-256 at rest
    - Add configuration notes for TLS 1.3 in transit
    - _Requirements: 8.4, 8.5_
  
  - [ ]* 18.2 Write property test for data encryption verification
    - **Property 20: Data Encryption Verification**
    - **Validates: Requirements 8.4, 8.5**

- [ ] 19. Implement API versioning
  - [ ] 19.1 Add API version headers to responses
    - Include version information in all API responses
    - _Requirements: 9.7_
  
  - [ ]* 19.2 Write property test for API versioning
    - **Property 24: API Versioning**
    - **Validates: Requirements 9.7**

- [ ] 20. Performance optimization and testing
  - [ ] 20.1 Add performance benchmarks
    - Benchmark EDRR parsing for 10,000 subject records
    - Benchmark DQI calculation
    - Benchmark Monte Carlo simulation (1000 iterations)
    - _Requirements: 10.2, 10.3, 10.5_
  
  - [ ]* 20.2 Write property test for large dataset processing
    - **Property 25: Large Dataset Processing**
    - **Validates: Requirements 10.2**
  
  - [ ]* 20.3 Write unit tests for performance requirements
    - Test aggregation completes within 10 seconds for 1,000 subjects
    - Test dashboard renders within 2 seconds
    - Test simulation completes within 3 seconds
    - _Requirements: 10.3, 10.4, 10.5_

- [ ] 21. Integration and end-to-end testing
  - [ ]* 21.1 Write integration tests for frontend-backend communication
    - Test /api/sites endpoint integration
    - Test /api/nl-query endpoint integration
    - Test error handling across the stack
    - _Requirements: 9.1, 9.2_
  
  - [ ]* 21.2 Write end-to-end workflow tests
    - Test: Upload EDRR → View sites → Investigate critical site → Approve mitigation
    - Test: Submit NL query → Receive response → Provide feedback → Verify correction stored
    - Test: Adjust Digital Twin parameters → View forecast → Switch scenarios → Verify recalculation
    - _Requirements: 1.1, 2.1, 3.1, 4.1, 5.1, 6.1_

- [ ] 22. Final checkpoint - Ensure all tests pass and system is integrated
  - Run full test suite (unit tests and property tests)
  - Verify all correctness properties are validated
  - Ensure all requirements are covered by implementation
  - Ask the user if questions arise or if any adjustments are needed

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP delivery
- Each task references specific requirements for traceability
- Property tests validate universal correctness properties from the design document
- Unit tests validate specific examples, edge cases, and integration points
- Checkpoints ensure incremental validation throughout implementation
- The implementation follows a backend-first approach, then frontend views, then cross-cutting concerns
- Authentication and encryption tasks are stub implementations for demonstration purposes
- Performance testing ensures the system meets scalability requirements
