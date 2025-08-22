# Stream Pilot

Automated system for Leetcode streamers to generate thumbnails, titles, descriptions, and select problems for scheduled streams using natural language.

## Structure

- **frontend/**: User interface for stream setup and review
- **backend/**: API and business logic for OpenAI, Leetcode, YouTube, and feedback
- **shared/**: Shared types, constants, and utilities between Frontend and Backend
- **docs/**: Documentation and architecture
- **scripts/**: DevOps and setup scripts

See directory structure in project description for details.

## Contributing

If you want to contribute to this project, please follow standard branch naming protocols:

Use descriptive names for branches. Examples:

- `feature/user-authentication`
- `feature/frontend-navbar`
- `bugfix/fix-thumbnail-generation`
- `bugfix/leetcode-api-error`
- `docs/update-readme`
- `chore/update-dependencies`
- `refactor/backend-services`
- `test/add-api-tests`

Avoid using generic names like `dev` or `test`.
Always create a new branch from `main` before starting your work.

This helps keep the repository organized and makes collaboration easier for everyone.

## Environment Variables

This project uses environment variables for configuration.  
Copy the `.env.example` file to `.env` and fill in your own values.

```sh
cp .env.example .env
```

Update the variables in `.env` with your personal credentials and API keys.  
Do **not** commit your `.env` file to
