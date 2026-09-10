# Legal Metrology Compliance Checker - Frontend

Standalone React frontend for scanning and checking compliance of packaged commodities.

## Tech Stack

- **Framework:** React 18 + Vite
- **Styling:** Tailwind CSS
- **Routing:** React Router 6
- **HTTP:** Axios
- **Camera:** react-webcam

## Setup

```bash
# Install dependencies
npm install

# Start dev server
npm run dev
```

Frontend runs at: http://localhost:3000

## Project Structure

```
frontend/
├── src/
│   ├── main.jsx          # Entry point
│   ├── App.jsx           # Router setup
│   ├── index.css         # Global styles
│   ├── components/
│   │   └── Navbar.jsx    # Navigation bar
│   ├── pages/
│   │   ├── Home.jsx      # Landing page
│   │   ├── Scan.jsx      # Upload/Camera scan
│   │   ├── History.jsx   # Scan history table
│   │   └── Dashboard.jsx # Stats dashboard
│   ├── services/         # API service functions
│   ├── hooks/            # Custom React hooks
│   └── utils/            # Helper functions
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
└── README.md
```

## Features

- **Image Upload:** Select product images from device
- **Live Camera:** Capture product labels in real-time
- **Compliance Results:** View pass/fail for each rule
- **Scan History:** Filter and view past scans
- **Dashboard:** Compliance statistics overview

## API Integration

The frontend proxies `/api/*` requests to the backend at `http://localhost:8000`.

Configure via `.env`:
```
VITE_API_URL=http://localhost:8000
```

## Build for Production

```bash
npm run build
```

Output goes to `dist/` folder.
