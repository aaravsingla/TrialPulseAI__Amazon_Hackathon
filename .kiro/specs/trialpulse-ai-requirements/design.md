# Design Document: TrialPulse-AI

## Overview

TrialPulse-AI is a full-stack clinical operations assistant that processes Electronic Data Review Report (EDRR) Excel files to provide real-time site monitoring, automated risk detection, AI-powered analysis, and predictive simulation capabilities. The system follows a client-server architecture with a React TypeScript frontend and Python FastAPI backend, leveraging Google's Gemini 1.5 Flash for natural language processing.

The platform enables trial managers to:
- Monitor site performance metrics in real-time through an interactive dashboard
- Investigate site issues using coordinated multi-agent analysis
- Review and approve mitigation plans through human-in-the-loop gates
- Forecast Database Lock timelines using Monte Carlo simulation
- Query trial data using natural language

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React + TS)                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Command  │  │  Agent   │  │ Digital  │  │    NL    │   │
│  │  Center  │  │Workspace │  │   Twin   │  │Interface │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                    HTTP/REST (Axios)
                            │
┌─────────────────────────────────────────────────────────────┐
│                   Backend (FastAPI + Python)                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ API Routes   │  │ Data Loader  │  │   Agent      │     │
│  │ /api/sites   │  │ EDRR Parser  │  │  Simulator   │     │
│  │ /api/nl-query│  │              │  │              │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                            │                                 │
│                    ┌──────────────┐                         │
│                    │   Schema     │                         │
│                    │  Generator   │                         │
│                    │ (DQI Calc)   │                         │
│                    └──────────────┘                         │
└─────────────────────────────────────────────────────────────┘
                            │
                    ┌──────────────┐
                    │  Gemini 1.5  │
                    │    Flash     │
                    └──────────────┘
```

### Technology Stack

**Frontend:**
- React 19.2.0 with TypeScript 5.9.3
- Vite 7.2.4 for build tooling
- Tailwind CSS 3.4.17 for styling
- Recharts for data visualization
- Framer Motion for animations
- Axios for HTTP requests

**Backend:**
- Python with FastAPI framework
- Uvicorn ASGI server
- Pandas for Excel data processing
- Google Generative AI SDK (Gemini 1.5 Flash)
- Python-dotenv for configuration

**Communication:**
- REST API with JSON payloads
- CORS enabled for local development
- HTTP status codes for error handling

## Components and Interfaces

### Frontend Components

#### 1. App Component (Root)
**Responsibility:** View routing and global state management

**State:**
- `currentView`: string - Active view identifier ('command', 'agents', 'digital_twin', 'nl_interface')
- `context`: object - Contextual data passed between views (e.g., siteId)

**Interface:**
```typescript
interface AppState {
  currentView: 'command' | 'agents' | 'digital_twin' | 'nl_interface';
  context: { siteId?: string } | null;
}

function handleNavigate(view: string, ctx?: any): void
```

#### 2. Command Center View
**Responsibility:** Real-time dashboard displaying site metrics and alerts

**Data Flow:**
1. Fetch site data from `/api/sites` on mount
2. Display metrics in stat cards
3. Render geographic map with site markers
4. Show risk timeline and alert feed
5. Handle site click to navigate to Agent Workspace

**Interface:**
```typescript
interface Site {
  id: string;
  name: string;
  lat: number;
  lng: number;
  status: 'Active' | 'Critical';
  patients: number;
  dqi: number;
  overdue_items: number;
  is_dummy: boolean;
}

interface CommandCenterProps {
  onNavigate: (view: string, context?: any) => void;
}
```

**Key Features:**
- Stat cards showing average DQI, critical alerts, active sites, DB lock timeline
- Interactive world map with pulsing alerts for critical sites
- Risk timeline chart showing DQI trends
- Live operational feed with color-coded alerts

#### 3. Agent Workspace View
**Responsibility:** Multi-agent investigation interface with HITL approval gate

**State:**
- `logs`: AgentLog[] - Sequential analysis messages
- `isRunning`: boolean - Investigation in progress
- `activeAgent`: string | null - Currently executing agent
- `showPlan`: boolean - Display mitigation plan
- `isReviewing`: boolean - Human supervisor reviewing plan
- `isAuthorized`: boolean - Plan approved for execution

**Interface:**
```typescript
interface AgentLog {
  id: string;
  agent: string;
  msg: string;
  type: 'info' | 'alert' | 'success';
}

interface AgentWorkspaceProps {
  siteId: string;
  onBack: () => void;
}
```

**Workflow:**
1. User initiates investigation protocol
2. DataQuality agent analyzes DQI components
3. SitePerformance agent identifies operational issues
4. Orchestrator agent synthesizes findings and proposes mitigation
5. HITL gate presents plan for human review
6. Human supervisor approves or rejects with e-signature
7. System executes approved plan

#### 4. Digital Twin View
**Responsibility:** Monte Carlo simulation for Database Lock forecasting

**State:**
- `activeScenario`: 'baseline' | 'reassign' | 'sla' - Selected intervention
- `staffCapacity`: number - Human calibration slider (50-150%)

**Interface:**
```typescript
interface DigitalTwinProps {
  onBack: () => void;
}

interface SimulationData {
  day: string;
  workload: number;
  backlog: number;
}
```

**Simulation Logic:**
```
capacityMultiplier = 1 + ((100 - staffCapacity) / 100)
adjustedBacklog = baseBacklog * capacityMultiplier
```

**Features:**
- Three intervention scenarios (baseline, CRA reassignment, SLA change)
- Human calibration slider for staff availability
- Dynamic recalculation on parameter changes
- Area chart showing workload vs backlog projection
- Bar chart comparing current vs projected metrics

#### 5. NL Interface View
**Responsibility:** Natural language query interface with active learning

**State:**
- `query`: string - User input
- `messages`: Message[] - Conversation history
- `loading`: boolean - AI processing
- `isListening`: boolean - Voice input active

**Interface:**
```typescript
interface Message {
  id: number;
  role: 'user' | 'ai';
  text: string;
  feedback?: 'positive' | 'negative' | null;
}

interface NLInterfaceProps {
  onBack: () => void;
}
```

**Active Learning Flow:**
1. User submits query
2. AI generates response
3. User provides feedback (thumbs up/down)
4. If negative, prompt for expert correction
5. Store correction for model retraining

### Backend Components

#### 1. API Routes (main.py)
**Responsibility:** HTTP endpoint handlers and request routing

**Endpoints:**

```python
@app.post("/api/nl-query")
async def nl_query(request: QueryRequest) -> dict:
    """
    Process natural language query using Gemini 1.5 Flash
    
    Args:
        request: QueryRequest with 'query' field
    
    Returns:
        {"response": str} - AI-generated response
    """

@app.get("/api/sites")
def get_all_sites() -> list[dict]:
    """
    Retrieve all site data with calculated metrics
    
    Returns:
        List of site objects with DQI scores and risk flags
    """
```

**Configuration:**
- CORS middleware allows all origins (development mode)
- Gemini API key loaded from environment variables
- Model: gemini-1.5-flash

#### 2. Data Loader (data_loader.py)
**Responsibility:** Parse and clean EDRR Excel files

**Function:**
```python
def load_real_subjects() -> pd.DataFrame:
    """
    Load and aggregate subject-level data from EDRR Excel
    
    Process:
    1. Read Excel file from data/ directory
    2. Extract Site ID from Subject ID (format: XXX-YYY)
    3. Aggregate open issues per site
    4. Count patients per site
    
    Returns:
        DataFrame with columns: Site ID, Open Issues, Patients
    """
```

**Data Cleaning:**
- Extract Site ID from "XXX-YYY" format in Subject ID column
- Handle missing files with professional mock data
- Aggregate "Total Open issue Count per subject" by site

#### 3. Schema Generator (schema_generator.py)
**Responsibility:** Generate master dataset with DQI scores and risk flags

**Function:**
```python
def generate_master_dataset() -> list[dict]:
    """
    Calculate DQI scores and risk levels for all sites
    
    Logic:
    - Identify site with maximum open issues as crisis site
    - Assign DQI 40-58 for crisis sites, 82-98 for normal sites
    - Flag sites with DQI < 60 as 'Critical'
    - Generate geographic coordinates for visualization
    
    Returns:
        List of site objects with calculated metrics
    """

def get_dqi_breakdown(site_id: str) -> dict:
    """
    Get detailed DQI component breakdown for a site
    
    Returns:
        {
            "visit_completion": int,
            "query_resolution": int,
            "safety": int,
            "total": int
        }
    """
```

**DQI Calculation:**
- DQI is a composite score (0-100)
- Components: visit completion, query resolution, safety reporting
- Crisis sites: DQI 40-58, low component scores
- Normal sites: DQI 82-98, high component scores

#### 4. Agent Simulator (agent_simulator.py)
**Responsibility:** Scripted multi-agent analysis for demonstration

**Function:**
```python
def run_agent_simulation(site_id: str) -> dict:
    """
    Return scripted analysis for Site 042
    
    Returns:
        {
            "site_id": str,
            "status": str,
            "agents": {
                "DataQuality": {
                    "status": str,
                    "message": str,
                    "timestamp": str
                },
                "SitePerformance": {...},
                "Orchestrator": {...}
            }
        }
    """
```

**Scripted Analysis for Site 042:**
- DataQuality: Detects DQI at 45, safety reporting lag > 14 days
- SitePerformance: Identifies CRA resignation on Oct 12
- Orchestrator: Proposes CRA reassignment and remote monitoring audit

## Data Models

### Site Model
```typescript
interface Site {
  id: string;                    // Site identifier (e.g., "042")
  name: string;                  // Display name
  lat: number;                   // Latitude for map visualization
  lng: number;                   // Longitude for map visualization
  status: 'Active' | 'Critical'; // Risk status
  patients: number;              // Enrolled patient count
  dqi: number;                   // Data Quality Index (0-100)
  overdue_items: number;         // Count of overdue tasks
  is_dummy: boolean;             // Flag for mock data
}
```

### DQI Breakdown Model
```typescript
interface DQIBreakdown {
  visit_completion: number;  // Visit completion score (0-100)
  query_resolution: number;  // Query resolution score (0-100)
  safety: number;            // Safety reporting score (0-100)
  total: number;             // Composite DQI score
}
```

### Agent Analysis Model
```typescript
interface AgentAnalysis {
  site_id: string;
  status: string;
  agents: {
    DataQuality: AgentResult;
    SitePerformance: AgentResult;
    Orchestrator: AgentResult;
  };
}

interface AgentResult {
  status: string;
  message: string;
  timestamp: string;
}
```

### Mitigation Plan Model
```typescript
interface MitigationPlan {
  site_id: string;
  actions: string[];           // List of proposed actions
  confidence: number;          // AI confidence score (0-100)
  reasoning: string;           // Explanation of proposal
  requires_approval: boolean;  // HITL gate flag
  approved: boolean;           // Approval status
  approver_id?: string;        // Human supervisor identifier
  approval_timestamp?: string; // ISO 8601 timestamp
}
```

### Simulation Scenario Model
```typescript
interface SimulationScenario {
  id: 'baseline' | 'reassign' | 'sla';
  name: string;
  description: string;
  backlog_curve: number[];     // Projected backlog at [0, 30, 60, 90] days
  workload_curve: number[];    // Projected workload at [0, 30, 60, 90] days
}
```

### Message Model (NL Interface)
```typescript
interface Message {
  id: number;
  role: 'user' | 'ai';
  text: string;
  feedback?: 'positive' | 'negative' | null;
  correction?: string;         // Expert correction for active learning
  timestamp: string;           // ISO 8601 timestamp
}
```

### Query Request Model
```python
class QueryRequest(BaseModel):
    query: str  # Natural language query from user
```

### EDRR Data Model
```python
# Raw EDRR DataFrame schema
{
    'Subject ID': str,           # Format: "XXX-YYY" (Site-Subject)
    'Total Open issue Count per subject': int,
    # Additional columns vary by study
}

# Aggregated Site Stats DataFrame
{
    'Site ID': str,              # Extracted from Subject ID
    'Open Issues': int,          # Sum of open issues
    'Patients': int              # Count of subjects
}
```


## Correctness Properties

A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.

### Property 1: EDRR Parsing Completeness
*For any* valid EDRR Excel file, parsing should extract all required fields (Site ID, visit completion status, query counts, safety reporting metrics) and the extracted data should contain entries for all subjects in the file.

**Validates: Requirements 1.1**

### Property 2: Site Aggregation Correctness
*For any* set of subject-level records, when aggregated by Site ID, the sum of open issues for all subjects at a site should equal the site's total open issues count, and the count of subjects should equal the site's patient count.

**Validates: Requirements 1.2**

### Property 3: DQI Calculation Consistency
*For any* set of DQI component scores (visit completion rate, query resolution rate, safety reporting timeliness), the calculated composite DQI score should be deterministic and within the valid range [0, 100].

**Validates: Requirements 1.3**

### Property 4: Invalid Input Error Handling
*For any* EDRR file with malformed data or missing required columns, the system should return an error message that specifically identifies which validation failed, and should not proceed with processing.

**Validates: Requirements 1.4**

### Property 5: Data Persistence Round Trip
*For any* aggregated site data, persisting the data and then retrieving it should produce data equivalent to the original aggregated data.

**Validates: Requirements 1.5**

### Property 6: Critical Site Threshold Detection
*For any* site with DQI below 60 or overdue items greater than 10, the system should flag the site with the appropriate risk status ('Critical' for DQI < 60, 'High Risk' for overdue items > 10).

**Validates: Requirements 2.2, 2.4, 7.2, 7.3**

### Property 7: Dashboard Rendering Completeness
*For any* set of site data, the Command Center dashboard should display all required metrics (DQI scores, enrollment counts, overdue items) and all sites should appear on the geographic map with color-coded status indicators, with critical sites having pulsing alert styling.

**Validates: Requirements 2.1, 2.3, 2.5**

### Property 8: Multi-Agent Workflow Completeness
*For any* site investigation, the multi-agent workflow should execute all three agents (DataQuality, SitePerformance, Orchestrator) in sequence, each agent should produce analysis output, and the final report should contain findings from all three agents with supporting evidence.

**Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.8**

### Property 9: HITL Authorization Requirements
*For any* mitigation plan that involves resource reallocation or budget changes exceeding $10,000, the HITL gate should require electronic signature approval, and the plan should not be executable without explicit approval.

**Validates: Requirements 4.2, 4.3, 4.7**

### Property 10: HITL Review Interface Completeness
*For any* mitigation plan presented for review, the HITL gate interface should display the full investigation report, proposed actions, expected outcomes, and estimated costs.

**Validates: Requirements 4.1, 4.4**

### Property 11: Audit Logging Completeness
*For any* system event that requires auditing (mitigation plan approval, risk alert generation, data access), the audit log should contain all required fields: timestamp, user/site identifier, event type, and relevant metric values or action details.

**Validates: Requirements 4.6, 7.6, 8.6**

### Property 12: Monte Carlo Iteration Count
*For any* Digital Twin simulation, the system should execute at least 1000 Monte Carlo iterations and the output should include a probability distribution, median forecast date, and 90% confidence interval.

**Validates: Requirements 5.2, 5.6, 5.7**

### Property 13: Digital Twin Dynamic Recalculation
*For any* Digital Twin simulation, when staff availability is adjusted, both the projected backlog count and timeline delay should change, and the relationship should be: lower staff availability increases backlog and delay, higher staff availability decreases backlog and delay.

**Validates: Requirements 5.3, 5.4**

### Property 14: Simulation Parameter Acceptance
*For any* Digital Twin simulation, all required input parameters (current backlog count, staff availability, query resolution rate, visit completion rate) should be accepted and used in the calculation.

**Validates: Requirements 5.5**

### Property 15: NL Query Processing Pipeline
*For any* natural language query submitted to the NL Interface, the system should process the query using Gemini 1.5 Flash, retrieve relevant site data as context, and return a response with supporting data.

**Validates: Requirements 6.1, 6.2, 6.3, 6.4**

### Property 16: Active Learning Correction Round Trip
*For any* expert correction provided through the NL Interface feedback mechanism, the correction should be stored and retrievable for future model training.

**Validates: Requirements 6.6**

### Property 17: Enrollment Rate Alert Generation
*For any* site where enrollment rate drops below 50% of target rate for two consecutive weeks, the system should generate a 'Performance Warning' alert that appears on the Command Center dashboard.

**Validates: Requirements 7.4, 7.5**

### Property 18: Authentication Enforcement
*For any* request to access clinical trial data, the system should reject requests without valid authentication credentials.

**Validates: Requirements 8.1**

### Property 19: Role-Based Authorization
*For any* user attempting to access a resource, the system should verify the user's role has appropriate permissions, and should deny access if permissions are insufficient.

**Validates: Requirements 8.2, 8.3**

### Property 20: Data Encryption Verification
*For any* clinical trial data stored at rest, the data should be encrypted using AES-256, and all data transmissions should use TLS 1.3 or higher.

**Validates: Requirements 8.4, 8.5**

### Property 21: API Endpoint Availability
*For any* valid request to the `/api/sites` or `/api/nl-query` endpoints, the system should return a response with appropriate HTTP status code and JSON-formatted data matching the expected schema.

**Validates: Requirements 9.1, 9.2, 9.6**

### Property 22: API Request Validation
*For any* API request with invalid parameters or malformed format, the system should return a 400 status code with a descriptive error message identifying the validation failure.

**Validates: Requirements 9.3, 9.4**

### Property 23: CORS Policy Enforcement
*For any* cross-origin API request, the system should include appropriate CORS headers allowing requests from authorized domains.

**Validates: Requirements 9.5**

### Property 24: API Versioning
*For any* API response, the response headers should include API version information.

**Validates: Requirements 9.7**

### Property 25: Large Dataset Processing
*For any* EDRR file containing up to 10,000 subject records, the system should successfully parse and aggregate the data without errors.

**Validates: Requirements 10.2**

## Error Handling

### Data Processing Errors

**EDRR File Validation:**
- Missing required columns → Return error: "Missing required column: {column_name}"
- Malformed Subject ID → Return error: "Invalid Subject ID format at row {row_number}: expected XXX-YYY"
- Non-numeric issue counts → Return error: "Invalid issue count at row {row_number}: expected integer"
- Empty file → Return error: "EDRR file contains no data"

**Data Aggregation Errors:**
- No valid Site IDs extracted → Return error: "No valid Site IDs found in data"
- Negative issue counts → Log warning, treat as zero
- Missing patient data → Use count of subjects as fallback

### API Errors

**Request Validation:**
- Missing required fields → 400 Bad Request: "Missing required field: {field_name}"
- Invalid JSON → 400 Bad Request: "Invalid JSON format"
- Unsupported HTTP method → 405 Method Not Allowed

**Authentication/Authorization:**
- Missing credentials → 401 Unauthorized: "Authentication required"
- Invalid credentials → 401 Unauthorized: "Invalid credentials"
- Insufficient permissions → 403 Forbidden: "Insufficient permissions for this resource"

**External Service Errors:**
- Gemini API failure → Return fallback response: "AI service temporarily unavailable. Please try again."
- Gemini API timeout → Return error: "Query processing timed out. Please simplify your query."
- Rate limit exceeded → 429 Too Many Requests: "Rate limit exceeded. Please wait before retrying."

### Simulation Errors

**Digital Twin:**
- Invalid parameter ranges → Return error: "Parameter {param_name} must be between {min} and {max}"
- Simulation convergence failure → Log warning, return best-effort forecast with confidence flag
- Insufficient data for forecast → Return error: "Insufficient historical data for reliable forecast"

### Multi-Agent Investigation Errors

**Agent Execution:**
- Agent timeout → Log error, continue with partial results
- Agent exception → Log error, mark agent as failed, continue workflow
- All agents fail → Return error: "Investigation failed. Please try again or contact support."

**HITL Gate:**
- Approval timeout → Plan remains in pending state, notify supervisor
- Invalid signature → Reject approval, prompt for re-authentication
- Network failure during approval → Retry with exponential backoff

### General Error Handling Principles

1. **Fail Gracefully:** Never expose stack traces or internal errors to users
2. **Provide Context:** Error messages should identify what failed and why
3. **Enable Recovery:** Suggest corrective actions when possible
4. **Log Everything:** All errors logged with timestamp, context, and stack trace
5. **User-Friendly Messages:** Technical details in logs, plain language for users

## Testing Strategy

### Dual Testing Approach

The testing strategy employs both unit testing and property-based testing as complementary approaches:

**Unit Tests:**
- Verify specific examples and edge cases
- Test integration points between components
- Validate error conditions and boundary cases
- Focus on concrete scenarios with known expected outcomes

**Property-Based Tests:**
- Verify universal properties across all inputs
- Use randomized input generation for comprehensive coverage
- Test invariants and mathematical properties
- Minimum 100 iterations per property test

Together, these approaches provide comprehensive coverage: unit tests catch concrete bugs in specific scenarios, while property tests verify general correctness across the input space.

### Property-Based Testing Configuration

**Framework Selection:**
- **Python Backend:** Use `hypothesis` library for property-based testing
- **TypeScript Frontend:** Use `fast-check` library for property-based testing

**Test Configuration:**
- Minimum 100 iterations per property test (due to randomization)
- Each property test must reference its design document property
- Tag format: `# Feature: trialpulse-ai-requirements, Property {number}: {property_text}`

**Example Property Test Structure (Python):**
```python
from hypothesis import given, strategies as st

@given(st.lists(st.integers(min_value=0, max_value=100), min_size=1))
def test_site_aggregation_correctness(issue_counts):
    """
    Feature: trialpulse-ai-requirements, Property 2: Site Aggregation Correctness
    
    For any set of subject-level records, when aggregated by Site ID,
    the sum of open issues should equal the site's total.
    """
    # Generate subject data with random site IDs
    subjects = [
        {"site_id": "001", "issues": count}
        for count in issue_counts
    ]
    
    # Aggregate
    aggregated = aggregate_by_site(subjects)
    
    # Verify sum matches
    assert aggregated["001"]["total_issues"] == sum(issue_counts)
```

**Example Property Test Structure (TypeScript):**
```typescript
import fc from 'fast-check';

describe('Feature: trialpulse-ai-requirements, Property 6: Critical Site Threshold Detection', () => {
  it('should flag sites with DQI < 60 as Critical', () => {
    fc.assert(
      fc.property(
        fc.integer({ min: 0, max: 59 }), // DQI below threshold
        (dqi) => {
          const site = { id: '001', dqi, overdue_items: 5 };
          const flagged = checkSiteRisk(site);
          return flagged.status === 'Critical';
        }
      ),
      { numRuns: 100 }
    );
  });
});
```

### Test Coverage by Component

**Backend (Python):**

1. **Data Loader Tests:**
   - Unit: Test with sample Excel files (valid, malformed, missing columns)
   - Property: Test aggregation correctness (Property 2)
   - Property: Test parsing completeness (Property 1)
   - Property: Test error handling (Property 4)

2. **Schema Generator Tests:**
   - Unit: Test DQI calculation with known component scores
   - Property: Test DQI calculation consistency (Property 3)
   - Property: Test critical site detection (Property 6)
   - Unit: Test geographic coordinate generation

3. **API Routes Tests:**
   - Unit: Test endpoint responses with mock data
   - Property: Test API endpoint availability (Property 21)
   - Property: Test request validation (Property 22)
   - Property: Test CORS headers (Property 23)
   - Unit: Test Gemini API integration with mocked responses

4. **Agent Simulator Tests:**
   - Unit: Test scripted analysis for Site 042
   - Property: Test multi-agent workflow completeness (Property 8)
   - Unit: Test fallback for non-scripted sites

**Frontend (TypeScript):**

1. **Command Center Tests:**
   - Unit: Test stat card rendering with sample data
   - Property: Test dashboard rendering completeness (Property 7)
   - Property: Test critical site threshold detection (Property 6)
   - Unit: Test site click navigation

2. **Agent Workspace Tests:**
   - Unit: Test simulation execution flow
   - Property: Test HITL authorization requirements (Property 9)
   - Property: Test HITL review interface completeness (Property 10)
   - Unit: Test approval/rejection workflows

3. **Digital Twin Tests:**
   - Unit: Test scenario switching
   - Property: Test Monte Carlo iteration count (Property 12)
   - Property: Test dynamic recalculation (Property 13)
   - Property: Test parameter acceptance (Property 14)
   - Unit: Test chart rendering with sample data

4. **NL Interface Tests:**
   - Unit: Test message display and input handling
   - Property: Test NL query processing pipeline (Property 15)
   - Property: Test active learning correction round trip (Property 16)
   - Unit: Test feedback UI interactions

### Integration Tests

**End-to-End Workflows:**
1. Upload EDRR file → View sites on Command Center → Investigate critical site → Approve mitigation plan
2. Submit NL query → Receive response → Provide feedback → Verify correction stored
3. Adjust Digital Twin parameters → View updated forecast → Switch scenarios → Verify recalculation

**API Integration:**
1. Test frontend-backend communication for all endpoints
2. Test error handling across the stack
3. Test CORS configuration with cross-origin requests

### Test Data Strategy

**Synthetic Data Generation:**
- Use property-based testing libraries to generate random valid inputs
- Create edge case generators (empty files, maximum sizes, boundary values)
- Generate invalid inputs for error handling tests

**Sample Data:**
- Maintain small sample EDRR files for unit tests
- Include valid, malformed, and edge case examples
- Version control test data with the codebase

**Mock Data:**
- Mock Gemini API responses for consistent testing
- Mock external dependencies (file system, network)
- Use dependency injection for testability

### Continuous Testing

**Pre-commit Hooks:**
- Run unit tests before allowing commits
- Run linting and type checking

**CI/CD Pipeline:**
- Run full test suite on pull requests
- Run property-based tests with increased iterations (1000+)
- Generate coverage reports
- Fail builds on test failures or coverage drops

**Performance Testing:**
- Benchmark critical paths (EDRR parsing, DQI calculation, simulation)
- Monitor for performance regressions
- Load test API endpoints

### Test Maintenance

**Property Test Failures:**
- When a property test fails, capture the failing example
- Add the failing example as a unit test
- Fix the bug and verify both tests pass
- Keep the property test to prevent regressions

**Test Documentation:**
- Each test should reference the requirement it validates
- Property tests must reference the design property number
- Include comments explaining test rationale

**Test Refactoring:**
- Keep tests DRY with shared fixtures and helpers
- Refactor tests when implementation changes
- Maintain test readability over cleverness

