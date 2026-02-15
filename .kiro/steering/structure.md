# Project Structure

## Root Layout

```
/
├── backend/           # Python FastAPI server
├── frontend/          # React TypeScript application
├── screenshots_prototype/  # UI mockups and design references
└── .kiro/            # Kiro configuration and steering rules
```

## Backend Structure (`/backend`)

```
backend/
├── main.py                 # FastAPI app entry point, API routes
├── data_loader.py          # Excel data loading and cleaning
├── schema_generator.py     # Site data aggregation and risk scoring
├── agent_simulator.py      # Multi-agent analysis simulation logic
├── check_models.py         # Model validation utilities
├── .env                    # Environment variables (API keys)
├── data/                   # Clinical trial data files
│   └── Study 1_Compiled_EDRR_updated.xlsx
├── venv/                   # Python virtual environment
└── __pycache__/           # Python bytecode cache
```

### Backend Module Responsibilities

- **main.py**: Defines `/api/nl-query` and `/api/sites` endpoints, integrates Gemini AI
- **data_loader.py**: Parses EDRR Excel files, extracts Site ID and aggregates open issues
- **schema_generator.py**: Generates master dataset with DQI scores and risk flags
- **agent_simulator.py**: Returns scripted multi-agent analysis for Site 042

## Frontend Structure (`/frontend`)

```
frontend/
├── src/
│   ├── main.tsx              # React app entry point
│   ├── App.tsx               # Root component with view routing
│   ├── App.css               # Global app styles
│   ├── index.css             # Tailwind imports and base styles
│   ├── views/                # Full-page view components
│   │   ├── CommandCenter.tsx    # Main dashboard with stats and map
│   │   ├── AgentWorkspace.tsx   # Multi-agent analysis view
│   │   ├── DigitalTwin.tsx      # Site monitoring interface
│   │   └── NLInterface.tsx      # AI chat interface
│   ├── components/
│   │   ├── ui/               # Reusable UI primitives
│   │   │   ├── badge.tsx
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   └── input.tsx
│   │   └── visuals/          # Data visualization components
│   │       ├── AgentNetwork.tsx   # Agent interaction diagram
│   │       ├── RiskTimeline.tsx   # Timeline chart
│   │       └── WorldMap.tsx       # Geographic site map
│   ├── lib/
│   │   └── utils.ts          # Utility functions (cn helper)
│   ├── types/
│   │   └── react-simple-maps.d.ts  # Type definitions
│   └── assets/               # Static assets (SVGs, images)
├── public/                   # Static files served at root
├── index.html                # HTML entry point
├── vite.config.ts            # Vite configuration
├── tailwind.config.js        # Tailwind CSS configuration
├── tsconfig.json             # TypeScript configuration
├── package.json              # Dependencies and scripts
└── node_modules/             # Installed packages
```

### Frontend Component Organization

- **views/**: Page-level components representing distinct application screens
- **components/ui/**: Generic, reusable UI components (buttons, cards, inputs)
- **components/visuals/**: Domain-specific visualization components for trial data
- **lib/**: Shared utilities and helper functions

### View Routing

App.tsx manages view state with simple string-based routing:
- `'command'` → CommandCenter (default)
- `'agents'` → AgentWorkspace (with site context)
- `'digital_twin'` → DigitalTwin
- `'nl_interface'` → NLInterface

Navigation handled via floating bottom navigation bar.

## Naming Conventions

- **React Components**: PascalCase (e.g., `CommandCenter.tsx`)
- **Utilities**: camelCase (e.g., `data_loader.py`, `utils.ts`)
- **CSS Classes**: Tailwind utility classes, kebab-case for custom classes
- **API Routes**: kebab-case (e.g., `/api/nl-query`)

## Data Flow

1. Backend loads Excel data via `data_loader.py`
2. `schema_generator.py` aggregates and scores site data
3. FastAPI serves data through `/api/sites` endpoint
4. Frontend fetches data with axios in view components
5. Components render visualizations and UI based on site data

## Configuration Files

- **Frontend**: `vite.config.ts`, `tailwind.config.js`, `tsconfig.json`, `eslint.config.js`
- **Backend**: `.env` for secrets, no explicit config files (uses defaults)
- **Kiro**: `.kiro/steering/` for AI assistant guidance
