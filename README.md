https://to-do-api-ten.vercel.app


POST /task

Request Body:
{
    "name": "Complete project report",
    "status": 0,
    "priority": "P2",
    "due_date": "2024-02-25 15:00:00"
}

Response:
{
    "message": "Task created successfully",
    "task_id": "609b8c69e95d0d00160eb3c5"
}


GET /tasks

Response:

    {
        "_id": "609b8c69e95d0d00160eb3c5",
        "name": "Complete project report",
        "status": 0,
        "priority": "P2",
        "due_date": "2024-02-25 15:00:00"
    },
    {
        "_id": "609b8d67e95d0d00160eb3c6",
        "name": "Review project presentation",
        "status": 1,
        "priority": "P1",
        "due_date": "2024-02-26 10:00:00"
    },
    ...



GET /tasks/priority/P2

Response:

    {
        "_id": "609b8c69e95d0d00160eb3c5",
        "name": "Complete project report",
        "status": 0,
        "priority": "P2",
        "due_date": "2024-02-25 15:00:00"
    },
    ...



GET /tasks/today

Response:

    {
        "_id": "609b8c69e95d0d00160eb3c5",
        "name": "Complete project report",
        "status": 0,
        "priority": "P2",
        "due_date": "2024-02-25 15:00:00"
    },
    ...


PUT /task/<task-id>/ (update task)

DELETE /task/<task-id>/ (delete task)



