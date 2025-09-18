# Reflex Todo App

A modern, collaborative task management web app built with [Reflex](https://reflex.dev) and PostgreSQL.

## Features

- **Add, Edit, Delete Tasks:** Create tasks, update their details, and remove them as needed.
- **Task Details:** Click a task to view and edit its title, description, completion status, and image.
- **Image Upload:** Attach images to tasks for better context.
- **Live Updates:** Changes sync across browser tabs automatically.
- **Task Filters:** View all, active, or completed tasks. Clear completed tasks with one click.
- **Drag-and-Drop Reordering:** Rearrange tasks by dragging them; the order is saved in the database.
- **Persistent Storage:** All tasks and details are stored in a PostgreSQL database.
- **No User Management:** Anyone can view and manage all tasks—perfect for team or shared lists.
- **Beautiful UI:** Gradient header, responsive layout, and modern design using Reflex components.

## How It Works

- **Backend:**
  - Uses Reflex's State class to manage all logic and database operations.
  - SQLModel ORM connects to PostgreSQL for reliable data storage.
  - All changes (add, edit, reorder, delete) are instantly saved and reflected for all users.

- **Frontend:**
  - Built with Reflex UI components (`rx.input`, `rx.button`, `rx.vstack`, etc.).
  - Conditional rendering and list display use `rx.cond` and `rx.foreach`.
  - Drag-and-drop reordering updates the order field in the database.

## Project Structure

```
todo_app/
├── models.py          # Task model definition
├── state.py           # App logic and state management
├── pages/
│   ├── index.py       # Main page (task list, add, filter, reorder)
│   ├── edit_details.py# Edit task details
│   └── view_details.py# View task details
├── todo_app.py        # App entry point and page registration
├── migrations/        # Database migration files
└── README.md          # Project documentation
```

## Setup & Usage

1. **Install dependencies:**
   ```sh
   pip install reflex sqlmodel psycopg2
   ```
2. **Configure database:**
   - Set your PostgreSQL connection string in `rxconfig.py`.
3. **Run migrations:**
   ```sh
   reflex db migrate
   ```
4. **Start the app:**
   ```sh
   reflex run
   ```
5. **Open in browser:**
   - Visit [http://localhost:3000](http://localhost:3000)

## How to Use

- Type a new task and click "+" to add it.
- Click a task's name to view or edit details.
- Use checkboxes to mark tasks as completed.
- Drag tasks to reorder them.
- Use filter buttons to show all, active, or completed tasks.
- Click "Clear Completed" to remove finished tasks.

## Design & Technology Notes

- **Reflex**: Python web framework for building reactive UIs.
- **SQLModel**: ORM for database models and queries.
- **PostgreSQL**: Reliable, scalable database for all task data.
- **No user accounts**: All users share the same list.
- **Live sync**: Tasks update across tabs and users automatically.

## Contributing

Pull requests and suggestions are welcome! For major changes, please open an issue first.

## License

MIT
