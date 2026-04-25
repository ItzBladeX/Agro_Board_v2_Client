AgroBoard/
├── client_app/  
│   ├── .streamlit/  
│   │     └──config.toml       
│   └─  app/
│       ├── __pycache__/
│       ├── assets/ 
│       │   └── logo.png       
│       ├── components/
│       │   ├── ui/
│       │   │   │text.py
│       │   ├── charts.py/
│       │   ├── tables.py/
│       │   └──weather_matrix.py/
│       ├── models/
│       ├── pages/
│       │   ├── about.py
│       │   ├── crop.py
│       │   ├── inventory.py
│       │   └── livestock.py
│       ├── services/
│       └── utils/         # API calls to server
│   
│
├── server/                   # Central backend (THE CORE)
│   ├── api/                  # FastAPI / Flask endpoints
│   ├── services/
│   ├── models/
│   ├── database/
│   └── 

├── admin_app/                # Streamlit admin dashboard
│   ├── app/
│   │   ├── main.py
│   │   └── services/         # API calls to server
│   └── .streamlit/
│
├── shared/                   # Optional shared utilities
│   ├── schemas.py            # request/response formats
│   └── constants.py
│
└── requirements.txt