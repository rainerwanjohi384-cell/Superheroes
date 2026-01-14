# Superheroes API

A Flask REST API for managing superheroes and their superpowers. This application allows you to create, retrieve, and manage heroes and their associated powers.

## Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd Superheroes
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Initialize and seed the database
```bash
python app.py
```

This will create the SQLite database and populate it with initial data.

### Running the Server

```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Heroes

#### GET /heroes
Returns a list of all heroes.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Kamala Khan",
    "super_name": "Ms. Marvel"
  },
  {
    "id": 2,
    "name": "Doreen Green",
    "super_name": "Squirrel Girl"
  }
]
```

#### GET /heroes/:id
Returns a specific hero with their associated powers.

**Response:**
```json
{
  "id": 1,
  "name": "Kamala Khan",
  "super_name": "Ms. Marvel",
  "hero_powers": [
    {
      "id": 1,
      "hero_id": 1,
      "power_id": 2,
      "strength": "Strong",
      "hero": {
        "id": 1,
        "name": "Kamala Khan",
        "super_name": "Ms. Marvel"
      },
      "power": {
        "id": 2,
        "name": "flight",
        "description": "gives the wielder the ability to fly through the skies at supersonic speed"
      }
    }
  ]
}
```

**Error Response (404):**
```json
{
  "error": "Hero not found"
}
```

### Powers

#### GET /powers
Returns a list of all powers.

**Response:**
```json
[
  {
    "id": 1,
    "name": "super strength",
    "description": "gives the wielder super-human strengths"
  },
  {
    "id": 2,
    "name": "flight",
    "description": "gives the wielder the ability to fly through the skies at supersonic speed"
  }
]
```

#### GET /powers/:id
Returns a specific power.

**Response:**
```json
{
  "id": 1,
  "name": "super strength",
  "description": "gives the wielder super-human strengths"
}
```

**Error Response (404):**
```json
{
  "error": "Power not found"
}
```

#### PATCH /powers/:id
Updates a power's description.

**Request:**
```json
{
  "description": "updated description that is at least 20 characters long"
}
```

**Success Response (200):**
```json
{
  "id": 1,
  "name": "super strength",
  "description": "updated description that is at least 20 characters long"
}
```

**Validation Error Response (400):**
```json
{
  "errors": ["description must be present and at least 20 characters long"]
}
```

**Not Found Response (404):**
```json
{
  "error": "Power not found"
}
```

### Hero Powers

#### POST /hero_powers
Creates a new association between a hero and a power.

**Request:**
```json
{
  "strength": "Average",
  "hero_id": 3,
  "power_id": 1
}
```

**Success Response (201):**
```json
{
  "id": 11,
  "hero_id": 3,
  "power_id": 1,
  "strength": "Average",
  "hero": {
    "id": 3,
    "name": "Gwen Stacy",
    "super_name": "Spider-Gwen"
  },
  "power": {
    "id": 1,
    "name": "super strength",
    "description": "gives the wielder super-human strengths"
  }
}
```

**Validation Error Response (400):**
```json
{
  "errors": ["strength must be one of ['Strong', 'Weak', 'Average']"]
}
```

## Data Models

### Hero
- `id` (Integer): Primary key
- `name` (String): Hero's real name
- `super_name` (String): Hero's superhero name
- `hero_powers` (Relationship): One-to-many relationship with HeroPower

### Power
- `id` (Integer): Primary key
- `name` (String): Power name
- `description` (String): Power description (minimum 20 characters)
- `hero_powers` (Relationship): One-to-many relationship with HeroPower

### HeroPower
- `id` (Integer): Primary key
- `hero_id` (Integer): Foreign key to Hero
- `power_id` (Integer): Foreign key to Power
- `strength` (String): Power strength level (Strong, Weak, or Average)
- `hero` (Relationship): Many-to-one relationship with Hero
- `power` (Relationship): Many-to-one relationship with Power

## Validations

### Power Model
- `description` must be at least 20 characters long

### HeroPower Model
- `strength` must be one of: `'Strong'`, `'Weak'`, or `'Average'`

## Database

The application uses SQLite for data storage. The database file (`heroes.db`) is created automatically when you run `python app.py` for the first time.

## File Structure

```
Superheroes/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── heroes.db          # SQLite database (created at runtime)
```

## Technologies Used

- **Flask**: Web framework
- **Flask-SQLAlchemy**: ORM for database operations
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping
- **SQLite**: Lightweight database

## Testing

The API has been thoroughly tested against the requirements and all endpoints work as specified in the Postman collection.

## License

This project is created for educational purposes.
